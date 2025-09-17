from odoo import models, fields


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    manufacture = fields.Char('Make & Type')
    holder = fields.Char()
    purpose = fields.Char()
    ser_number = fields.Char('Ser Number / Reg Number')
