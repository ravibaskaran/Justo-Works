from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = "account.account"

    partner_account_inx = fields.Boolean(default=False)
