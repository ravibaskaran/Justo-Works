# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning
from pytz import timezone


class ReportPurchase(models.TransientModel):
    _name = 'report.purchase'
    _inherit = 'beta.reports'
    _description = 'Purchase Summary Report'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    report_type = fields.Selection([
        ('both', 'Both'),
        ('purchase', 'Purchase'),
        ('purchase_return', 'Purchase Return')], String="Report Order", default="both")

    @api.model
    def default_get(self, fields_list):
        res = super(ReportPurchase, self).default_get(fields_list)
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
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        products = ''

        if data['date_from'] and data['date_to']:
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d")
            days = date_to - date_from

            for i in range(days.days + 1):
                day = date_from + timedelta(days=i)
                date = day.strftime("%Y-%m-%d")
                data['date'] = date
            date_from = date_from.strftime('%d/%m/%Y')
            date_to = date_to.strftime('%d/%m/%Y')
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'branch_name': data['branch_name'],
            'branch_ids': branch,
            'lines': self.get_purchase_summary(data),
        }

    def get_purchase_summary(self, data):
            sales = {}
            returns = {}
            amount_total, taxable_total, tax_sum, sales_value_total = 0, 0, 0, 0
            total_add = 0
            sgst_sum = 0
            cgst_sum = 0
            igst_sum = 0
            date_start = data['date_from']
            date_end = data['date_to']
            branch_ids = data['branch_ids']

            type = 'purchase'
            domain = [('invoice_date', '>=', date_start),
                      ('invoice_date', '<=', date_end), ('state', '=', 'posted')]
            invces = self.env['account.move']
            if type == 'purchase':
                if data['report_type'] == 'both':
                    sales = self.get_report_data(invces, data, 'in_invoice', 1)
                    returns = self.get_report_data(invces, data, 'in_refund', -1)
                    amount_total = sales['total']['amount_total'] - \
                                   returns['total']['amount_total']
                    taxable_total = sales['total']['taxable_total'] - \
                                    returns['total']['taxable_total']
                    tax_sum = sales['total']['tax_sum'] - \
                              returns['total']['tax_sum']
                    sgst_sum = sales['total']['sgst_sum'] - \
                               returns['total']['sgst_sum']
                    cgst_sum = sales['total']['cgst_sum'] - \
                               returns['total']['cgst_sum']
                    igst_sum = sales['total']['igst_sum'] - \
                               returns['total']['igst_sum']
                    sales_value_total = sales['total']['sales_value_total'] - \
                                        returns['total']['sales_value_total']
                    total_add = sales['total']['total_add'] - \
                                returns['total']['total_add']
                elif data['report_type'] == 'purchase':
                    sales = self.get_report_data(invces, data, 'in_invoice', 1)
                elif data['report_type'] == 'purchase_return':
                    returns = self.get_report_data(invces, data, 'in_refund', -1)
                    #print(returns)
            return {
                'type': sales,
                'date_start': date_start,
                'date_end': date_end,
                'sales': sales,
                'returns': returns,
                'branch_ids': branch_ids,
                'amount_total': amount_total,
                'taxable_total': taxable_total,
                'sales_value_total': sales_value_total,
                'tax_sum': tax_sum,
                'total_add': total_add,
                'sgst_sum': sgst_sum,
                'cgst_sum': cgst_sum,
                'igst_sum': igst_sum
                }

    def get_report_data(self, invoices, data, move_type, sign):
            date_start = data['date_from']
            date_end = data['date_to']
            branch_ids = data['branch_ids']
            # dom = [('invoice_date', '>=', date_start),
            # ('invoice_date', '<=', date_end), ('state', '=', 'posted'), ('branch_id', 'in', branch_ids)]
            dom = [('invoice_date', '>=', date_start),
                   ('invoice_date', '<=', date_end), ('state', '=', 'posted')]
            dom.append(('move_type', 'in', [move_type]))
            if 'expiry_type' in self.env['account.move']._fields:
                if move_type == 'in_invoice':
                    dom.append(('expiry_type', '!=', 'expiry_rpl'))
                elif move_type == 'in_refund':
                    dom.append(('expiry_type', '!=', 'expiry_rtn'))
            invoices = invoices.search(dom, order='name asc')
            final_data = []
            taxable_sum = 0
            tax_sum = 0
            total_sum = 0
            cgst_sum = 0
            sgst_sum = 0
            igst_sum = 0
            sales_value_total = 0
            total_add = 0
            for inv in invoices:
                cgst = 0
                sgst = 0
                igst = 0
                for line in inv.line_ids:
                    if line.tax_line_id:
                        if 'CGST' in line.tax_line_id.name:
                            cgst += line.price_total
                        if 'SGST' in line.tax_line_id.name:
                            sgst += line.price_total
                        if 'IGST' in line.tax_line_id.name:
                            igst += line.price_total
                cgst_sum += cgst
                sgst_sum += sgst
                igst_sum += igst

                taxable_sum += inv.amount_untaxed
                tax_sum += inv.amount_tax
                total_sum += inv.amount_total
                # sales_value = sum(inv.invoice_line_ids.mapped('sales_value'))
                sales_value = 0
                # for i in inv.invoice_line_ids:
                #     tqty = (i.quantity + i.free_qty) if 'free_qty' in i._fields else i.quantity
                #     sales_value += i.sales_rate * tqty
                # sales_value = inv.total_mrp
                sales_value_total += sales_value
                #total_add += inv.other_charge_total
                total_add += 0
                final_data.append({
                    'number': inv.name,
                    # 'bill_number': inv.bill_number,
                    'bill_number': '',
                    # 'bill_date': inv.bill_date.strftime("%d/%m/%Y"),
                    'bill_date': inv.invoice_date.strftime("%d/%m/%Y"),
                    'date': inv.date.strftime("%d/%m/%Y"),
                    'customer': inv.partner_id.name,
                    'taxable': inv.amount_untaxed,
                    'tax': inv.amount_tax,
                    #'additional_charges': inv.other_charge_total,
                    'additional_charges': 0,
                    'total': inv.amount_total,
                    'sales_value': sales_value,
                    'cgst': cgst,
                    'sgst': sgst,
                    'igst': igst,
                })

            return {'sales_lines': final_data,
                    'total': {
                        'taxable_total': taxable_sum,
                        'tax_sum': tax_sum,
                        'amount_total': total_sum,
                        'sales_value_total': sales_value_total,
                        'total_add': total_add,
                        'cgst_sum': cgst_sum,
                        'sgst_sum': sgst_sum,
                        'igst_sum': igst_sum,
                    }}

    def get_html(self):
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'), report_type=self.report_type)
        #print(res['lines']['lines'])

        self.template_area = self.env.ref('purchase_summary_report.report_purchase_summary')._render({
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'report_type': self.report_type,
            'data': res['lines'],
            'lines': res['lines']['lines']
        })

    def _get_report_data(self, date_from=False, date_to=False, report_type=False):
        is_branch = False
        branch_name = ''

        if 'branch_id' in self.env.user._fields:
            branch_list = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            branch_default = self.env['res.branch'].search(
                [('id', '=', self.env.user.branch_id.id)])
            is_branch = True
        else:
            branch_default = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])

            is_branch = False
        rl = ''

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))

        data = {
            'date_from': date_from,
            'date_to': date_to,
            'report_type': report_type if report_type else False,
            'branch_name': branch_name,
            'branch_ids': rl if rl else (branch_default.id,),

        }
        dat = self.get_report_values(data=data)

        do = {}
        lo = {}
        if 'branch_id' in self.env.user._fields:
            for l in branch_list:
                if l.id != branch_default.id:
                    lo[l.id] = l.name
        return {
            'lines': dat,
            'variants': do,
            'branch': lo,
            'bid': branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }
