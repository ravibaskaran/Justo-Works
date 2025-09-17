# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    odoobot_state = fields.Selection(default="disabled")
    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Inbox')],
        'Notification Management', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Inbox: notifications appear in your  Inbox")

    def preference_change_password(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'change_password',
            'target': 'new',
            'name': 'Inexoft',
        }

    @api.model
    def remove_odoo_from_action_help(self):
        data = self.env['ir.actions.act_window'].search([])
        for act in data:
            if act.help:
                act.help = act.help.replace('Odoo', 'Software').replace('odoo', 'software')
