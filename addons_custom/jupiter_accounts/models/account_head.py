from odoo import models, fields, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    opening_balance = fields.Float()
    opening_type = fields.Selection([('debit', 'Debit'), ('credit', 'Credit')])

    def update_opening(self):
        return {
            'name': _('Update Opening'),
            'type': 'ir.actions.act_window',
            'res_model': 'opening.updater',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_account_id': self.id, 'default_amount': self.opening_balance,
                        'default_type': self.opening_type},
        }
