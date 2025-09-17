# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaIncentiveInvoiceReport(models.TransientModel):  # change this
    _name = 'beta.incentive.invoice.report'  # change this
    _inherit = 'beta.reports'
    _description = "Incentive Invoice Report"

    date_from = fields.Date()
    date_to = fields.Date()
    report_type = fields.Selection([('all', 'All'), ('selected', 'Selected')],
                                   default='all')
    detailed = fields.Boolean(default=False)
    partner_ids = fields.Many2many('res.partner')
    outstanding = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaIncentiveInvoiceReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = today
        res['date_to'] = today
        return res

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
        if data['ctype'] == 'selected':
            if self.partner_ids:
                for customer in self.partner_ids:
                    customers += customer.name + ", "
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
        date_from = data['date_from']
        date_to = data['date_to']
        detailed = data['detailed']
        customer = data['ctype']
        customer_ids = self.partner_ids.ids
        docs = []
        product_final_lis = []
        type1 = 'in_invoice'
        if self.outstanding:
            domain = " and am.amount_residual > 0"
        else:
            domain = " and am.date <= '%s' and am.date >= '%s' " % (date_to, date_from)
        if customer == 'all' and detailed == True:
            self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total ,
            am.amount_untaxed,
SUM(CASE WHEN tax.name LIKE '%CGST%' THEN aml.price_subtotal ELSE 0 END) AS cgst,
SUM(CASE WHEN tax.name LIKE '%SGST%' THEN aml.price_subtotal ELSE 0 END) AS sgst,
SUM(CASE WHEN tax.name LIKE '%IGST%' THEN aml.price_subtotal ELSE 0 END) AS igst,
am.amount_residual as due
                from account_move as am left join res_partner as rp ON rp.id = am.partner_id 
                LEFT JOIN 
account_move_line AS aml ON aml.move_id = am.id
LEFT JOIN 
account_tax AS tax ON tax.id = aml.tax_line_id
                where aml.tax_line_id IS NOT NULL and
                am.move_type = '""" + str(type1) + """'  and am.state='posted' and  am.project_invoice_type = 'employee_invoice'
                """ + domain + """ GROUP BY 
