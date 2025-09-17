from ast import Store
from odoo import models, fields, api, _


class MultipleAccountOpening(models.Model):
    _inherit = "account.journal"

    type = fields.Selection(selection_add=[

        ('adj_receipt', 'Adj Receipt'),
        ('adj_issue', 'Adj Issue'),
        ('damage', 'Damage Voucher'),
        ('stock_correction', 'Stock Correction'),
        ('rate_update', 'Rate Update Voucher'),
        ('cust_inout', 'Customer In Out'),
        ('supp_inout', 'Supplier In Out'),
        ('receipt_voucher', 'Receipt Voucher'),
        ('payment_voucher', 'Payment Voucher'),
        ('journal_voucher', 'Journal Voucher')

    ], required=True,
        help="Select 'Sale' for customer invoices journals.\n" \
             "Select 'Purchase' for vendor bills journals.\n" \
             "Select 'Cash' or 'Bank' for journals that are used in customer or vendor payments.\n" \
             "Select 'General' for miscellaneous operations journals."
    , ondelete={
'adj_receipt': 'cascade',
'adj_issue': 'cascade',
'damage': 'cascade',
'stock_correction': 'cascade',
'rate_update': 'cascade',
'cust_inout': 'cascade',
'supp_inout': 'cascade',
'receipt_voucher': 'cascade',
'payment_voucher': 'cascade',
'journal_voucher': 'cascade'})


    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank'),
        ('upi', 'UPI')
    ])

    def name_get(self):
        res = []
        if self._context.get('short_name'):
            for journal in self:
                if journal.short_name:
                    name = journal.short_name
                else:
                    name = journal.name
                res += [(journal.id, name)]
        else:
            res = super(MultipleAccountOpening, self).name_get()
        return res

    short_name = fields.Char(string='Short Name', store=True)



    @api.model
    def create(self, vals):
        if vals.get('type') in ('cust_inout', 'supp_inout') and vals.get('refund_sequence') and not vals.get(
                'refund_sequence_id'):
            vals.update({'refund_sequence_id': self.sudo()._create_sequence(vals, refund=True).id})
        res = super(MultipleAccountOpening, self).create(vals)
        return res