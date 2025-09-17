# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import UserError


class BetaGeneralLedger(models.TransientModel):  # change this
    _name = 'beta.general.ledger'  # change this
    _inherit = 'beta.reports'

    @api.model
    def get_account_domain(self):
        try:
            if self.env['ir.config_parameter'].sudo().get_param('general_ledger.gl_ignore_ac_heads'):
                return [('id', 'not in', [eval(i) for i in self.env[
                'ir.config_parameter'].sudo().get_param('general_ledger.gl_ignore_ac_heads').strip('][').split(',')])]
            else:
                return []
        except:
            return []

    name = fields.Char(default='General Ledger')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    account_ids = fields.Many2many('account.account', string='Accounts', domain=get_account_domain)
    with_initial = fields.Boolean()
    day_summary = fields.Boolean()
    month_summary = fields.Boolean()
    month_total = fields.Boolean()

    @api.onchange('day_summary')
    def onchange_day_summary(self):
        if self.day_summary:
            self.month_summary = False

    @api.onchange('month_summary')
    def onchange_month_summary(self):
        if self.month_summary:
            self.day_summary = False
            self.month_total = False

    @api.model
    def default_get(self, fields_list):
        res = super(BetaGeneralLedger, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        if not self.env.context.get('default_date_from') and not self.env.context.get('default_date_to'):
            res['date_from'] = fin_start
            res['date_to'] = today
        return res

    # ▼ Fully Settlement ▼
    def paid_or_not(self, inv):
        paid_or_not = False
        if inv.invoice_payments_widget != 'false' and inv.invoice_payment_state == 'paid':
            pay_json_value = inv.sudo()._get_reconciled_info_JSON_values()
            bill_type = True

            # ▼ if bill type is credit then fully settlement is False ▼
            if 'bill_type' in self.env['account.move']._fields:
                if inv.bill_type == 'credit':
                    bill_type = False
            type = "Cash"
            for pay in pay_json_value:
                if inv.invoice_date == pay['date'] and type == pay['journal_name'] and len(
                        pay_json_value) == 1 and bill_type:
                    self.env.cr.execute("select amount from account_payment where id=" + str(pay['account_payment_id']))
                    payment_amt = self.env.cr.fetchall()[0][0]
                    if inv.amount_total == payment_amt:
                        type = pay['journal_name']
                        paid_or_not = True
                    else:
                        paid_or_not = False
                else:
                    paid_or_not = False
                    break

        return paid_or_not

    def check_payment_invoice(self, payment):
        paid_or_not = False
        if len(payment.reconciled_invoice_ids) == 1:
            for inv in payment.reconciled_invoice_ids:
                paid_or_not = self.paid_or_not(inv)
        return paid_or_not

    def get_general_ledger(self, data):
        move_line_obj = self.env['account.move.line']
        domain = [('move_id.state', '=', 'posted')]
        if data['date_from']:
            domain.append(('move_id.date', '>=', data['date_from']))
        if data['date_to']:
            domain.append(('move_id.date', '<=', data['date_to']))
        if data['account_ids']:
            domain.append(('account_id', 'in', data['account_ids']))
        acc_to_ignore = self.env['ir.config_parameter'].sudo().get_param(
            'dynamic_general_ledger.gl_ignore_ac_heads')
        if acc_to_ignore:
            acc_to_ignore = tuple(acc_to_ignore.strip('][').split(','))
            domain.append(('account_id', 'not in', [int(a_id) for a_id in acc_to_ignore]))
        opening_move = self.env.company.account_opening_move_id
        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))
            opening_move = self.env['account.move']
            branch_obj = self.env['res.branch']
            branches = branch_obj.search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in branch_obj._fields:
                for branch in branches:
                    account_opening_move_id = branch.account_opening_move_id
                    if account_opening_move_id and account_opening_move_id.state == 'posted':
                        opening_move += account_opening_move_id

        if opening_move:
            domain.append(('move_id.id', 'not in', opening_move.ids))
        print('domain', domain)
        moves = move_line_obj.search(domain, order="date asc, id asc").sorted(key=lambda r: (r.account_id.name).upper())
        datas = {}
        for moveline in moves:
            move_name = moveline.move_id.name
            move_id = moveline.move_id.id
            model = moveline.move_id._name
            form = False
            if 'direct_journal_type_inx' in moveline.move_id._fields:
                if moveline.move_id.direct_journal_type_inx:
                    if moveline.move_id.direct_journal_type_inx in (
                    'receipt', 'payment_reverse', 'payment', 'receipt_reverse'):
                        form = self.env.ref('inexoft_account_voucher.direct_journal_view_move_form', False)
                    else:
                        form = False

            remarks = ''
            if 'direct_journal_item_ids' in moveline.move_id._fields:
                remarks = moveline.name if moveline.move_id.direct_journal_item_ids else ''
            if 'direct_journal_type_inx' in moveline.move_id._fields:
                if moveline.move_id.direct_journal_type_inx not in (
                'payment', 'receipt', 'receipt_reverse', 'payment_reverse'):
                    remarks = moveline.name if moveline.move_id.line_ids else ''
            if moveline.move_id.move_type == 'in_invoice':
                remarks = 'Purchase'
                form = self.env.ref('purchase_custom.view_move_form_purchase_custom', False)
            elif moveline.move_id.move_type == 'out_invoice':
                remarks = 'Sales'
                form = self.env.ref('direct_sales_with_lot.view_move_form_direct_sales_with_lot', False)

            elif moveline.move_id.move_type == 'in_refund':
                remarks = 'Purchase Return'
                form = self.env.ref('purchase_custom.view_move_form_purchase_custom', False)
            elif moveline.move_id.move_type == 'out_refund':
                remarks = 'Sales Return'
                form = self.env.ref('direct_sales_with_lot.view_move_form_direct_sales_with_lot', False)
            if moveline.payment_id:
                move_name = moveline.payment_id.name
                move_id = moveline.payment_id.id
                model = moveline.payment_id._name
                if moveline.payment_id.partner_type == 'customer':
                    remarks = 'Customer Reciept'
                if moveline.payment_id.partner_type == 'supplier':
                    remarks = 'Supplier Reciept'

            if data['day_summary']:
                factor = moveline.date
            elif data['monthSummary']:
                date = str(moveline.date)
                d = datetime.strptime(date, "%Y-%m-%d")
                m = d.strftime('%B')
                y = str(d.year)
                factor = m + '-' + y
            else:
                if 'is_discount_line' in moveline._fields and moveline.is_discount_line:
                    factor = str(moveline.move_id.id) + 'disc'
                else:
                    factor = moveline.move_id.id
            type = moveline.move_id.move_type
            debit = moveline.debit
            credit = moveline.credit
            if remarks not in ['Purchase','Purchase Return']:
                if moveline.payment_id:
                    fully_settled = self.check_payment_invoice(moveline.payment_id)
                    if fully_settled:
                        continue
                    else:
                        pass
                else:
                    fully_settled = self.paid_or_not(moveline.move_id)
                    if 'is_freight' in moveline._fields:
                        opo = not moveline.is_rounding_line and not moveline.is_freight
                    else:
                        opo = not moveline.is_rounding_line
                    if opo and (fully_settled and ((debit > 0 and type == "out_invoice") or (
                            credit > 0 and type in ["out_refund", "in_invoice"]))):
                        if moveline.is_rounding_line:
                            print("voucher no:", moveline.move_id.name, debit, credit, fully_settled)
                        if 'is_discount_line' in moveline._fields:
                            if not moveline.is_discount_line:
                                continue
                        else:
                            continue

            partner = moveline.partner_id.name if moveline.partner_id else ''
            if moveline.account_id.id in datas:
                if factor in datas[moveline.account_id.id]['data']:
                    datas[moveline.account_id.id]['data'][factor]['credit'] += credit
                    datas[moveline.account_id.id]['data'][factor]['debit'] += debit
                    datas[moveline.account_id.id]['data'][factor][
                        'partner'] += ', ' + partner if moveline.move_id.move_type == 'entry' and \
                                                        datas[moveline.account_id.id]['data'][factor][
                                                            'partner'] != partner else ''
                else:
                    datas[moveline.account_id.id]['data'][factor] = {
                        'date': moveline.date.strftime('%d-%m-%Y') if not data['monthSummary'] else factor,
                        'partner': partner,
                        'move': move_name,
                        'move_id': move_id,
                        'model': model,
                        'form': form.id if form else False,
                        'name': moveline.account_id.name,
                        'credit': credit,
                        'debit': debit,
                        'remarks': remarks
                    }

            else:
                datas[moveline.account_id.id] = {
                    'name': moveline.account_id.name,
                    'data': {
                        factor: {
                            'date': moveline.date.strftime('%d-%m-%Y') if not data['monthSummary'] else factor,
                            'partner': partner,
                            'move': move_name,
                            'move_id': move_id,
                            'model': model,
                            'form': form.id if form else False,
                            'name': moveline.account_id.name,
                            'credit': credit,
                            'debit': debit,
                            'remarks': remarks
                        },
                    },
                    'credit': 0,
                    'debit': 0,
                }
        if data['with_initial_balance']:
            domain = [('code', '!=', str(999999))]
            if data['account_ids']:
                domain.append(('id', 'in', data['account_ids']))
            accounts = self.env['account.account'].search(domain)
            for account in accounts:
                if 'branch' in data:
                    opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], data['branch'])
                else:
                    opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], branch=False)
                if opening[0] or opening[1]:
                    if account.id in datas:
                        datas[account.id]['credit'] = opening[0]
                        datas[account.id]['debit'] = opening[1]
                    else:
                        datas[account.id] = {
                            'name': account.name,
                            'data': [],
                            'credit': opening[0],
                            'debit': opening[1],
                        }
        return datas

    def get_ledger_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id', '=', account)])
            selected_year = datetime.strptime(str(date_from), '%Y-%m-%d')
            date_f = datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            date_fr = datetime.strptime(str(date_f), '%d-%m-%Y').date()
            if not account_id.user_type_id.include_initial_balance:
                if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                    fin_date = str(selected_year.year - 1) + '-04-01'
                else:
                    fin_date = str(selected_year.year) + '-04-01'
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
            else:
                if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                        "%Y-%m-%d") == date_from:
                    for openline in opening_move.line_ids:
                        if openline.account_id.id == account:
                            moves += openline
            for move in moves:
                credit += move.credit
                debit += move.debit
        return (credit, debit)

    def get_report_values(self, data=None):
        lines = {}
        date_from = date_to = False
        account_obj = self.env['account.account']
        accounts = ''
        if data['date_from']:
            try:
                date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")
        if data['date_to']:
            try:
                date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")
        if data['account_ids']:
            for account in data['account_ids']:
                accounts += account_obj.browse(account).name + ", "

        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        if data['date_from'] and data['date_to']:
            lines = self.get_general_ledger(data)
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'with_initial_balance': data['with_initial_balance'],
            'day_summary': data['day_summary'],
            'accounts': accounts,
            'lines': lines,
            'branch_name': branch_name,
            'monthSummary': data['monthSummary'],
            'monthTotal': data['monthTotal'],
            'o': self,
            'breadcrumbs': data['breadcrumbs'],
        }

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'),
                                    report_account=self.account_ids.ids if self.account_ids else False,
                                    with_initial=self.with_initial,
                                    day_summary=self.day_summary,
                                    breadcrumbs=False,
                                    month_summary=self.month_summary, month_total=self.month_total)
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('general_ledger.report_general_ledger')._render(
            {'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'accounts': res['lines']['accounts'],
             'with_initial_balance': res['lines']['with_initial_balance'],
             'day_summary': res['lines']['day_summary'],
             'branch_name': res['lines']['branch_name'],
             'breadcrumbs': res['lines']['breadcrumbs'],
             'monthSummary': res['lines']['monthSummary'],
             'monthTotal': res['lines']['monthTotal'],
             'o': self,
             })
        self.template_area = res['lines']

    def _get_report_data(self, date_from=False, date_to=False, report_account=False, with_initial=False,
                         day_summary=False, breadcrumbs=False, month_summary=False,
                         month_total=False):
        if date_to and date_from:
            if date_from > date_to:
                raise Warning("From date can't be greater than To date")
        acc = []
        domain = []
        acc_to_ignore = self.env['ir.config_parameter'].sudo().get_param(
            'dynamic_general_ledger.gl_ignore_ac_heads')
        if acc_to_ignore:
            domain.append(('id', 'not in', acc_to_ignore.strip('][').split(',')))
        if breadcrumbs:
            if report_account:
                acc.append(int(report_account))
        else:
            if report_account:
                for account in report_account:
                    acc.append(int(account))
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'account_ids': acc if acc else False,
            'with_initial_balance': with_initial,
            'day_summary': day_summary,
            'breadcrumbs': breadcrumbs,
            'monthSummary': month_summary,
            'monthTotal': month_total,
        }
        dat = self.get_report_values(data=data)
        return {
            'lines': dat
        }
