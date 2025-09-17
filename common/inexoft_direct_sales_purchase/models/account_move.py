# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.tools.float_utils import float_compare
from datetime import datetime
from pytz import timezone


# ♦ ▼ Inherited 'Account Move'. ▼ ♦
class AccountMove(models.Model):
    _inherit = 'account.move'

    # Todo: Need to change the bellow code with constrain no need both create and write strick.

    @api.constrains('invoice_line_ids')
    def check_invoice_line_ids(self):
        if self.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund'] and not self.invoice_line_ids:
            raise ValidationError(_('You need to add a line before saving..'))

    # @api.model
    # def create(self, vals):
    #     res = super(AccountMove, self).create(vals)
    #     if res.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund'] and not res.invoice_line_ids:
    #         raise UserError(_('You need to add a line before saving..'))
    #     return res
    #
    # def write(self, vals):
    #     res = super(AccountMove, self).write(vals)
    #     if self._origin.id and self.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund'] and not self.invoice_line_ids:
    #         raise UserError(_('You need to add a line before saving.'))
    #     return res

    @api.model
    def default_get(self, fieldsname):
        res = super(AccountMove, self).default_get(fieldsname)
        if self._context.get('default_direct_move_type'):
            res['direct_move_warehouse_id'] = self.env['stock.warehouse'].search([
                ('company_id', '=', self.env.company.id)
            ], limit=1).id
        return res

    direct_move_type = fields.Selection([('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    direct_move_warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    direct_move_picking_id = fields.Many2one('stock.picking', string="Direct Move Stock Picking", copy=False)

    # ▼ Get Actual Indian date ▼
    def get_direct_move_date(self):
        date = self.invoice_date
        if not date:
            date = datetime.now().date()
        indian_time = self.get_actual_time(date)
        return indian_time

    # ▼ To get Actual Time ▼
    def get_actual_time(self, date):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        result_utc_datetime = datetime.now() - UTC_OFFSET_TIMEDELTA
        actual = datetime.combine(date, result_utc_datetime.time())
        return actual + UTC_OFFSET_TIMEDELTA

    # ▼ Check Available Quantity of Lot ▼
    def check_qty_lot_custom(self):

        if self.direct_move_type and self.move_type != 'out_refund':
            for line in self.invoice_line_ids:
                if line.lot_id and line.product_tracking != 'none':
                    qty = sum(self.invoice_line_ids.filtered(
                        lambda l: l.product_id == line.product_id and l.lot_id == line.lot_id).mapped('quantity'))
                    quantity = line.product_uom_id._compute_quantity(
                        qty, line.product_id.uom_id)
                    if line.lot_id.direct_sellable_qty < quantity:
                        raise UserError(_('%s has no enough stock %s') % (line.product_id.name, line.lot_id.name))

        if self.direct_move_type and self.move_type not in ['in_invoice', 'out_refund']:
            for line in self.invoice_line_ids:
                if line.product_id.type == 'product':
                    qty = sum(self.invoice_line_ids.filtered(
                        lambda l: l.product_id == line.product_id).mapped('quantity'))
                    quantity = line.product_uom_id._compute_quantity(
                        qty, line.product_id.uom_id)
                    if line.product_id.sudo().qty_available < quantity:
                        raise UserError(_('%s has no enough stock') % (line.product_id.name))

    # ▼ Custom Action Post ▼
    def action_post_custom(self):
        self.check_qty_lot_custom()
        product_type_items = self.invoice_line_ids.filtered(lambda x: x.product_id.type == 'product')
        if not product_type_items:
            return self.action_post()
        direct_move = self.direct_move_type and self.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund']
        if direct_move:
            if not self.direct_move_picking_id or self.direct_move_picking_id.state != 'done':
                for line in self.invoice_line_ids:
                    res = line.check_qty_availability_lot()
                    if res:
                        msg = line.product_id.name + " not enough stock"
                        if line.lot_id:
                            msg += " in " + line.lot_id.name
                        raise UserError(msg)
            if not self.direct_move_picking_id or (self.direct_move_picking_id and self.direct_move_picking_id.state == 'cancel'):
                self.create_direct_move_picking()
            if not self.direct_move_picking_id:
                raise UserError("No delivery/Receipt found!")
            if self.direct_move_picking_id.state not in ['done', 'cancel']:
                track_moves = self.invoice_line_ids.filtered(lambda p: p.product_tracking != 'none').mapped('direct_stock_move_id')
                none_track_moves = self.invoice_line_ids.filtered(lambda p: p.product_tracking == 'none').mapped('direct_stock_move_id')
                all_moves = track_moves + none_track_moves
                for move in all_moves:
                    move._action_confirm(merge=False)
                    move._action_assign()
                    for moveline in move.move_line_ids:
                        moveline.write({'qty_done': moveline.product_uom_qty})
                res = self.direct_move_picking_id.button_validate()
                if self.direct_move_picking_id.state != 'done':
                    return res
            if self.direct_move_picking_id.state == 'done':
                return self.action_post()

    def action_post(self):
        product_type_items = self.invoice_line_ids.filtered(lambda x: x.product_id.type == 'product')
        if not product_type_items:
            return super(AccountMove, self).action_post()
        direct_move = self.direct_move_type and self.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund']
        if direct_move:
            if not self.direct_move_picking_id:
                raise UserError("No delivery/Receipt found!")
        return super(AccountMove, self).action_post()

    def create_direct_move_picking(self):
        picking_obj = self.env['stock.picking']
        direct_move_type = self.direct_move_type
        type = self.move_type
        if direct_move_type == 'incoming' and type == 'in_invoice':
            picking_type = self.direct_move_warehouse_id.in_type_id
            location = self.partner_id.property_stock_supplier
            location_dest = picking_type.default_location_dest_id
        elif direct_move_type == 'incoming' and type == 'in_refund':
            picking_type = self.direct_move_warehouse_id.out_type_id
            location = picking_type.default_location_src_id
            location_dest = self.partner_id.property_stock_supplier
        elif direct_move_type == 'outgoing' and type == 'out_invoice':
            picking_type = self.direct_move_warehouse_id.out_type_id
            location = picking_type.default_location_src_id
            location_dest = self.partner_id.property_stock_customer
        elif direct_move_type == 'outgoing' and type == 'out_refund':
            picking_type = self.direct_move_warehouse_id.in_type_id
            location = self.partner_id.property_stock_customer
            location_dest = picking_type.default_location_dest_id
        picking = picking_obj.with_context(default_picking_type_id=picking_type.id).create({
            'partner_id': self.partner_id.id,
            'date': self.date,
            'origin': self.name,
            'location_id': location.id,
            'location_dest_id': location_dest.id,
            'company_id': self.company_id.id,
            'direct_transaction_type': 'purchase' if direct_move_type == 'incoming' else 'sale',
            'scheduled_date': self.get_direct_move_date(),
            'move_type':'direct',
        })
        self.with_context(direct_move_updating=True).direct_move_picking_id = picking.id
        self.invoice_line_ids.filtered(lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves_inx(picking)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_tracking = fields.Selection(related="product_id.tracking")
    direct_stock_move_id = fields.Many2one("stock.move")
    lot_id = fields.Many2one("stock.production.lot", string="Lot/Serial")
    lot_name = fields.Char(string="Lot/Serial", copy=False)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        self.lot_id = False
        return res

    @api.onchange('quantity', 'lot_id', 'product_uom_id')
    def check_qty_availability_lot(self):
        if self.move_id.direct_move_type and self.product_tracking != 'none' and self.move_id.move_type != 'out_refund':
            if self.lot_id:
                quantity = self.product_uom_id._compute_quantity(self.quantity, self.product_id.uom_id)
                if self.lot_id.direct_sellable_qty < quantity:
                    self.quantity = 1
                    return {
                        'warning': {'title': _('Not enough stock'),
                                    'message': _("Not enough stock"), },
                    }

        if self.move_id.direct_move_type and self.product_id.type == 'product' and self.move_id.move_type not in ['in_invoice', 'out_refund']:
            quantity = self.product_uom_id._compute_quantity(
                self.quantity, self.product_id.uom_id)
            if self.product_id.sudo().qty_available < quantity:
                self.quantity = 1
                return {
                    'warning': {'title': _('Not enough stock'),
                                'message': _("Not enough stock"), },
                }

    def check_product_availability_inx(self, warehouse_id):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        product = self.product_id.with_context(
            warehouse=warehouse_id.id,
            lang=self.env.user.lang or 'en_US'
        )
        product_qty = self.product_uom_id._compute_quantity(
            self.quantity, self.product_id.uom_id)
        if float_compare(product.qty_available, product_qty, precision_digits=precision) == -1:
            return False
        return True

    def _create_stock_moves_inx(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            if not line.exclude_from_invoice_tab:
                price_unit = line.price_unit
                template = {
                    'name': line.name or '',
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'product_uom_qty': line.quantity,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'picking_id': picking.id,
                    'state': 'draft',
                    'company_id': line.move_id.company_id.id,
                    'price_unit': price_unit,
                    'picking_type_id': picking.picking_type_id.id,
                    'route_ids': 1 and [(6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                    'warehouse_id': picking.picking_type_id.warehouse_id.id,
                    'inv_line_id': line.id,
                }
                if line.move_id.direct_move_type == 'incoming' and line.move_id.move_type == 'in_invoice' or (line.move_id.direct_move_type == 'outgoing' and line.move_id.move_type == 'out_refund'):
                    template['move_line_nosuggest_ids'] = [(0, 0, {
                        'product_id': line.product_id.id,
                        'lot_name': line.lot_name,
                        'lot_id': line.lot_id.id if line.lot_id else False,
                        'product_uom_qty': line.quantity,
                        'product_uom_id': line.product_uom_id.id,
                        'location_id': picking.location_id.id,
                        'location_dest_id': picking.location_dest_id.id,
                        'picking_id': picking.id,
                    })]
                create_move_id = moves.create(template)
                line.direct_stock_move_id = create_move_id.id
        return done
