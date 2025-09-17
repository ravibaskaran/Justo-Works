# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import http
from odoo.http import request

class KgHideMenu(http.Controller):

    @http.route('/correct_user_hide_menu', auth='public')
    def correct_user_hide_menu(self, **kw):
        if request.env.user.has_group('base.group_system'):
            users = request.env['res.users'].sudo().search([])
            for user in users:
                user.hide_menu_access_ids = user.hide_menu_ids.ids
        else:
            return 'Access Denied'