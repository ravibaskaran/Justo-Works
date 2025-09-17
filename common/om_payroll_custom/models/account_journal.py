from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    type = fields.Selection(selection_add=[('payslip', 'Payslip Journal')], ondelete={'payslip': 'cascade'})
    refund_sequence_number_next=fields.Integer()
    profit_account_id=fields.Many2one('account.account')
    loss_account_id=fields.Many2one('account.account')

    @api.model
    def create(self, vals):
        if vals.get('type') == 'payslip' and vals.get('refund_sequence') and not vals.get('refund_sequence_id'):
            vals.update({'refund_sequence_id': self.sudo()._create_sequence(vals, refund=True).id})
        res = super(AccountJournal, self).create(vals)
        return res
