from odoo import models, fields


class Regions(models.Model):
    _inherit = 'regions'

    incentive_type = fields.Selection([('1', 'Type 1'), ('2', 'Type 2')])
