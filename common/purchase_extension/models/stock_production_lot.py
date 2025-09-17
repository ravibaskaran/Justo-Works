# ♦ Import ♦
from odoo import models, fields, api


# ♦ ▼ Inherited 'Stock Production Lot'. ▼ ♦
class stockProductionLotInherit(models.Model):
    _inherit = 'stock.production.lot'

    p_rate = fields.Float(string='Purchase Rate', store=True)
    packing = fields.Many2one('uom.uom', string="Packing")
    sales_rate = fields.Float(string="Sales Rate")
    sales_disc = fields.Float(string="Sales Discount")
    mrp = fields.Float(string="Unit Rate")
    expiry = fields.Date(string='Expiry')


    # def name_get(self):
    #     result = []
    #     for lot in self:
    #         result.append((lot.id, lot.name))
    #     return result

    @api.model_create_multi
    def create(self, vals_list):
        res = super(stockProductionLotInherit, self).create(vals_list)
        for lot in res:
            packing = lot.packing
            if lot.product_id.uom_id.id != packing.id:
                mrp = lot.sales_rate * packing.factor
                lot.mrp = float(mrp)
            else:
                lot.mrp = lot.sales_rate
        return res




