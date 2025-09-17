# -*- coding: utf-8 -*-

from odoo import models, fields, api

#


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    sales_rate = fields.Float(string="Sales Rate")
    packing = fields.Many2one('uom.uom', string="UOM")
    mrp = fields.Float(string="Sales Rate")
    branch_qty_compute = fields.Float(compute="_compute_branch_sellable_qty")

    def _compute_branch_sellable_qty(self):
        branch = self.env.user.branch_id.id
        location = self.env['stock.warehouse'].search(
            [('branch_id', '=', branch)], limit=1).lot_stock_id.id
        for lot in self:
            qty = 0
            quants = lot.quant_ids.filtered(
                lambda l: l.location_id.id == location and l.quantity > 0 and l.lot_id.id == lot.id)
            for quant in quants:
                qty += (quant.quantity - quant.reserved_quantity)
            lot.branch_qty_compute = qty

    def name_get(self):
        result = []
        if self._context.get('show_qty'):
            for lot in self:
                name = lot.name + " - Stock - " + \
                                    "{0:,.2f}".format(lot.branch_qty_compute) + \
                                " " + lot.product_uom_id.name
                result.append((lot.id, name))
        else:
            result = super(StockProductionLot, self).name_get()
        return result

    @api.model_create_multi
    def create(self, vals_list):
        res = super(StockProductionLot, self).create(vals_list)
        for lot in res:
            packing = lot.packing
            if lot.product_id.uom_id.id != packing.id:
                mrp = lot.sales_rate * packing.factor
                lot.mrp = float(mrp)
            else:
                lot.mrp = lot.sales_rate
        return res
