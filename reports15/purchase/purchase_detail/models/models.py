# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


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
        res['date_from'] = today
        res['date_to'] = today
        return res

    def get_html(self):
        if self.date_from > self.date_to:
            raise Warning('From date should be less than to date')
        res = self._get_report_data()
        self.template_area = self.env.ref('purchase_detail.report_purchase_detail')._render({
            'table': res,
            'date_start': self.date_from,
            'date_end': self.date_to,
            'transaction_type': dict(self._fields['transaction_type'].selection).get(self.transaction_type),
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
                    <th class="text-center" style="width: 10%">Uom</th>
                    <th class="text-center" style="width: 10%">Price</th>
                    <th class="text-center" style="width: 14%">Taxable</th>
                    <th class="text-center" style="width: 8%">Tax %</th>
                    <th class="text-center" style="width: 16%">Purchase Value</th>
                </thead>
                <tbody>"""
        domain = [('move_type', '=', self.transaction_type), ('invoice_date', '>=', self.date_from),
                  ('invoice_date', '<=', self.date_to), ('state', 'not in', ('draft', 'cancel'))]
        if self.report_type == 'supplier':
            domain.append(('partner_id', 'in', self.supplier_ids.ids))
        # if self.branch_exist:
        #     domain.append(('branch_id', 'in', self.branch_ids.ids))
        moves = self.env['account.move'].search(domain, order='name')
        grand_purchase_value = 0
        for move in moves:
            table += """
                <tr>
                    <td class="font-italic text-center font-weight-bold"><span>""" + str(move.name) + "</span><br/><span style='font-size: 11px;'>" + str(move.invoice_date.strftime('%d/%m/%Y')) + """</span></td>
                    <td class="font-weight-bold font-italic" colspan='14'>""" + str(move.partner_id.name) + ' (' + str(move.ref if move.ref else '') + '-' + str(move.bill_date.strftime('%d/%m/%Y') if move.bill_date else '') + ')' + """</td>
                </tr>
            """
            total_purchase_value = 0
            for line in move.invoice_line_ids:
                purchase_value = (line.quantity * line.price_unit) + ((line.quantity * line.price_unit) * sum(line.tax_ids.mapped('amount')) / 100)
                table += """
                        <tr>
                            <td/>
                            <td>""" + str(line.product_id.name) + """</td>
                            <td class="text-right">""" + str("{:,.2f}".format(line.quantity)) + """</td>
                            <td class="text-center">""" + str(line.product_uom_id.name) + """</td>
                            <td class="text-right">""" + str("{:,.2f}".format(line.price_unit)) + """</td>
                            <td class="text-right">""" + str("{:,.2f}".format(line.price_subtotal)) + """</td>
                            <td class="text-right">""" + str("{:,.2f}".format(sum(line.tax_ids.mapped('amount')))) + """</td>
                            <td class="text-right">""" + str("{:,.2f}".format(purchase_value)) + """</td>
                        </tr>
                    """
                total_purchase_value += purchase_value
            table += """
                <tr class="font-weight-bold">
                    <td/>
                    <td class="font-italic">Bill Value/Mrp Value</td>
                    <td colspan="5"/>
                    <td class="text-right">""" + str("{:,.2f}".format(total_purchase_value)) + """</td>
                </tr>
            """
            grand_purchase_value += total_purchase_value
        table += """
            <tr class="font-weight-bold">
                <td/>
                <td class="font-italic" style="padding-top: .5rem !important; padding-bottom: .5rem !important;"><span>Grand Total</span></td>
                <td colspan="5"/>
                <td class="text-right" style="padding-top: .5rem !important; padding-bottom: .5rem !important;">""" + str("{:,.2f}".format(grand_purchase_value)) + """</td>
            </tr>
        """
        return table
