# -*- coding: utf-8 -*-
#  ♦ Import ♦
from odoo import models, api, fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning, UserError


# ♦ Daybook Co-Operative ♦
class ReportDaybookCoOp(models.TransientModel):
    _name = 'beta.daybook.co.op'
    _inherit = 'beta.reports'

    name = fields.Char(default='DayBook Co Op')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    dayabook_entries_filter = fields.Boolean(default=False)


    @api.model
    def default_get(self, fields_list):
        res = super(ReportDaybookCoOp, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = today
        res['date_to'] = today
        return res

    def get_report_values(self, data=None):
        date_from = date_to = False
        details = {}
        if data['date_from'] and data['date_to']:
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d")
            days = date_to - date_from
            details = {}

            for i in range(days.days + 1):
                day = date_from + timedelta(days=i)
                date = day.strftime("%Y-%m-%d")
                data['date'] = date
                rows = self.get_sale_details(data)
                result = {'rec': []}
                abc = []
                dat = []
                rslt = []
                for j in rows['records']:
                    for m in rows['records'][j]['data']:
                        both = False
                        if rows['records'][j]['data'][m]['debit'] > 0 and rows['records'][j]['data'][m]['credit'] > 0:
                            both = True
                        # Credit
                        if rows['records'][j]['data'][m]['credit'] == 0 or both:
                            invoice_no = str(rows['records'][j]['name'])
                            if invoice_no[:8] == 'SUPP.OUT':
                                inv_no = invoice_no[9:]
                            elif invoice_no[:7] == 'CUST.IN':
                                inv_no = invoice_no[8:]
                            else:
                                inv_no = invoice_no
                            abc.append({
                                'invoice_no': inv_no,
                                'account_name': rows['records'][j]['data'][m]['name'],
                                'credit': rows['records'][j]['data'][m]['credit'],
                                'debit': rows['records'][j]['data'][m]['debit'],
                                'partner_name': rows['records'][j]['data'][m]['partner'],
                                'type': rows['records'][j]['data'][m]['type'],
                                'cash_type': rows['records'][j]['data'][m]['cash_type'],
                                'model': rows['records'][j]['data'][m]['model'],
                                'id': rows['records'][j]['data'][m]['id'],
                                'form': rows['records'][j]['data'][m]['form'],
                                # 'sequence': rows['records'][j]['data'][m]['sequence'],
                            })
                        if rows['records'][j]['data'][m]['debit'] == 0:
                            invoice_no = str(rows['records'][j]['name'])
                            if invoice_no[:8] == 'SUPP.OUT':
                                inv_no = invoice_no[9:]
                            elif invoice_no[:7] == 'CUST.IN':
                                inv_no = invoice_no[8:]
                            else:
                                inv_no = invoice_no
                            dat.append({
                                'invoice_no': inv_no,
                                'account_name': rows['records'][j]['data'][m]['name'],
                                'credit': rows['records'][j]['data'][m]['credit'],
                                'debit': rows['records'][j]['data'][m]['debit'],
                                'partner_name': rows['records'][j]['data'][m]['partner'],
                                'type': rows['records'][j]['data'][m]['type'],
                                'cash_type': rows['records'][j]['data'][m]['cash_type'],
                                'model': rows['records'][j]['data'][m]['model'],
                                'id': rows['records'][j]['data'][m]['id'],
                                'form': rows['records'][j]['data'][m]['form'],
                                # 'sequence': rows['records'][j]['data'][m]['sequence'],
                            })
                doc = sorted(abc, key=lambda i: i['invoice_no'])
                # doc = sorted(doc1, key=lambda i: i['sequence'])
                credit_tot = debit_tot = 0
                for c in range(len(doc)):
                    try:
                        if doc[c]['account_name'] == doc[c+1]['account_name']:
                            credit_tot += doc[c]['credit']
                            debit_tot += doc[c]['debit']
                            rslt.append({
                                'invoice_no': doc[c]['invoice_no'],
                                'account_name': doc[c]['account_name'],
                                'credit': doc[c]['credit'],
                                'debit': doc[c]['debit'],
                                'partner_name': doc[c]['partner_name'],
                                'type': doc[c]['type'],
                                'cash_type': doc[c]['cash_type'],
                                'credit_tot': None,
                                'debit_tot': None,
                                'model': doc[c]['model'],
                                'id': doc[c]['id'],
                                'form': doc[c]['form'],
                            })
                        else:
                            credit_tot += doc[c]['credit']
                            debit_tot += doc[c]['debit']
                            rslt.append({
                                'invoice_no': doc[c]['invoice_no'],
                                'account_name': doc[c]['account_name'],
                                'credit': doc[c]['credit'],
                                'debit': doc[c]['debit'],
                                'partner_name': doc[c]['partner_name'],
                                'type': doc[c]['type'],
                                'cash_type': doc[c]['cash_type'],
                                'credit_tot': credit_tot,
                                'debit_tot': debit_tot,
                                'model': doc[c]['model'],
                                'id': doc[c]['id'],
                                'form': doc[c]['form'],
                            })
                            credit_tot = debit_tot = 0
                    except:
                        credit_tot += doc[c]['credit']
                        debit_tot += doc[c]['debit']
                        rslt.append({
                            'invoice_no': doc[c]['invoice_no'],
                            'account_name': doc[c]['account_name'],
                            'credit': doc[c]['credit'],
                            'debit': doc[c]['debit'],
                            'partner_name': doc[c]['partner_name'],
                            'type': doc[c]['type'],
                            'cash_type': doc[c]['cash_type'],
                            'credit_tot': credit_tot,
                            'debit_tot': debit_tot,
                            'model': doc[c]['model'],
                            'id': doc[c]['id'],
                            'form': doc[c]['form'],
                        })
                # doc1 = sorted(dat, key=lambda i: i['sequence'])
                doc1 = sorted(dat, key=lambda i: i['invoice_no'])
                credit_tot = debit_tot = 0
                for c in range(len(doc1)):
                    try:
                        if doc1[c]['account_name'] == doc1[c + 1]['account_name']:
                            credit_tot += doc1[c]['credit']
                            debit_tot += doc1[c]['debit']
                            rslt.append({
                                'invoice_no': doc1[c]['invoice_no'],
                                'account_name': doc1[c]['account_name'],
                                'credit': doc1[c]['credit'],
                                'debit': doc1[c]['debit'],
                                'partner_name': doc1[c]['partner_name'],
                                'type': doc1[c]['type'],
                                'cash_type': doc1[c]['cash_type'],
                                'credit_tot': None,
                                'debit_tot': None,
                                'model': doc1[c]['model'],
                                'id': doc1[c]['id'],
                                'form': doc1[c]['form'],
                            })
                        else:
                            credit_tot += doc1[c]['credit']
                            debit_tot += doc1[c]['debit']
                            rslt.append({
                                'invoice_no': doc1[c]['invoice_no'],
                                'account_name': doc1[c]['account_name'],
                                'credit': doc1[c]['credit'],
                                'debit': doc1[c]['debit'],
                                'partner_name': doc1[c]['partner_name'],
                                'type': doc1[c]['type'],
                                'cash_type': doc1[c]['cash_type'],
                                'credit_tot': credit_tot,
                                'debit_tot': debit_tot,
                                'model': doc1[c]['model'],
                                'id': doc1[c]['id'],
                                'form': doc1[c]['form'],
                            })
                            credit_tot = debit_tot = 0
                    except:
                        credit_tot += doc1[c]['credit']
                        debit_tot += doc1[c]['debit']
                        rslt.append({
                            'invoice_no': doc1[c]['invoice_no'],
                            'account_name': doc1[c]['account_name'],
                            'credit': doc1[c]['credit'],
                            'debit': doc1[c]['debit'],
                            'partner_name': doc1[c]['partner_name'],
                            'type': doc1[c]['type'],
                            'cash_type': doc1[c]['cash_type'],
                            'credit_tot': credit_tot,
                            'debit_tot': debit_tot,
                            'model': doc1[c]['model'],
                            'id': doc1[c]['id'],
                            'form': doc1[c]['form'],
                        })
                result['rec'] = rslt
                result['debit_total'] = rows['debit_total']
                result['credit_total'] = rows['credit_total']
                result['debit_total_cash'] = rows['debit_total_cash']
                result['credit_total_cash'] = rows['credit_total_cash']
                result['cash_opening'] = rows['cash_opening']
                result['cash_closing'] = rows['cash_closing']
                if result['rec'] or (date_from == date_to):
                    details[day.strftime("%d-%m-%Y")] = result
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
            'report_type': data.get('report_type') if data else '',
            'branch_name': branch_name
        }

    # ♦ ▼ Fully Settlement ▼ ♦
    def paid_or_not(self, inv):
        paid_or_not = False
        other_paid_or_not = False
        cash_in = False
        if inv.invoice_payments_widget != 'false' and inv.payment_state == 'paid':
            pay_json_value = inv.sudo()._get_reconciled_info_JSON_values()

            # ▼ if bill type is credit fully settle is set to False ▼
            bill_type = True
            if 'bill_type' in self.env['account.move']._fields:
                if inv.bill_type == 'credit':
                    bill_type = False

            types = ["Cash", "Bank", "UPI"]
            type = "Cash"
            payment_amt = 0
            for pay in pay_json_value:
                if pay['journal_name'] == type:
                    cash_in = True
                if inv.invoice_date == pay['date'] and len(pay_json_value) == 1 and pay['account_payment_id'] and bill_type:
                    self.env.cr.execute("select amount from account_payment where id=" + str(pay['account_payment_id']))
                    payment_amt += self.env.cr.fetchall()[0][0]
                    if inv.amount_total == payment_amt and type == pay['journal_name']:
                        type = pay['journal_name']
                        paid_or_not = True
                    else:
                        paid_or_not = False
                elif inv.invoice_date == pay['date'] and len(pay_json_value) != 1 and pay['account_payment_id'] and self.dayabook_entries_filter:
                    self.env.cr.execute("select amount from account_payment where id=" + str(pay['account_payment_id']))
                    qry_res = self.env.cr.fetchall()
                    payment_amt += qry_res[0][0]
                else:
                    paid_or_not = False
                    break

            if inv.amount_total == payment_amt and not cash_in and self.dayabook_entries_filter:
                other_paid_or_not = True
        return paid_or_not, other_paid_or_not

    def check_payment_invoice(self, payment):
        paid_or_not = False
        other_paid_or_not = False

        if len(payment.reconciled_invoice_ids) == 1:
            for inv in payment.reconciled_invoice_ids:
                paid_or_not, other_paid_or_not = self.paid_or_not(inv)
        return paid_or_not, other_paid_or_not

    def get_sale_details(self, data):
        account_move_line_obj = self.env['account.move.line']       # ← Account move line object
        hr_daily_attendance_obj_exist = False
        if self.env['ir.model'].search([('model', '=', 'hr.daily.attendance')]):
            hr_daily_attendance_obj_exist = True
            hr_daily_attendance_obj = self.env['hr.daily.attendance']
        cash_credit = cash_debit = debit_total = credit_total = credit_total_cash = debit_total_cash = 0
        datas = {
            'data': [],
            'records': {},
        }
        dataq = {
            'data': [],
            'result': {}
        }

        # ▼ Setting Domain ▼
        domain = [('move_id.state', '=', 'posted'),('move_id.date', '=', data['date'])]

        if data.get('allowed_company_ids'):
            domain.append(('company_id', 'in', data.get('allowed_company_ids')))

        #  ▼  Company Opening ▼
        opening_move = self.env.company.account_opening_move_id

        # ▼ Branch  Opening ▼
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
        movelines = account_move_line_obj.search(domain, order='account_id asc')
        discount_ledger_credit = self.env['ir.config_parameter'].sudo().get_param('sales_disc_journal_entries.discount_ledger_credit')
        discount_ledger_debit = self.env['ir.config_parameter'].sudo().get_param('sales_disc_journal_entries.discount_ledger')
        split_discount_lines = False
        # if discount_ledger_debit == discount_ledger_credit:
        #     split_discount_lines = True
        self.dayabook_entries_filter = self.env['ir.config_parameter'].sudo().get_param('daybook_co_op.dayabook_entries_filter')
        fully_settled = False
        move_line_fields = account_move_line_obj._fields
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
            slip = False
            if self.env['ir.model'].search([('model', '=', 'hr.payslip')]):
                slip = self.env['hr.payslip'].sudo().search([('move_ids', '=', line.move_id.id)])

            attendance = False
            if hr_daily_attendance_obj_exist:
                attendance = hr_daily_attendance_obj.sudo().search([('invoice_id', '=', line.move_id.id)])

            debit = line.debit
            credit = line.credit
            cash_type = line.move_id.direct_journal_id_inx.type
            cash_type2 = line.move_id.journal_id.type
            print(line.account_id.name,"name")
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
            if type not in ['VB','VR']:
                if line.payment_id:
                    if line.payment_id.partner_type != 'supplier':
                        fully_settled, other_paid_or_not = self.check_payment_invoice(line.payment_id)

                        if fully_settled:
                            continue
                        else:
                            pass

                        if other_paid_or_not and ((credit > 0 and type == "CR") or (debit > 0 and type == "SP")):
                            continue
                        else:
                            pass
                else:

                    fully_settled, other_paid_or_not = self.paid_or_not(line.move_id)
                    if 'is_freight' in move_line_fields:
                        opo = not line.is_rounding_line and not line.is_freight
                    else:
                        opo = not line.is_rounding_line

                    if opo and (fully_settled and ((debit > 0 and type == "CI") or (credit > 0 and type in ["VB", "CR"]))):
                        if 'is_discount_line' in move_line_fields:
                            if not line.is_discount_line:
                                continue
                        else:
                            continue
                    elif fully_settled:
                        if 'is_discount_line' in move_line_fields:
                            if not line.is_discount_line:
                                cash_type = "cash"
                                cash_type2 = "cash"
                        else:
                            cash_type = "cash"
                            cash_type2 = "cash"

                    if 'is_freight' in move_line_fields:
                        opo = not line.is_rounding_line and not line.is_freight
                    else:
                        opo = not line.is_rounding_line

                    if opo and (other_paid_or_not and ((debit > 0 and type == "CI") or (credit > 0 and type == "CR"))):
                        if 'is_discount_line' in move_line_fields:
                            if not line.is_discount_line:
                                continue
                        else:
                            continue
            print(line.account_id.name, "name final")
            if line.account_id.id in data['cash_account_ids']:
                cash_credit += credit
                cash_debit += debit
            else:
                if 'is_payslip_adjustment_line' in line._fields and line.is_payslip_adjustment_line:
                    account_grouper = str(line.account_id.id) + "_payslip_adj"
                else:
                    account_grouper = line.account_id.id
                if line.move_id.direct_journal_id_inx:
                    # if line.move_id.move_type == 'entry':
                    #     partner = line.partner_id.name if line.partner_id else line.name if line.name else ''
                    # else:
                    #     partner = line.partner_id.name if line.partner_id else ''
                    if line.move_id.id in datas['records']:
                        if line.account_id.id in datas['records'][line.move_id.id]['data']:
                            datas['records'][line.move_id.id]['data'][line.account_id.id]['credit'] += line.debit
                            datas['records'][line.move_id.id]['data'][line.account_id.id]['debit'] += line.credit
                            if not (self.env['ir.model'].search([('model', '=', 'fund.generator')]) and (self.env['fund.generator'].search([('invoice_id', '=', line.move_id.id)]) or self.env['fund.generator.line'].search([('invoice_id', '=', line.move_id.id)]))):
                                if datas['records'][line.move_id.id]['data'][line.account_id.id]['partner'] != line.partner_id.name:
                                    datas['records'][line.move_id.id]['data'][line.account_id.id]['partner'] += ', ' + line.partner_id.name if line.partner_id else ''
                        else:
                            if line.payment_id:
                                form = False
                                voucher_name = line.payment_id.name
                                voucher_model = line.payment_id._name
                                voucher_id = line.payment_id.id
                            elif slip:
                                form = self.env.ref('om_hr_payroll.view_hr_payslip_form', False)
                                voucher_name = slip.number
                                voucher_model = 'hr.payslip'
                                voucher_id = slip.id
                            else:
                                voucher_name = line.move_id.name
                                voucher_model = line.move_id._name
                                voucher_id = line.move_id.id
                                if self.env['ir.model'].search([('model', '=', 'fund.generator')]) and self.env['fund.generator'].search([('invoice_id', '=', line.move_id.id)]):
                                    partner_td = line.name
                                elif attendance:
                                    partner_td = line.name
                                else:
                                    partner_td = line.partner_id.name if line.partner_id else line.name
                                    # if line.description and 'payslip<>' in line.description:
                                    #     payslip_note = line.description.split('<>')
                                    #     partner_td += (' - ' + payslip_note[1]) if len(payslip_note) > 1 else ''

                                if self.env['ir.model'].search([('model', '=', 'production.move')]) and self.env['production.move'].search([('invoice_id', '=', line.move_id.id)]):
                                    partner_td = line.name
                            datas['records'][line.move_id.id]['data'][account_grouper] = {
                                'invoice_no': voucher_name,
                                'name': line.account_id.name,
                                'credit': debit,
                                'debit': credit,
                                'partner': partner_td if partner_td else '',
                                'type': type,
                                'move_type': line.move_id.move_type,
                                'cash_type': cash_type,
                                'fully_settled': fully_settled,
                                'model': voucher_model,
                                'id': voucher_id,
                                'form': form.id if form else False,
                                'sequence': line.account_id.sequence if 'sequence' in line.account_id._fields else None,
                                'account_type': line.account_id.user_type_id.name,
                            }
                    else:
                        partner_td = line.partner_id.name if line.partner_id else line.move_id.ref
                        # if line.description and 'payslip<>' in line.description:
                        #     payslip_note = line.description.split('<>')
                        #     partner_td += (' - ' + payslip_note[1]) if len(payslip_note) > 1 else ''
                        if line.journal_id.type in ('agent_collection', 'day_deposit'):
                            grouper = str(line.id) + line.move_id.name
                        else:
                            grouper = line.move_id.id
                        if line.payment_id:
                            form = False
                            voucher_name = line.payment_id.name
                            voucher_model = line.payment_id._name
                            voucher_id = line.payment_id.id
                        elif slip:
                            form = self.env.ref('om_hr_payroll.view_hr_payslip_form', False)
                            voucher_name = slip.number
                            voucher_model = 'hr.payslip'
                            voucher_id = slip.id
                        else:
                            voucher_name = line.move_id.name
                            voucher_model = line.move_id._name
                            voucher_id = line.move_id.id
                        if attendance:
                            partner_td = line.name

                        # ▼ Production ▼
                        if self.env['ir.model'].search([('model', '=', 'production.move')]) and self.env['production.move'].search([('invoice_id', '=', line.move_id.id)]):
                            partner_td = line.name
                        datas['records'][grouper] = {
                            'name': voucher_name,
                            'data': {
                                account_grouper: {
                                    'invoice_no': voucher_name,
                                    'name': line.account_id.name,
                                    'credit': debit,
                                    'debit': credit,
                                    'partner': partner_td,
                                    'type': type,
                                    'move_type': line.move_id.move_type,
                                    'cash_type': cash_type,
                                    'fully_settled': fully_settled,
                                    'model': voucher_model,
                                    'id': voucher_id,
                                    'form': form.id if form else False,
                                    'sequence': line.account_id.sequence if 'sequence' in line.account_id._fields else None,
                                    'account_type': line.account_id.user_type_id.name,
                                }
                            }
                        }
                    if cash_type == 'cash':
                        debit_total_cash += debit
                        credit_total_cash += credit
                    else:
                        debit_total += debit
                        credit_total += credit
                else:
                    if 'is_discount_line' in line._fields and line.is_discount_line:
                        grouper = str(line.move_id.id) + 'disc'
                        if split_discount_lines:
                            grouper += '_debit' if credit > 0 else '_credit'
                    else:
                        grouper = line.move_id.id

                    if grouper in datas['records']:
                        if account_grouper in datas['records'][grouper]['data']:
                            datas['records'][grouper]['data'][account_grouper]['credit'] += line.debit
                            datas['records'][grouper]['data'][account_grouper]['debit'] += line.credit
                        else:
                            if line.payment_id:
                                form = False
                                voucher_name = line.payment_id.name
                                voucher_model = line.payment_id._name
                                voucher_id = line.payment_id.id
                            elif slip:
                                form = self.env.ref('om_hr_payroll.view_hr_payslip_form', False)
                                voucher_name = slip.number
                                voucher_model = 'hr.payslip'
                                voucher_id = slip.id
                            else:
                                voucher_name = line.move_id.name
                                voucher_model = line.move_id._name
                                voucher_id = line.move_id.id
                            partner_td = line.partner_id.name if line.partner_id else line.move_id.ref
                            # if line.description and 'payslip<>' in line.description:
                            #     payslip_note = line.description.split('<>')
                            #     partner_td += (' - ' + payslip_note[1]) if len(payslip_note) > 1 else ''
                            if attendance:
                                partner_td = line.name
                            if self.env['ir.model'].search([('model', '=', 'production.move')]) and self.env['production.move'].search([('invoice_id', '=', line.move_id.id)]):
                                partner_td = line.name

                            datas['records'][grouper]['data'][account_grouper] = {
                                'invoice_no': voucher_name,
                                'name': line.account_id.name,
                                'credit': line.debit,
                                'debit': line.credit,
                                'partner': partner_td,
                                'type': type,
                                'move_type': line.move_id.move_type,
                                'cash_type': cash_type2,
                                'fully_settled': fully_settled,
                                'model': voucher_model,
                                'id': voucher_id,
                                'form': form.id if form else False,
                                'sequence': line.account_id.sequence if 'sequence' in line.account_id._fields else None,
                                'account_type': line.account_id.user_type_id.name,
                            }

                    else:
                        if line.payment_id:
                            form = False
                            voucher_name = line.payment_id.name
                            voucher_model = line.payment_id._name
                            voucher_id = line.payment_id.id
                        elif slip:
                            form = self.env.ref('om_hr_payroll.view_hr_payslip_form', False)
                            voucher_name = slip.number
                            voucher_model = 'hr.payslip'
                            voucher_id = slip.id
                        else:
                            voucher_name = line.move_id.name
                            voucher_model = line.move_id._name
                            voucher_id = line.move_id.id

                        partner_td = line.partner_id.name if line.partner_id else line.move_id.ref
                        # if line.description and line.description and 'payslip<>' in line.description:
                        #     payslip_note = line.description.split('<>')
                        #     partner_td += (' - ' + payslip_note[1]) if len(payslip_note) > 1 else ''
                        if attendance:
                            partner_td = line.name
                        if self.env['ir.model'].search([('model', '=', 'production.move')]) and self.env['production.move'].search([('invoice_id', '=', line.move_id.id)]):
                            partner_td = line.name
                        datas['records'][grouper] = {
                            'name': voucher_name,
                            'data': {
                                account_grouper: {
                                    'invoice_no': line.payment_id.name if line.payment_id else line.move_id.name,
                                    'name': line.account_id.name,
                                    'credit': line.debit,
                                    'debit': line.credit,
                                    'partner': partner_td,
                                    'type': type,
                                    'move_type': line.move_id.move_type,
                                    'fully_settled': fully_settled,
                                    'cash_type': cash_type2,
                                    'model': voucher_model,
                                    'id': voucher_id,
                                    'form': form.id if form else False,
                                    'sequence': line.account_id.sequence if 'sequence' in line.account_id._fields else None,
                                    'account_type': line.account_id.user_type_id.name,
                                }
                            }
                        }
                    if cash_type2 == 'cash':
                        debit_total_cash += debit
                        credit_total_cash += credit
                    else:
                        debit_total += debit
                        credit_total += credit
        datas['debit_total'] = debit_total
        datas['credit_total'] = credit_total
        datas['debit_total_cash'] = debit_total_cash
        datas['credit_total_cash'] = credit_total_cash
        opening = self.get_cash_opening(data)
        cash_closing = (credit_total + credit_total_cash + opening[1]) - (debit_total + debit_total_cash + opening[0])
        datas['cash_opening'] = opening
        datas['cash_closing'] = cash_closing
        print(datas)
        return datas

    def get_cash_opening(self, data):
        move_line_obj = self.env['account.move.line']
        credit = debit = 0
        domain = [
            ('move_id.state', '=', 'posted'),
            ('move_id.date', '<', data['date']),
            ('account_id', 'in', data['cash_account_ids'])
        ]

        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))
        if data.get('allowed_company_ids'):
            domain.append(('company_id', 'in', data.get('allowed_company_ids')))
        movelines = move_line_obj.search(domain, order='account_id asc')
        opening_move = self.env.company.account_opening_move_id

        if 'branch' in data:
            branch = self.env['res.branch'].search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in self.env['res.branch']:
                for branches in branch:
                    account_opening_move_id = branches.account_opening_move_id
                    opening_move = account_opening_move_id
                    if opening_move and opening_move.state == 'posted' and opening_move.date.strftime("%Y-%m-%d") == data['date']:
                        for openline in opening_move.line_ids:
                            if openline.account_id.id in data['cash_account_ids']:
                                movelines += openline
        else:
            if opening_move and opening_move.state == 'posted' and opening_move.date.strftime("%Y-%m-%d") == data['date']:
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

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')

        res = self._get_report_data(
            searchDateFrom=self.date_from.strftime('%Y-%m-%d'),
            searchDateTo=self.date_to.strftime('%Y-%m-%d'),
        )

        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('daybook_co_op.report_daybook_co_op')._render({
            'date_from': res['lines']['date_from'],
            'date_to': res['lines']['date_to'],
            'data': res['lines']['data'],
            'details': res['lines']['details'],
            'report_type': res['lines']['report_type'],
        })

        self.template_area = res['lines']

    def _get_report_data(self, searchDateFrom=False, searchDateTo=False):
        cash_journal_ids = self.env['account.journal'].search([('type', '=', 'cash')])
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
        }
        cash_ids = []
        for journal in cash_journal_ids:
            cash_ids.append(journal.default_account_id.id)
            cash_ids.append(journal.loss_account_id.id)
            cash_ids.append(journal.profit_account_id.id)
        data['cash_account_ids'] = cash_ids
        if self._context.get('allowed_company_ids'):
            data['allowed_company_ids'] = self._context.get('allowed_company_ids')
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }

