# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import datetime
from odoo.exceptions import Warning
from pytz import timezone


class StockProduct(models.TransientModel):
    _name = 'stock.issue'
    _inherit = 'beta.reports'
    _description = 'Stock Receipt/Issue'

    name = fields.Char(default='Report')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    detailed = fields.Boolean(string="Detailed")
    t_type = fields.Selection([
        ('issue', 'Issue'),
        ('receipt', 'Receipt')], String="Transaction Type", default="issue", widget='radio')
    detailed = fields.Boolean()
    receipt = fields.Boolean()
    # ptype = fields.Selection([
    #     ('all', 'All'),
    #     ('selected_product', 'Product')], String="Report Type", default="all")
    # product_ids = fields.Many2one('product.product')

    @api.onchange('t_type')
    def _onchange_boolean(self):
        if self.t_type == 'issue':
            self.receipt = False
            self.detailed = True
            self.detailed
        if self.t_type == 'receipt':
            self.detailed = False
            self.receipt = True
            self.receipt

    @api.model
    def default_get(self, fields_list):
        res = super(StockProduct, self).default_get(fields_list)
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
        product_obj = self.env['product.product']
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        products = ''

        if data['date_from']:
            try:
                date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except TypeError:
                raise Warning("Invalid Date Format")
        if data['date_to']:
            try:
                date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except TypeError:
                raise Warning("Invalid Date Format")
        # if data['ptype'] == 'selected_product':
        if data['product_ids']:
            for product in data['product_ids']:
                products += product_obj.browse(product).name + ", "

        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            't_type': data['t_type'],
            'detailed': data['detailed'],
            'receipt': data['receipt'],
            # 'ptype': data['ptype'],
            'product_ids': products,
            'branch_ids': branch,
            'isbranch': data['isbranch'],
            'branch_name': data['branch_name'],
            'lines': self.get_product_sales(data),
        }

    def get_product_sales(self, data):
        # if 'branch_id' in self.env.user._fields:
        sales = {}
        amount_total, taxable_total, tax_sum = 0, 0, 0
        date_from = data['date_from']
        date_to = data['date_to']
        detailed = data['detailed']
        type = data['t_type']
        receipt = data['receipt']
        product_ids = data['product_ids']
        branch_ids = data['branch_ids']
        # receipt = data['receipt']
        # print(data)
        docs = []
        i = 0
        name = ''
        uid = ''

        product_final_lis = []
        product_final = []
        type1 = []
        # print(detailed)
        if detailed == True:

            if len(branch_ids) == 1:
                branch = branch_ids[0]
                branch_filter = "and si.branch_id = " + str(branch) + " "
            else:
                branch = tuple(branch_ids)
                branch_filter = "and si.branch_id in " + str(branch) + " "

            # print(len(branch),'brancg')
            if 'p_rate' in self.env['stock.inventory.line']._fields:
                self.env.cr.execute(
                    """select si.seq,si.id,si.date_wo_time,si.adj_type,sil.product_id,sil.product_qty,sil.inventory_id,sil.sales_rate,pt.name from stock_inventory as si  JOIN stock_inventory_line as sil ON (sil.inventory_id=si.id) LEFT JOIN product_product as pp ON (sil.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id)  where  si.date_wo_time<='""" + date_to + """' and si.date_wo_time>='""" + date_from + """' and si.adj_type='issue'  order by  si.date_wo_time""")
                kt = 'False'
            else:
                self.env.cr.execute(
                    """select si.seq,si.id,si.date_wo_time,si.adj_type,sil.product_id,sil.product_qty,sil.inventory_id,pt.name from stock_inventory as si  JOIN stock_inventory_line as sil ON (sil.inventory_id=si.id) LEFT JOIN product_product as pp ON (sil.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id)  where  si.date_wo_time<='""" + date_to + """' and si.date_wo_time>='""" + date_from + """' and si.adj_type='issue' order by  si.date_wo_time""")
                # print("else")
                kt = 'True'
            for dt in self.env.cr.dictfetchall():
                # print(dt)
                sales_rate = dt.get('sales_rate', 0)
                # sales_rate = dt['sales_rate']
                product_qty = dt['product_qty']
                amount = sales_rate * product_qty
                # print(amount)
                docs.append({
                    'id': dt['id'],

                    'v_no': dt['seq'],

                    'date': dt['date_wo_time'].strftime("%d/%m/%Y"),

                    'product_name': dt['name'],

                    'product_qty': dt['product_qty'],
                    'sales_rate': dt.get('sales_rate', 0),
                    # 'branch_ids': dt['branch_ids'],
                    'amount': amount,

                })
                # print(docs)
            if len(docs) > 0:
                uid = docs[0]['id']
                total_amount = 0
                # branch = docs[0]['branch_id']
                total_qty = 0
                i = 0

                product_final.append({'name': 8,
                                      'product_name': None,
                                      'date': None,
                                      'invoice_no': None,
                                      'branch_name': None,
                                      'customer': None,
                                      'description': None,
                                      'hsn_code': None,
                                      'product_qty': None,
                                      'product_uom_id': None,
                                      'price_unit': None,
                                      'tax': None,
                                      'price_total': None,
                                      'product_uom_id': None,
                                      'cost': None,
                                      'amount': None,
                                      })

                product_final.append({'name': 5,
                                      'product_name': docs[0]['v_no'],

                                      'date': docs[0]['date'],
                                      'transfer': None,
                                      'branch_name': None,
                                      'invoice_no': None,
                                      'branch_name': None,
                                      'customer': None,
                                      'description': None,
                                      'hsn_code': None,
                                      'product_qty': None,
                                      'product_uom_id': None,
                                      'price_unit': None,
                                      'tax': None,
                                      'price_total': None,
                                      'product_uom_id': None,
                                      'cost': None,
                                      'amount': None,
                                      })
                # print(docs[0])
                while (i < len(docs)):
                    # if (branch == docs[i]['branch_id']):
                    if (uid == docs[i]['id']):
                        product_id = docs[i]['id']
                        # pid = docs[i]['pid']
                        name = docs[i]['v_no']
                        name2 = name
                        total_qty = total_qty + docs[i].get('amount', 0)
                        product_final.append({'name': 4,
                                              'product_name': docs[i]['product_name'],
                                              'date': docs[i]['date'],
                                              'product_uom_id': docs[i].get('product_uom_id', 0),
                                              'p_rate': docs[i].get('p_rate', 0),
                                              'sales_rate': docs[i].get('sales_rate', 0),
                                              # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                                              # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                                              'product_uom_id': docs[i].get('product_uom_id', 0),
                                              'amount': docs[i].get('amount', 0),

                                              'branch_name': None,
                                              'product_qty': round(docs[i]['product_qty'], 3),
                                              })

                    else:

                        product_final.append({'name': 1,
                                              'product_name': None,
                                              'date': None,
                                              # 'invoice_no': None,
                                              'branch_name': None,
                                              # 'customer': None,
                                              # 'description': None,
                                              'hsn_code': None,
                                              'product_qty': total_qty,
                                              'product_uom_id': None,
                                              'cost': None,
                                              # 'price_unit': None,
                                              # 'tax': None,
                                              # 'price_total': round(total_amount, 3),
                                              })

                        product_final_lis = product_final_lis + product_final
                        total_amount = 0

                        total_qty = 0
                        product_final = []
                        # pid = docs[i]['pid']
                        uid = docs[i]['id']

                        product_final.append({'name': 5,
                                              'product_name': docs[i]['v_no'],
                                              'date': docs[i]['date'],
                                              'branch_name': None,
                                              'product_qty': None,
                                              'product_uom_id': None,
                                              'p_rate': None,
                                              'sales_rate': None,
                                              # 'sales_disc_r': None,
                                              # 'sales_disc_w': None,
                                              'product_uom_id': None,
                                              'amount': None,

                                              })
                        product_final.append({'name': 4,
                                              'product_name': docs[i]['product_name'],
                                              'date': docs[i]['date'],
                                              'branch_name': None,
                                              'product_qty': round(docs[i]['product_qty'], 3),
                                              'product_uom_id': docs[i].get('product_uom_id', 0),
                                              'p_rate': docs[i].get('p_rate', 0),
                                              'sales_rate': docs[i].get('sales_rate', 0),
                                              # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                                              # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                                              'product_uom_id': docs[i].get('product_uom_id', 0),
                                              'amount': docs[i].get('amount', 0),

                                              })

                        product_id = docs[i]['id']
                        product_name = docs[i]['v_no']
                        total_qty = total_qty + docs[i].get('amount', 0)

                    # else:
                    #     product_final.append({'name': 1,
                    #                           'product_name': None,
                    #
                    #                           'date': None,
                    #                           # 'invoice_no': None,
                    #                           'branch_name': None,
                    #                           # 'customer': None,
                    #                           # 'description': None,
                    #                           'hsn_code': None,
                    #                           'product_qty': total_qty,
                    #                           # 'product_qty': total_qty,
                    #                           'product_uom_id': None,
                    #                           'cost': None,
                    #                           # 'price_unit': None,
                    #                           # 'tax': None,
                    #                           # 'price_total': round(total_amount, 3),
                    #                           })
                    #     # product_final.append({'name': 10,
                    #     #                       'product_name': None,
                    #     #                       'date': None,
                    #     #                       # 'invoice_no': None,
                    #     #                       'branch_name': None,
                    #     #                       # 'customer': None,
                    #     #                       # 'description': None,
                    #     #                       'hsn_code': None,
                    #     #                       # 'product_qty': branch_qty,
                    #     #                       'product_uom_id': None,
                    #     #                       'cost': None,
                    #     #                       # 'price_unit': None,
                    #     #                       # 'tax': None,
                    #     #                       # 'price_total': round(branch_total, 3),
                    #     #                       })
                    #     # branch = docs[i]['branch_id']
                    #     uid = docs[i]['id']
                    #     total_qty = 0
                    #
                    #     # product_final.append({'name': 8,
                    #     #                       'product_name': None,
                    #     #                       'date': None,
                    #     #
                    #     #                       'hsn_code': None,
                    #     #                       'product_qty': None,
                    #     #                       'product_uom_id': None,
                    #     #                       'cost': None,
                    #     #                       # 'price_unit': None,
                    #     #                       # 'tax': None,
                    #     #                       # 'price_total': None,
                    #     #                       })
                    #
                    #     product_final.append({'name': 5,
                    #                           'product_name': docs[i]['v_no'],
                    #
                    #                           'date': docs[i]['date'],
                    #
                    #                           })
                    #     if (uid == docs[i]['id']):
                    #         product_id = docs[i]['id']
                    #         # pid = docs[i]['pid']
                    #         # name = docs[i]['name']
                    #         name2 = name
                    #         total_qty = total_qty + docs[i].get('amount', 0)
                    #         product_final.append({'name': 4,
                    #                               'product_name': docs[i]['v_no'],
                    #
                    #                               'date': docs[i]['date'],
                    #                               'branch_name': None,
                    #                               'product_qty': round(docs[i]['product_qty'], 3),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'p_rate': docs[i].get('p_rate', 0),
                    #                               'sales_rate': docs[i].get('sales_rate', 0),
                    #                               # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                    #                               # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'amount': docs[i].get('amount', 0),
                    #
                    #                               })
                    #
                    #     else:
                    #
                    #         product_final.append({'name': 1,
                    #                               'product_name': None,
                    #
                    #                               'date': None,
                    #                               # 'invoice_no': None,
                    #                               'branch_name': None,
                    #                               # 'customer': None,
                    #                               # 'description': None,
                    #                               'hsn_code': None,
                    #                               # 'product_qty': total_qty,
                    #                               'product_uom_id': None,
                    #                               'cost': None,
                    #                               'product_qty': total_qty,
                    #                               # 'price_unit': None,
                    #                               # 'tax': None,
                    #                               # 'price_total': round(total_amount, 3),
                    #                               })
                    #
                    #         total_amount = 0
                    #
                    #         total_qty = 0
                    #         product_final = []
                    #         # pid = docs[i]['pid']
                    #         uid = docs[i]['id']
                    #
                    #         product_final.append({'name': 5,
                    #                               'product_name': docs[i]['name'],
                    #
                    #                               'date': docs[i]['date'],
                    #                               # 'product_id': docs[i]['name'],
                    #                               'branch_name': None,
                    #                               'product_qty': None,
                    #                               'product_uom_id': None,
                    #                               'p_rate': None,
                    #                               'sales_rate': None,
                    #                               # 'sales_disc_r': None,
                    #                               # 'sales_disc_w': None,
                    #                               'product_uom_id': None,
                    #                               'amount': None,
                    #
                    #                               })
                    #         product_final.append({'name': 4,
                    #                               'product_name': docs[i]['name'],
                    #
                    #                               'date': docs[i]['date'],
                    #                               'branch_name': None,
                    #                               'product_qty': round(docs[i]['product_qty'], 3),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'p_rate': docs[i].get('p_rate', 0),
                    #                               'sales_rate': docs[i].get('sales_rate', 0),
                    #                               # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                    #                               # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'amount': docs[i].get('amount', 0),
                    #
                    #                               })
                    #
                    #         product_id = docs[i]['id']
                    #         product_name = docs[i]['name']
                    #         total_qty = total_qty + docs[i].get('amount', 0)

                    i = i + 1

                product_final.append({'name': 1,
                                      'product_name': 'Total',
                                      'date': None,
                                      # 'invoice_no': None,
                                      'branch_name': None,
                                      # 'customer': None,
                                      # 'description': None,
                                      'hsn_code': None,
                                      'product_qty': round(total_qty, 3),
                                      'product_uom_id': None,
                                      'cost': None,
                                      # 'price_unit': None,
                                      # 'tax': None,
                                      # 'price_total': round(total_amount, 3),
                                      })
                product_final.append({'name': 10,
                                      'product_name': None,
                                      'product_id': None,
                                      'date': None,
                                      # 'invoice_no': None,
                                      'branch_name': None,
                                      # 'customer': None,
                                      # 'description': None,
                                      'hsn_code': None,
                                      # 'product_qty': branch_qty,
                                      'product_uom_id': None,
                                      'cost': None,
                                      # 'price_unit': None,
                                      # 'tax': None,
                                      # 'price_total': round(branch_total, 3),
                                      })
                product_final_lis = product_final_lis + product_final
                # print(product_final_lis)
            return {
                'branch': True,
                'docsnn': product_final_lis,
                'type': kt,
            }

        if receipt == True:
            # print(receipt, 'receipt')
            # if branch_ids:
            # for branch in branch_ids:
            if len(branch_ids) == 1:
                branch = branch_ids[0]
                branch_filter = "and si.branch_id = " + str(branch) + " "
            else:
                branch = tuple(branch_ids)
                branch_filter = "and si.branch_id in " + str(branch) + " "

            # branch = str(branch_ids[0])
            if 'p_rate' in self.env['stock.inventory.line']._fields:
                self.env.cr.execute(
                    """select si.seq,si.id,si.date_wo_time,si.adj_type,si.state,sil.product_id,sil.product_qty,sil.inventory_id,sil.prod_lot_id as lot_name,sil.p_rate,sil.sales_rate,sil.product_uom_id,uu.name as uom,pt.name as product_name from stock_inventory as si LEFT JOIN stock_inventory_line as sil ON (sil.inventory_id=si.id) LEFT JOIN product_product as pp ON (sil.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id) LEFT JOIN uom_uom as uu ON (uu.id=sil.product_uom_id)  where  si.date_wo_time<='""" + date_to + """' and si.date_wo_time>='""" + date_from + """' and si.adj_type='receipt' and si.state='done'  order by  si.date_wo_time""")
                kt = 'False'
            else:
                self.env.cr.execute(
                    """select si.seq,si.id,si.date_wo_time,si.adj_type,si.state,sil.product_id,sil.product_qty,sil.inventory_id,pt.name as product_name from stock_inventory as si  JOIN stock_inventory_line as sil ON (sil.inventory_id=si.id) LEFT JOIN product_product as pp ON (sil.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id)  where  si.date_wo_time<='""" + date_to + """' and si.date_wo_time>='""" + date_from + """' and si.adj_type='receipt' and si.state='done'  order by  si.date_wo_time""")
                kt = 'True'
                # print("""select si.seq,si.id,si.date_wo_time,si.branch_id,si.adj_type,si.state,sil.product_id,sil.product_qty,sil.inventory_id,pt.name from stock_inventory as si  JOIN stock_inventory_line as sil ON (sil.inventory_id=si.id) LEFT JOIN product_product as pp ON (sil.product_id = pp.id) LEFT JOIN product_template as pt ON (pp.product_tmpl_id=pt.id)  where  si.date_wo_time<='""" + date_to + """' and si.date_wo_time>='""" + date_from + """' and si.adj_type='receipt' and si.state='done' """+branch_filter+""" order by  si.date_wo_time""")
            for dt in self.env.cr.dictfetchall():
                # print(dt)
                sales_rate = dt.get('sales_rate', 0)
                product_qty = dt['product_qty']
                amount = sales_rate * product_qty
                docs.append({
                    'id': dt['id'],

                    'v_no': dt['seq'],

                    'date': dt['date_wo_time'].strftime("%d/%m/%Y"),
                    'product_name': dt['product_name'],

                    'product_id': dt['product_id'],

                    'product_qty': dt['product_qty'],
                    # 'branch_id': dt['branch_id'],
                    'lot': dt.get('lot_name'),
                    'p_rate': dt.get('p_rate', 0),
                    'sales_rate': dt.get('sales_rate', 0),
                    # 'sales_disc_r': dt.get('sales_disc_r', 0),
                    # 'sales_disc_w': dt.get('sales_disc_w', 0),
                    'uom': dt.get('uom'),
                    'amount': amount,

                })
                # print(docs)
            if len(docs) > 0:
                uid = docs[0]['id']

                # branch = docs[0]['branch_id']
                total_qty = 0
                i = 0

                product_final.append({'name': 8,
                                      'product_name': None,
                                      'product_id': None,
                                      'date': None,
                                      'invoice_no': None,
                                      'branch_name': None,
                                      'customer': None,
                                      'description': None,
                                      'hsn_code': None,
                                      'product_qty': None,
                                      'uom': None,
                                      'price_unit': None,
                                      'tax': None,
                                      'price_total': None,
                                      'uom': None,
                                      'cost': None,
                                      'amount': None,
                                      })

                product_final.append({'name': 5,
                                      'product_name': docs[0]['v_no'],
                                      'product_id': docs[0]['product_name'],
                                      'date': docs[0]['date'],
                                      'transfer': None,
                                      'branch_name': None,
                                      'invoice_no': None,
                                      'branch_name': None,
                                      'customer': None,
                                      'description': None,
                                      'hsn_code': None,
                                      'product_qty': None,
                                      'product_uom_id': None,
                                      'price_unit': None,
                                      'tax': None,
                                      'price_total': None,
                                      'product_uom_id': None,
                                      'cost': None,
                                      'amount': None,
                                      })
                # print(docs[0])
                while (i < len(docs)):
                    if (uid == docs[i]['id']):
                        product_id = docs[i]['id']
                        # pid = docs[i]['pid']
                        name = docs[i]['v_no']
                        name2 = name
                        total_qty = total_qty + docs[i].get('amount', 0)
                        product_final.append({'name': 4,
                                              'product_name': docs[i]['product_name'],
                                              'product_id': docs[i]['product_id'],
                                              'date': docs[i]['date'],
                                              'lot': docs[i].get('lot', 0),
                                              'p_rate': docs[i].get('p_rate', 0),
                                              'sales_rate': docs[i].get('sales_rate', 0),
                                              # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                                              # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                                              'uom': docs[i].get('uom', 0),
                                              'amount': docs[i].get('amount', 0),

                                              'branch_name': None,
                                              'product_qty': round(docs[i]['product_qty'], 3),
                                              })

                    else:

                        product_final.append({'name': 1,
                                              'product_name': None,
                                              'product_id':None,
                                              'date': None,
                                              # 'invoice_no': None,
                                              'branch_name': None,
                                              # 'customer': None,
                                              # 'description': None,
                                              'hsn_code': None,
                                              'product_qty': total_qty,
                                              'uom': None,
                                              'cost': None,
                                              # 'price_unit': None,
                                              # 'tax': None,
                                              # 'price_total': round(total_amount, 3),
                                              })

                        product_final_lis = product_final_lis + product_final
                        total_amount = 0

                        total_qty = 0
                        product_final = []
                        # pid = docs[i]['pid']
                        uid = docs[i]['id']

                        product_final.append({'name': 5,
                                              'product_name': docs[i]['v_no'],
                                              'product_id': docs[i]['v_no'],
                                              'date': docs[i]['date'],
                                              'branch_name': None,
                                              'product_qty': None,
                                              'lot': None,
                                              'p_rate': None,
                                              'sales_rate': None,
                                              # 'sales_disc_r': None,
                                              # 'sales_disc_w': None,
                                              'uom': None,
                                              'amount': None,

                                              })
                        product_final.append({'name': 4,
                                              'product_name': docs[i]['product_name'],
                                              'product_id': docs[i]['product_name'],
                                              'date': docs[i]['date'],
                                              'branch_name': None,
                                              'product_qty': round(docs[i]['product_qty'], 3),
                                              'lot': docs[i].get('lot', 0),
                                              'p_rate': docs[i].get('p_rate', 0),
                                              'sales_rate': docs[i].get('sales_rate', 0),
                                              # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                                              # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                                              'uom': docs[i].get('uom', 0),
                                              'amount': docs[i].get('amount', 0),

                                              })

                        product_id = docs[i]['id']
                        product_name = docs[i]['v_no']
                        total_qty = total_qty + docs[i].get('amount', 0)

                    # else:
                    #     product_final.append({'name': 1,
                    #                           'product_name': None,
                    #                           'product_id': None,
                    #                           'date': None,
                    #                           # 'invoice_no': None,
                    #                           'branch_name': None,
                    #                           # 'customer': None,
                    #                           # 'description': None,
                    #                           'hsn_code': None,
                    #                           'product_qty': total_qty,
                    #                           # 'product_qty': total_qty,
                    #                           'product_uom_id': None,
                    #                           'cost': None,
                    #                           # 'price_unit': None,
                    #                           # 'tax': None,
                    #                           # 'price_total': round(total_amount, 3),
                    #                           })
                    #     # product_final.append({'name': 10,
                    #     #                       'product_id': None,
                    #     #                       'date': None,
                    #     #                       # 'invoice_no': None,
                    #     #                       'branch_name': None,
                    #     #                       # 'customer': None,
                    #     #                       # 'description': None,
                    #     #                       'hsn_code': None,
                    #     #                       # 'product_qty': branch_qty,
                    #     #                       'product_uom_id': None,
                    #     #                       'cost': None,
                    #     #                       # 'price_unit': None,
                    #     #                       # 'tax': None,
                    #     #                       # 'price_total': round(branch_total, 3),
                    #     #                       })
                    #     branch = docs[i]['branch_id']
                    #     uid = docs[i]['id']
                    #     total_qty = 0
                    #
                    #     # product_final.append({'name': 8,
                    #     #                       'product_id': None,
                    #     #                       'date': None,
                    #     #
                    #     #                       'hsn_code': None,
                    #     #                       'product_qty': None,
                    #     #                       'product_uom_id': None,
                    #     #                       'cost': None,
                    #     #                       # 'price_unit': None,
                    #     #                       # 'tax': None,
                    #     #                       # 'price_total': None,
                    #     #                       })
                    #
                    #     product_final.append({'name': 5,
                    #                           'product_name': docs[i]['v_no'],
                    #                           'product_id': docs[i]['name'],
                    #                           'date': docs[i]['date'],
                    #
                    #                           })
                    #     if (uid == docs[i]['id']):
                    #         product_id = docs[i]['id']
                    #         # pid = docs[i]['pid']
                    #         # name = docs[i]['name']
                    #         name2 = name
                    #         total_qty = total_qty + docs[i].get('amount', 0)
                    #         product_final.append({'name': 4,
                    #                               'product_name': docs[i]['product_name'],
                    #                               'product_id': docs[i]['product_name'],
                    #                               'date': docs[i]['date'],
                    #                               'branch_name': None,
                    #                               'product_qty': round(docs[i]['product_qty'], 3),
                    #                               'lot': docs[i].get('lot', 0),
                    #                               'p_rate': docs[i].get('p_rate', 0),
                    #                               'sales_rate': docs[i].get('sales_rate', 0),
                    #                               # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                    #                               # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'amount': docs[i].get('amount', 0),
                    #
                    #                               })
                    #
                    #     else:
                    #
                    #         product_final.append({'name': 1,
                    #                               'product_name': None,
                    #                               'product_id':None,
                    #                               'date': None,
                    #                               # 'invoice_no': None,
                    #                               'branch_name': None,
                    #                               # 'customer': None,
                    #                               # 'description': None,
                    #                               'hsn_code': None,
                    #                               # 'product_qty': total_qty,
                    #                               'product_uom_id': None,
                    #                               'cost': None,
                    #                               'product_qty': total_qty,
                    #                               # 'price_unit': None,
                    #                               # 'tax': None,
                    #                               # 'price_total': round(total_amount, 3),
                    #                               })
                    #
                    #         total_amount = 0
                    #
                    #         total_qty = 0
                    #         product_final = []
                    #         # pid = docs[i]['pid']
                    #         uid = docs[i]['id']
                    #
                    #         product_final.append({'name': 5,
                    #                               'product_name': docs[i]['v_no'],
                    #                               'product_id': docs[i]['name'],
                    #                               'date': docs[i]['date'],
                    #                               'product_id': docs[i]['name'],
                    #
                    #                               'branch_name': None,
                    #                               'product_qty': None,
                    #                               'lot': None,
                    #                               'p_rate': None,
                    #                               'sales_rate': None,
                    #                               # 'sales_disc_r': None,
                    #                               # 'sales_disc_w': None,
                    #                               'product_uom_id': None,
                    #                               'amount': None,
                    #
                    #                               })
                    #         product_final.append({'name': 4,
                    #                               'product_name': docs[i]['product_name'],
                    #                               'product_id': docs[i]['name'],
                    #                               'date': docs[i]['date'],
                    #                               'branch_name': None,
                    #                               'product_qty': round(docs[i]['product_qty'], 3),
                    #                               'lot': docs[i].get('lot', 0),
                    #                               'p_rate': docs[i].get('p_rate', 0),
                    #                               'sales_rate': docs[i].get('sales_rate', 0),
                    #                               # 'sales_disc_r': docs[i].get('sales_disc_r', 0),
                    #                               # 'sales_disc_w': docs[i].get('sales_disc_w', 0),
                    #                               'product_uom_id': docs[i].get('product_uom_id', 0),
                    #                               'amount': docs[i].get('amount', 0),
                    #
                    #                               })
                    #
                    #         product_id = docs[i]['id']
                    #         product_name = docs[i]['name']
                    #         total_qty = total_qty + docs[i].get('amount', 0)

                    i = i + 1

                product_final.append({'name': 1,
                                      'product_name': 'Total',
                                      'date': None,
                                      # 'invoice_no': None,
                                      'branch_name': None,
                                      # 'customer': None,
                                      # 'description': None,
                                      'hsn_code': None,
                                      # 'product_qty': round(total_qty, 3),
                                      'uom': None,
                                      'cost': None,
                                      'product_qty': round(total_qty, 3),
                                      # 'price_unit': None,
                                      # 'tax': None,
                                      # 'price_total': round(total_amount, 3),
                                      })
                product_final.append({'name': 10,
                                      'product_name': None,
                                      'product_id': None,
                                      'date': None,
                                      # 'invoice_no': None,
                                      'branch_name': None,
                                      # 'customer': None,
                                      # 'description': None,
                                      'hsn_code': None,
                                      # 'product_qty': branch_qty,
                                      'uom': None,
                                      'cost': None,
                                      # 'price_unit': None,
                                      # 'tax': None,
                                      # 'price_total': round(branch_total, 3),
                                      })
                product_final_lis = product_final_lis + product_final
            print(product_final_lis)
            return {
                'branch': True,
                'type': kt,
                'docsnn': product_final_lis,
            }

    def get_html(self):
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'), detailed=self.detailed,
                                    receipt=self.receipt, t_type=self.t_type)
        case = 0

        if res['lines']['date_from'] and res['lines']['date_to']:
            if res['lines']['detailed']:

                case = 1
            else:
                case = 2
            # if res['lines']['t_type'] == 'both':
            #     case = 3
            # if res['lines']['ptype'] == 'selected_product' and res['lines']['detailed']:
            #     if res['lines']['product_ids']:
            #         case = 1
            # if res['lines']['ptype'] == 'selected_product' and not res['lines']['detailed'] and res['lines']['t_type'] != 'both':
            #     case = 2

        self.template_area = self.env.ref('stock_recipt_issue_report.report_stock_receipt_issue')._render(
            {'lines': res['lines']['lines'],
             'date_from':self.date_from.strftime('%d-%m-%Y'),
             'date_to': self.date_to.strftime('%d-%m-%Y'),
             'data': res['lines']['data'],
             'case': case,
             'detailed': self.detailed,
             'receipt': self.receipt,
             # 'ptype': self.ptype,
             't_type': self.t_type,
             # 'product_ids': res['lines']['product_ids'],
             # 'branch_ids': res['lines']['branch_ids'],
             # 'isbranch': res['lines']['isbranch'],
             # 'branch_name': res['lines']['branch_name'],
             })
        # print(res['lines']['product_ids'])
        return res

    def _get_report_data(self, date_from=False, date_to=False, detailed=False,receipt=False,
                         t_type=False ):
        tk = self.env['product.product'].search([], order='name')
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
        # if product_ids:
        #     rp = [int(i) for i in product_ids]

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
            #'ptype': ptype if ptype else False,
            'product_ids': rp if rp else False,
            'detailed': detailed if detailed else False,
            'receipt': receipt if receipt else False,
            'branch_ids': rl if rl else (branch_default.id,),
            'isbranch': is_branch,
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
        return {
            'lines': dat,
            'variants': do,
            'branch': lo,
            'bid': branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }
