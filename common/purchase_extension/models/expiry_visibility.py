# -*- coding: utf-8 -*-

from odoo import models, fields, api


#  ♦ ▼ Inherit Config Setting ▼ ♦
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_expiry = fields.Boolean("Show Expiry", implied_group='purchase_extension.group_expiry',default=False)