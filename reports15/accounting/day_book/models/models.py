# -*- coding: utf-8 -*-
from pytz import timezone
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class BetaDayBook(models.TransientModel):  # change this
    _name = 'beta.day.book'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Day Book')  # change this
    date_from = fields.Date()
    date_to = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaDayBook, self).default_get(fields_list)
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
        details = {}
        if data['date_from'] and data['date_to']:
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d")
            days = date_to - date_from

            for i in range(days.days + 1):
                day = date_from + timedelta(days=i)
                date = day.strftime("%Y-%m-%d")
                data['date'] = date
                rows = self.get_sale_details(data)
                if rows['records'] or (date_from == date_to):
                    details[day.strftime("%d-%m-%Y")] = rows
            date_from = date_from.strftime('%d/%m/%Y')
            date_to = date_to.strftime('%d/%m/%Y')
        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'details': details,
            'branch_name': branch_name
        }

    #  ▼ Fully Settle ▼
    def paid_or_not(self, inv):
        paid_or_not = False
        if inv.invoice_payments_widget != 'false' and inv.payment_state == 'paid':
            pay_json_value = inv.sudo()._get_reconciled_info_JSON_values()
            bill_type = True

            # ▼ if bill type is credit then fully settle is False ▼
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

    def get_sale_details(self, data):
        account_move_line_obj = self.env['account.move.line']
        cash_credit = cash_debit = debit_total = credit_total = 0
        datas = {
            'data': [],
            'records': {},
        }
        domain = [('move_id.state', '=', 'posted'), ('move_id.date', '=', data['date'])]
        if data.get('allowed_company_ids'):
            domain.append(
                ('company_id', 'in', data.get('allowed_company_ids')))

        opening_move = self.env.company.account_opening_move_id

        # ▼ Branch Opening ▼
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

        movelines = account_move_line_obj.search(domain)
        for line in movelines:
            type = ''
            if line.move_id.move_type == 'out_invoice':
                type = "CI"
            elif line.move_id.move_type == 'out_refund':
                type = "CR"
            elif line.move_id.move_type == 'in_invoice':
                type = "VB"
            elif line.move_id.move_type == 'in_refund':
                type = "VR"
            elif line.move_id.move_type == 'out_receipt':
                type = "SR"
            elif line.move_id.move_type == 'in_receipt':
                type = "PR"
            elif line.move_id.move_type == 'entry':
                if line.payment_id:
                    if line.payment_id.payment_type == 'outbound':
                        type = "SP"
                    elif line.payment_id.payment_type == 'inbound':
                        type = 'CR'
                    elif line.payment_id.payment_type == 'transfer':
                        type = 'IT'
                else:
                    if line.move_id.direct_journal_type_inx == 'receipt':
                        type = 'RV'
                    elif line.move_id.direct_journal_type_inx == 'payment':
                        type = 'PV'
                    else:
                        type = 'JV'

            debit = line.debit
            credit = line.credit
            if not type in ['VB', 'VR']:
                if line.payment_id:

                    fully_settled = self.check_payment_invoice(line.payment_id)
                    if fully_settled:
                        continue
                    else:
                        pass
                else:

                    fully_settled = self.paid_or_not(line.move_id)

                    if 'is_freight' in line._fields:
                        opo = not line.is_rounding_line and not line.is_freight
                    else:
                        opo = not line.is_rounding_line

                    if opo and (fully_settled and ((debit > 0 and type == "CI") or (credit > 0 and type in ["VB", "CR"]))):
                        if 'is_discount_line' in line._fields:
                            if not line.is_discount_line:
                                continue
                        else:
                            continue
                    elif fully_settled:
                        if 'is_discount_line' in line._fields:
                            if not line.is_discount_line:
                                cash_type = "cash"
                                cash_type2 = "cash"
                        else:
                            cash_type = "cash"
                            cash_type2 = "cash"

            if line.account_id.id in data['cash_account_ids']:
                cash_credit += credit
                cash_debit += debit
            else:
                if self.env['ir.config_parameter'].sudo().get_param('day_book.daybook_default_order') == 'voucher':
                    first_grouper = line.move_id.id
                    second_grouper = line.account_id.id
                else:
                    first_grouper = line.account_id.id
                    second_grouper = line.move_id.id
                if line.payment_id:
                    form = False
                else:
                    if line.move_id.move_type == 'entry':
                        if line.move_id.direct_journal_type_inx in ['receipt', 'payment']:
                            form = self.env.ref('inexoft_account_voucher.direct_journal_view_move_form', False)
                        else:
                            form = self.env.ref('account.view_move_form', False)
                    elif line.move_id.move_type in ['in_invoice', 'in_refund']:
                        form = self.env.ref('account.view_move_form', False)
                    else:
                        form = False
                if first_grouper in datas['records']:
                    if second_grouper in datas['records'][first_grouper]['data']:
                        datas['records'][first_grouper]['data'][second_grouper]['credit'] += debit
                        datas['records'][first_grouper]['data'][second_grouper]['debit'] += credit
                    else:
                        datas['records'][first_grouper]['data'][second_grouper] = {
                            'name': line.account_id.name,
                            'credit': debit,
                            'debit': credit,
                            'partner': line.partner_id.name,
                            'type': type,
                            'move_name': line.payment_id.name if line.payment_id else line.move_id.name,
                            'model': line.payment_id._name if line.payment_id else line.move_id._name,
                            'id': line.payment_id.id if line.payment_id else line.move_id.id,
                            'form': form.id if form else False,
                        }
                else:

                    datas['records'][first_grouper] = {
                        # 'name': line.payment_id.name if line.payment_id else line.move_id.name,
                        # 'model': line.payment_id._name if line.payment_id else line.move_id._name,
                        # 'id': line.payment_id.id if line.payment_id else line.move_id.id,
                        # 'form': form.id if form else False,
                        'data': {
                            second_grouper: {
                                'name': line.account_id.name,
                                'credit': line.debit,
                                'debit': line.credit,
                                'partner': line.partner_id.name,
                                'type': type,
                                'move_name': line.payment_id.name if line.payment_id else line.move_id.name,
                                'model': line.payment_id._name if line.payment_id else line.move_id._name,
                                'id': line.payment_id.id if line.payment_id else line.move_id.id,
                                'form': form.id if form else False,
                            }
                        }
                    }
                debit_total += debit
                credit_total += credit
        datas['debit_total'] = debit_total
        datas['credit_total'] = credit_total
        opening = self.get_cash_opening(data)
        cash_closing = (credit_total + opening[1]) - (debit_total + opening[0])
        datas['cash_opening'] = opening
        datas['cash_closing'] = cash_closing
        return datas

    def get_cash_opening(self, data):
        move_line_obj = self.env['account.move.line']
        credit = debit = 0

        domain = [
            ('move_id.state', '=', 'posted'),
            ('move_id.date', '<', data['date']),
            ('account_id', 'in', data['cash_account_ids'])
        ]

        if data.get('allowed_company_ids'):
            domain.append(('company_id', 'in', data.get('allowed_company_ids')))
        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))
        opening_moves = self.env.company.account_opening_move_id
        if 'branch' in data:
            # if self.env.user.branch_id:
            domain.append(('move_id.branch_id', 'in', data['branch']))
            opening_moves = self.env['account.move']
            branch_obj = self.env['res.branch']
            branches = branch_obj.search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in branch_obj._fields:
                for branch in branches:
                    account_opening_move_id = branch.account_opening_move_id
                    if account_opening_move_id and account_opening_move_id.state == 'posted':
                        opening_moves += account_opening_move_id

        movelines = move_line_obj.search(domain, order="account_id asc")
        for opening_move in opening_moves:
            if opening_move and opening_move.date.strftime("%Y-%m-%d") == data['date']:
                for openline in opening_move.line_ids:
                    if openline.account_id.id in data['cash_account_ids']:
                        movelines += openline
        for line in movelines:
            debit += line.debit
            credit += line.credit
        diff = credit - debit
        if diff > 0:
            credit = diff
            debit = 0
        else:
            credit = 0
            debit = abs(diff)
        return (credit, debit)

    def get_actual_date(self, TZ_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(TZ_datetime, fmt)
        result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime(fmt)

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'))
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('day_book.report_daybook')._render({
            'date_from': res['lines']['date_from'],
            'date_to': res['lines']['date_to'],
            'data': res['lines']['data'],
            'details': res['lines']['details'],
            'branch_name': res['lines']['branch_name'],
        })
        self.template_area = res['lines']

    def _get_report_data(self, date_from=False, date_to=False):
        if date_to and date_from:
            if date_from > date_to:
                raise Warning("From date can't be greater than To date")
        cash_journal_ids = self.env['account.journal'].search(
            [('type', '=', 'cash')])
        data = {
            'date_from': date_from,
            'date_to': date_to,
        }
        cash_ids = []
        for journal in cash_journal_ids:
            cash_ids.append(journal.default_account_id.id)
            cash_ids.append(journal.loss_account_id.id)
            cash_ids.append(journal.profit_account_id.id)
        data['cash_account_ids'] = cash_ids
        if self._context.get('allowed_company_ids'):
            data['allowed_company_ids'] = self._context.get(
                'allowed_company_ids')
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
