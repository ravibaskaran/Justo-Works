# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval


class DashboardSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_dashboard_walk_in_api = fields.Boolean(config_parameter="jupiter_dashboard_tres.enable_dashboard_walk_in_api")
    dashboard_walk_in_api_url = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_walk_in_api_url")
    dashboard_walk_in_api_username = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_walk_in_api_username")
    dashboard_walk_in_api_key = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_walk_in_api_key")
    enable_dashboard_new_cp_api = fields.Boolean(config_parameter="jupiter_dashboard_tres.enable_dashboard_new_cp_api")
    dashboard_new_cp_api_url = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_new_cp_api_url")
    dashboard_new_cp_api_username = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_new_cp_api_username")
    dashboard_new_cp_api_key = fields.Char(config_parameter="jupiter_dashboard_tres.dashboard_new_cp_api_key")
