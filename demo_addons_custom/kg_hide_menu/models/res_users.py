# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/


from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    hide_menu_access_ids = fields.Many2many('ir.ui.menu', 'ir_ui_hide_menu_rel', 'uid', 'menu_id',
                                            string='Hide Access Menu')

    # def write(self, vals):
    #     if vals.get('hide_menu_access_ids'):
    #         self.env.ref('kg_hide_menu.group_hide_menu_toggle').sudo().write({'users': [(4, self.id)]})
    #     return super(ResUsers, self).write(vals)
    #
    # def copy(self, default=None):
    #     record = super(ResUsers, self).copy(default=default)
    #     self.env.ref('kg_hide_menu.group_hide_menu_toggle').sudo().write({'users': [(3, self.id)]})
    #     self.env.ref('kg_hide_menu.group_hide_menu_toggle').sudo().write({'users': [(4, record.id)]})
    #     return record