am.id, rp.id order by rp.name """)
            for dt in self.env.cr.dictfetchall():
                docs.append({
                    'id': dt['id'],
                    'date': dt['date'].strftime("%d/%m/%Y"),
                    'invoice_no': dt['invoice'],
                    'customer': dt['name'],
                    'cgst': dt['cgst'],
                    'sgst': dt['sgst'],
                    'igst': dt['igst'],
                    'amount_untaxed': dt['amount_untaxed'],
                    'total': dt['total'],
                    'due': dt['due'],
                })

            if len(docs) > 0:
                cid = docs[0]['id']
                grand_total = 0
                cgst_grand_total = 0
                sgst_grand_total = 0
                igst_grand_total = 0
                amount_untaxed_grand_total = 0
                due_grand_total = 0
                customer_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                amount_untaxed_total = 0
                due_total = 0
                i = 0
                product_final_lis.append({'name': 6,
                                          'customer': docs[0]['customer'],
                                          'date': None,
                                          'invoice_no': None,
                                          'total': None,
                                          'cgst': None,
                                          'sgst': None,
                                          'igst': None,
                                          'amount_untaxed': None,
                                          'due': None,
                                          })

                while i < len(docs):
                    if cid == docs[i]['id']:
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  'cgst': docs[i]['cgst'],
                                                  'sgst': docs[i]['sgst'],
                                                  'igst': docs[i]['igst'],
                                                  'amount_untaxed': docs[i]['amount_untaxed'],
                                                  'due': docs[i]['due'],
                                                  })
                        grand_total += docs[i]['total']
                        cgst_grand_total += docs[i]['cgst']
                        sgst_grand_total += docs[i]['sgst']
                        igst_grand_total += docs[i]['igst']
                        amount_untaxed_grand_total += docs[i]['amount_untaxed']
                        due_grand_total += docs[i]['due']
                        customer_total += docs[i]['total']
                        cgst_total += docs[i]['cgst']
                        sgst_total += docs[i]['sgst']
                        igst_total += docs[i]['igst']
                        amount_untaxed_total += docs[i]['amount_untaxed']
                        due_total += docs[i]['due']
                    else:
                        product_final_lis.append({'name': 10,
                                                  'customer': 'Total',
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': customer_total,
                                                  'cgst': cgst_total,
                                                  'sgst': sgst_total,
                                                  'igst': igst_total,
                                                  'amount_untaxed': amount_untaxed_total,
                                                  'due': due_total,
                                                  })
                        cid = docs[i]['id']
                        customer_total = 0
                        cgst_total = 0
                        sgst_total = 0
                        igst_total = 0
                        amount_untaxed_total = 0
                        due_total = 0
                        product_final_lis.append({'name': 6,
                                                  'customer': docs[i]['customer'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': None,
                                                  'cgst': None,
                                                  'sgst': None,
                                                  'igst': None,
                                                  'amount_untaxed': None,
                                                  'due': None,
                                                  })
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  'cgst': docs[i]['cgst'],
                                                  'sgst': docs[i]['sgst'],
                                                  'igst': docs[i]['igst'],
                                                  'amount_untaxed': docs[i]['amount_untaxed'],
                                                  'due': docs[i]['due'],
                                                  })
                        grand_total += docs[i]['total']
                        cgst_grand_total += docs[i]['cgst']
                        sgst_grand_total += docs[i]['sgst']
                        igst_grand_total += docs[i]['igst']
                        amount_untaxed_grand_total += docs[i]['amount_untaxed']
                        due_grand_total += docs[i]['due']
                        customer_total += docs[i]['total']
                        cgst_total += docs[i]['cgst']
                        sgst_total += docs[i]['sgst']
                        igst_total += docs[i]['igst']
                        amount_untaxed_total += docs[i]['amount_untaxed']
                        due_total += docs[i]['due']
                    i = i + 1
                product_final_lis.append({'name': 10,
                                          'customer': 'Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': customer_total,
                                          'cgst': cgst_total,
                                          'sgst': sgst_total,
                                          'igst': igst_total,
                                          'amount_untaxed': amount_untaxed_total,
                                          'due': due_total,
                                          })
                product_final_lis.append({'name': 10,
                                          'customer': 'Grand Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': grand_total,
                                          'cgst': cgst_grand_total,
                                          'sgst': sgst_grand_total,
                                          'igst': igst_grand_total,
                                          'amount_untaxed': amount_untaxed_grand_total,
                                          'due': due_grand_total,
                                          })

            return {
                'docsnn': product_final_lis,
            }

        if customer == 'all' and detailed == False:
            grand_total = 0
            due_total = 0
            self.env.cr.execute(
                """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total, SUM(am.amount_residual) as due from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                    am.move_type = '""" + str(type1) + """' 
                                    and am.state='posted' 
                                   and am.project_invoice_type = 'employee_invoice' """ + domain + """ group by rp.name order by rp.name""")
            for dt in self.env.cr.dictfetchall():
                product_final_lis.append({
                    'name': 1,
                    'partner_name': dt['name'],
                    'invoice_count': dt['count'],
                    'total': dt['total'],
                    'due': dt['due'],

                })
                grand_total += dt['total']
                due_total += dt['due']
            product_final_lis.append({
                'name': 10,
                'partner_name': None,
                'invoice_count': None,
                'total': grand_total,
                'due': due_total,
            })

            return {
                'docsnn': product_final_lis,
            }
        if customer == 'selected' and detailed == False:
            grand_total = 0
            due_total = 0
            self.env.cr.execute(
                """select rp.name, COUNT(partner_id) as count , SUM(am.amount_total) as total, SUM(am.amount_residual) as due from account_move as am left join res_partner as rp ON rp.id = am.partner_id where 
                                    am.move_type = '""" + str(type1) + """' and am.partner_id in """ + str(
                    tuple(customer_ids)).replace(",)", ")") + """
                                    and am.state='posted' 
                                    and am.project_invoice_type = 'employee_invoice' """ + domain + """ group by rp.name order by rp.name""")
            for dt in self.env.cr.dictfetchall():
                product_final_lis.append({
                    'name': 1,
                    'partner_name': dt['name'],
                    'invoice_count': dt['count'],
                    'total': dt['total'],
                    'due': dt['due']

                })
                grand_total += dt['total']
                due_total += dt['due']
            product_final_lis.append({
                'name': 10,
                'partner_name': None,
                'invoice_count': None,
                'total': grand_total,
                'due': due_total,
            })

            return {
                'docsnn': product_final_lis,
            }
        if customer == 'selected' and detailed == True:
            for customers in customer_ids:
                self.env.cr.execute("""select rp.id, rp.name, am.date,am.name as invoice, am.amount_total as total ,
                am.amount_untaxed,
