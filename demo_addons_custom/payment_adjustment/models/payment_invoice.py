# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class PaymentInvoice(models.Model):
    """payment invoice model """
    _name = 'payment.invoice'

    invoice_date = fields.Date(string='Invoice/Bill Date', )
    invoice_number_id = fields.Many2one('account.move', )
    opening_move_id = fields.Many2one('account.move.line',)
    invoice_number = fields.Text(string='Number', compute='compute_invoice_number', inverse='inverse_invoice_number', store=True)
    amount_total_in_currency_signed = fields.Float(string='Invoice/Bill Amount')
    amount_residual = fields.Float(string='Amount Due')
    settled_amount = fields.Float(string='Settled Amount')
    amount_balance = fields.Float(string='Balance', store=True)
    invoice_balance = fields.Float(string='Balance', store=True, default=lambda self: self.amount_residual)
    account_payment_id = fields.Many2one('account.payment', 'payment_id')
    payment_invoice_checkbox = fields.Boolean(string='Add To Payment',
                                              help='Enable if you want to add the invoice to this payment', default=False)
    payment_amount = fields.Float(string='Amount', readonly=True)
    remarks = fields.Selection([
        ('not_paid', 'Not Paid'), ('partial_paid', 'Partially Paid'), ('full_paid', 'Full Paid')
    ], default='not_paid')
    is_account_opening = fields.Boolean(default=False)

    @api.depends('invoice_number_id')
    def compute_invoice_number(self):
        for rec in self:
            if rec.invoice_number_id:
                rec.invoice_number = rec.invoice_number_id.name

    def inverse_invoice_number(self):
        pass

    @api.onchange('payment_invoice_checkbox')
    def change_balance_amount(self):
        """function for calculate balance amount"""
        if self.payment_invoice_checkbox:
            amount = self.account_payment_id.sub_amount
            print(amount)
            if amount <= 0.00:
                raise UserError("Payment amount is adjusted to Invoices/Bills or the payment amount is zero!")
            if self.amount_residual <= amount:
                self.invoice_balance = 0.00
                self.remarks = 'full_paid'
                self.settled_amount = self.amount_residual
            else:
                self.invoice_balance = self.amount_residual - amount
                if self.invoice_balance <= 0.00:
                    self.remarks = 'not_paid'
                    self.invoice_balance = 0.00
                else:
                    self.remarks = 'partial_paid'
                    # self.invoice_balance = self.amount_balance
                    self.settled_amount = (self.amount_residual - self.invoice_balance)
        else:
            self.invoice_balance = 0.00
            self.remarks = 'not_paid'
