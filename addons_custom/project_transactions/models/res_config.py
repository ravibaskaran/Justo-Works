# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    incentive_product_id = fields.Many2one('product.product', 'Incentive Service',
                                           config_parameter='project_transactions.incentive_product_id')
