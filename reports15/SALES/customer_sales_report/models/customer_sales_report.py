# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaCustomerSalesReport(models.TransientModel):  # change this
    _name = 'beta.customer.sales.report'  # change this
    _inherit = 'beta.reports'
    # _rec_name = "Customer Sales Report"

    date_from = fields.Date(default=datetime.today())
    date_to = fields.Date(default=datetime.today())
    transaction_type = fields.Selection([('sales', 'Sales'), ('sales_return', 'Sales Return')],
                                        default='sales')
    report_type = fields.Selection([('all', 'All'), ('selected_customer', 'Customer')],
                                   default='all')
    detailed = fields.Boolean(default=False)
    customer_ids = fields.Many2many('res.partner')

    @api.model
    def get_report_values(self, data=None):
        date_from = self.date_from.strftime('%d/%m/%Y')
        date_to = self.date_to.strftime('%d/%m/%Y')
        customer_obj = self.env['res.partner']
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        customers = ''

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
        if data['ctype'] == 'selected_customer':
            if data['customer_ids']:
                for customer in data['customer_ids']:
                    customers += customer_obj.browse(customer).name + ", "
                    print('customers', customers)

        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            't_type': data['t_type'],
            'detailed': data['detailed'],
            'ctype': data['ctype'],
            'customer_ids': customers,
            # 'branch_ids': branch,
            # 'isbranch': data['isbranch'],
            # 'branch_name': data['branch_name'],
            'lines': self.get_customer_wise_sales(data),
        }

    def get_customer_wise_sales(self, data):
        sales = {}
        amount_total, taxable_total, tax_sum = 0, 0, 0
        date_from = data['date_from']
        date_to = data['date_to']
        detailed = data['detailed']
        type = data['t_type']
        customer = data['ctype']
        customer_ids = data['customer_ids']
        # branch_ids = data['branch_ids']

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
        if type == 'sales':
            type1 = 'out_invoice'

        if type == 'sales_return':
            type1 = 'out_refund'

        if customer == 'all' and detailed == True:
            if 'branch_id' in self.env.user._fields:
                # if branch_ids:
                #     for branch in branch_ids:
                #         brh = str(branch)
                        self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                                                from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                                     am.move_type = '""" + str(
                            type1) + """' and am.branch_id='""" +
                                            # brh
                                            + """' and am.state='posted' and 
                                                                                     am.date<='""" + date_to + """' and 
                                                                                  am.date>='""" + date_from + """' order by rp.name,am.date,am.name """)
                        for dt in self.env.cr.dictfetchall():
                            docs.append({
                                'id': dt['id'],
                                'date': dt['date'].strftime("%d/%m/%Y"),
                                'invoice_no': dt['invoice'],
                                'customer': dt['name'],
                                'total': dt['total'],
                            })
            else:
                self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                    from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                    am.move_type = '""" + str(type1) + """'  and am.state='posted' 
                    and am.date<='""" + date_to + """' and am.date>='""" + date_from + """' order by rp.name """)
                for dt in self.env.cr.dictfetchall():
                    docs.append({
                        'id': dt['id'],
                        'date': dt['date'].strftime("%d/%m/%Y"),
                        'invoice_no': dt['invoice'],
                        'customer': dt['name'],
                        'total': dt['total'],
                    })

            if len(docs) > 0:
                cid = docs[0]['id']
                grand_total = 0
                customer_total = 0
                i = 0
                product_final_lis.append({'name': 6,
                                          'customer': docs[0]['customer'],
                                          'date': None,
                                          'invoice_no': None,
                                          'total': None,
                                          })

                while i < len(docs):
                    if cid == docs[i]['id']:
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  })
                        grand_total += docs[i]['total']
                        customer_total += docs[i]['total']
                    else:
                        product_final_lis.append({'name': 10,
                                                  'customer': 'Customer Total',
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': customer_total,
                                                  })
                        cid = docs[i]['id']
                        customer_total = 0
                        product_final_lis.append({'name': 6,
                                                  'customer': docs[i]['customer'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': None,
                                                  })
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  })
                        grand_total += docs[i]['total']
                        customer_total += docs[i]['total']
                    i = i + 1
                product_final_lis.append({'name': 10,
                                          'customer': 'Customer Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': customer_total,
                                          })
                product_final_lis.append({'name': 10,
                                          'customer': 'Grand Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': grand_total,
                                          })

            return {
                'docsnn': product_final_lis,
            }

        if customer == 'all' and detailed == False:
            grand_total = 0
            if 'branch_id' in self.env.user._fields:
                # if branch_ids:
                #     for branch in branch_ids:
                #         brh = str(branch)
                        self.env.cr.execute(
                            """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                am.branch_id='""" +
                            # brh
                            + """' and  am.move_type = '""" + str(type1) + """' 
                                                                            and am.state='posted' and am.date<='""" + date_to + """' 
                                                                            and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
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

            else:
                self.env.cr.execute(
                    """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                        am.move_type = '""" + str(type1) + """' 
                                                                                                and am.state='posted' and am.date<='""" + date_to + """' 
                                                                                                and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
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
        if customer == 'selected_customer' and detailed == False:
            grand_total = 0
            if 'branch_id' in self.env.user._fields:
                # if branch_ids:
                #     for branch in branch_ids:
                #         brh = str(branch)
                        self.env.cr.execute(
                            """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                am.branch_id='""" +
                            # brh
                            + """'and am.partner_id in """ + str(
                                tuple(customer_ids)).replace(",)", ")") + """ and  am.move_type = '""" + str(type1) + """' 
                                                                            and am.state='posted' and am.date<='""" + date_to + """' 
                                                                            and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
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

            else:
                self.env.cr.execute(
                    """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                        am.move_type = '""" + str(type1) + """' and am.partner_id in """ + str(
                        tuple(customer_ids)).replace(",)", ")") + """
                                                                                                and am.state='posted' and am.date<='""" + date_to + """' 
                                                                                                and am.date>='""" + date_from + """' group by rp.name order by rp.name""")
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
        if customer == 'selected_customer' and detailed == True:
            if 'branch_id' in self.env.user._fields:
                # if branch_ids:
                #     for branch in branch_ids:
                #         brh = str(branch)
                        for customers in customer_ids:
                            self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                                from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                am.move_type = '""" + str(type1) + """'and am.partner_id = '""" + str(
                                customers) + """' and am.branch_id='""" +
                                                # brh
                                                + """' and 
                                am.state='posted' and am.date<='""" + date_to + """' and 
                                am.date>='""" + date_from + """' order by rp.name """)
                            for dt in self.env.cr.dictfetchall():
                                docs.append({
                                    'id': dt['id'],
                                    'date': dt['date'].strftime("%d/%m/%Y"),
                                    'invoice_no': dt['invoice'],
                                    'customer': dt['name'],
                                    'total': dt['total'],
                                })
            else:
                for customers in customer_ids:
                    self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total 
                                                        from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                                        am.move_type = '""" + str(type1) + """'and am.partner_id = '""" + str(
                        customers) + """'  and am.state='posted' and am.date<='""" + date_to + """' and 
                                                        am.date>='""" + date_from + """' order by rp.name """)
                    for dt in self.env.cr.dictfetchall():
                        docs.append({
                            'id': dt['id'],
                            'date': dt['date'].strftime("%d/%m/%Y"),
                            'invoice_no': dt['invoice'],
                            'customer': dt['name'],
                            'total': dt['total'],
                        })

            if len(docs) > 0:
                cid = docs[0]['id']
                grand_total = 0
                customer_total = 0
                i = 0
                product_final_lis.append({'name': 6,
                                          'customer': docs[0]['customer'],
                                          'date': None,
                                          'invoice_no': None,
                                          'total': None,
                                          })

                while i < len(docs):
                    if cid == docs[i]['id']:
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  })
                        grand_total += docs[i]['total']
                        customer_total += docs[i]['total']
                    else:
                        product_final_lis.append({'name': 10,
                                                  'customer': 'Customer Total',
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': customer_total,
                                                  })
                        cid = docs[i]['id']
                        customer_total = 0
                        product_final_lis.append({'name': 6,
                                                  'customer': docs[i]['customer'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': None,
                                                  })
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  })
                        grand_total += docs[i]['total']
                        customer_total += docs[i]['total']
                    i = i + 1
                product_final_lis.append({'name': 10,
                                          'customer': 'Customer Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': customer_total,
                                          })
                product_final_lis.append({'name': 10,
                                          'customer': 'Grand Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': grand_total,
                                          })

            return {
                'docsnn': product_final_lis,
            }

    def get_html(self):
        res = self._get_report_data()
        case = 0
        if res['lines']['date_from'] and res['lines']['date_to']:
            if res['lines']['detailed']:
                case = 1
            else:
                case = 2
            if res['lines']['t_type'] == 'both':
                case = 3
            if res['lines']['ctype'] == 'selected_customer' and res['lines']['detailed']:
                if res['lines']['customer_ids']:
                    case = 1

        # res['lines']['report_type'] = 'html'
        # res['lines']['report_structure'] = 'all'
        self.template_area = self.env.ref('customer_sales_report.report_customer')._render(
            {'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'case': case,
             'detailed': res['lines']['detailed'],
             'ctype': res['lines']['ctype'],
             't_type': res['lines']['t_type'],
             'customer_ids': res['lines']['customer_ids'],
             # 'branch_ids': res['lines']['branch_ids'],
             # 'isbranch': res['lines']['isbranch'],
             # 'branch_name': res['lines']['branch_name'],
             })
        print('res', res)
        return res

    @api.model
    def _get_report_data(self):
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
            branch_default = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])

            is_branch = False
        rp = ''
        rl = ''
        if self.customer_ids:
            rp = [int(i) for i in self.customer_ids]

        # if report_location:
        #     rl = [int(i) for i in report_location]

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))

        data = {
            'date_from': str(self.date_from),
            'date_to': str(self.date_to),
            't_type': self.transaction_type if self.transaction_type else False,
            'ctype': self.report_type if self.report_type else False,
            'customer_ids': rp if rp else False,
            'detailed': self.detailed if self.detailed else False,
            # 'branch_name': branch_name,
            # 'branch_ids': rl if rl else (branch_default.id,),
            # 'isbranch': is_branch,

        }
        print('data', data)
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
            'bid': branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }
