# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import Warning


class BetaPurchaseDetail(models.TransientModel):  # change this
    _name = 'beta.purchase.detail'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Purchase Detail')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    transaction_type = fields.Selection([('in_invoice', 'Purchase'), ('in_refund', 'Purchase Return')], 'Transaction',
                                        default='in_invoice')
    report_type = fields.Selection([('all', 'All Supplier'), ('supplier', 'Selected Supplier')], 'Type',
                                   default='all')
    supplier_ids = fields.Many2many('res.partner', string='Suppliers', domain=[('supplier_rank', '>', 0)])
    @api.model
    def default_get(self, fields_list):
        res = super(BetaPurchaseDetail, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    def get_html(self):
        if self.date_from > self.date_to:
            raise Warning('From date should be less than to date')
        res = self._get_report_data()
        self.template_area = self.env.ref('beta_purchase_detail.report_beta_purchase_detail')._render({
            'table': res,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'transaction_type': dict(self._fields['transaction_type'].selection).get(self.transaction_type),
            #'branch_names': ', '.join(self.branch_ids.mapped('name'))
        })

    def _get_report_data(self):
        table = """<table id="tableId" rules="groups" frame="hsides" border="1"
                   class="table table-bordered table-striped"
                   style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px;">
                <style>.table td{ padding: .8px !important;}</style>
                <thead>
                    <th class="text-center" style="width: 17%">Vr.No</th>
                    <th class="text-center" style="width: 35%">Product Name</th>
                    <th class="text-center" style="width: 10%">Qty</th>
                    <th class="text-center" style="width: 8%">Batch</th>
                    <th class="text-center" style="width: 10%">Uom</th>
                    <th class="text-center" style="width: 10%">Price</th>
                    <th class="text-center" style="width: 10%">Rate</th>
                    <th class="text-center" style="width: 11%">Disc %</th>
                    <th class="text-center" style="width: 10%">Disc Amt</th>
                    <th class="text-center" style="width: 14%">Taxable</th>
                    <th class="text-center" style="width: 8%">Tax %</th>
                    <th class="text-center" style="width: 16%">Purchase Value</th>
                    <th class="text-center" style="width: 14%">Sales Value</th>
                </thead>
                <tbody>"""
        domain = [('move_type', '=', self.transaction_type), ('invoice_date', '>=', self.date_from),
                  ('invoice_date', '<=', self.date_to), ('state', 'not in', ('draft', 'cancel'))]
        if 'expiry_type' in self.env['account.move']._fields:
            domain.append(('expiry_type', 'not in', ['expiry_rtn', 'expiry_rpl']))

        if self.report_type == 'supplier':
            domain.append(('partner_id', 'in', self.supplier_ids.ids))
        #if self.branch_exist:
            #domain.append(('branch_id', 'in', self.branch_ids.ids))
        moves = self.env['account.move'].search(domain, order='name')
        grand_sales_value = 0
        grand_purchase_value = 0
        for move in moves:
            table += """
                <tr>
                    <td class=" text-center font-weight-bold"><span>""" + str(move.name) + "</span><br/><span style='font-size: 11px;'>" + str(move.invoice_date.strftime('%d/%m/%Y')) + """</span></td>
                    <td class="font-weight-bold " colspan='14'>""" + str(move.partner_id.name) + ' (' + str(move.name) + '-' + str(move.invoice_date.strftime('%d/%m/%Y')) + ')' + """</td>
                </tr>
            """
            total_sales_value = 0
            total_purchase_value = 0

            for line in move.invoice_line_ids:
                # sales_rate = 0
                # sales_disc=0
                # lot_name=""
                discount_amt=line.price_subtotal*line.discount/100
                purchase_value = (line.quantity * line.price_unit) + ((line.quantity * line.price_unit) * sum(line.tax_ids.mapped('amount')) / 100)
                if self.transaction_type=='in_invoice':
                    table += """
                            <tr>
                                <td/>
                                <td>""" + str(line.product_id.name) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.quantity)) + """</td>
                                <td class="text-center">""" + str(line.lot_name) + """</td>
                                <td class="text-center">""" + str(line.product_uom_id.name) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.price_unit)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.product_id.list_price)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.discount)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(discount_amt)) + """</td> 
                                <td class="text-right">""" + str("{:,.2f}".format(line.price_subtotal)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(sum(line.tax_ids.mapped('amount')))) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(purchase_value)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.quantity * line.product_id.list_price)) + """</td>
                            </tr>
                        """
                else:table += """
                            <tr>
                                <td/>
                                <td>""" + str(line.product_id.name) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.quantity)) + """</td>
                                <td class="text-center">""" + str(line.lot_id.name) + """</td>
                                <td class="text-center">""" + str(line.product_uom_id.name) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.price_unit)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.product_id.list_price)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.discount)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(discount_amt)) + """</td> 
                                <td class="text-right">""" + str("{:,.2f}".format(line.price_subtotal)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(sum(line.tax_ids.mapped('amount')))) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(purchase_value)) + """</td>
                                <td class="text-right">""" + str("{:,.2f}".format(line.quantity * line.product_id.list_price)) + """</td>
                            </tr>
                        """
                total_sales_value += line.quantity * line.product_id.list_price
                total_purchase_value += purchase_value
            table += """
                <tr class="font-weight-bold">
                    <td/>
                    <td >Bill Value/Mrp Value</td>
                    <td colspan="8"/>
                    <td/>
                    <td class="text-right">""" + str("{:,.2f}".format(total_purchase_value)) + """</td>
                    <td class="text-right">""" + str("{:,.2f}".format(total_sales_value)) + """</td>
                </tr>
            """
            grand_sales_value += total_sales_value
            grand_purchase_value += total_purchase_value
        table += """
            <tr class=" text-center font-weight-bold" style='font-size: 15px;'>
                <td/>
                <td  style="padding-top: .5rem !important; padding-bottom: .5rem !important;"><span  style='font-size: 15px;'>Grand Total</span></td>
                <td colspan="8"/>
                <td/>
                <td class="text-right" style="padding-top: .5rem !important; padding-bottom: .5rem !important;><span style='font-size: 18px;'">""" + str("{:,.2f}".format(grand_purchase_value)) + """</td>
                <td class="text-right" style="padding-top: .5rem !important; padding-bottom: .5rem !important;><span style='font-size: 18px;'">""" + str("{:,.2f}".format(grand_sales_value)) + """</td>
            </tr>
        """
        return table
