from odoo import fields, models, api, _
from odoo.exceptions import UserError


#  ♦ ▼ Inherited 'Purchase Order'. ▼ ♦
class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    no_backorder = fields.Boolean(default=False)
    bill_count = fields.Integer(compute='_compute_bill_count')

    def _compute_bill_count(self):
        bills = self.env['account.move'].search([('purchase_order', '=', self.id)])
        self.bill_count = len(bills) if bills else False

    @api.onchange('date_order')
    def onchange_date_order(self):
        warning = False
        latest_order = self.env['purchase.order'].search([], order="date_order desc", limit=1)
        if latest_order and self.date_order < latest_order.date_order:
            self.date_order = None
            warning = True
        if warning:
            return {'warning': {'title': _('Warning!'), 'message': _('Please select valid date'), }}

    def print(self):
        result = self.env.ref('purchase.action_report_purchase_order').report_action(self)
        result['default_print_option'] = 'print'
        return result




    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': partner_bank_id.id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'direct_move_type': 'incoming',
            'direct_move_warehouse_id': self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1).id
        }
        return invoice_vals


# ♦ ▼ Inherited 'Purchase Order Line'. ▼ ♦
class PuchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    qty_purchased = fields.Float(compute='_compute_qty_purchased')

    def _compute_qty_purchased(self):
        account_moves = self.env['account.move.line'].search([('purchase_order_line_id', '=', self.id)])
        qty_purchased = sum(move.quantity for move in account_moves)
        self.qty_purchased = qty_purchased

