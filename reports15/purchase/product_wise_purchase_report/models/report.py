# -*- coding: utf-8 -*-
from odoo import models, api,fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning,ValidationError
from pytz import timezone


class ReportPurchase(models.TransientModel):
    _name = 'report.product'
    _inherit = 'beta.reports'
    _description = 'Product Wise Purchase'

    name = fields.Char(default='Report')  # change this
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    detailed = fields.Boolean(string="Detailed")
    t_type = fields.Selection([
        ('purchase', 'Purchase'),
        ('purchase_returns', 'Purchase Return')], String="Transaction Type",default="purchase")
    ptype = fields.Selection([
        ('all', 'All'),
        ('selected_product', 'Product')], String="Report Type",default="all")
    report_product=fields.Many2many('product.product')


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
        print(res['date_from'])
        return res

    @api.onchange('ptype')
    def onchange_supplier(self):
        if self.ptype == 'all':
            self.write({
                'report_product': False
            })

    def get_report_values(self, data=None):
        date_from = date_to = False
        product_obj = self.env['product.product']
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

        if data['ptype'] == 'selected_product':
            if data['product_ids']:
                for product in data['product_ids']:
                    products += product_obj.browse(product).name + ", "
            else:
                raise ValidationError("No Products Are Selected !!!")


        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            't_type': data['t_type'],
            'detailed': data['detailed'],
            'ptype': data['ptype'],
            'product_ids': products,
            'branch_ids': branch,
            'branch_name': data['branch_name'],
            'isbranch':data['isbranch'],
            'lines': self.get_product_purchase(data),
        }

    def get_product_purchase(self, data):
        if 'branch_id' in self.env.user._fields:
            sales = {}
            amount_total, taxable_total, tax_sum = 0, 0, 0
            date_from = data['date_from']
            date_to = data['date_to']
            detailed = data['detailed']
            type = data['t_type']
            print(data['t_type'])
            product = data['ptype']
            print(data['ptype'])
            product_ids = data['product_ids']
            branch_ids = data['branch_ids']
            docs = []
            i = 0
            name = ''
            uid = ''

            product_final_lis = []
            product_final = []
            type1 = []
            filter = ''
            if type == 'purchase':
                type1 = 'in_invoice'

            if type == 'purchase_returns':
                type1 = 'in_refund'
            exp_filter = ''
            if 'expiry_type' in self.env['account.move']._fields:
                if type1 in ['in_invoice','in_refund']:
                    exp_filter = " and am.expiry_type is null "
            print(exp_filter)
            if product == 'all' and detailed == True:
                if branch_ids:
                    for branch in branch_ids:
                        brh = str(branch)

                        self.env.cr.execute(
                            """select am.name,am.move_type as type,rb.name as branch_name,aml.branch_id, pt.id as id,pp.id as pid, aml.date as date, aml.move_name as invoice_no, pt.name as product_name, rp.name as customer,aml.description, aml.l10n_in_hsn_code as hsn_code,aml.quantity as qty,uu.name as uom, aml.price_unit as price_unit, at.amount as tax ,aml.price_total from account_move as am LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) LEFT JOIN product_product as pp ON (aml.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) LEFT JOIN uom_uom as uu ON (aml.product_uom_id=uu.id) LEFT JOIN res_branch as rb ON (rb.id=aml.branch_id) where aml.product_id IS NOT NULL and aml.date<='""" + date_to + """' and aml.date>='""" + date_from + """' and aml.exclude_from_invoice_tab ='FALSE' and am.move_type='""" + str(
                                type1) + """'  and am.state='posted' """ + exp_filter +""" and am.branch_id='""" + brh + """' order by pt.name, date, aml.move_name""")

                        for dt in self.env.cr.dictfetchall():
                            docs.append({
                                'id': dt['id'],
                                'pid': dt['pid'],
                                'branch_id': dt['branch_id'],
                                'date': dt['date'].strftime("%d/%m/%Y"),
                                'invoice_no': dt['invoice_no'],
                                'customer': dt['customer'],
                                'product_name': dt['product_name'],
                                'description': dt['description'],
                                'hsn_code': dt['hsn_code'],
                                'qty': dt['qty'],
                                'uom': dt['uom'],
                                'price_unit': dt['price_unit'],
                                'tax': dt['tax'],
                                'price_total': dt['price_total'],
                                'trans': dt['name'],
                                'type': dt['type'],
                                'branch_name': dt['branch_name'],
                            })
                if len(docs) > 0:
                    uid = docs[0]['id']
                    total_amount = 0
                    branch = docs[0]['branch_id']
                    branch_total = 0
                    branch_qty = 0
                    total_qty = 0
                    i = 0

                    product_final.append({'name': 8,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': docs[0]['branch_name'],
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': None,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': None,
                                          })

                    product_final.append({'name': 5,
                                          'product_name': docs[0]['product_name'],
                                          'date': None,
                                          'branch_name': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': None,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': None,
                                          })
                    while (i < len(docs)):
                        if (branch == docs[i]['branch_id']):
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                name = docs[i]['product_name']
                                name2 = name
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                total_qty = total_qty + docs[i]['qty']
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                            else:

                                product_final.append({'name': 1,
                                                      'product_name': None,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': total_qty,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(total_amount, 3),
                                                      })

                                product_final_lis = product_final_lis + product_final
                                total_amount = 0

                                total_qty = 0
                                product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                product_final.append({'name': 5,
                                                      'product_name': docs[i]['product_name'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': None,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': None,
                                                      })
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                                product_id = docs[i]['id']
                                product_name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                branch_total = branch_total + docs[i]['price_total']
                        else:
                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': total_qty,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(total_amount, 3),
                                                  })
                            product_final.append({'name': 10,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': branch_qty,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(branch_total, 3),
                                                  })
                            branch = docs[i]['branch_id']
                            branch_total = 0
                            branch_qty = 0
                            uid = docs[i]['id']
                            quantity = 0
                            amount = 0
                            total_amount = 0
                            total_qty = 0
                            product_final.append({'name': 8,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': docs[i]['branch_name'],
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': None,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })

                            product_final.append({'name': 5,
                                                  'product_name': docs[i]['product_name'],
                                                  'date': None,
                                                  'branch_name': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': None,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                name = docs[i]['product_name']
                                name2 = name
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                total_qty = total_qty + docs[i]['qty']
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                            else:

                                product_final.append({'name': 1,
                                                      'product_name': None,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': total_qty,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(total_amount, 3),
                                                      })

                                total_amount = 0

                                total_qty = 0
                                product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                product_final.append({'name': 5,
                                                      'product_name': docs[i]['product_name'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': None,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': None,
                                                      })
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                                product_id = docs[i]['id']
                                product_name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']

                        i = i + 1

                    product_final.append({'name': 1,
                                          'product_name': 'Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': round(total_qty, 3),
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(total_amount, 3),
                                          })
                    product_final.append({'name': 10,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': branch_qty,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(branch_total, 3),
                                          })
                    product_final_lis = product_final_lis + product_final

                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,
                    'case': 1,

                }

            if product == 'all' and detailed == False:
                if branch_ids:
                    for branch in branch_ids:
                        brh = str(branch)
                        self.env.cr.execute(
                            """select am.name,am.move_type as type,rb.name as branch_name,aml.branch_id, pt.id as id,pp.id as pid, aml.date as date, aml.move_name as invoice_no, pt.name as product_name, rp.name as customer,aml.description, aml.l10n_in_hsn_code as hsn_code,aml.quantity as qty,uu.name as uom, aml.price_unit as price_unit, at.amount as tax ,aml.price_total from account_move as am LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) LEFT JOIN product_product as pp ON (aml.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) LEFT JOIN uom_uom as uu ON (aml.product_uom_id=uu.id) LEFT JOIN res_branch as rb ON (rb.id=aml.branch_id) where aml.product_id IS NOT NULL and aml.date<='""" + date_to + """' and aml.date>='""" + date_from + """' and aml.exclude_from_invoice_tab ='FALSE' and am.move_type='""" + str(
                                type1) + """' and am.state='posted' """ + exp_filter +""" and am.branch_id='""" + brh + """' order by pt.name, date, aml.move_name""")

                        for dt in self.env.cr.dictfetchall():
                            docs.append({
                                'id': dt['id'],
                                'pid': dt['pid'],
                                'branch_id': dt['branch_id'],
                                'date': dt['date'].strftime("%d/%m/%Y"),
                                'invoice_no': dt['invoice_no'],
                                'branch_name': dt['branch_name'],
                                'customer': dt['customer'],
                                'product_name': dt['product_name'],
                                'description': dt['description'],
                                'hsn_code': dt['hsn_code'],
                                'qty': dt['qty'],
                                'uom': dt['uom'],
                                'price_unit': dt['price_unit'],
                                'tax': dt['tax'],
                                'price_total': dt['price_total'],
                                'trans': dt['name'],

                            })

                if len(docs) > 0:
                    uid = docs[0]['id']
                    quantity = 0
                    amount = 0
                    branch = docs[0]['branch_id']
                    total_amount = 0
                    branch_total = 0
                    total_qty = 0
                    total_discount = 0
                    netamount = 0
                    i = 0
                    product_final.append({'name': 8,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': docs[i]['branch_name'],
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': None,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': None,
                                          })

                    while (i < len(docs)):
                        if (branch == docs[i]['branch_id']):
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                quantity = quantity + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                name = docs[i]['product_name']
                                amount = amount + round(docs[i]['price_total'], 3)
                                amount1 = round(amount, 2)
                                total_qty = total_qty + docs[i]['qty']
                                total_amount = total_amount + round(docs[i]['price_total'], 3)
                                branch_total = branch_total + round(docs[i]['price_total'], 3)

                            else:
                                product_final.append({'name': 1,
                                                      'product_name': name,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'qty': round(quantity, 3),
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(amount, 3),
                                                      })

                                # product_final_lis = product_final_lis + product_final

                                quantity = 0

                                amount = 0

                                # product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                amount = amount + round(docs[i]['price_total'], 3)

                                quantity = quantity + docs[i]['qty']

                                product_id = docs[i]['id']
                                name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                total_amount = total_amount + round(docs[i]['price_total'], 3)
                                branch_total = branch_total + round(docs[i]['price_total'], 3)

                        else:
                            product_final.append({'name': 3,
                                                  'product_name': name,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'qty': quantity,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(amount, 3),
                                                  })
                            product_final.append({'name': 10,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'qty': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(branch_total, 3),
                                                  })
                            branch = docs[i]['branch_id']
                            quantity = 0
                            amount = 0
                            branch_total = 0
                            uid = docs[i]['id']

                            product_final.append({'name': 8,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': docs[i]['branch_name'],
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': None,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                quantity = quantity + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                name = docs[i]['product_name']
                                amount = amount + round(docs[i]['price_total'], 3)
                                amount1 = round(amount, 2)
                                total_qty = total_qty + docs[i]['qty']
                                total_amount = total_amount + round(docs[i]['price_total'], 3)
                                branch_total = branch_total + round(docs[i]['price_total'], 3)

                            else:
                                product_final.append({'name': 1,
                                                      'product_name': name,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'qty': round(quantity, 3),
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(amount, 3),
                                                      })

                                # product_final_lis = product_final_lis + product_final

                                quantity = 0

                                amount = 0

                                product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                amount = amount + round(docs[i]['price_total'], 3)

                                quantity = quantity + docs[i]['qty']

                                product_id = docs[i]['id']
                                name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                total_amount = total_amount + round(docs[i]['price_total'], 3)
                                branch_total = branch_total + round(docs[i]['price_total'], 3)

                        i = i + 1
                    netamount = netamount + total_amount
                    # product_final_lis = product_final_lis + product_final
                    product_final.append({'name': 3,
                                          'product_name': name,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'qty': quantity,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(amount, 3),
                                          })
                    product_final.append({'name': 10,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'qty': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(branch_total, 3),
                                          })

                    product_final_lis = product_final
                    product_total = {'name': 2,
                                     'product_name': 'Total',
                                     'date': None,
                                     'invoice_no': None,
                                     'branch_name': None,
                                     'customer': None,
                                     'qty': total_qty,
                                     'price_unit': None,
                                     'tax': None,
                                     'price_total': round(netamount, 3),
                                     }
                    product_final_lis.append(product_total)
                    print(product_final_lis,"product_final_lis")
                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,
                    'case': 2,

                }

            if product == 'selected_product':
                if branch_ids:
                    for branch in branch_ids:
                        brh = str(branch)
                        for product in product_ids:
                            self.env.cr.execute(
                                """select am.name,am.move_type as type,aml.branch_id,rb.name as branch_name, pt.id as id,pp.id as pid, aml.date as date, aml.move_name as invoice_no, pt.name as product_name, rp.name as customer,aml.description, aml.l10n_in_hsn_code as hsn_code,aml.quantity as qty,uu.name as uom, aml.price_unit as price_unit, at.amount as tax ,aml.price_total from account_move as am LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) LEFT JOIN product_product as pp ON (aml.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) LEFT JOIN uom_uom as uu ON (aml.product_uom_id=uu.id) LEFT JOIN res_branch as rb ON (rb.id=aml.branch_id) where aml.product_id IS NOT NULL and aml.date<='""" + date_to + """' and aml.date>='""" + date_from + """' and aml.exclude_from_invoice_tab ='FALSE' and am.move_type='""" + str(
                                    type1) + """' and am.state='posted' """ + exp_filter +""" and pp.id='""" + str(product) + """' and am.branch_id='""" + brh + """' order by pt.name, date, aml.move_name""")
                            for dt in self.env.cr.dictfetchall():
                                docs.append({
                                    'id': dt['id'],
                                    'pid': dt['pid'],
                                    'branch_id': dt['branch_id'],
                                    'date': dt['date'].strftime("%d/%m/%Y"),
                                    'invoice_no': dt['invoice_no'],
                                    'customer': dt['customer'],
                                    'product_name': dt['product_name'],
                                    'description': dt['description'],
                                    'hsn_code': dt['hsn_code'],
                                    'qty': dt['qty'],
                                    'uom': dt['uom'],
                                    'price_unit': dt['price_unit'],
                                    'tax': dt['tax'],
                                    'price_total': dt['price_total'],
                                    'trans': dt['name'],
                                    'type': dt['type'],
                                    'branch_name': dt['branch_name'],
                                })

                if len(docs) > 0:
                    uid = docs[0]['id']
                    total_amount = 0
                    branch = docs[0]['branch_id']
                    branch_total = 0
                    branch_qty = 0
                    total_qty = 0
                    i = 0

                    product_final.append({'name': 8,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': docs[0]['branch_name'],
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': None,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': None,
                                          })

                    product_final.append({'name': 5,
                                          'product_name': docs[0]['product_name'],
                                          'date': None,
                                          'branch_name': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': None,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': None,
                                          })
                    while (i < len(docs)):
                        if (branch == docs[i]['branch_id']):
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                name = docs[i]['product_name']
                                name2 = name
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                total_qty = total_qty + docs[i]['qty']
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                            else:

                                product_final.append({'name': 1,
                                                      'product_name': None,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': total_qty,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(total_amount, 3),
                                                      })

                                product_final_lis = product_final_lis + product_final
                                total_amount = 0

                                total_qty = 0
                                product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                product_final.append({'name': 5,
                                                      'product_name': docs[i]['product_name'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': None,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': None,
                                                      })
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                                product_id = docs[i]['id']
                                product_name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                branch_total = branch_total + docs[i]['price_total']
                        else:
                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': total_qty,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(total_amount, 3),
                                                  })
                            product_final.append({'name': 10,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': branch_qty,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': round(branch_total, 3),
                                                  })
                            branch = docs[i]['branch_id']
                            branch_total = 0
                            branch_qty = 0
                            uid = docs[i]['id']
                            quantity = 0
                            amount = 0
                            total_amount = 0
                            total_qty = 0
                            product_final.append({'name': 8,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'branch_name': docs[i]['branch_name'],
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': None,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })

                            product_final.append({'name': 5,
                                                  'product_name': docs[i]['product_name'],
                                                  'date': None,
                                                  'branch_name': None,
                                                  'invoice_no': None,
                                                  'branch_name': None,
                                                  'customer': None,
                                                  'description': None,
                                                  'hsn_code': None,
                                                  'qty': None,
                                                  'uom': None,
                                                  'price_unit': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })
                            if (uid == docs[i]['id']):
                                product_id = docs[i]['id']
                                pid = docs[i]['pid']
                                name = docs[i]['product_name']
                                name2 = name
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']
                                total_qty = total_qty + docs[i]['qty']
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                            else:

                                product_final.append({'name': 1,
                                                      'product_name': None,
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': total_qty,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': round(total_amount, 3),
                                                      })

                                total_amount = 0

                                total_qty = 0
                                product_final = []
                                pid = docs[i]['pid']
                                uid = docs[i]['id']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000

                                product_final.append({'name': 5,
                                                      'product_name': docs[i]['product_name'],
                                                      'date': None,
                                                      'invoice_no': None,
                                                      'branch_name': None,
                                                      'customer': None,
                                                      'description': None,
                                                      'hsn_code': None,
                                                      'qty': None,
                                                      'uom': None,
                                                      'price_unit': None,
                                                      'tax': None,
                                                      'price_total': None,
                                                      })
                                product_final.append({'name': 4,
                                                      'product_name': docs[i]['trans'],
                                                      'date': docs[i]['date'],
                                                      'invoice_no': docs[i]['invoice_no'],
                                                      'branch_name': None,
                                                      'customer': docs[i]['customer'],
                                                      'description': docs[i]['description'],
                                                      'hsn_code': docs[i]['hsn_code'],
                                                      'qty': round(docs[i]['qty'], 3),
                                                      'uom': docs[i]['uom'],
                                                      'price_unit': round(docs[i]['price_unit'], 3),
                                                      'tax': docs[i]['tax'],
                                                      'price_total': round(docs[i]['price_total'], 3),
                                                      })

                                product_id = docs[i]['id']
                                product_name = docs[i]['product_name']
                                total_qty = total_qty + docs[i]['qty']
                                if docs[i]['tax'] == None:
                                    docs[i]['tax'] = 0.000
                                total_amount = total_amount + docs[i]['price_total']
                                branch_total = branch_total + docs[i]['price_total']
                                branch_qty = branch_qty + docs[i]['qty']

                        i = i + 1

                    product_final.append({'name': 1,
                                          'product_name': 'Total',
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': round(total_qty, 3),
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(total_amount, 3),
                                          })
                    product_final.append({'name': 10,
                                          'product_name': None,
                                          'date': None,
                                          'invoice_no': None,
                                          'branch_name': None,
                                          'customer': None,
                                          'description': None,
                                          'hsn_code': None,
                                          'qty': branch_qty,
                                          'uom': None,
                                          'price_unit': None,
                                          'tax': None,
                                          'price_total': round(branch_total, 3),
                                          })
                    product_final_lis = product_final_lis + product_final

                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,
                    'case': 1,

                }
        else:
            sales = {}
            amount_total, taxable_total, tax_sum = 0, 0, 0
            date_from = data['date_from']
            date_to = data['date_to']
            detailed = data['detailed']
            type = data['t_type']
            product = data['ptype']
            product_ids = data['product_ids']

            docs = []
            i = 0
            name = ''
            uid = ''

            product_final_lis = []
            product_final = []
            type1 = []
            filter = ''
            if type == 'purchase':
                type1 = 'in_invoice'

            if type == 'purchase_returns':
                type1 = 'in_refund'
            exp_filter = ''
            if 'expiry_type' in self.env['account.move']._fields:
                if type1 in ['in_invoice', 'in_refund']:
                    exp_filter = " and am.expiry_type is null "

            if product == 'all' and detailed == True:
                filt2 = ''
                #if 'direct_move_type' in self.env['account.move']._fields:
                  #  filt2 = " and direct_move_type = 'incoming' "
                q1="""select am.name, pt.id as id,pp.id as pid, aml.date as date,
                                     aml.move_name as invoice_no, pt.name as product_name, 
                                     rp.name as customer,aml.quantity as qty, aml.price_unit as price_unit, 
                                     aml.discount as discount, at.amount as tax ,aml.price_total from account_move as am
                                      LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) 
                                      LEFT JOIN product_product as pp ON (aml.product_id = pp.id)
                                       LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) 
                                       LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) 
                                       LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) 
                                       LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) where aml.product_id IS NOT NULL 
                                       and aml.date<='""" + date_to + """' and aml.date>='""" + date_from + """' 
                                       and aml.exclude_from_invoice_tab ='FALSE' """ + exp_filter + """ and am.move_type ='""" + str(
                    type1) + """' and am.state='posted'  """ + str(filt2) + str(
                    filter) + """ order by pt.name, date, aml.move_name """
                self.env.cr.execute(q1)
                for dt in self.env.cr.dictfetchall():
                    docs.append({
                        'id': dt['id'],
                        'pid': dt['pid'],
                        'date': dt['date'].strftime("%d/%m/%Y"),
                        'invoice_no': dt['invoice_no'],
                        'customer': dt['customer'],
                        'product_name': dt['product_name'],
                        'qty': dt['qty'],
                        'price_unit': dt['price_unit'],
                        'discount': dt['discount'],
                        'tax': dt['tax'],
                        'price_total': dt['price_total'],
                        'trans': dt['name']
                    })
                if len(docs) > 0:
                    uid = docs[0]['id']
                    total_amount = 0
                    total_qty = 0

                    i = 0

                    product_final.append({'name': 5,
                                          'product_name': docs[0]['product_name'],
                                          'date': None,
                                          'invoice_no': None,
                                          'customer': None,
                                          'qty': None,
                                          'price_unit': None,
                                          'discount': None,
                                          'tax': None,
                                          'price_total': None,
                                          })
                    while (i < len(docs)):
                        if (uid == docs[i]['id']):

                            product_id = docs[i]['id']

                            pid = docs[i]['pid']

                            name = docs[i]['product_name']
                            name2 = name

                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000

                            total_amount = total_amount + docs[i]['price_total']

                            total_qty = total_qty + docs[i]['qty']

                            product_final.append({'name': 4,
                                                  'product_name': docs[i]['trans'],
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'customer': docs[i]['customer'],
                                                  'qty': round(docs[i]['qty'], 3),

                                                  'price_unit': round(docs[i]['price_unit'], 3),
                                                  'discount': round(docs[i]['discount'], 3),
                                                  'tax': docs[i]['tax'],
                                                  'price_total': round(docs[i]['price_total'], 3),
                                                  })


                        else:

                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'customer': None,
                                                  'qty': total_qty,

                                                  'price_unit': None,
                                                  'discount': None,
                                                  'tax': None,
                                                  'price_total': round(total_amount, 3),
                                                  })

                            product_final_lis = product_final_lis + product_final
                            total_amount = 0

                            total_qty = 0

                            product_final = []
                            pid = docs[i]['pid']
                            uid = docs[i]['id']
                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000

                            product_final.append({'name': 5,
                                                  'product_name': docs[i]['product_name'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'customer': None,
                                                  'qty': None,

                                                  'price_unit': None,
                                                  'discount': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })
                            product_final.append({'name': 4,
                                                  'product_name': docs[i]['trans'],
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'customer': docs[i]['customer'],
                                                  'qty': round(docs[i]['qty'], 3),

                                                  'price_unit': round(docs[i]['price_unit'], 3),
                                                  'discount': round(docs[i]['discount'], 3),
                                                  'tax': docs[i]['tax'],
                                                  'price_total': round(docs[i]['price_total'], 3),
                                                  })

                            product_id = docs[i]['id']
                            product_name = docs[i]['product_name']
                            total_qty = total_qty + docs[i]['qty']

                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000
                            total_amount = total_amount + docs[i]['price_total']

                        i = i + 1
                    product_final_lis = product_final_lis + product_final
                    product_total = {'name': 2,
                                     'product_name': 'Total',
                                     'date': None,
                                     'invoice_no': None,
                                     'customer': None,
                                     'qty': round(total_qty, 3),

                                     'price_unit': None,
                                     'discount': None,
                                     'tax': None,
                                     'price_total': round(total_amount, 3),
                                     }
                    product_final_lis.append(product_total)

                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,

                    'case': 4,
                }

            if product == 'all' and detailed == False:
                filt2 = ''
                #if 'direct_move_type' in self.env['account.move']._fields:
                    #filt2 = " and direct_move_type = 'incoming' "
                self.env.cr.execute(
                    """select am.name, pt.id as id,pp.id as pid, aml.date as date,
                     aml.move_name as invoice_no, pt.name as product_name,
                      rp.name as customer,aml.quantity as qty, aml.price_unit as price_unit, 
                      aml.discount as discount,  at.amount as tax ,
                      aml.price_total from account_move as am 
                      LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) 
                      LEFT JOIN product_product as pp ON (aml.product_id = pp.id) 
                      LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) 
                      LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) 
                      LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) 
                      LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) 
                      where aml.product_id IS NOT NULL and aml.date<='""" + date_to + """' and aml.date>='""" + date_from + """'
                       and aml.exclude_from_invoice_tab ='FALSE' """ + exp_filter +""" 
                      and am.move_type ='""" + str(
                        type1) + """' and am.state='posted'""" + str(filt2) + str(
                        filter) + """ order by pt.name, date, aml.move_name """)

                for dt in self.env.cr.dictfetchall():
                    docs.append({
                        'id': dt['id'],
                        'pid': dt['pid'],
                        'date': dt['date'].strftime("%d/%m/%Y"),
                        'invoice_no': dt['invoice_no'],
                        'customer': dt['customer'],
                        'product_name': dt['product_name'],
                        'qty': dt['qty'],
                        'price_unit': dt['price_unit'],
                        'discount': dt['discount'],
                        'tax': dt['tax'],
                        'price_total': dt['price_total'],
                        'trans': dt['name']
                    })
                if len(docs) > 0:
                    uid = docs[0]['id']
                    discount = 0
                    quantity = 0
                    freeqty = 0
                    amount = 0
                    replaceqty = 0

                    total_amount = 0
                    total_qty = 0

                    total_discount = 0
                    netamount = 0
                    i = 0

                    while (i < len(docs)):
                        if (uid == docs[i]['id']):

                            product_id = docs[i]['id']
                            discount = discount + docs[i]['discount']

                            pid = docs[i]['pid']

                            quantity = quantity + docs[i]['qty']
                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000
                            name = docs[i]['product_name']
                            amount = amount + round(docs[i]['price_total'], 3)
                            amount1 = round(amount, 2)
                            total_qty = total_qty + docs[i]['qty']
                            total_amount = total_amount + round(docs[i]['price_total'], 3)
                            total_discount = total_discount + docs[i]['discount']

                        else:
                            product_final.append({'name': 1,
                                                  'product_name': name,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'customer': None,
                                                  'qty': round(quantity, 3),
                                                  'price_unit': None,
                                                  'discount': None,
                                                  'tax': None,
                                                  'price_total': round(amount, 3),
                                                  })

                            product_final_lis = product_final_lis + product_final
                            discount = 0
                            quantity = 0

                            amount = 0

                            product_final = []
                            pid = docs[i]['pid']
                            uid = docs[i]['id']
                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000
                            amount = amount + round(docs[i]['price_total'], 3)
                            discount = discount + docs[i]['discount']
                            quantity = quantity + docs[i]['qty']
                            product_id = docs[i]['id']
                            name = docs[i]['product_name']
                            total_discount = total_discount + docs[i]['discount']
                            total_qty = total_qty + docs[i]['qty']
                            total_amount = total_amount + round(docs[i]['price_total'], 3)
                        i = i + 1
                    netamount = netamount + total_amount
                    product_final_lis = product_final_lis + product_final
                    product_final.append({'name': 3,
                                          'product_name': name,
                                          'date': None,
                                          'invoice_no': None,
                                          'customer': None,
                                          'qty': quantity,
                                          'price_unit': None,
                                          'discount': None,
                                          'tax': None,
                                          'price_total': round(amount, 3),
                                          })

                    product_final_lis = product_final_lis + product_final
                    product_total = {'name': 2,
                                     'product_name': 'Total',
                                     'date': None,
                                     'invoice_no': None,
                                     'customer': None,
                                     'qty': total_qty,

                                     'price_unit': None,
                                     'discount': None,
                                     'tax': None,
                                     'price_total': round(netamount, 3),
                                     }
                    product_final_lis.append(product_total)
                #print(product_final_lis)
                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,
                    'case': 2,

                }

            if product == 'selected_product':
                for product in product_ids:
                    filt2 = ''
                    #if 'direct_move_type' in self.env['account.move']._fields:
                        #filt2 = "  and direct_move_type = 'incoming'  "
                    self.env.cr.execute(
                        """select am.name, pt.id as id,pp.id as pid, aml.date as date,
                         aml.move_name as invoice_no, pt.name as product_name, 
                         rp.name as customer,aml.quantity as qty, aml.price_unit as price_unit, 
                         aml.discount as discount, at.amount as tax ,
                         aml.price_total from account_move as am 
                         LEFT JOIN account_move_line as aml ON (aml.move_id=am.id) 
                         LEFT JOIN product_product as pp ON (aml.product_id = pp.id)
                          LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) 
                          LEFT JOIN res_partner as rp ON (aml.partner_id=rp.id) 
                          LEFT JOIN account_move_line_account_tax_rel as tax ON (aml.id=tax.account_move_line_id) 
                          LEFT JOIN account_tax as at ON (tax.account_tax_id=at.id) 
                          where aml.product_id IS NOT NULL and aml.date<='""" + date_to + """' and aml.date>='""" +
                        date_from + """' and aml.exclude_from_invoice_tab ='FALSE' """ + exp_filter +""" and 
                        am.move_type ='""" + str(
                            type1) + """' and aml.product_id='""" + str(product) + """' and am.state='posted' """+str(filt2)+""" order by pt.name, date, aml.move_name """)
                    for dt in self.env.cr.dictfetchall():
                        docs.append({
                            'id': dt['id'],
                            'pid': dt['pid'],
                            'date': dt['date'].strftime("%d/%m/%Y"),
                            'invoice_no': dt['invoice_no'],
                            'customer': dt['customer'],
                            'product_name': dt['product_name'],
                            'qty': dt['qty'],
                            'price_unit': dt['price_unit'],
                            'discount': dt['discount'],
                            'tax': dt['tax'],
                            'price_total': dt['price_total'],
                            'trans': dt['name']
                        })
                        #print(dt['invoice_no'])
                if len(docs) > 0:
                    uid = docs[0]['id']
                    total_amount = 0
                    total_qty = 0

                    i = 0

                    product_final.append({'name': 5,
                                          'product_name': docs[0]['product_name'],
                                          'date': None,
                                          'invoice_no': None,
                                          'customer': None,
                                          'qty': None,

                                          'price_unit': None,
                                          'discount': None,
                                          'tax': None,
                                          'price_total': None,
                                          })
                    while (i < len(docs)):
                        if (uid == docs[i]['id']):

                            product_id = docs[i]['id']

                            pid = docs[i]['pid']

                            name = docs[i]['product_name']
                            name2 = name

                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000

                            total_amount = total_amount + docs[i]['price_total']

                            total_qty = total_qty + docs[i]['qty']

                            product_final.append({'name': 4,
                                                  'product_name': docs[i]['trans'],
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'customer': docs[i]['customer'],
                                                  'qty': round(docs[i]['qty'], 3),

                                                  'price_unit': round(docs[i]['price_unit'], 3),
                                                  'discount': round(docs[i]['discount'], 3),
                                                  'tax': docs[i]['tax'],
                                                  'price_total': round(docs[i]['price_total'], 3),
                                                  })


                        else:

                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'customer': None,
                                                  'qty': total_qty,

                                                  'price_unit': None,
                                                  'discount': None,
                                                  'tax': None,
                                                  'price_total': round(total_amount, 3),
                                                  })

                            product_final_lis = product_final_lis + product_final
                            total_amount = 0

                            total_qty = 0

                            product_final = []
                            pid = docs[i]['pid']
                            uid = docs[i]['id']
                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000

                            product_final.append({'name': 5,
                                                  'product_name': docs[i]['product_name'],
                                                  'date': None,
                                                  'invoice_no': None,
                                                  'customer': None,
                                                  'qty': None,

                                                  'price_unit': None,
                                                  'discount': None,
                                                  'tax': None,
                                                  'price_total': None,
                                                  })
                            product_final.append({'name': 4,
                                                  'product_name': docs[i]['trans'],
                                                  'date': docs[i]['date'],
                                                  'invoice_no': docs[i]['invoice_no'],
                                                  'customer': docs[i]['customer'],
                                                  'qty': round(docs[i]['qty'], 3),

                                                  'price_unit': round(docs[i]['price_unit'], 3),
                                                  'discount': round(docs[i]['discount'], 3),
                                                  'tax': docs[i]['tax'],
                                                  'price_total': round(docs[i]['price_total'], 3),
                                                  })

                            product_id = docs[i]['id']
                            product_name = docs[i]['product_name']
                            total_qty = total_qty + docs[i]['qty']

                            if docs[i]['tax'] == None:
                                docs[i]['tax'] = 0.000
                            total_amount = total_amount + docs[i]['price_total']

                        i = i + 1
                    product_final_lis = product_final_lis + product_final
                    product_total = {'name': 2,
                                     'product_name': 'Total',
                                     'date': None,
                                     'invoice_no': None,
                                     'customer': None,
                                     'qty': round(total_qty, 3),

                                     'price_unit': None,
                                     'discount': None,
                                     'tax': None,
                                     'price_total': round(total_amount, 3),
                                     }
                    product_final_lis.append(product_total)
                return {
                    'date_from': date_from,
                    'date_to': date_to,
                    'docs': docs,
                    'docsnn': product_final_lis,
                    'type': type,
                    'case': 1,

                }


    def get_html(self):
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'), date_to=self.date_to.strftime('%Y-%m-%d'),
                                 detailed=self.detailed, ptype=self.ptype, t_type=self.t_type,report_product=self.report_product)
        case = 0
        if res['lines']['date_from'] and res['lines']['date_to']:
            if res['lines']['detailed']:
                case = 1
            else:
                case = 2
            if res['lines']['t_type'] == 'both':
                case = 3
            if res['lines']['ptype'] == 'selected_product':
                if res['lines']['product_ids']:
                    case = 1

        self.template_area = self.env.ref('product_wise_purchase_report.report_product_purchase')._render(
            { 'date_from': self.date_from.strftime('%d-%m-%Y'),
                'date_to': self.date_to.strftime('%d-%m-%Y'),
                'ptype': self.ptype,
                't_type': self.t_type,
              'detailed': self.detailed,
             'data': res['lines'],
              'lines': res['lines']['lines'],
             'product_ids': res['lines']['product_ids'],
             #'branch_ids': res['lines']['branch_ids'],
             #'isbranch': res['lines']['isbranch'],
             #'branch_name': res['lines']['branch_name'],
             })
        #print(res['lines'])
        return res


    def _get_report_data(self, date_from=False, milk=False, raw=False, date_to=False, detailed=False, ptype=False, t_type=False,report_product=False):
        tk = self.env['product.product'].search([], order='name')
        # loc = self.env['stock-.location'].search([('usage', '=', 'internal')])
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
        if report_product:
            rp = [int(i) for i in report_product]

        #if report_location:
        #   rl = [int(i) for i in report_location]

       # if 'branch_id' in self.env.user._fields:
         #   if rl:
         #       branch = self.env['res.branch'].search([('id', 'in', rl)])
          #      branch_name = ', '.join(branch.mapped('name'))

        data = {
            'date_from': date_from,
            'date_to': date_to,
            't_type': t_type if t_type else False,
            'ptype': ptype if ptype else False,
            'product_ids': rp if rp else False,
            'milk': milk if milk else False,
            'raw': raw if raw else False,
            'detailed': detailed if detailed else False,
            'branch_ids': rl if rl else (branch_default.id,),
            'isbranch':is_branch,
            'branch_name': branch_name,

        }
        dat = self.get_report_values(data=data)

        do = {}
        lo = {}
        for i in tk:
            do[i.id] = i.name
        if 'branch_id' in self.env.user._fields:
            for l in branch_list:
                if l.id != branch_default.id:
                    lo[l.id] = l.name
        print(dat)
        return {
            'lines': dat,
            'variants': do,
            'branch': lo,
            'bid':branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }

