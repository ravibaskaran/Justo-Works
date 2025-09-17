# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    """inherited account move line model """
    _inherit = 'account.move.line'

    def remove_move_reconcile(self):
        result = super(AccountMoveLine, self).remove_move_reconcile()
        print(123456789)
        if self.env.context.get('move_id'):
            current_invoice = self.env['account.move'].browse(self.env.context.get('move_id'))
            print(current_invoice)
            payment_invoices = self.env['payment.invoice'].search([
                ('account_payment_id.is_reconciled_payment', '=', True)
            ])
            for payment_invoice in payment_invoices:
                print(payment_invoice.invoice_number_id)
                if payment_invoice.invoice_number_id.id == current_invoice.id:
                    raise UserError('You can only unreconcile the payment through the payment form RESET TO DRAFT')
        return result