SUM(CASE WHEN tax.name LIKE '%CGST%' THEN aml.price_subtotal ELSE 0 END) AS cgst,
SUM(CASE WHEN tax.name LIKE '%SGST%' THEN aml.price_subtotal ELSE 0 END) AS sgst,
SUM(CASE WHEN tax.name LIKE '%IGST%' THEN aml.price_subtotal ELSE 0 END) AS igst,
am.amount_residual as due
                                                    from account_move as am left join res_partner as rp ON rp.id = am.partner_id 
                                                    LEFT JOIN 
account_move_line AS aml ON aml.move_id = am.id
LEFT JOIN 
account_tax AS tax ON tax.id = aml.tax_line_id
where aml.tax_line_id IS NOT NULL and
                                                    am.move_type = '""" + str(type1) + """'and am.partner_id = '""" + str(
                    customers) + """'  and am.state='posted' and am.project_invoice_type = 'employee_invoice' 
                                                     """ + domain + """ GROUP BY 
am.id, rp.id order by rp.name """)
                for dt in self.env.cr.dictfetchall():
                    docs.append({
                        'id': dt['id'],
                        'date': dt['date'].strftime("%d/%m/%Y"),
                        'invoice_no': dt['invoice'],
                        'customer': dt['name'],
                        'cgst': dt['cgst'],
                        'sgst': dt['sgst'],
                        'igst': dt['igst'],
                        'amount_untaxed': dt['amount_untaxed'],
                        'total': dt['total'],
                        'due': dt['due'],
                    })

            if len(docs) > 0:
                cid = docs[0]['id']
                grand_total = 0
                cgst_grand_total = 0
                sgst_grand_total = 0
                igst_grand_total = 0
                amount_untaxed_grand_total = 0
                due_grand_total = 0
                customer_total = 0
                cgst_total = 0
                sgst_total = 0
                igst_total = 0
                due_total = 0
                amount_untaxed_total = 0
                i = 0
                product_final_lis.append({'name': 6,
                                          'customer': docs[0]['customer'],
                                          'date': None,
                                          'invoice_no': None,
                                          'total': None,
                                          'cgst': None,
                                          'sgst': None,
                                          'igst': None,
                                          'amount_untaxed': None,
                                          'due': None,
                                          })

                while i < len(docs):
                    if cid == docs[i]['id']:
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  'cgst': docs[i]['cgst'],
                                                  'sgst': docs[i]['sgst'],
                                                  'igst': docs[i]['igst'],
                                                  'amount_untaxed': docs[i]['amount_untaxed'],
                                                  'due': docs[i]['due'],
                                                  })
                        grand_total += docs[i]['total']
                        cgst_grand_total += docs[i]['cgst']
                        sgst_grand_total += docs[i]['sgst']
                        igst_grand_total += docs[i]['igst']
                        amount_untaxed_grand_total += docs[i]['amount_untaxed']
                        due_grand_total += docs[i]['due']
                        customer_total += docs[i]['total']
                        cgst_total += docs[i]['cgst']
                        sgst_total += docs[i]['sgst']
                        igst_total += docs[i]['igst']
                        amount_untaxed_total += docs[i]['amount_untaxed']
                        due_total += docs[i]['due']
                    else:
                        product_final_lis.append({'name': 10,
                                                  'customer': 'Total',
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': customer_total,
                                                  'cgst': cgst_total,
                                                  'sgst': sgst_total,
                                                  'igst': igst_total,
                                                  'amount_untaxed': amount_untaxed_total,
                                                  'due': due_total,
                                                  })
                        cid = docs[i]['id']
                        cgst_total = 0
                        sgst_total = 0
                        igst_total = 0
                        amount_untaxed_total = 0
                        due_total = 0
                        customer_total = 0
                        product_final_lis.append({'name': 6,
                                                  'customer': docs[i]['customer'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'total': None,
                                                  'cgst': None,
                                                  'sgst': None,
                                                  'igst': None,
                                                  'amount_untaxed': None,
                                                  'due': None,
                                                  })
                        product_final_lis.append({'name': 1,
                                                  'customer': None,
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'total': docs[i]['total'],
                                                  'cgst': docs[i]['cgst'],
                                                  'sgst': docs[i]['sgst'],
                                                  'igst': docs[i]['igst'],
                                                  'amount_untaxed': docs[i]['amount_untaxed'],
                                                  'due': docs[i]['due'],
                                                  })
                        grand_total += docs[i]['total']
                        cgst_grand_total += docs[i]['cgst']
                        sgst_grand_total += docs[i]['sgst']
                        igst_grand_total += docs[i]['igst']
                        amount_untaxed_grand_total += docs[i]['amount_untaxed']
                        due_grand_total += docs[i]['due']
                        customer_total += docs[i]['total']
                        cgst_total += docs[i]['cgst']
                        sgst_total += docs[i]['sgst']
                        igst_total += docs[i]['igst']
                        amount_untaxed_total += docs[i]['amount_untaxed']
                        due_total += docs[i]['due']
                    i = i + 1
                product_final_lis.append({'name': 10,
                                          'customer': 'Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': customer_total,
                                          'cgst': cgst_total,
                                          'sgst': sgst_total,
                                          'igst': igst_total,
                                          'amount_untaxed': amount_untaxed_total,
                                          'due': due_total,
                                          })
                product_final_lis.append({'name': 10,
                                          'customer': 'Grand Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'total': grand_total,
                                          'cgst': cgst_grand_total,
                                          'sgst': sgst_grand_total,
                                          'igst': igst_grand_total,
                                          'amount_untaxed': amount_untaxed_grand_total,
                                          'due': due_grand_total,
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
            if res['lines']['ctype'] == 'selected' and res['lines']['detailed']:
                if res['lines']['customer_ids']:
                    case = 1

        # res['lines']['report_type'] = 'html'
        # res['lines']['report_structure'] = 'all'
        self.template_area = self.env.ref('incentive_invoice_report.report_incentive_invoice')._render(
            {'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'case': case,
             'detailed': res['lines']['detailed'],
             'ctype': res['lines']['ctype'],
             't_type': res['lines']['t_type'],
             'outstanding': self.outstanding,
             # 'branch_ids': res['lines']['branch_ids'],
             # 'isbranch': res['lines']['isbranch'],
             # 'branch_name': res['lines']['branch_name'],
             })
        print('res', res)
        return res

    @api.model
    def _get_report_data(self):
        data = {
            'date_from': str(self.date_from),
            'date_to': str(self.date_to),
            't_type': 'sales',
            'ctype': self.report_type if self.report_type else False,
            'detailed': self.detailed if self.detailed else False,
        }
        print('data', data)
        dat = self.get_report_values(data=data)

        return {
            'lines': dat,
        }
