from ast import Store
from odoo import models, fields, api, _


class AccountAccount(models.Model):
    _inherit = "account.account"

    hide = fields.Boolean(
        string='Hide From Journal / Receipt / Payment Voucher',
        required=False)
    
