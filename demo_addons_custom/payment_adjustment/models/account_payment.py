# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning
from num2words import num2words


class AccountPayment(models.Model):
    """inherited account_payment model """
    _inherit = 'account.payment'

    payment_invoice_ids = fields.One2many('payment.invoice', 'account_payment_id', string='Invoice')
    hide_reconcile_button = fields.Boolean(default=False)
    total_amount = fields.Float("Total Amount", compute='compute_total_amount', store=True)
    sub_amount = fields.Float("Total Sub Amount")
    draft_boolean = fields.Boolean(default=False)
    is_reconciled_payment = fields.Boolean(default=False)

    @api.onchange('amount', 'payment_invoice_ids')
    def update_amount_sub_amount(self):
        self.sub_amount = self.amount - (sum([item.amount_residual for item in self.payment_invoice_ids if item.payment_invoice_checkbox]) + sum([item.amount_balance for item in self.payment_invoice_ids]))

    @api.onchange('partner_id', 'draft_boolean')
    def change_invoice_list(self):
        """function for change invoice list"""
        for record in self:
            if record.payment_type in 'inbound':
                payment_invoice_ids = self.env['account.move'].search([
                    ('partner_id.id', '=', record.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', 'in', ['not_paid', 'partial']),
                    ('state', '=', 'posted'),
                ])
                record.write({'payment_invoice_ids': [(5,0,0)]})
                record.payment_invoice_ids = [(0,0,{
                    'invoice_date': invoice.invoice_date,
                    'invoice_number_id': invoice.id,
                    'amount_total_in_currency_signed': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                }) for invoice in payment_invoice_ids]
            else:
                payment_invoice_ids = self.env['account.move'].search([
                    ('partner_id.id', '=', record.partner_id.id),
                    ('move_type', '=', 'in_invoice'),
                    ('payment_state', 'in', ['not_paid', 'partial']),
                    ('state', '=', 'posted'),
                ])
                record.write({'payment_invoice_ids': [(5,0,0)]})
                record.payment_invoice_ids = [(0,0,{
                    'invoice_date': invoice.invoice_date,
                    'invoice_number_id': invoice.id,
                    'amount_total_in_currency_signed': abs(invoice['amount_total']),
                    'amount_residual': invoice.amount_residual,
                }) for invoice in payment_invoice_ids]

    @api.onchange('amount')
    def change_reset_invoice(self):
        for rec in self.payment_invoice_ids:
            rec.settled_amount = 0.00
            rec.remarks = 'not_paid'
            rec.payment_invoice_checkbox = False
            # if rec.amount_residual != rec.invoice_balance:
            rec.invoice_balance = rec.amount_residual

    @api.depends('payment_invoice_ids.amount_residual', 'payment_invoice_ids.payment_invoice_checkbox')
    def compute_total_amount(self):
        """function for calculate total amount"""
        for record in self:
            payment_invoice_ids = record.payment_invoice_ids.filtered(lambda l: l.payment_invoice_checkbox)
            total_amount = sum(invoice.amount_residual for invoice in payment_invoice_ids)
            record.total_amount = total_amount

    def create_payments_for_invoices(self):
        """Create payments for selected invoices"""
        line_ids = self.env['account.move'].search([
            ('name', '=', self.name)
        ])
        line_ids = line_ids.line_ids
        # line_ids = self.move_id.line_ids
        payment_invoice_ids = self.payment_invoice_ids.filtered(lambda l: l.payment_invoice_checkbox and l.invoice_number_id)
        if payment_invoice_ids:
            if payment_invoice_ids[0].invoice_balance != 0.00:
                print(payment_invoice_ids)
                payment_invoice_ids = payment_invoice_ids.sorted(key=lambda l: l.id, reverse=True)
        for line_id in line_ids:
            print('line id',line_id)
            for invoice in payment_invoice_ids:
                invoice.invoice_number_id.js_assign_outstanding_line(line_id.id)
        self.hide_reconcile_button = True
        self.payment_invoice_ids = self.payment_invoice_ids.filtered(lambda l: l.payment_invoice_checkbox)
        self.write({
            'is_reconciled_payment': True
        })
        return True

    def custom_reset_draft(self):
        """a custom reset button method for reset payment"""
        print(11111)
        for record in self.payment_invoice_ids:
            if record.invoice_number_id:
                payments = self.env['payment.invoice'].search([
                    ('invoice_number_id', '=', record.invoice_number_id.id),
                    ('account_payment_id.is_reconciled_payment', '=', True)
                ])
                print(';;;;',payments)
                if payments:
                    for rec in payments:
                        if rec.create_date > record.create_date:
                            return {
                                'name': 'Warning',
                                'type': 'ir.actions.act_window',
                                'res_model': 'warning.wizard',
                                'view_mode': 'form',
                                'view_type': 'form',
                                'target': 'new',
                                'context': {
                                    'default_record_id': record.id,
                                    'default_rec_id': rec.invoice_number_id.id,
                                    'stop_execution': True
                                }
                            }
        # If no payment with a later create_date is found, continue with action_draft()
        self.action_draft()
        self.hide_reconcile_button = False
        self.write({
            'is_reconciled_payment': False
        })
        return True

    def post(self):
        result = super(AccountPayment, self).post()
        for line in self.payment_invoice_ids:
            payments = self.env['payment.invoice'].search([
                ('invoice_number_id', '=', line.invoice_number_id.id)
            ])
            if payments:
                for rec in payments:
                    if rec.create_date > line.create_date:
                        payments = payments.filtered(lambda l: l.create_date > line.create_date)
                        print(payments)
                        previous_inv_balance = 0.00
                        for index, record in enumerate(payments):
                            print(record)
                            if index == 0:
                                record.write({
                                    'amount_residual': line.invoice_balance,
                                })
                                record.write({
                                    'invoice_balance': (record.amount_residual - record.settled_amount)
                                })
                                previous_inv_balance = record.invoice_balance
                                if record.invoice_balance == 0.00:
                                    record.write({
                                        'remarks': 'full_paid'
                                    })
                                else:
                                    record.write({
                                        'remarks': 'partial_paid'
                                    })
                            else:
                                record.write({
                                    'amount_residual': previous_inv_balance,
                                })
                                record.write({
                                    'invoice_balance': (record.amount_residual - record.settled_amount)
                                })
                                previous_inv_balance = record.invoice_balance
                                if record.invoice_balance == 0.00:
                                    record.write({
                                        'remarks': 'full_paid'
                                    })
                                else:
                                    record.write({
                                        'remarks': 'partial_paid'
                                    })
        return result

    def print_payment_voucher(self):
        # print(self.currency_id.symbol)
        total_in_words = num2words(self.amount, lang='en_IN').title()
        data = {
            'voucher_number': self.move_id.name,
            'payment_type': self.payment_type,
            'partner': self.partner_id.name,
            'amount': self.amount,
            'currency': self.currency_id.symbol,
            'date': self.date.strftime('%d-%m-%Y'),
            'memo': self.ref,
            'journal': self.journal_id.name,
            'payment_method': self.payment_method_line_id.name,
            'company_bank': self.partner_bank_id.acc_number,
            'total_in_words': total_in_words,
            'slips': [],
        }
        for rec in self.payment_invoice_ids:
            data['slips'].append({
                'invoice_date': rec.invoice_date.strftime('%d-%m-%Y'),
                'number': rec.invoice_number_id.name,
                'bill_value': rec.amount_total_in_currency_signed,
                'amount_residual': rec.amount_residual,
                'settled_amount': rec.settled_amount,
                'invoice_balance': rec.invoice_balance,
                'remarks': rec.remarks,
            })
        company = self.env.user.company_id
        data.update({
            # 'company_logo': company.logo,  # Add the appropriate field for the logo
            'company_name': company.name,
            'company_address': company.street,  # Update with the correct field for the address
            'company_phone': company.phone,
            'company_email': company.email,
        })
        print(data)
        report_ref = self.env.ref('payment_adjustment.action_print_payment_voucher')
        return report_ref.report_action(self, {'data': data})
