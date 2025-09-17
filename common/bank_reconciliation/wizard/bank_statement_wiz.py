# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date


class BankStatement(models.Model):
    _name = 'bank.statement'

    @api.model
    def default_get(self, fieldsname):
        res = super(BankStatement, self).default_get(fieldsname)
        today = date.today()
        if today < datetime.strptime('01-04-' + str(today.year), '%d-%m-%Y').date():
            fin_date = str(today.year - 1) + '-04-01'
        else:
            fin_date = str(today.year) + '-04-01'
        res['date_from'] = fin_date
        res['date_to'] = today
        return res

    @api.onchange('journal_id')
    def get_lines(self):
        self.account_id = self.journal_id.default_account_id.id
        check = self.check()
        if check:
            raise UserError("Already Exists")
        self.currency_id = self.journal_id.currency_id or self.journal_id.company_id.currency_id or \
                           self.env.user.company_id.currency_id

    def check(self):
        check = self.env['bank.statement'].search(
            [('account_id', '=', self.account_id.id), ('id', '!=', self._origin.id)], limit=1)
        return check

    def opening(self):
        return self.env.company.account_opening_move_id

    def add_domain(self):
        return [('account_id', '=', self.account_id.id), ('move_id.state', '=', 'posted')]

    def branch(self):
        return False

    def branch_name(self):
        return None

    def get_report(self):
        domain = self.add_domain()
        opening_move = self.opening()

        if self.date_from:
            domain += [('date', '>=', self.date_from)]
        if self.date_to:
            domain += [('date', '<=', self.date_to)]
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise UserError("Date To should be greater than Date From")
        else:
            today = date.today()
            if today < datetime.strptime('01-04-' + str(today.year), '%d-%m-%Y').date():
                fin_date = str(today.year - 1) + '-04-01'
            else:
                fin_date = str(today.year) + '-04-01'
            if not self.date_from:
                self.date_from = fin_date
            if not self.date_to:
                self.date_to = today

        if opening_move:
            domain += [('move_id.id', 'not in', opening_move.ids)]
        lines = self.env['account.move.line'].search(domain)
        for line in self.statement_lines:
            line.bank_statement_id = self.id
        self.statement_lines = lines

        self.name = self.account_id.name
        branch = self.branch()
        if self.account_id and self.date_from:
            self.ledger_opening = self.get_ledger_credit_and_debit(self.account_id.id,
                                                                   self.date_from.strftime("%Y-%m-%d"), branch)

    @api.onchange('ledger_opening', 'bank_opening')
    def onchange_opening(self):
        self._compute_amount()

    @api.depends('statement_lines.statement_date')
    def _compute_amount(self):
        gl_balance = 0
        bank_balance = 0
        current_update = 0
        opening_move = self.opening()
        domain = self.add_domain()
        if opening_move:
            domain += [('move_id.id', 'not in', opening_move.ids)]
        lines = self.env['account.move.line'].search(domain)
        gl_balance += sum([line.debit - line.credit for line in lines])
        domain += [('id', 'not in', self.statement_lines.ids), ('statement_date', '!=', False)]
        lines = self.env['account.move.line'].search(domain)
        bank_balance += sum([line.balance for line in lines])
        current_update += sum([line.debit - line.credit if line.statement_date else 0 for line in self.statement_lines])
        self.gl_balance = gl_balance + self.ledger_opening
        self.bank_balance = bank_balance + current_update + self.bank_opening
        self.balance_difference = self.gl_balance - self.bank_balance

    name = fields.Char(default="Bank Reconciliation")
    journal_id = fields.Many2one('account.journal', 'Bank', domain=[('type', '=', 'bank')])
    account_id = fields.Many2one('account.account', 'Bank Account')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    statement_lines = fields.One2many('account.move.line', 'bank_statement_id')
    gl_balance = fields.Monetary('Balance as per Company Books', readonly=True, compute='_compute_amount')
    bank_balance = fields.Monetary('Balance as per Bank', readonly=True, compute='_compute_amount')
    balance_difference = fields.Monetary('Amounts not Reflected in Bank', readonly=True, compute='_compute_amount')
    current_update = fields.Monetary('Balance of entries updated now')
    currency_id = fields.Many2one('res.currency', string='Currency')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get('bank.statement'))
    ledger_opening = fields.Float()
    bank_opening = fields.Float()

    def get_ledger_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id', '=', account)])
            if not account_id.user_type_id.include_initial_balance:
                today = date.today()
                if today < datetime.strptime('01-04-' + str(today.year), '%d-%m-%Y').date():
                    fin_date = str(today.year - 1) + '-04-01'
                else:
                    fin_date = str(today.year) + '-04-01'
                domain.append(('date', '>=', fin_date))
            if branch:
                domain.append(('move_id.branch_id', 'in', branch))
            moves = self.env['account.move.line'].search(domain)
            opening_move = self.env.company.account_opening_move_id
            if branch:
                branch_id = self.env['res.branch'].search([('id', 'in', branch)])
                if 'account_opening_move_id' in self.env['res.branch']:
                    for b in branch_id:
                        account_opening_move_id = b.account_opening_move_id
                        opening_move = account_opening_move_id
            if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                    "%Y-%m-%d") == date_from:
                for openline in opening_move.line_ids:
                    if openline.account_id.id == account:
                        moves += openline
            for move in moves:
                credit += move.credit
                debit += move.debit
        return abs(debit - credit)

    def journal_voucher_creation(self):
        self.ensure_one()
        return {
            'name': _('Journal Voucher'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'domain': [('direct_journal_entry_inx', '=', True), (
                'direct_journal_type_inx', 'not in', ['payment', 'receipt', 'receipt_reverse', 'payment_reverse'])],
            'view_id': self.env.ref('account.view_move_form').id,
            'type': 'ir.actions.act_window',
            'context': {'default_type': 'entry', 'default_direct_journal_entry_inx': True, 'view_no_maturity': True,
                        'bank_account': self.account_id.id, 'bank_reconciliation': True},
            'target': 'new',
        }

    # self._context.get('default_type') == 'out_invoice':
    def clear_value(self):
        self.update({'statement_lines': None})

    def bank_reconcil_get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from.strftime('%d/%m/%Y') if self.date_from else None,
                'date_to': self.date_to.strftime('%d/%m/%Y') if self.date_to else None,
                'branch_name': self.branch_name(),
                'ledger_opening': self.ledger_opening,
                'statement_lines': self.statement_lines.ids,
                'bank_opening': self.bank_opening,
                'gl_balance': self.gl_balance,
                'bank_balance': self.bank_balance,
                'balance_difference': self.balance_difference

            }
        }
        return self.env.ref('bank_reconciliation.bank_reconciliation_report_action').report_action(self, data=data)


