from odoo import models, fields, api


# ♦ ▼ Inherited 'Stock Picking'. ▼ ♦
class StockPicking(models.Model):
    _inherit = "stock.picking"

    direct_transaction_type = fields.Selection([('sale','Sale'),('purchase','Purchase')])

    @api.depends('move_lines.state', 'move_lines.date')
    def _compute_scheduled_date(self):
        for picking in self:
            if picking.direct_transaction_type:
                pass
            else:
                super(StockPicking, picking)._compute_scheduled_date()

    @api.model
    def create(self, values):
        # Add code here
        print(values,"values")
        return super(StockPicking, self).create(values)

    def action_done(self):
        res = super(StockPicking, self).action_done()
        if self.direct_transaction_type:
            self.date_done = self.env['account.move'].search([('direct_move_picking_id','=',self.id)]).get_direct_move_date()
        return res


# ♦ ▼ Inherited 'Stock Move'. ▼ ♦
class StockMove(models.Model):
    _inherit = "stock.move"

    inv_line_id = fields.Many2one("account.move.line")

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        for move in res:
            if move.inv_line_id:
                move.date = move.inv_line_id.move_id.get_direct_move_date()
        return res

    def write(self, vals):
        if vals.get('date'):
            if self.inv_line_id:
                vals['date'] = self.inv_line_id.move_id.get_direct_move_date()
        res = super(StockMove, self).write(vals)
        return res

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
        if self.inv_line_id and self.inv_line_id.lot_id:
            lot_id = self.inv_line_id.lot_id
        return super()._update_reserved_quantity(need, available_quantity, location_id, lot_id=lot_id,
            package_id=package_id, owner_id=owner_id, strict=strict,)

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant
        )
        if reserved_quant and self.inv_line_id.lot_id:
            vals["lot_id"] = self.inv_line_id.lot_id.id

        return vals
    
    
# ♦ ▼ Inherited 'Stock Move line '. ▼ ♦
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for line in self:
            if line.move_id and line.move_id.inv_line_id:
                line.date = line.move_id.inv_line_id.move_id.get_direct_move_date()
        return res
    

# ♦ ▼ Inherited 'Stock Production Lot'. ▼ ♦
class stockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    direct_sellable_qty = fields.Float(compute="_compute_direct_sellable_qty", store=True)

    @api.depends('product_qty')
    def _compute_direct_sellable_qty(self):
        for lot in self:
            qty = 0
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
            for quant in quants:
                qty += (quant.quantity - quant.reserved_quantity)
            lot.direct_sellable_qty = qty

    def name_get(self):
        result = []
        if self._context.get('show_qty'):
            for lot in self:
                name = lot.name + "/" + "{0:,.2f}".format(lot.direct_sellable_qty) + " " + lot.product_uom_id.name
                result.append((lot.id, name))
        else:
            result = super(stockProductionLot, self).name_get()
        return result