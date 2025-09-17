# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class BetaCashBook(models.TransientModel):  # change this
    _name = 'beta.cash.book'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Cash Book')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    two_column = fields.Boolean()       # Show Report In Two Columns
    summary = fields.Boolean()          # Show Report in Summary

    @api.model
    def default_get(self, fields_list):
        """
        returns the current financial date for date form and date to field
        """
        res = super(BetaCashBook, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    def get_report_values(self, data=None):
        date_from = date_to = False
        account_obj = self.env['account.account']
        accounts = ''

        # ▼ Converting a date to give formate ▼
        if data['date_from']:
            try:
                date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")

        # ▼ Converting a date to give formate ▼
        if data['date_to']:
            try:
                date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")

        if data['account_ids']:
            for account in data['account_ids']:
                accounts += account_obj.browse(account).name + ", "

        # ▼ Branch Name ▼
        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''

        date_data = []
        if data['date_from'] and data['date_to']:
            fdate = datetime.strptime(data['date_from'], "%Y-%m-%d")
            tdate = datetime.strptime(data['date_to'], "%Y-%m-%d")
            days = tdate - fdate

            # ▼ Looping Date Range ▼
            for i in range(days.days + 1):
                day = fdate + timedelta(days=i)
                date = day.strftime("%Y-%m-%d")
                date_data.append(
                    {datetime.strptime(date, "%Y-%m-%d").strftime('%d/%m/%Y'): self.get_cash_book(data, date)})

        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'with_initial_balance': data['with_initial_balance'],
            'summary': data['summary'],
            'accounts': accounts,
            'date_data': date_data,
            'branch_name': branch_name
        }

    # ▼ Fully Settlement ▼
    def paid_or_not(self, inv):
        paid_or_not = False
        if inv.invoice_payments_widget != 'false' and inv.payment_state == 'paid':
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

    def get_cash_book(self, data, date):
        move_line_obj = self.env['account.move.line']
        domain = [('move_id.state', '=', 'posted')]
        if data['date_from']:
            domain.append(('move_id.date', '>=', date))
        if data['date_to']:
            domain.append(('move_id.date', '<=', date))
        if data['account_ids']:
            domain.append(('account_id', 'not in', data['account_ids']))
        opening_move = self.env.company.account_opening_move_id
        if 'branch' in data:
            branch = self.env['res.branch'].search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in self.env['res.branch']:
                for branches in branch:
                    account_opening_move_id = branches.account_opening_move_id
                    if account_opening_move_id and account_opening_move_id.state == 'posted':
                        opening_move += account_opening_move_id

        if opening_move:
            domain.append(('move_id.id', 'not in', opening_move.ids))
        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))
        if data['twoCol']:
            moves = move_line_obj.search(domain, order="date asc, id asc").sorted(
                key=lambda r: r.move_id.name.upper())
        else:
            moves = move_line_obj.search(domain, order="date asc, id asc").sorted(
                key=lambda r: r.account_id.name.upper())
        datas = {}
        for moveline in moves:
            move_name = moveline.move_id.name
            model = moveline.move_id._name
            res_id = moveline.move_id.id
            remarks = ''
            if 'direct_journal_item_ids' in moveline.move_id._fields:
                remarks = moveline.name if moveline.move_id.direct_journal_item_ids else ''
            if 'direct_journal_type_inx' in moveline.move_id._fields:
                if moveline.move_id.direct_journal_type_inx not in (
                        'payment', 'receipt', 'receipt_reverse', 'payment_reverse'):
                    remarks = moveline.name if moveline.move_id.line_ids else ''
            if moveline.move_id.move_type == 'in_invoice':
                remarks = 'Purchase'
            elif moveline.move_id.move_type == 'out_invoice':
                remarks = 'Sales'
            elif moveline.move_id.move_type == 'in_refund':
                remarks = 'Purchase Return'
            elif moveline.move_id.move_type == 'out_refund':
                remarks = 'Sales Return'
            if moveline.payment_id:
                move_name = moveline.payment_id.name
                model = moveline.payment_id._name
                res_id = moveline.payment_id.id
                if moveline.payment_id.partner_type == 'customer':
                    remarks = 'Customer Reciept'
                if moveline.payment_id.partner_type == 'supplier':
                    remarks = 'Supplier Reciept'
            type = moveline.move_id.move_type
            debit = moveline.debit
            credit = moveline.credit
            cash_type = moveline.move_id.direct_journal_id_inx.type
            cash_type2 = moveline.move_id.journal_id.type
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
                    if opo and (fully_settled and (
                            (debit > 0 and type == "out_invoice") or (
                            credit > 0 and type in ["out_refund", "in_invoice"]))):
                        if moveline.is_rounding_line:
                            print("voucher no:", moveline.move_id.name, debit, credit, fully_settled)
                        continue
                    elif fully_settled:
                        cash_type = "cash"
                        cash_type2 = "cash"
                    if type == 'JV':
                        cash_type = "cash"
                        cash_type2 = "cash"
            if 'is_discount_line' in moveline._fields and moveline.is_discount_line:
                continue
            else:
                factor = moveline.move_id.id
            partner = moveline.partner_id.name if moveline.partner_id else ''
            if data['summary']:
                factor = moveline.account_id.id
            if cash_type == "cash" or cash_type2 == "cash":
                if moveline.account_id.id in datas:
                    if factor in datas[moveline.account_id.id]['data'] and moveline.journal_id.type not in (
                            'agent_collection', 'day_deposit'):
                        datas[moveline.account_id.id]['data'][factor]['credit'] += debit
                        datas[moveline.account_id.id]['data'][factor]['debit'] += credit
                        if partner not in datas[moveline.account_id.id]['data'][factor]['partner']:
                            datas[moveline.account_id.id]['data'][factor]['partner'] += ', ' + partner

                    else:
                        dest_acc_name = moveline.account_id.name
                        if moveline.journal_id.type in ('agent_collection', 'day_deposit'):
                            grouper = str(moveline.id) + moveline.move_id.name
                        else:
                            grouper = factor

                        # noinspection PyTypeChecker
                        datas[moveline.account_id.id]['data'][grouper] = {
                            'date': moveline.date.strftime('%d-%m-%Y'),
                            'partner': partner,
                            'move': move_name,
                            'name': dest_acc_name,
                            'credit': debit,
                            'debit': credit,
                            'remarks': remarks,
                            'model': model,
                            'res_id': res_id,
                        }
                else:
                    dest_acc_name = moveline.account_id.name
                    datas[moveline.account_id.id] = {
                        'date': datetime.strptime(date, "%Y-%m-%d").strftime('%d/%m/%Y'),
                        'data': {
                            factor: {
                                'date': moveline.date.strftime('%d-%m-%Y'),
                                'partner': partner,
                                'move': move_name,
                                'name': dest_acc_name,
                                'credit': debit,
                                'debit': credit,
                                'remarks': remarks,
                                'model': model,
                                'res_id': res_id,
                            },
                        },
                        'credit': 0,
                        'debit': 0,
                        'first_opening': 1 if date == data['date_from'] else 0,
                    }
        if data['with_initial_balance']:
            domain = [('code', '!=', str(999999))]
            if data['account_ids']:
                domain.append(('id', 'in', data['account_ids']))
            accounts = self.env['account.account'].search(domain)
            for account in accounts:
                if date == data['date_from']:
                    if 'branch' in data:
                        opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], data['branch'])
                    else:
                        opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], branch=False)
                    if opening[0] or opening[1]:
                        if opening[0] > opening[1]:
                            dr = 0
                            cr = opening[0] - opening[1]
                        else:
                            dr = opening[1] - opening[0]
                            cr = 0
                        if account.id in datas:
                            datas[account.id]['credit'] = cr
                            datas[account.id]['debit'] = dr
                        else:
                            datas['opening'] = {
                                'date': datetime.strptime(date, "%Y-%m-%d").strftime('%d/%m/%Y'),
                                'data': [],
                                'credit': cr,
                                'debit': dr,
                                'first_opening': 1 if cr > 0 or dr > 0 else 0,
                            }
        return datas

    def get_ledger_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            if branch:
                domain.append(('move_id.branch_id', 'in', branch))
            moves = self.env['account.move.line'].search(domain)
            opening_move = self.env.company.account_opening_move_id
            if branch:
                branch_id = self.env['res.branch'].search([('id', 'in', branch)])
                if 'account_opening_move_id' in self.env['res.branch']:
                    for branch in branch_id:
                        account_opening_move_id = branch.account_opening_move_id
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

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'),
                                    two_column=self.two_column, summary=self.summary)
        res['lines'] = self.env.ref('cash_book.report_cash_book')._render({
            'date_data': res['lines']['date_data'],
            'date_from': res['lines']['date_from'],
            'date_to': res['lines']['date_to'],
            'data': res['lines']['data'],
            'summary': res['lines']['summary'],
            'accounts': res['lines']['accounts'],
            'with_initial_balance': res['lines']['with_initial_balance'],
            'branch_name': res['lines']['branch_name'],
         })
        self.template_area = res['lines']

    def _get_report_data(self, date_from=False, date_to=False, two_column=False, summary=False):
        if date_to and date_from:
            if date_from > date_to:
                raise UserError("From date can't be greater than To date")
        cash_book_account = self.env['ir.config_parameter'].sudo().get_param('cash_book.cash_book_account_id')
        if not cash_book_account:
            raise UserError("You haven't configured Cash Book Account in Settings\n"
                            "Please select your cash account for Cash Book")
        accounts = []
        if cash_book_account:
            accounts_summ = tuple(cash_book_account.strip('][').split(','))
            if cash_book_account != '[]':
                accounts = self.env['account.account'].search([('id', 'in', [int(b_id) for b_id in accounts_summ])]).mapped('id')
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'account_ids': accounts,
            'with_initial_balance': True,
            'twoCol': two_column,
            'summary': summary if summary else False,
        }
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