class BankReconciliationReport(models.AbstractModel):
    _name = 'report.bank_reconciliation.bank_reconciliation_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        ledger_opening = data['form']['ledger_opening']
        statement_lines = data['form']['statement_lines']
        bank_opening = data['form']['bank_opening']
        branch_name = data['form']['branch_name']
        gl_balance = data['form']['gl_balance']
        bank_balance = data['form']['bank_balance']
        balance_difference = data['form']['balance_difference']
        docs = []
        for line in statement_lines:
            line_id = self.env['account.move.line'].search([('id', '=', line)])
            docs.append({
                'account': line_id.account_id.name,
                'partner': line_id.partner_id.name,
                'label': line_id.name,
                'ref': line_id.ref,
                'date': line_id.date,
                'statement_date': line_id.statement_date,
                'debit': line_id.debit,
                'credit': line_id.credit,
            })
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_from': date_from,
            'date_to': date_to,
            'ledger_opening': ledger_opening,
            'bank_opening': bank_opening,
            'docs': docs,
            'branch_name': branch_name,
            'gl_balance': gl_balance,
            'bank_balance': bank_balance,
            'balance_difference': balance_difference
        }


class AccountMoveBank(models.Model):
    _inherit = 'account.move'

    @api.onchange('line_ids')
    def onchange_line_ids(self):
        if 'bank_reconciliation' in self._context and self._context.get('bank_reconciliation'):
            if len(self.line_ids) == 0:
                line = [(0, 0, {
                    'account_id': self._context.get('bank_account'),
                    'partner_id': None,
                    'debit': 0,
                    'credit': 0,
                    'name': None,
                })]
                self.update({'line_ids': line})
            else:
                if self.line_ids[0].account_id.id != self._context.get('bank_account'):
                    raise UserError('Cannot Change the Bank Account ID')
