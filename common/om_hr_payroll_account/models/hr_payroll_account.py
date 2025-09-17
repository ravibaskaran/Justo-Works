# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    def _get_partner_id(self, credit_account):
        """
        Get partner_id of slip line to use in account_move_line
        """
        # use partner of salary rule or fallback on employee's address
        register_partner_id = self.salary_rule_id.register_id.partner_id
        partner_id = register_partner_id.id or self.slip_id.employee_id.address_home_id.id
        if credit_account:
            if register_partner_id or self.salary_rule_id.account_credit.internal_type in ('receivable', 'payable'):
                return partner_id
        else:
            if register_partner_id or self.salary_rule_id.account_debit.internal_type in ('receivable', 'payable'):
                return partner_id
        return False


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    date = fields.Date('Date Account', states={'draft': [('readonly', False)]}, readonly=True,
        help="Keep empty to use the period of the validation(Payslip) date.", default=date.today())
    move_ids = fields.Many2many('account.move', string='Accounting Entry', readonly=True, copy=False)
    payable_amount = fields.Float('Payable Amount')
    account_journal_id = fields.Many2one('account.journal', string='Journal',
                                            domain="[('type', 'in', ('bank', 'cash'))]")
    journal_id = fields.Many2one('account.journal', 'Payslip')

    def action_payslip_cancel(self):
        moves = self.mapped('move_ids')
        moves.filtered(lambda x: x.state == 'posted').button_cancel()
        moves.unlink()
        return super(HrPayslip, self).action_payslip_cancel()

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()

        for slip in self:
            domains = [
                [('employee_id', '=', slip.employee_id.id),
                 ('date_from', '<=', slip.date_to),
                 ('date_to', '>=', slip.date_to), ('state', '=', 'done'), ('id', '!=', slip.id)],
                [('employee_id', '=', slip.employee_id.id),
                 ('date_from', '<=', slip.date_from),
                 ('date_to', '>=', slip.date_from), ('state', '=', 'done'), ('id', '!=', slip.id)],
                [('employee_id', '=', slip.employee_id.id),
                 ('date_from', '>=', slip.date_from),
                 ('date_from', '<=', slip.date_to), ('state', '=', 'done'), ('id', '!=', slip.id)],
                [('employee_id', '=', slip.employee_id.id),
                 ('date_to', '>=', slip.date_from),
                 ('date_to', '<=', slip.date_to), ('state', '=', 'done'), ('id', '!=', slip.id)]
            ]
            for domain in domains:
                data = self.env['hr.payslip'].search(domain)
                if data:
                    raise UserError('Payslip already exists for the employee at the selected time period')
            data = self.env['hr.payslip'].search(
                [('employee_id', '=', slip.employee_id.id), ('date_from', '>=', slip.date_to), ('state', '=', 'done'),
                 ('id', '!=', slip.id)])
            if data:
                raise UserError('Previous date entry not allowed!')

            dom = [('type', '=', 'payslip')]
            if 'branch_id' in slip._fields:
                dom.append(('branch_id', '=', self.branch_id.id))
            journal_id = self.env['account.journal'].search(dom, limit=1)
            if journal_id:
                self.journal_id = journal_id
            else:
                raise UserError('Payslip Journal Configuration Missing')
            slip.number = slip.number or self.journal_id.refund_sequence_id.next_by_id()
            line_ids = []
            cash_line_ids = []
            deduction_total = 0.0
            addition_total = 0.0
            date = slip.date or slip.date_to
            name = _('Payslip of %s') % (slip.employee_id.name)
            move_dict = {
                'narration': name,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
                'date': date,
            }
            move_dict1 = {
                'narration': name,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
                'date': date,
            }
            if not slip.employee_id.address_home_id:
                raise UserError('Partner missing in employee!')
            if 'branch_id' in slip._fields:
                move_dict['branch_id'] = slip.branch_id.id
                move_dict1['branch_id'] = slip.branch_id.id
            if not any(line.salary_rule_id.account_debit and line.salary_rule_id.account_credit for line in slip.details_by_salary_rule_category):
                raise UserError(_('Missing Debit Or Credit Account in Salary Rule'))
            for line in slip.details_by_salary_rule_category:
                amount = round(line.total, 2)
                debit_account_id = line.salary_rule_id.account_debit.id
                credit_account_id = line.salary_rule_id.account_credit.id
                if line.category_id.type == 'deduction':
                    debit_line = (0, 0, {
                        'name': line.name,
                        'account_id': debit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'credit': amount,
                        'debit': 0.0,
                        'partner_id': slip.employee_id.address_home_id.id
                    })
                    line_ids.append(debit_line)
                    deduction_total += amount
                    addition_total -= amount
                elif line.category_id.type == 'addition':
                    addition_total += amount
                elif line.category_id.type == 'z_adjustment':
                    line_ids.append((0, 0, {
                        'name': line.name,
                        'account_id': debit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'debit': amount,
                        'credit': 0.0,
                        'partner_id': slip.employee_id.address_home_id.id,
                        'is_payslip_adjustment_line': True
                    }))
                    line_ids.append((0, 0, {
                        'name': line.name,
                        'account_id': credit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'credit': amount,
                        'debit': 0.0,
                        'partner_id': slip.employee_id.address_home_id.id,
                        'is_payslip_adjustment_line': True
                    }))

            if not slip.journal_id.profit_account_id :
                raise UserError(_('The Expense Journal "%s" has not properly configured the Credit Account!') % (slip.journal_id.name))

            addition_credit = (0, 0, {
                'name': 'Addition',
                'account_id': slip.journal_id.profit_account_id.id,
                'journal_id': slip.journal_id.id,
                'date': date,
                'credit': 0.0,
                'debit': addition_total,
                'partner_id': slip.employee_id.address_home_id.id
            })

            addition_debit = (0, 0, {
                'name': 'Addition',
                'account_id': slip.account_journal_id.loss_account_id.id,
                'journal_id': slip.journal_id.id,
                'date': date,
                'credit': addition_total,
                'debit': 0.0,
                'partner_id': slip.employee_id.address_home_id.id
            })
            if slip.account_journal_id.type == 'cash':
                cash_line_ids.append(addition_credit)
                cash_line_ids.append(addition_debit)
            else:
                line_ids.append(addition_credit)
                line_ids.append(addition_debit)
            line_ids.append((0, 0, {
                'name': 'Deduction',
                'account_id': slip.journal_id.profit_account_id.id,
                'journal_id': slip.journal_id.id,
                'date': date,
                'credit': 0.0,
                'debit': deduction_total,
                'partner_id': slip.employee_id.address_home_id.id
            }))
            # print(line_ids)
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            slip.move_ids = move
            slip.write({'date': date})
            move.post()
            # if 'direct_journal_id_inx' in move._fields:
            #     move.direct_journal_id_inx = slip.account_journal_id.id
            if slip.account_journal_id.type == 'cash':
                move_dict1['line_ids'] = cash_line_ids
                # slip.write({'move_id': move.id, 'date': date})
                print(move_dict1,'move_dict')
                move1 = self.env['account.move'].create(move_dict1)
                slip.move_ids += move1
                move1.post()
                if 'direct_journal_id_inx' in move1._fields:
                    move1.direct_journal_id_inx = slip.account_journal_id.id
            # slip.number = move.name
        return res


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    account_tax_id = fields.Many2one('account.tax', 'Tax')
    account_debit = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Credit Account', domain=[('deprecated', '=', False)])


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    journal_id = fields.Many2one('account.journal', 'Salary Journal')


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    journal_id = fields.Many2one('account.journal', 'Salary Journal', states={'draft': [('readonly', False)]},
                                 readonly=True, required=True,
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'general')],
                                                                                         limit=1))
