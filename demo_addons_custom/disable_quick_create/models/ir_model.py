from odoo import fields, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    disable_create_edit = fields.Boolean(
        string='Disabling the Create and Edit option', default=True)
