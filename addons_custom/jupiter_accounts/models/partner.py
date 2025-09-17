from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    opening_balance = fields.Float()
    opening_type = fields.Selection([('debit', 'Debit'), ('credit', 'Credit')])

    def name_get(self):
        res = []
        for partner in self:
            name = partner.name
            res.append((partner.id, name))
        return res

    def update_opening(self):
        if self.is_vendor:
            account = self.property_account_payable_id
        else:
            account = self.property_account_receivable_id
        return {
            'name': _('Update Opening'),
            'type': 'ir.actions.act_window',
            'res_model': 'opening.updater',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_account_id': account.id, 'default_amount': self.opening_balance,
                        'default_type': self.opening_type},
        }