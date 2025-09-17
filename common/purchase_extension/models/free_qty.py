# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    free_qty = fields.Float("Free Qty", digits='Product Unit of Measure')
    # replace_qty = fields.Float("Replace Qty", digits='Product Unit of Measure')

    def _create_stock_moves_inx(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            if not line.exclude_from_invoice_tab:
                price_unit = line.price_unit
                qty = line.quantity + line.free_qty
                template = {
                    'name': line.name or '',
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'product_uom_qty': qty,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'picking_id': picking.id,
                    'state': 'draft',
                    'company_id': line.move_id.company_id.id,
                    'price_unit': price_unit,
                    'picking_type_id': picking.picking_type_id.id,
                    'route_ids': 1 and [ (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                    'warehouse_id': picking.picking_type_id.warehouse_id.id,
                    'inv_line_id': line.id,
                }
                if line.move_id.direct_move_type == 'incoming' and line.move_id.move_type == 'in_invoice' or ( line.move_id.direct_move_type == 'outgoing' and line.move_id.move_type == 'out_refund'):
                    template['move_line_nosuggest_ids'] = [(0, 0, {
                        'product_id': line.product_id.id,
                        'lot_name': line.lot_name,
                        'lot_id': line.lot_id.id if line.lot_id else False,
                        'product_uom_qty': qty,
                        'product_uom_id': line.product_uom_id.id,
                        'location_id': picking.location_id.id,
                        'location_dest_id': picking.location_dest_id.id,
                        'picking_id': picking.id,
                    })]
                create_move_id = moves.create(template)
                line.direct_stock_move_id = create_move_id.id
        return done

    def write(self, vals):
        res = super(AccountMoveLine, self).write(vals)
        if ('free_qty' in vals) and self.direct_stock_move_id:
            self.move_id.direct_move_picking_id.state = 'draft'
            self.direct_stock_move_id.product_uom_qty = self.quantity + self.free_qty
            self.direct_stock_move_id._action_confirm()
            self.direct_stock_move_id._action_assign()
        return res

    # @api.onchange('quantity', 'lot_id', 'product_uom_id', 'free_qty')
    # def check_qty_availability_lot(self):
    #     if self.move_id.direct_move_type and self.product_id.tracking != 'none' and self.move_id.move_type != 'out_refund':
    #         if self.lot_id:
    #             # lines = self.move_id.invoice_line_ids.filtered(
    #             #     lambda l: l.product_id == self.product_id and l.lot_id == self.lot_id)
    #             # qty = sum(lines.mapped('quantity')) + sum(lines.mapped('free_qty')) + sum(lines.mapped('replace_qty'))
    #             qty = self.quantity + self.free_qty
    #             quantity = self.product_uom_id._compute_quantity(qty, self.product_id.uom_id)
    #             if self.lot_id.direct_sellable_qty < quantity:
    #                 return {
    #                     'warning': {'title': _('Not enough stock'),
    #                                 'message': _("Not enough stock"), },
    #                 }
        # if self.move_id.direct_move_type and self.product_id.type == 'product' and self.move_id.type not in [
        #     'in_invoice', 'out_refund']:
        #     qty = self.quantity + self.free_qty
        #     quantity = self.product_uom_id._compute_quantity(qty, self.product_id.uom_id)
        #     if self.product_id.sudo().qty_available < quantity:
        #         return {
        #             'warning': {'title': _('Not enough stock'),
        #                         'message': _("Not enough stock"), },
        #         }


# class AccountMove(models.Model):
#     _inherit = 'account.move'

    # def check_qty_lot_custom(self):
    #     if self.direct_move_type and self.type != 'out_refund':
    #         for line in self.invoice_line_ids:
    #             if line.lot_id and line.product_tracking != 'none':
    #                 lines = self.invoice_line_ids.filtered(
    #                     lambda l: l.product_id == line.product_id and l.lot_id == line.lot_id)
    #                 qty = sum(lines.mapped('quantity')) + sum(lines.mapped('free_qty'))
    #                 quantity = line.product_uom_id._compute_quantity(qty, line.product_id.uom_id)
    #                 if line.lot_id.direct_sellable_qty < quantity:
    #                     raise Warning(_('%s has no enough stock %s') % (line.product_id.name, line.lot_id.name))
    #
    #     if self.direct_move_type and self.move_type not in ['in_invoice', 'out_refund']:
    #         for line in self.invoice_line_ids:
    #             if line.product_id.type == 'product':
    #                 lines = self.invoice_line_ids.filtered(
    #                     lambda l: l.product_id == line.product_id)
    #                 qty = sum(lines.mapped('quantity')) + sum(lines.mapped('free_qty'))
    #                 quantity = line.product_uom_id._compute_quantity(qty, line.product_id.uom_id)
    #                 if line.product_id.sudo().qty_available < quantity:
    #                     raise Warning( _('%s has no enough stock') % (line.product_id.name))
