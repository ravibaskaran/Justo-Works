# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaSalesReport(models.TransientModel):  # change this
    _name = 'beta.sales.report'  # change this
    _inherit = 'beta.reports'

    new_logic = fields.Boolean(default=False)

    name = fields.Char(default='Booking Report')  # change this
    # journal = fields.Many2one('account.journal', domain=[('type', '=', ['cash', 'bank'])], create=False)
    report_type = fields.Selection([('bill_wise', 'Bill Wise'), ('date_wise', 'Date Wise'),
                                    ('month_wise', 'Month Wise')], default='bill_wise')
    report_order = fields.Selection([('both', 'Both'), ('sales', 'Sales'), ('sales_return', 'Sales Return')],
                                    default='both')
    bill_type_wise = fields.Boolean(default=False)
    include_cancel = fields.Boolean(default=False)
    date_from = fields.Date(default=datetime.today())
    date_to = fields.Date(default=datetime.today())

    @api.model
    def get_report_values(self):
        date_from = date_to = False
        branch = ''
        # if 'branch_id' in self.env.user._fields:
        #     branch_obj = self.env['res.branch']
        #     if data['branch_ids']:
        #         if len(data['branch_ids']) > 1:
        #             pass
        #         else:
        #             data['branch_total'] = False
        #         for locati in data['branch_ids']:
        #             branch += branch_obj.browse(locati).name + ","
        # if not self.journal:
        #     self.update({'pay_type': 'All'})
        # if self.date_from:
        #     try:
        #         self.date_from = datetime.strptime(
        #             self.date_from, "%Y-%m-%d").strftime('%d/%m/%Y')
        #     except TypeError:
        #         raise Warning("Invalid Date Format")
        # if self.date_to:
        #     try:
        #         self.date_to = datetime.strptime(
        #             self.date_to, "%Y-%m-%d").strftime('%d/%m/%Y')
        #     except TypeError:
        #         raise Warning("Invalid Date Format")

        return {
            'data': self,
            'date_from': self.date_from.strftime('%d/%m/%Y'),
            'date_to': self.date_to.strftime('%d/%m/%Y'),
            # 'branch_total': data['branch_total'],
            # 'branch_ids': branch,
            'summary': self.report_type,
            'lines': self.get_sales_summary(),
        }

    def get_sales_summary(self):
        sales = {}
        returns = {}
        payment_summary = []
        amount_total, taxable_total, tax_sum, other_charge_total, rounding_value_total = 0, 0, 0, 0, 0
        sgst_sum = 0
        cgst_sum = 0
        igst_sum = 0
        cess_sum = 0
        discount_total = 0
        total_bill_value = 0
        total_mrp = 0
        date_start = self.date_from
        date_end = self.date_to
        # branch_ids = data['branch_ids']
        type = 'sales'
        invces = self.env['account.move']
        if type == 'sales':
            if self.report_order == 'both':
                sales = self.get_report_data(invces, 'out_invoice', 1)
                # print('sales:', sales)
                returns = self.get_report_data(invces, 'out_refund', -1)
                amount_total = sales['total']['amount_total'] - \
                    returns['total']['amount_total']
                taxable_total = sales['total']['taxable_total'] - \
                    returns['total']['taxable_total']
                sgst_sum = sales['total']['sgst_sum'] - \
                    returns['total']['sgst_sum']
                cgst_sum = sales['total']['cgst_sum'] - \
                    returns['total']['cgst_sum']
                igst_sum = sales['total']['igst_sum'] - \
                    returns['total']['igst_sum']
                cess_sum = sales['total']['cess_sum'] - \
                    returns['total']['cess_sum']

                tax_sum = sales['total']['tax_sum'] - \
                    returns['total']['tax_sum']
                rounding_value_total = sales['total']['rounding_value_sum'] - \
                    returns['total']['rounding_value_sum']
                other_charge_total = sales['total']['other_charge_sum'] - \
                    returns['total']['other_charge_sum']
                discount_total = sales['total']['total_discount'] - \
                    returns['total']['total_discount']
                total_bill_value = sales['total']['bill_val_total'] - \
                    returns['total']['bill_val_total']
                total_mrp = sales['total']['mrp_total'] - \
                    returns['total']['mrp_total']
            elif self.report_order == 'sales':
                sales = self.get_report_data(invces, 'out_invoice', 1)
            elif self.report_order == 'sales_return':
                returns = self.get_report_data(invces, 'out_refund', -1)
                # print('returns',returns)

        return {
            'type': sales,
            'date_start': date_start,
            'date_end': date_end,
            'sales': sales,
            # 'branch_ids': branch_ids,
            'returns': returns,
            'taxable_total': taxable_total,
            'tax_sum': tax_sum,
            # 'branch_total': data['branch_total'],
            'rounding_value_total': rounding_value_total,
            'other_charge_total': other_charge_total,
            'amount_total': amount_total,
            'discount_total': discount_total,
            'total_bill_value': total_bill_value,
            'sgst_sum': sgst_sum,
            'cgst_sum': cgst_sum,
            'igst_sum': igst_sum,
            'cess_sum': cess_sum,
            'total_mrp': total_mrp
        }

    def get_report_data(self, invoices, type, sign):
        date_start = self.date_from
        date_end = self.date_to
        date_start = date_start.strftime('%Y-%m-%d')
        date_end = date_end.strftime('%Y-%m-%d')
        print('date:',date_start,date_end)
        # branch_ids = self.branch_ids
        # branch_total = data['branch_total']
        ac_mv = self.env['account.move']
        # print(data['include_cancel'], "data['include_cancel']")
        # print("data['summary']", data['summary'])
        dom = []
        if self.include_cancel and self.report_type == "bill_wise":
            qr_dom = """
                    am.state in ('posted','cancel') and
                    am.invoice_date>='""" + date_start + """' and
                    am.invoice_date<='""" + date_end + """'
                    """
        else:
            qr_dom = """
               am.state = 'posted' and 
               am.invoice_date>='""" + date_start + """' and 
               am.invoice_date<='""" + date_end + """'     
           """
        # if 'branch_id' in ac_mv._fields:
        #     dom = [('invoice_date', '>=', date_start),
        #            ('invoice_date', '<=', date_end), ('state', '=', 'posted'), ('branch_id', 'in', branch_ids)]
        #     branch_id_ids = ','.join([str(br) for br in branch_ids])
        #     branch_join = ''
        #     branch = ''
        #     if branch_id_ids:
        #         qr_dom += "  and am.branch_id in  (" + branch_id_ids + ")"
        #         branch_join = " left join res_branch rb on am.branch_id=rb.id"
        #         branch = "rb.name as branch_name,"
        # else:
            dom = [('invoice_date', '>=', date_start),
                   ('invoice_date', '<=', date_end), ('state', '=', 'posted')]

            # .replace('[', '(').replace(']', ')')
        dom.append(('type', 'in', [type]))
        qr_dom += "  and am.move_type in ('"+type+"')"
        order_by = ''
        if self.report_type == 'bill_wise':
            order_by = ' order by am.date,am.name'
        else:
            order_by = ' order by am.date'

        final_data = []
        taxable_sum = 0
        tax_sum = 0
        cgst_sum = 0
        sgst_sum = 0
        igst_sum = 0
        cess_sum = 0
        total_sum = 0
        total_discount = 0
        bill_val_total = 0
        rounding_value_sum = 0
        other_charge_sum = 0
        mrp_total = 0
        mobile = None
        card_no = None
        payment_summary = {}
        summary = {}
        account_move_obj = self.env['account.move']
        account_move_line_obj = self.env['account.move.line']
        account_payment_obj = self.env['account.payment']
        account_journal_obj = self.env['account.journal']

        account_move_fields = account_move_obj._fields
        account_move_line_fields = account_move_line_obj._fields
        account_payment_fields = account_payment_obj._fields
        journal_fields = account_journal_obj._fields
        if self.report_type != 'month_wise':
            inv_date = "TO_CHAR(am.invoice_date ,'DD/MM/YYYY') as invoice_date,"
        else:
            inv_date = "TO_CHAR(am.invoice_date ,'Month-YYYY') as invoice_date,"

        self.new_logic = True
        # self.new_logic = False
        if self.new_logic:
            qr_fields = ("""am.state state,aml.id aml_id ,am.id move_id,am.name move_name,am.date move_date,
            am.amount_untaxed,am.amount_tax, """ + inv_date + """"""
                         # +str(branch)+
                         """
            acr.rounding,am.amount_total,aml.quantity line_quantity,aml.price_unit line_price_unit,aml.exclude_from_invoice_tab
                ,am.narration,atx.name,aml.price_total,ap.id payment_id,ap.create_date,ap.amount payment_amount,aj.name journal_name,aj.code journal_short_name
                ,aml.tax_line_id,atx.name line_tax_name,rp.name partner_name
                """)
            if 'other_charge_total' in account_move_fields:
                qr_fields += ",am.other_charge_total"
            if 'mobile' in account_payment_fields:
                qr_fields += ",ap.mobile"
            if 'card_no' in account_payment_fields:
                qr_fields += ",ap.card_no"
            if 'amount_discount' in account_move_obj:
                qr_fields += ",am.amount_discount"
            if 'bill_amount' in account_move_obj:
                qr_fields += ",am.bill_amount"
            if 'payment_type' in journal_fields:
                qr_fields += ",aj.payment_type"
            # if 'payment_type' in journal_fields:
            #     qr_fields += ",aj.payment_type"

            qry1 = ("""
                select """ + qr_fields + """               
                from 
                account_move_line aml 
                left join account_move am on am.id=aml.move_id
                left join res_partner rp on rp.id=am.partner_id
                left join account_tax atx on aml.tax_line_id=atx.id
                left join account_partial_reconcile apr on apr.full_reconcile_id = aml.full_reconcile_id
                left join account_move_line aml2 on (aml2.id != aml.id and (apr.debit_move_id=aml2.id or apr.credit_move_id=aml2.id) )
                left join account_payment ap on aml2.payment_id=ap.id
                left join account_journal aj on aj.id=ap.move_id
                left join account_cash_rounding acr on acr.id=am.invoice_cash_rounding_id
                """
                    # +str(branch_join)+
                    """
                where  
            """+qr_dom+""" """+str(order_by)+""" """)
            # print("qry1", qry1)
            # and am.id = 55430
            self.env.cr.execute(qry1)
            invoices = self.env.cr.dictfetchall()
            print('invoices:', invoices)
            data_dict = {}
            for line in invoices:
                state = line.get('state')
                move_id = line.get('move_id')
                move_name = line.get('move_name')
                move_date = line.get('move_date')
                branch = line.get('branch_name')
                invoice_date = line.get('invoice_date')
                narration = line.get('narration')
                if state != 'cancel':
                    amount_untaxed = line.get('amount_untaxed') or 0
                    amount_tax = line.get('amount_tax') or 0
                    rounding_value = float(line.get('rounding_value') or 0)
                    amount_total = line.get('amount_total') or 0
                    price_total = line.get('price_total') or 0
                    payment_id = line.get('payment_id')
                    payment_date = line.get('payment_date')
                    journal_name = line.get('journal_name')
                    journal_short_name = line.get('journal_short_name')
                    other_charge_total = line.get('other_charge_total') or 0
                    mobile = line.get('mobile') or ''
                    card_no = line.get('card_no') or ''
                    exclude_from_invoice_tab = line.get('exclude_from_invoice_tab')
                    line_quantity = line.get('line_quantity') or 0
                    line_price_unit = line.get('line_price_unit') or 0
                    amount_gtotal = 0
                    if exclude_from_invoice_tab == False:
                        amount_gtotal = line_quantity * line_price_unit
                    amount_discount = line.get('amount_discount') or 0
                    bill_amount = line.get('bill_amount') or 0
                    tax_line_id = line.get('tax_line_id')
                    line_tax_name = line.get('line_tax_name')
                    partner_name = line.get('partner_name')
                    payment_type = line.get('payment_type') or False
                    payment_amount = line.get('payment_amount') or 0
                else:
                    amount_untaxed = 0
                    amount_tax = 0
                    rounding_value = 0
                    amount_total = 0

                    price_total = 0
                    payment_id = line.get('payment_id')
                    payment_date = line.get('payment_date')
                    journal_name = line.get('journal_name')
                    journal_short_name = line.get('journal_short_name')
                    other_charge_total = line.get('other_charge_total') or 0
                    mobile = line.get('mobile') or ''
                    card_no = line.get('card_no') or ''
                    exclude_from_invoice_tab = line.get('exclude_from_invoice_tab')
                    line_quantity = 0
                    line_price_unit = 0
                    amount_gtotal = 0
                    if exclude_from_invoice_tab == False:
                        amount_gtotal = line_quantity * line_price_unit
                    amount_discount = 0
                    bill_amount = 0
                    tax_line_id = line.get('tax_line_id')
                    line_tax_name = line.get('line_tax_name')
                    partner_name = line.get('partner_name')
                    payment_type = False
                    payment_amount = 0

                bill_type = ''

                inv_amt_total = amount_total
                mrp = bill_amount

                cgst = 0
                sgst = 0
                igst = 0
                cess = 0
                if tax_line_id:
                    if 'CGST' in line_tax_name:
                        cgst = price_total
                    if 'SGST' in line_tax_name:
                        sgst = price_total
                    if 'IGST' in line_tax_name:
                        igst = price_total
                    if 'CESS' in line_tax_name:
                        cess = price_total

                if payment_id:
                    # if invoice_date == payment_date and payment_amount == amount_gtotal:
                    if payment_type:
                        # if 'payment_type' in journal_fields:
                        bill_type = dict(journal_fields['payment_type'].selection).get(payment_type)
                    elif journal_short_name:
                        bill_type = journal_short_name
                    else:
                        bill_type = journal_name
                        # type = bill_type
                    # if payment_details.get(payment_id):
                    # else:
                    #     bill_type = "Credit"

                else:
                    bill_type = "Credit"
                type = 'Credit'
                re = ''
                if data_dict.get(move_id):
                    if narration:
                        re = narration[:30]
                    elif mobile:
                        re = mobile
                    elif card_no:
                        re = card_no
                    else:
                        re = ''
                    data_dict.get(move_id)['cgst'] += cgst
                    data_dict.get(move_id)['sgst'] += sgst
                    data_dict.get(move_id)['igst'] += igst
                    data_dict.get(move_id)['cess'] += cess
                    data_dict.get(move_id)['bill_val'] += amount_gtotal
                    data_dict.get(move_id)['remarks'] = re

                    # if data_dict.get(move_id)['type'] != "Credit" and bill_type:
                    #     type = bill_type
                    if payment_id:
                        if data_dict[move_id]['payments'].get(payment_id):
                            pass
                        else:
                            data_dict[move_id]['payments'][payment_id] = [payment_date, bill_type, payment_amount]

                        # data_dict.get(move_id)['type'] = bill_type
                else:
                    # type = bill_type

                    if narration:
                        re = narration[:30]
                    elif mobile:
                        re = mobile
                    elif card_no:
                        re = card_no
                    else:
                        re = ''
                    # print('move_name', move_name)
                    data_dict[move_id] = {
                        'state': state,
                        'number': move_name,
                        'date': move_date.strftime("%d/%m/%Y"),
                        'invoice_date': invoice_date,
                        'customer': partner_name,
                        'taxable': amount_untaxed,
                        'tax': amount_tax / 2,
                        'rounding': rounding_value,
                        'other_charges': other_charge_total,
                        'total': inv_amt_total,
                        'type': type,
                        'branch': branch,
                        'discount': amount_discount,
                        'bill_val': amount_gtotal,
                        'cgst': cgst,
                        'sgst': sgst,
                        'igst': igst,
                        'cess': cess,
                        'mrp': mrp,
                        'remarks': re,
                        'payments': {},
                    }
                    # print(move_id, data_dict)
                    if payment_id:
                        data_dict[move_id]['payments'][payment_id] = [payment_date, bill_type, payment_amount]
            # print('data_dict', data_dict)
            for inv_line in data_dict:
                amount_discount = data_dict[inv_line]['discount']  # amount_discount
                amount_gtotal = data_dict[inv_line]['bill_val']  # amount_gtotal
                rounding_value = data_dict[inv_line]['rounding']  # rounding_value
                other_charge_total = data_dict[inv_line]['other_charges']  # other_charge_total
                inv_amt_total = data_dict[inv_line]['total']  # inv_amt_total
                mrp = data_dict[inv_line]['mrp']  # mrp
                amount_untaxed = data_dict[inv_line]['taxable']  # amount_untaxed
                amount_tax = data_dict[inv_line]['tax']  # amount_tax / 2
                date = data_dict[inv_line]['date']
                amount_untaxed = data_dict[inv_line]['taxable']  # inv.amount_untaxed
                sgst = data_dict[inv_line]['sgst']
                cgst = data_dict[inv_line]['cgst']
                igst = data_dict[inv_line]['igst']
                cess = data_dict[inv_line]['cess']
                # cess = inv_amt_total - (sgst + cgst + igst)
                type = "Credit"
                payments = data_dict[inv_line]['payments']
                if payments:
                    print(786)
                    bil_ty1 = list(payments.values())[0][1]
                    tot_pay_amt = 0
                    for payment in payments:
                        tot_pay_amt += payments[payment][2]
                        if bil_ty1 != payments[payment][1] or date != payments[payment][0]:
                            type = "Credit"
                            break
                    else:
                        if inv_amt_total == tot_pay_amt:
                            type = bil_ty1
                            data_dict[inv_line]['type'] = type

                # if type == self.journal or self.journal == "All":

                cgst_sum += cgst
                sgst_sum += sgst
                igst_sum += igst
                cess_sum += cess

                total_discount += amount_discount
                bill_val_total += amount_gtotal
                rounding_value_sum += rounding_value
                other_charge_sum += other_charge_total
                total_sum += inv_amt_total
                mrp_total += mrp
                taxable_sum += amount_untaxed
                tax_sum += amount_tax/2
                # if payment_summary.get(type):
                #     payment_summary[type]['bill_val'] += amount_gtotal
                #     payment_summary[type]['discount'] += amount_discount
                #     payment_summary[type]['taxable'] += amount_untaxed
                #     payment_summary[type]['sgst'] += sgst
                #     payment_summary[type]['cgst'] += cgst
                #     payment_summary[type]['igst'] += igst
                #     payment_summary[type]['cess'] += cess
                #     payment_summary[type]['mrp'] += mrp
                #     payment_summary[type]['rounding'] += rounding_value
                #     payment_summary[type]['other_charges'] += other_charge_total
                #     payment_summary[type]['total'] += inv_amt_total
                # else:
                #     payment_summary[type] = {
                #         'bill_val': amount_gtotal,
                #         'discount': amount_discount,
                #         'taxable': amount_untaxed,
                #         'sgst': sgst,
                #         'cgst': cgst,
                #         'igst': igst,
                #         'cess': cess,
                #         'mrp': mrp,
                #         'rounding': rounding_value,
                #         'other_charges': other_charge_total,
                #         'total': inv_amt_total
                #     }
                final_data.append(data_dict[inv_line])


        if self.report_type != 'bill_wise':
            for line in final_data:
                # print('line', line)
                if line['invoice_date'] in summary:
                    summary[line['invoice_date']]['taxable'] += line['taxable']
                    summary[line['invoice_date']]['rounding'] += line['rounding']
                    summary[line['invoice_date']]['other_charges'] += line['other_charges']
                    summary[line['invoice_date']]['total'] += line['total']
                    summary[line['invoice_date']]['discount'] += line['discount']
                    summary[line['invoice_date']]['bill_val'] += line['bill_val']
                    summary[line['invoice_date']]['cgst'] += line['cgst']
                    summary[line['invoice_date']]['sgst'] += line['sgst']
                    summary[line['invoice_date']]['igst'] += line['igst']
                    summary[line['invoice_date']]['cess'] += line['cess']
                    summary[line['invoice_date']]['mrp'] += line['mrp']
                    # if branch_total:
                    #     if line['branch'] in summary[line['invoice_date']]['branch']:
                    # summary[line['invoice_date']]['taxable'] += line['taxable']
                    # summary[line['invoice_date']]['rounding'] += line['rounding']
                    # summary[line['invoice_date']]['other_charges'] += line['other_charges']
                    # summary[line['invoice_date']]['total'] += line['total']
                    # summary[line['invoice_date']]['discount'] += line['discount']
                    # summary[line['invoice_date']]['bill_val'] += line['bill_val']
                    # summary[line['invoice_date']]['cgst'] += line['cgst']
                    # summary[line['invoice_date']]['sgst'] += line['sgst']
                    # summary[line['invoice_date']]['igst'] += line['igst']
                    # summary[line['invoice_date']]['cess'] += line['cess']
                    # summary[line['invoice_date']]['mrp'] += line['mrp']
                # else:
                    summary[line['invoice_date']] = {
                        'taxable': line['taxable'],
                        'rounding': line['rounding'],
                        'other_charges': line['other_charges'],
                        'total': line['total'],
                        'discount': line['discount'],
                        'bill_val': line['bill_val'],
                        'cgst': line['cgst'],
                        'sgst': line['sgst'],
                        'igst': line['igst'],
                        'cess': line['cess'],
                        'mrp': line['mrp'],
                    }
                # else:
                #     if branch_total:
                    summary[line['invoice_date']] = {
                        'date': line['invoice_date'],
                        'taxable': line['taxable'],
                        'rounding': line['rounding'],
                        'other_charges': line['other_charges'],
                        'total': line['total'],
                        'discount': line['discount'],
                        'bill_val': line['bill_val'],
                        'cgst': line['cgst'],
                        'sgst': line['sgst'],
                        'igst': line['igst'],
                        'cess': line['cess'],
                        'mrp': line['mrp'],
                        'branch': {
                            line['branch']: {
                                'taxable': line['taxable'],
                                'rounding': line['rounding'],
                                'other_charges': line['other_charges'],
                                'total': line['total'],
                                'discount': line['discount'],
                                'bill_val': line['bill_val'],
                                'cgst': line['cgst'],
                                'sgst': line['sgst'],
                                'igst': line['igst'],
                                'cess': line['cess'],
                                'mrp': line['mrp'],
                            }
                        }
                    }
                else:
                    summary[line['invoice_date']] = {
                        'date': line['invoice_date'],
                        'taxable': line['taxable'],
                        'rounding': line['rounding'],
                        'other_charges': line['other_charges'],
                        'total': line['total'],
                        'discount': line['discount'],
                        'bill_val': line['bill_val'],
                        'cgst': line['cgst'],
                        'sgst': line['sgst'],
                        'igst': line['igst'],
                        'cess': line['cess'],
                        'mrp': line['mrp'],
                    }
            final_data = None
        else:
            pass
            # if self.bill_type_wise:
            #     final_data = sorted(final_data, key=lambda i: (i['type'], i['date']), reverse=False)
            #     seen_numbers = set()
            #     filtered_final_data = []
            #     for item in final_data:
            #         number = item.get('number')
            #         if number not in seen_numbers:
            #             seen_numbers.add(number)
            #             filtered_final_data.append(item)
            #     final_data = filtered_final_data
            # print('final_data', final_data)
        # print(payment_summary,"payment_summary")
        return {'sales_lines': final_data,
                'total': {
                    'taxable_total': taxable_sum,
                    'tax_sum': tax_sum,
                    'rounding_value_sum': rounding_value_sum,
                    'other_charge_sum': other_charge_sum,
                    'amount_total': total_sum,
                    'total_discount': total_discount,
                    'bill_val_total': bill_val_total,
                    'cgst_sum': cgst_sum,
                    'sgst_sum': sgst_sum,
                    'igst_sum': igst_sum,
                    'cess_sum': cess_sum,
                    'mrp_total': mrp_total
                },
                'payment_summarys': payment_summary,
                'summarys': summary,
                }

    # @api.model
    def get_html(self):
        res = self._get_report_data()
        # print('res', res)
        inv = self.env['account.move']
        is_gtotal = False
        is_discount = False
        if 'amount_gtotal' in inv._fields:
            is_gtotal = True
        if 'amount_discount' in inv._fields:
            is_discount = True

        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        # res['lines'] = self.env.ref('sales_summary.report_sales_summary').render(
        self.template_area = self.env.ref('sales_summary.report_sales_summary')._render({
            'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'report_order': res['lines']['report_type'],
             # 'branch_ids': res['lines']['branch_ids'],
             'is_gtotal': is_gtotal,
             'summary': res['lines']['summary'],
             # 'branch_total': res['lines']['branch_total'],
             'is_discount': is_discount

        })
        # print(res)
        return res

    @api.model
    def _get_report_data(self):
        is_branch = False

        if 'branch_id' in self.env.user._fields:
            branch_list = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            branch_default = self.env['res.branch'].search(
                [('id', '=', self.env.user.branch_id.id)])
            is_branch = True
        else:
            branch_default = self.env['res.company'].search(
                [('id', '=', self.env.user.company_id.id)])

            is_branch = False
        rl = ''

        # if self.report_location:
        #     rl = [int(i) for i in report_location]

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            # 'branch_ids': rl if rl else (branch_default.id,),
            'sale_subtype': self.report_type if self.report_type else False,
            # 'pay_type': self.journal if self.journal else False,
            # 'summary': summary if summary else False,
            # 'branch_total': branch_total if branch_total else False,
            'bill_type_wise': self.bill_type_wise if self.bill_type_wise else False,
            'include_cancel': self.include_cancel if self.include_cancel else False,
        }
        dat = self.get_report_values()
        # print('dat', dat)

        do = {}
        lo = {}
        pay_types = []
        account_journal = []
        if 'branch_id' in self.env.user._fields:
            for l in branch_list:
                if l.id != branch_default.id:
                    lo[l.id] = l.name

        account_journal_obj = self.env['account.journal']
        journal_fields = account_journal_obj._fields
        account_journals = account_journal_obj.search([('type', 'in', ['cash', 'bank'])])

        if 'short_name' in journal_fields:
            for journal in account_journals:
                if journal.short_name:
                    account_journal.append(journal.short_name)
                else:
                    account_journal.append(journal.name)
        else:
            account_journal = account_journals.mapped('name')

        pay_types = account_journal
        pay_types.append("Credit")
        if pay_types:
            pay_types = sorted(pay_types)
        return {
            'lines': dat,
            'variants': do,
            'branch': lo,
            'bid': branch_default.id,
            'bname': branch_default.name,
            'pay_types': pay_types,
            'is_branch': is_branch,
        }