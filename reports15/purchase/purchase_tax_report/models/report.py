# -*- coding: utf-8 -*-
from odoo import models, api,fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning
from pytz import timezone
from odoo.exceptions import UserError


class ReportProduct(models.TransientModel):
    _name = 'purchase.tax'  # change this
    _inherit = 'beta.reports'
    _description = 'Purchase Tax Report'

    name = fields.Char(default='Report')  # change this
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    tax_filter=fields.Boolean(string="Tax Filter")
    type_purchase = fields.Selection([
        ('both', 'Both'),
        ('purchase', 'Purchase'),
        ('purchase_return', 'Purchase Return')],String="Report Order",default="both")
    order = fields.Selection([
        ('bill_wise', 'Bill Wise'),
        ('date_wise', 'Day wise'),
        ('month_wise', 'Month Wise')],widget="radio",default="bill_wise")
    report_tax=fields.Many2many('account.tax',domain=[('type_tax_use', '=', 'purchase')],string="Taxes")

    @api.model
    def default_get(self, fields_list):
        res = super(ReportProduct, self).default_get(fields_list)
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
            'branch_ids': branch,
            'branch_name': data['branch_name'],
            'lines': self.get_purchase_tax(data),
        }

    def get_purchase_tax(self, data):
        date_start = data['date_from']
        date_end = data['date_to']
        branch = data['branch_ids']
        type = 'purchase'
        sales = {}
        returns = {}
        if type == 'purchase':
            if data['type_purchase'] == 'both':
                sales = self.get_report_data(date_start, date_end, type, branch, 'purchase',data)
                returns = self.get_report_data(date_start, date_end, type, branch, 'purchase_return',data)
            elif data['type_purchase'] == 'purchase':
                sales = self.get_report_data(date_start, date_end, type, branch, 'purchase',data)
            elif data['type_purchase'] == 'purchase_return':
                returns = self.get_report_data(date_start, date_end, type, branch, 'purchase_return',data)


        return {
            # 'doc_ids': data['ids'],
            # 'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'sales': sales,
            'returns': returns,
            'type': type,
        }

    def get_report_data(self, date_start, date_end, type,branch, subtype,data):
        branch = branch
        total_sum = 0
        taxable_sum = 0
        cgst_sum = 0
        sgst_sum = 0
        igst_sum = 0
        cess_sum = 0
        lines = {}

        move_line_obj = self.env['account.move.line']
        if 'branch_id' in self.env.user._fields:
            domain = [('move_id.state', '=', 'posted'), ('move_id.invoice_date', '>=', date_start),
                      ('move_id.invoice_date', '<=', date_end),('branch_id','in', branch)]
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
                if 'expiry_type' in self.env['account.move']._fields:
                    domain.append(('move_id.expiry_type','!=','expiry_rpl'))
            elif subtype == 'purchase_return':
                domain.append(('move_id.move_type', 'in', ['in_refund']))
                if 'expiry_type' in self.env['account.move']._fields:
                    domain.append(('move_id.expiry_type', '!=', 'expiry_rtn'))

        move_line = move_line_obj.search(domain, order="move_id desc")
        for summary in move_line:
            price_unit = summary.price_unit
            if summary.discount != 0:
                price_unit = summary.price_unit - (summary.price_unit * summary.discount / 100)
            taxdata = {}
            if data['order'] == 'date_wise':
                grouper = summary.move_id.invoice_date
                line_date = summary.move_id.invoice_date.strftime('%d/%m/%Y')
                line_name = ''
                line_partner = ''
            elif data['order'] == 'month_wise':
                grouper = summary.move_id.invoice_date.strftime('%m/%Y')
                line_date = summary.move_id.invoice_date.strftime('%B -%Y')
                line_name = ''
                line_partner = ''
            else:
                grouper = summary.move_id.id
                line_date = summary.move_id.invoice_date.strftime('%d/%m/%Y')
                line_name = summary.move_id.name
                line_partner = summary.move_id.partner_id.name
            if summary.tax_ids:
                print(summary.tax_ids )
                print( data['tax_filter'])
                for tax in summary.tax_ids:
                    print("56474", data['tax_list'])
                    if tax.id not in data['tax_list'] and data['tax_filter'] == True:
                        continue
                    taxes = tax.compute_all(price_unit, quantity=summary.quantity)
                    cgst = 0
                    sgst = 0
                    igst = 0
                    cess = 0
                    if taxes['taxes']:
                        for comtax in taxes['taxes']:
                            if 'cgst' in comtax['name'].lower():
                                cgst += comtax['amount']
                            elif 'sgst' in comtax['name'].lower():
                                sgst += comtax['amount']
                            elif 'igst' in comtax['name'].lower():
                                igst += comtax['amount']
                            elif 'cess' in comtax['name'].lower():
                                cess += comtax['amount']
                        if tax.id in taxdata:
                            taxdata[tax.id]['total_excluded'] += taxes['total_excluded']
                            taxdata[tax.id]['total_included'] += taxes['total_included']
                            taxdata[tax.id]['cgst'] += cgst
                            taxdata[tax.id]['sgst'] += sgst
                            taxdata[tax.id]['igst'] += igst
                            taxdata[tax.id]['cess'] += cess
                        else:
                            taxdata[tax.id] = {
                                'total_excluded': taxes['total_excluded'],
                                'total_included': taxes['total_included'],
                                'cgst': cgst,
                                'sgst': sgst,
                                'igst': igst,
                                'cess': cess,
                            }
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
                        else:
                            lines[final[0]['tax_id']]['data'][grouper] = {
                                'date': line_date,
                                'name': line_name,
                                'partner': line_partner,
                                'base': total_excluded,
                                'cgst': cgst,
                                'sgst': sgst,
                                'igst': igst,
                                'cess': cess,
                                'amount': total_included,
                            }
                        lines[final[0]['tax_id']]['total_base'] += total_excluded
                        lines[final[0]['tax_id']]['total_cgst'] += cgst
                        lines[final[0]['tax_id']]['total_sgst'] += sgst
                        lines[final[0]['tax_id']]['total_igst'] += igst
                        lines[final[0]['tax_id']]['total_cess'] += cess
                        lines[final[0]['tax_id']]['total_amount'] += total_included
                    else:
                        lines[final[0]['tax_id']] = {
                            'name': self.env['account.tax'].search([('id', '=', final[0]['tax_id'])], limit=1).name,
                            'data': {
                                grouper: {
                                    'date': line_date,
                                    'name': line_name,
                                    'partner': line_partner,
                                    'base': total_excluded,
                                    'cgst': cgst,
                                    'sgst': sgst,
                                    'igst': igst,
                                    'cess': cess,
                                    'amount': total_included,
                                }
                            },
                            'total_base': total_excluded,
                            'total_cgst': cgst,
                            'total_sgst': sgst,
                            'total_igst': igst,
                            'total_cess': cess,
                            'total_amount': total_included,
                        }
                    total_sum += total_included
                    taxable_sum += total_excluded
                    cgst_sum += cgst
                    sgst_sum += sgst
                    igst_sum += igst
                    cess_sum += cess
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
                        else:
                            lines[0]['data'][grouper] = {
                                'date': line_date,
                                'name': line_name,
                                'partner': line_partner,
                                'base': summary.quantity * summary.price_unit,
                                'cgst': 0,
                                'sgst': 0,
                                'igst': 0,
                                'cess': 0,
                                'amount': summary.quantity * summary.price_unit,
                            }
                        lines[0]['total_base'] += summary.price_unit
                        lines[0]['total_amount'] += summary.quantity * summary.price_unit
                    else:
                        # print(move.name, 'untaxed', move_total)
                        lines[0] = {
                            'name': 'Untaxed',
                            'data': {
                                grouper: {
                                    'date': line_date,
                                    'name': line_name,
                                    'partner': line_partner,
                                    'base': summary.quantity * summary.price_unit,
                                    'cgst': 0,
                                    'sgst': 0,
                                    'igst': 0,
                                    'cess': 0,
                                    'amount': summary.quantity * summary.price_unit,
                                }
                            },
                            'total_base': summary.quantity * summary.price_unit,
                            'total_cgst': 0,
                            'total_sgst': 0,
                            'total_igst': 0,
                            'total_cess': 0,
                            'total_amount': summary.quantity * summary.price_unit,
                        }

        return {
            'lines': lines,
            'type': type,
            'amount_total': total_sum,
            'taxable_total': taxable_sum,
            'cgst_total': cgst_sum,
            'sgst_total': sgst_sum,
            'igst_total': igst_sum,
            'cess_total': cess_sum,
        }


    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'),type_purchase=self.type_purchase,tax_filter=self.tax_filter,order=self.order,report_tax=self.report_tax)
        print("3456",self.report_tax)

        self.template_area = self.env.ref('purchase_tax_report.report_purchase_tax')._render({
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'type_purchase' : self.type_purchase ,
            'order':self.order,
            'tax_filter':self.tax_filter,
            'report_tax':self.report_tax,
            'data': res['lines'],
            'lines':res['lines']['lines']
        })

    def _get_report_data(self, date_from=False, date_to=False,type_purchase=False,tax_filter=False,order=False,report_tax=False):
        is_branch = False
        branch_name = ''
        if 'branch_id' in self.env.user._fields:
            branch_list = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            branch_default = self.env['res.branch'].search(
                [('id', '=', self.env.user.branch_id.id)])
            is_branch = True
        else:
            branch_default = self.env['res.company'].search([('id','=',self.env.user.company_id.id)])

            is_branch = False
        rl = ''
        tax_list = []
        if report_tax:
            for tax in report_tax:
                tax_list.append(int(tax))
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'type_purchase': type_purchase if type_purchase else False,
            'branch_name': branch_name,
            'branch_ids': rl if rl else (branch_default.id,),
            'tax_list': tax_list if tax_list else [],
            'tax_filter': tax_filter,
            'order': order
        }
        print('222',tax_list)
        dat = self.get_report_values(data=data)
        tk = self.env['account.tax'].search([('type_tax_use', '=', 'purchase')], order='name')
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
            'bid':branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }
