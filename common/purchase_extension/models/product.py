from odoo import fields, models, api


class productProduct(models.Model):
    _inherit = 'product.template'

    generate_serial_number = fields.Boolean(default=False)
