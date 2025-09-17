# -*- coding: utf-8 -*-
from odoo import models, api,fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning
from pytz import timezone


class ReportSupplierProduct(models.TransientModel):
    _name = 'supplier.report'
    _inherit = 'beta.reports'
    _description = 'Supplier Wise Purchase'

    name = fields.Char(default='Report')  # change this
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    detailed = fields.Boolean(string="Detailed")
    t_type = fields.Selection([
        ('purchase', 'Purchase'),
        ('purchase_return', 'Purchase Return')], String="Transaction Type", default="purchase")
    ctype = fields.Selection([
        ('all', 'All'),
        ('selected_supplier', 'Supplier')], String="Report Type", default="all")
    report_supplier = fields.Many2many('res.partner')

    @api.model
    def default_get(self, fields_list):
        res = super(ReportSupplierProduct, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    @api.onchange('ctype')
    def onchange_supplier(self):
        if self.ctype == 'all':
            self.write({
                'report_supplier': False
            })

    def get_report_values(self, data=None):
        date_from = date_to = False
        supplier_obj = self.env['res.partner']
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        suppliers = ''

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

        if data['ctype'] == 'selected_supplier':
            if data['supplier_ids']:
                for supplier in data['supplier_ids']:
                    suppliers += supplier_obj.browse(supplier).name + ", "

        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            't_type': data['t_type'],
            'detailed': data['detailed'],
            'ctype': data['ctype'],
            'supplier_ids': suppliers,
            'branch_ids': branch,
            'isbranch': data['isbranch'],
            'branch_name': data['branch_name'],
            'lines': self.get_supplier_wise_purchase(data),
        }

    def get_supplier_wise_purchase(self, data):
            purchase = {}
            amount_total, taxable_total, tax_sum = 0, 0, 0
            date_from = data['date_from']
            date_to = data['date_to']
            detailed = data['detailed']
            type = data['t_type']
            supplier = data['ctype']
            supplier_ids = data['supplier_ids']
            branch_ids = data['branch_ids']

            docs = []
            i = 0
            name = ''
            uid = ''
            client = ''
            product_final_lis = []
            product_final = []
            type1 = []
            client_ids = ''
            self.env.cr.execute("""select id as id from res_partner order by name""")
            if type == 'purchase':
                type1 = 'in_invoice'

            if type == 'purchase_return':
                type1 = 'in_refund'

            exp_filter = ''
            if 'expiry_type' in self.env['account.move']._fields:
                if type1 in ['in_invoice', 'in_refund']:
                    exp_filter = " and expiry_type is null"

            if supplier == 'all' and detailed == True:
                if 'branch_id' in self.env.user._fields:
                    if branch_ids:
                        for branch in branch_ids:
                            brh = str(branch)
                            self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                                                from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                                     am.move_type = '""" + str(type1) + """' and am.branch_id='""" + brh + """' and 
                                                                     am.state='posted' """ + exp_filter +""" and 
                                                                                     am.date<='""" + date_to + """' and 
                                                                                  am.date>='""" + date_from + """' order by rp.name """ )
                            for dt in self.env.cr.dictfetchall():
                                docs.append({
                                    'id': dt['id'],
                                    'date': dt['date'].strftime("%d/%m/%Y"),
                                    'invoice_no': dt['invoice'],
                                    'supplier': dt['name'],
                                    'total': dt['total'],
                                })
                else:
                    filt2 = ''
                    self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                    from account_move as am left join res_partner as rp ON rp.id = am.partner_id where
                    am.move_type = '""" + str(type1) + """'  and am.state='posted'""" +  str(filt2) +  exp_filter +"""
                    and am.date<='""" + date_to + """' and am.date>='""" + date_from + """' order by rp.name """)

                    for dt in self.env.cr.dictfetchall():
                        docs.append({
                            'id': dt['id'],
                            'date': dt['date'].strftime("%d/%m/%Y"),
                            'invoice_no': dt['invoice'],
                            'supplier': dt['name'],
                            'total': dt['total'],
                        })

                if len(docs) > 0:
                    cid = docs[0]['id']
                    grand_total = 0
                    supplier_total = 0
                    i = 0
                    product_final_lis.append({'name': 6,
                                              'supplier': docs[0]['supplier'],
                                              'date': None,
                                              'invoice_no': None,
                                              'total': None,
                                              })

                    while i < len(docs):
                        if cid == docs[i]['id']:
                            product_final_lis.append({'name': 1,
                                                      'supplier': None,
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'total': docs[i]['total'],
                                                      })
                            grand_total += docs[i]['total']
                            supplier_total += docs[i]['total']
                        else:
                            product_final_lis.append({'name': 10,
                                                      'supplier': 'Supplier Total',
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'total': supplier_total,
                                                      })
                            cid = docs[i]['id']
                            supplier_total = 0
                            product_final_lis.append({'name': 6,
                                                      'supplier': docs[i]['supplier'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'total': None,
                                                      })
                            product_final_lis.append({'name': 1,
                                                      'supplier': None,
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'total': docs[i]['total'],
                                                      })
                            grand_total += docs[i]['total']
                            supplier_total += docs[i]['total']
                        i = i + 1
                    product_final_lis.append({'name': 10,
                                              'supplier': 'Supplier Total',
                                              'date': None,
                                              'invoice_no': None,
                                              'total': supplier_total,
                                              })
                    product_final_lis.append({'name': 10,
                                              'supplier': 'Grand Total',
                                              'date': None,
                                              'invoice_no': None,
                                              'total': grand_total,
                                              })

                return {
                    'docsnn': product_final_lis,
                }

            if supplier == 'all' and detailed == False:
                grand_total = 0
                if 'branch_id' in self.env.user._fields:
                    if branch_ids:
                        for branch in branch_ids:
                            brh = str(branch)
                            self.env.cr.execute(
                                """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                    am.branch_id='""" + brh + """' and  am.move_type = '""" + str(type1) + """' 
                                                                            and am.state='posted' """ + exp_filter +""" and am.date<='""" + date_to + """' 
                                                                            and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
                            for dt in self.env.cr.dictfetchall():

                                product_final_lis.append({
                                    'name':1,
                                    'partner_name': dt['name'],
                                    'invoice_count': dt['count'],
                                    'total': dt['total']
                                })
                                grand_total += dt['total']
                        product_final_lis.append({
                            'name': 10,
                            'partner_name': None,
                            'invoice_count': None,
                            'total': grand_total,
                        })

                else:
                    filt2 = ''
                    self.env.cr.execute(
                        """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as 
                        am left join res_partner as rp ON rp.id = am.partner_id where  am.move_type = '""" + str(type1)  + """' and am.state='posted' """ + str(filt2)
                        +""" and am.date<='""" + date_to + """' and am.date>='""" + date_from + """' """ + exp_filter + """ group by rp.name order by rp.name""")

                    for dt in self.env.cr.dictfetchall():
                        product_final_lis.append({
                            'name': 1,
                            'partner_name': dt['name'],
                            'invoice_count': dt['count'],
                            'total': dt['total']

                        })
                        grand_total += dt['total']
                    product_final_lis.append({
                        'name': 10,
                        'partner_name': None,
                        'invoice_count': None,
                        'total': grand_total,
                    })

                return {
                    'docsnn': product_final_lis,
                }
            if supplier == 'selected_supplier' and detailed == False:
                grand_total = 0
                if 'branch_id' in self.env.user._fields:
                    if branch_ids:
                        for branch in branch_ids:
                            brh = str(branch)
                            self.env.cr.execute(
                                """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                 am.branch_id='""" + brh + """'and am.partner_id in """ + str(tuple(supplier_ids)).replace(",)" ,")") +""" and  am.move_type = '""" + str(type1) + """' 
                                 and am.state='posted' """ + exp_filter +""" and am.date<='""" + date_to + """' and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
                            for dt in self.env.cr.dictfetchall():

                                product_final_lis.append({
                                    'name':1,
                                    'partner_name': dt['name'],
                                    'invoice_count': dt['count'],
                                    'total': dt['total']
                                })
                                grand_total += dt['total']
                        product_final_lis.append({
                            'name': 10,
                            'partner_name': None,
                            'invoice_count': None,
                            'total': grand_total,
                        })

                else:
                    filt2 = ''
                    self.env.cr.execute(
                        """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                         am.move_type = '""" + str(type1) + """' and am.partner_id in """ + str(tuple(supplier_ids)).replace(",)" ,")") +""" and am.state='posted' """
                        + str(filt2) +  exp_filter +""" and am.date<='""" + date_to + """' and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
                    for dt in self.env.cr.dictfetchall():
                        product_final_lis.append({
                            'name': 1,
                            'partner_name': dt['name'],
                            'invoice_count': dt['count'],
                            'total': dt['total']

                        })
                        grand_total += dt['total']
                    product_final_lis.append({
                        'name': 10,
                        'partner_name': None,
                        'invoice_count': None,
                        'total': grand_total,
                    })

                return {
                    'docsnn': product_final_lis,
                }
            if supplier == 'selected_supplier' and detailed == True:
                if 'branch_id' in self.env.user._fields:
                    if branch_ids:
                        for branch in branch_ids:
                            brh = str(branch)
                            for supplier in supplier_ids:


                                self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, 
                                am.amount_total as total from account_move as am 
                                left join res_partner as rp ON rp.id = am.partner_id where 
                                am.move_type = '""" + str(type1) + """'and 
                                am.partner_id = '""" + str(supplier) +"""' and am.branch_id='""" + brh + """' and 
                                am.state='posted' """ + exp_filter +""" and am.date<='""" + date_to + """' and 
                                am.date>='""" + date_from + """' order by rp.name """)
                                for dt in self.env.cr.dictfetchall():
                                    docs.append({
                                        'id': dt['id'],
                                        'date': dt['date'].strftime("%d/%m/%Y"),
                                        'invoice_no': dt['invoice'],
                                        'supplier': dt['name'],
                                        'total': dt['total'],
                                    })
                else:
                    for supplier in supplier_ids:
                        filt2 = ''
                    #print("111", supplier)
                        self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                                                    from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                    am.move_type = '""" + str(type1) + """'and am.partner_id = '""" + str(supplier) + """'  and 
                                                    am.state='posted'""" + str(filt2) +  exp_filter +""" and am.date<='""" + date_to + """' and 
                                                    am.date>='""" + date_from + """' order by rp.name """)
                    for dt in self.env.cr.dictfetchall():
                        docs.append({
                            'id': dt['id'],
                            'date': dt['date'].strftime("%d/%m/%Y"),
                            'invoice_no': dt['invoice'],
                            'supplier': dt['name'],
                            'total': dt['total'],
                        })

                if len(docs) > 0:
                    cid = docs[0]['id']
                    grand_total = 0
                    supplier_total = 0
                    i = 0
                    product_final_lis.append({'name': 6,
                                              'supplier': docs[0]['supplier'],
                                              'date': None,
                                              'invoice_no': None,
                                              'total': None,
                                              })

                    while i < len(docs):
                        if cid == docs[i]['id']:
                            product_final_lis.append({'name': 1,
                                                      'supplier': None,
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'total': docs[i]['total'],
                                                      })
                            grand_total += docs[i]['total']
                            supplier_total += docs[i]['total']
                        else:
                            product_final_lis.append({'name': 10,
                                                      'supplier': 'Supplier Total',
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'total': supplier_total,
                                                      })
                            cid = docs[i]['id']
                            supplier_total = 0
                            product_final_lis.append({'name': 6,
                                                      'supplier': docs[i]['supplier'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'total': None,
                                                      })
                            product_final_lis.append({'name': 1,
                                                      'supplier': None,
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'total': docs[i]['total'],
                                                      })
                            grand_total += docs[i]['total']
                            supplier_total += docs[i]['total']
                        i = i + 1
                    product_final_lis.append({'name': 10,
                                              'supplier': 'Supplier Total',
                                              'date': None,
                                              'invoice_no': None,
                                              'total': supplier_total,
                                              })
                    product_final_lis.append({'name': 10,
                                              'supplier': 'Grand Total',
                                              'date': None,
                                              'invoice_no': None,
                                              'total': grand_total,
                                              })
                return {
                    'docsnn': product_final_lis,
                }


    def get_html(self):
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'), date_to=self.date_to.strftime('%Y-%m-%d'),
                                 detailed=self.detailed, ctype=self.ctype, t_type=self.t_type,report_supplier=self.report_supplier)
        case = 0
        if res['lines']['date_from'] and res['lines']['date_to']:
            if res['lines']['detailed']:
                case = 1
            else:
                case = 2
            if res['lines']['t_type'] == 'both':
               case = 3
            if res['lines']['ctype'] == 'selected_supplier' and res['lines']['detailed']:
                if res['lines']['supplier_ids']:
                    case = 1

        self.template_area = self.env.ref('supplier_wise_purchase_report.report_supplier')._render(
            {'date_from': self.date_from.strftime('%d-%m-%Y'),
                'date_to': self.date_to.strftime('%d-%m-%Y'),
                'ctype': self.ctype,
                't_type': self.t_type,
             'case': case,
              'detailed': self.detailed,
             'data': res['lines'],
              'lines': res['lines']['lines'],
             'supplier_ids': res['lines']['supplier_ids'],
             })
        return res


    def _get_report_data(self ,date_from=False, date_to=False, detailed=False, ctype=False, t_type=False,report_supplier=False):
        cus = self.env['res.partner'].search([], order='name')
        # loc = self.env['stock.location'].search([('usage', '=', 'internal')])
        branch_name = ''
        is_branch = False
        if 'branch_id' in self.env.user._fields:
            branch_list = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            branch_default = self.env['res.branch'].search(
                [('id', '=', self.env.user.branch_id.id)])
            is_branch = True
        else:
            branch_default = self.env['res.company'].search([('id','=',self.env.user.company_id.id)])

            is_branch = False
        rp = ''
        rl = ''
        if report_supplier:
            rp = [int(i) for i in report_supplier]

        # if report_location:
        #     rl = [int(i) for i in report_location]

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))

        data = {
            'date_from': date_from,
            'date_to': date_to,
            't_type': t_type if t_type else False,
            'ctype': ctype if ctype else False,
            'supplier_ids': rp if rp else False,
            'detailed': detailed if detailed else False,
            'branch_name': branch_name,
            'branch_ids': rl if rl else (branch_default.id,),
            'isbranch': is_branch,

        }
        dat = self.get_report_values(data=data)

        do = {}
        lo = {}
        for i in cus:
            do[i.id] = i.name
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
