# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    daybook_default_order = fields.Selection([('account', 'Account'), ('voucher', 'Voucher Name')],
                                             string='Daybook Order By',
                                             default='account',
                                             required=True,
                                             config_parameter='day_book.daybook_default_order')
