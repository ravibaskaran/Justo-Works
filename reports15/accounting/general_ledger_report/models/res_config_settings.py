# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval


class ConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    def set_values(self):
        res = super(ConfigSettingsInherit, self).set_values()

        self.env['ir.config_parameter'].sudo().set_param('general_ledger_report.gl_ignore_ac_heads',
                                                         self.gl_ignore_ac_heads.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ConfigSettingsInherit, self).get_values()

        with_user = self.env['ir.config_parameter'].sudo()
        gl_ignore_ac_heads = with_user.get_param('general_ledger_report.gl_ignore_ac_heads')
        res.update(
            gl_ignore_ac_heads=[(6, 0, literal_eval(gl_ignore_ac_heads))] if gl_ignore_ac_heads else False, )
        return res

    gl_ignore_ac_heads = fields.Many2many('account.account')
