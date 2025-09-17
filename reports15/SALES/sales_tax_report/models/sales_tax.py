# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaSalesTaxReport(models.TransientModel):  # change this
    _name = 'beta.sales.tax.report'  # change this
    _inherit = 'beta.reports'

    date_from = fields.Date(default=datetime.today())
    date_to = fields.Date(default=datetime.today())
    report_type = fields.Selection([('bill_wise', 'Bill Wise'), ('date_wise', 'Date Wise'),
                                    ('month_wise', 'Month Wise')], default='bill_wise')
    report_order = fields.Selection([('both', 'Both'), ('sales', 'Sales'), ('sales_return', 'Sales Return')],
                                    default='both')
    tax_filter = fields.Boolean(default=False)
    tax_ids = fields.Many2many('account.tax', domain=[('type_tax_use', '=', 'sale')])

    @api.model
    def get_report_values(self, data=None):
        date_from = self.date_from.strftime('%d/%m/%Y')
        date_to = self.date_to.strftime('%d/%m/%Y')

        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        products = ''

        # if data['date_from']:
        #     try:
        #         date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
        #     except TypeError:
        #         raise Warning("Invalid Date Format")
        # if data['date_to']:
        #     try:
        #         date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
        #     except TypeError:
        #         raise Warning("Invalid Date Format")
        # print(data['order'])

        return {
            'data': data,
            'order': self.report_type,
            'date_from': date_from,
            'date_to': date_to,
            # 'branch_ids': branch,
            # 'branch_name': data['branch_name'],
            'lines': self.get_sales_tax(data),
            'orders': 'sss',
        }

    def get_sales_tax(self, data):
        date_start = data['date_from']
        date_end = data['date_to']
        # branch = data['branch_ids']
        type = 'sales'
        sales = {}
        returns = {}
        if type == 'sales':
            # print('type_invoice',data['type_invoice'])
            if data['type_invoice'] == 'both':
                sales = self.get_report_data(date_start, date_end, type, 'sales', data)
                returns = self.get_report_data(date_start, date_end, type, 'sales_return', data)
            elif data['type_invoice'] == 'sales':
                sales = self.get_report_data(date_start, date_end, type, 'sales', data)
            elif data['type_invoice'] == 'sales_return':
                returns = self.get_report_data(date_start, date_end, type, 'sales_return', data)
        return {
            # 'doc_ids': data['ids'],
            # 'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'sales': sales,
            'returns': returns,
            'type': type,
        }

    def get_report_data(self, date_start, date_end, type, subtype, data):
        # tax_data_dict = self.get_tax_data_dict()
        # branch = branch
        # print('date_start', date_start)
        total_sum = 0
        taxable_sum = 0
        cgst_sum = 0
        sgst_sum = 0
        igst_sum = 0
        cess_sum = 0
        total_qty = 0
        lines = {}

        move_line_obj = self.env['account.move.line']
        if 'branch_id' in self.env.user._fields:
            domain = [('move_id.state', '=', 'posted'), ('move_id.invoice_date', '>=', date_start)]
                      # ('move_id.invoice_date', '<=', date_end), ('branch_id', 'in', branch)]
        else:
            domain = [('move_id.state', '=', 'posted'), ('move_id.invoice_date', '>=', date_start),
                      ('move_id.invoice_date', '<=', date_end)]
        if type == 'sales':
            if subtype == 'sales':
                domain.append(('move_id.move_type', 'in', ['out_invoice']))
            elif subtype == 'sales_return':
                domain.append(('move_id.move_type', 'in', ['out_refund']))
        elif type == 'purchase':
            if subtype == 'purchase':
                domain.append(('move_id.move_type', 'in', ['in_invoice']))
            elif subtype == 'purchase_return':
                domain.append(('move_id.move_type', 'in', ['in_refund']))
        move_line = move_line_obj.search(domain, order="move_id desc")
        for summary in move_line:
            price_unit = summary.price_unit
            if summary.discount != 0:
                price_unit = summary.price_unit - (summary.price_unit * summary.discount / 100)
            taxdata = {}
            if data['order'] == 'date_wise':
                grouper = summary.move_id.invoice_date.strftime('%d/%m/%Y')
                line_date = summary.move_id.invoice_date.strftime('%d/%m/%Y')
                line_name = ''
                line_partner = ''
                line_gst = ''
            elif data['order'] == 'month_wise':
                grouper = summary.move_id.invoice_date.strftime('%m/%Y')
                line_date = summary.move_id.invoice_date.strftime('%B -%Y')
                line_name = ''
                line_partner = ''
                line_gst = ''
            else:
                grouper = summary.move_id.id
                line_date = summary.move_id.invoice_date.strftime('%d/%m/%Y')
                line_name = summary.move_id.name
                line_partner = summary.move_id.partner_id.name
                line_gst = summary.move_id.partner_id.vat
            if summary.tax_ids:

                ###########new logic####################
                taxes = summary.tax_ids.compute_all(price_unit, quantity=summary.quantity)
                cgst = 0
                sgst = 0
                igst = 0
                cess = 0
                if taxes['taxes']:
                    tax_id = summary.tax_ids[0].id
                    for comtax in taxes['taxes']:
                        cgst = 0
                        sgst = 0
                        igst = 0
                        cess = 0
                        if 'cgst' in comtax['name'].lower():
                            cgst += comtax['amount']
                        elif 'sgst' in comtax['name'].lower():
                            sgst += comtax['amount']
                        elif 'igst' in comtax['name'].lower():
                            igst += comtax['amount']
                        elif 'cess' in comtax['name'].lower():
                            cess += comtax['amount']
                        # tax_id = comtax['id']
                        if tax_id not in data['tax_list'] and data['tax_filter'] == 'True':

                            continue
                        if tax_id in taxdata:
                            # taxdata[tax_id]['total_excluded'] += taxes['total_excluded']
                            # taxdata[tax_id]['total_included'] += taxes['total_included']
                            taxdata[tax_id]['cgst'] += cgst
                            taxdata[tax_id]['sgst'] += sgst
                            taxdata[tax_id]['igst'] += igst
                            taxdata[tax_id]['cess'] += cess
                        else:
                            taxdata[tax_id] = {
                                'total_excluded': taxes['total_excluded'],
                                'total_included': taxes['total_included'],
                                'cgst': cgst,
                                'sgst': sgst,
                                'igst': igst,
                                'cess': cess,
                            }
                ###########new logic####################
                final = []
                for item in taxdata:
                    # if taxdata[item]['cgst'] != 0 or taxdata[item]['sgst'] != 0 or taxdata[item]['igst'] != 0 or \
                    #         taxdata[item]['cess'] != 0:
                    final.append({
                        'tax_id': item,
                        'cgst': taxdata[item]['cgst'],
                        'sgst': taxdata[item]['sgst'],
                        'igst': taxdata[item]['igst'],
                        'cess': taxdata[item]['cess'],
                        'total_excluded': taxdata[item]['total_excluded'],
                        'total_included': taxdata[item]['total_included'],
                    })
                    # print(summary.move_id.name,final)
                    total_excluded = round(final[0]['total_excluded'], 2)
                    cgst = round(final[0]['cgst'], 2)
                    sgst = round(final[0]['sgst'], 2)
                    igst = round(final[0]['igst'], 2)
                    cess = round(final[0]['cess'], 2)
                    total_included = round(final[0]['total_included'], 2)
                    if final[0]['tax_id'] in lines:
                        if grouper in lines[final[0]['tax_id']]['data']:
                            lines[final[0]['tax_id']]['data'][grouper]['base'] += total_excluded
                            lines[final[0]['tax_id']]['data'][grouper]['cgst'] += cgst
                            lines[final[0]['tax_id']]['data'][grouper]['sgst'] += sgst
                            lines[final[0]['tax_id']]['data'][grouper]['igst'] += igst
                            lines[final[0]['tax_id']]['data'][grouper]['cess'] += cess
                            lines[final[0]['tax_id']]['data'][grouper]['amount'] += total_included
                            lines[final[0]['tax_id']]['data'][grouper]['qty'] += summary.quantity
                        else:
                            lines[final[0]['tax_id']]['data'][grouper] = {
                                'date': line_date,
                                'name': line_name,
                                'partner': line_partner,
                                'gst': line_gst,
                                'base': total_excluded,
                                'cgst': cgst,
                                'sgst': sgst,
                                'igst': igst,
                                'cess': cess,
                                'amount': total_included,
                                'qty': summary.quantity,
                            }
                        lines[final[0]['tax_id']]['total_base'] += total_excluded
                        lines[final[0]['tax_id']]['total_cgst'] += cgst
                        lines[final[0]['tax_id']]['total_sgst'] += sgst
                        lines[final[0]['tax_id']]['total_igst'] += igst
                        lines[final[0]['tax_id']]['total_cess'] += cess
                        lines[final[0]['tax_id']]['total_amount'] += total_included
                        lines[final[0]['tax_id']]['total_qty'] += summary.quantity
                    else:
                        lines[final[0]['tax_id']] = {
                            'name': self.env['account.tax'].search([('id', '=', final[0]['tax_id'])], limit=1).name,
                            'data': {
                                grouper: {
                                    'date': line_date,
                                    'name': line_name,
                                    'partner': line_partner,
                                    'gst': line_gst,
                                    'base': total_excluded,
                                    'cgst': cgst,
                                    'sgst': sgst,
                                    'igst': igst,
                                    'cess': cess,
                                    'amount': total_included,
                                    'qty': summary.quantity,
                                }
                            },
                            'total_base': total_excluded,
                            'total_cgst': cgst,
                            'total_sgst': sgst,
                            'total_igst': igst,
                            'total_cess': cess,
                            'total_amount': total_included,
                            'total_qty': summary.quantity,
                        }
                    total_sum += total_included
                    taxable_sum += total_excluded
                    cgst_sum += cgst
                    sgst_sum += sgst
                    igst_sum += igst
                    cess_sum += cess
                    total_qty += summary.quantity
                # final = []
                if summary.id in [55098, 55101, 55100]:
                    summary
            else:

                if summary.product_id and summary.exclude_from_invoice_tab == False:
                    # print(summary.tax_ids)
                    total_sum += summary.quantity * summary.price_unit
                    taxable_sum += summary.quantity * summary.price_unit
                    # print(summary.move_id.name,summary.quantity,'*',summary.price_unit,'=',summary.quantity*summary.price_unit)
                    if 0 in lines:
                        if grouper in lines[0]['data']:
                            lines[0]['data'][grouper]['base'] += summary.quantity * summary.price_unit
                            lines[0]['data'][grouper]['amount'] += summary.quantity * summary.price_unit
                            lines[0]['data'][grouper]['qty'] += summary.quantity
                        else:
                            lines[0]['data'][grouper] = {
                                'date': line_date,
                                'name': line_name,
                                'partner': line_partner,
                                'gst': line_gst,
                                'base': summary.quantity * summary.price_unit,
                                'cgst': 0,
                                'sgst': 0,
                                'igst': 0,
                                'cess': 0,
                                'amount': summary.quantity * summary.price_unit,
                                'qty': summary.quantity,
                            }
                        lines[0]['total_base'] += summary.price_unit
                        lines[0]['total_amount'] += summary.quantity * summary.price_unit
                        lines[0]['total_qty'] += summary.quantity
                    else:
                        # print(move.name, 'untaxed', move_total)
                        lines[0] = {
                            'name': 'Untaxed',
                            'data': {
                                grouper: {
                                    'date': line_date,
                                    'name': line_name,
                                    'partner': line_partner,
                                    'gst': line_gst,
                                    'base': summary.quantity * summary.price_unit,
                                    'cgst': 0,
                                    'sgst': 0,
                                    'igst': 0,
                                    'cess': 0,
                                    'amount': summary.quantity * summary.price_unit,
                                    'qty': summary.quantity
                                }
                            },
                            'total_base': summary.quantity * summary.price_unit,
                            'total_cgst': 0,
                            'total_sgst': 0,
                            'total_igst': 0,
                            'total_cess': 0,
                            'total_amount': summary.quantity * summary.price_unit,
                            'total_qty': summary.quantity
                        }
        # print(lines,'lineslines')
        return {
            'lines': lines,
            'type': type,
            'amount_total': total_sum,
            'taxable_total': taxable_sum,
            'cgst_total': cgst_sum,
            'sgst_total': sgst_sum,
            'igst_total': igst_sum,
            'cess_total': cess_sum,
            'total_qty': total_qty
        }

    def get_html(self):
        res = self._get_report_data()
        # res['lines']['report_type'] = 'html'
        # res['lines']['report_structure'] = 'all'
        self.template_area = self.env.ref('sales_tax_report.report_sales_tax')._render({
            'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             # 'report_order': res['lines']['report_type'],
             # 'branch_ids': res['lines']['branch_ids'],
             # 'branch_name': res['lines']['branch_name'],
             'order': self.report_type,
             })
        print('res', res)
        return res

    @api.model
    def _get_report_data(self):
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

        # if report_location:
        #     rl = [int(i) for i in report_location]

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))
        tax_list = []
        if self.tax_ids:
            for tax in self.tax_ids:
                tax_list.append(int(tax))
        data = {
            'date_from': str(self.date_from),
            'date_to': str(self.date_to),
            # 'branch_name': branch_name,
            'type_invoice': self.report_order if self.report_order else False,
            # 'branch_ids': rl if rl else (branch_default.id,),
            'tax_list': tax_list if tax_list else [],
            'tax_filter': self.tax_filter,
            'order': self.report_type
        }
        # print(order,'rep')
        dat = self.get_report_values(data=data)
        tk = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('name', 'not in', ['CESS', 'cess'])],
                                            order='name')
        do = {}
        for i in tk:
            do[i.id] = i.name
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
            'orders': self.report_type,
        }