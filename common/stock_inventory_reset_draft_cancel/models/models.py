# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class StockInventoryInherit(models.Model):
    _inherit = 'stock.inventory'

    def action_reset_draft(self):
        if self.adj_type == 'receipt':
            for line in self.line_ids:
                if line.product_id.tracking == 'lot':
                    if line.prod_lot_id.product_qty < line.prod_qty:
                        raise Warning(_('Not enough stock for product %s in lot %s')%(line.product_id.name,line.prod_lot_id.name))
                else:
                    if line.product_id.qty_available < line.prod_qty:
                        raise Warning(_('Not enough stock for product %s')%line.product_id.name)
        self.mapped('move_ids')._action_cancel_custom()
        self.mapped('move_ids').unlink()
        # self.line_ids.unlink()
        # source_location =
        self.write({'state': 'draft'})


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_cancel_custom(self):
        # if any(move.state == 'done' and not move.scrapped for move in self):
        #     raise UserError(_('You cannot cancel a stock move that has been set to \'Done\'.'))
        moves_to_cancel = self.filtered(lambda m: m.state != 'cancel')
        # self cannot contain moves that are either cancelled or done, therefore we can safely
        # unlink all associated move_line_ids
        moves_to_cancel._do_unreserve()

        for move in moves_to_cancel:
            siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
            if move.propagate_cancel:
                # only cancel the next move if all my siblings are also cancelled
                if all(state == 'cancel' for state in siblings_states):
                    move.move_dest_ids.filtered(lambda m: m.state != 'done')._action_cancel()
            else:
                if all(state in ('done', 'cancel') for state in siblings_states):
                    move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                    move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
            # stock updation
            for line in move.move_line_ids:
                move_quantity = move.product_uom._compute_quantity(move.product_uom_qty,
                                                                   move.product_id.uom_id,
                                                                   rounding_method='HALF-UP')
                lot = False
                if line.product_id.tracking == 'lot':
                    lot = line.lot_id.id
                    source_domain = [('location_id', '=', move.location_id.id), ('lot_id', '=', line.lot_id.id),
                                     ('product_id', '=', line.product_id.id)]
                    dest_domain = [('location_id', '=', move.location_dest_id.id), ('lot_id', '=', line.lot_id.id),
                                   ('product_id', '=', line.product_id.id)]
                else:
                    source_domain = [('location_id', '=', move.location_id.id), ('product_id', '=', line.product_id.id)]
                    dest_domain = [('location_id', '=', move.location_dest_id.id), ('product_id', '=', line.product_id.id)]
                source_quant = self.env['stock.quant'].search(source_domain)
                dest_quant = self.env['stock.quant'].search(dest_domain)
                if not source_quant:
                    if move.product_id.type != 'consu':
                        self.action_cancel_quant_create2(move.product_id.id, move.location_id.id,
                                                         move_quantity, 0, move.company_id.id, lot)

                source_quant.sudo().quantity = source_quant.quantity + move.product_qty
                dest_quant.sudo().quantity = dest_quant.quantity - move.product_qty
        self.move_line_ids.unlink()
        self.write({'state': 'draft', 'move_orig_ids': [(5, 0, 0)]})
        return True



