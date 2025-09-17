from odoo import api, fields, models


class WarningWizard(models.TransientModel):
    _name = 'warning.wizard'
    _description = 'Warning wizard'

    message = fields.Text(readonly=True)
    account_payment_id = fields.Many2one('account.payment', string='Payment', compute='_compute_related_model_id')

    @api.model
    def default_get(self, fields):
        defaults = super(WarningWizard, self).default_get(fields)

        record = self.env.context.get('default_record_id')
        payments = self.env['payment.invoice'].search([
            ('id', '=', record)
        ])
        # print(payments)
        rec = self.env.context.get('default_rec_id')
        payments_rec = self.env['payment.invoice'].search([
            ('invoice_number_id', '=', rec),
            ('payment_invoice_checkbox', '=', True),
            ('account_payment_id.is_reconciled_payment', '=', True)
        ])
        # print(payments)
        warning_message = ''
        for record in payments:
            payments_rec = payments_rec.filtered(lambda l: l.create_date > record.create_date)
            warning_message += 'The Invoice/Bill number ' + record.invoice_number + ' is included in the following payments and reseting will affect the following payments:\n'
            # print(payments_rec)
            for rec in payments_rec:
                settled_amount_formatted = '{:.2f}'.format(float(rec.settled_amount))
                warning_message += str(rec.account_payment_id.name) + ' with the amount of ' + settled_amount_formatted +'\n'
                # break

        defaults['message'] = warning_message.strip()
        return defaults

    @api.depends('message')
    def _compute_related_model_id(self):
        for record in self:
            record_id = record.env.context.get('default_record_id')
            # rec_id = record.env.context.get('default_rec_id')
            # print(record_id,rec_id)
            if record_id:
                payment = self.env['payment.invoice'].search([('id', '=', record_id)], limit=1)
                if payment:
                    record.account_payment_id = payment.account_payment_id.id

    def continue_btn(self):
        # print(self.account_payment_id)
        self.account_payment_id.action_draft()
        self.account_payment_id.hide_reconcile_button = False
        self.account_payment_id.write({
            'is_reconciled_payment': False
        })
        print(3)
        for line in self.account_payment_id.payment_invoice_ids:
            payment_invoice = self.env['payment.invoice'].search([
                ('invoice_number_id', '=', line.invoice_number_id.id)
            ])
            if not line.invoice_number_id:
                account_move_line = self.env['account.move.line'].search([
                    # ('name', '=', 'Opening Journal Entry'),
                    ('partner_id', '=', self.account_payment_id.partner_id.id),
                    # ('parent_state', '!=', 'posted'),
                    ('account_internal_type', '=', 'payable'),
                    ('reconciled', '=', False),
                    ('credit', '=', line.amount_total_in_currency_signed),
                ])
                print(account_move_line)
                account_move_line.amount_residual = (account_move_line.amount_residual - line.settled_amount)
            print(line)
            payment_invoice = payment_invoice.filtered(lambda l:l.create_date > line.create_date)
            print(payment_invoice)
            previous_inv_balance = 0.00
            for index, record in enumerate(payment_invoice):
                print(record)
                if index == 0:
                    record.write({
                        'amount_residual': line.amount_residual,
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


    def cancel_btn(self):
        print('enter cancel')
        if self._context.get('stop_execution'):
        # self.account_payment_id.on_discard()
        # self.account_payment_id.create_payments_for_invoices()
            return {'type': 'ir.actions.act_window_close'}



