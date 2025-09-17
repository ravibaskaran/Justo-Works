# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_token = fields.Char("Access Token", config_parameter="real_estate_extension.employee_api_token")
    api_token_expiry_time = fields.Datetime("Token Expiry", config_parameter="real_estate_extension.employee_api_token_expiry")

    # API CONFIGURATIONS
    employee_api_url = fields.Char(config_parameter="real_estate_extension.employee_api_url")
    employee_fetching_api = fields.Char(config_parameter="real_estate_extension.employee_fetching_api")
    employee_api_username = fields.Char(config_parameter="real_estate_extension.employee_api_username")
    employee_api_key = fields.Char(config_parameter="real_estate_extension.employee_api_key")
    project_api_url = fields.Char(config_parameter="real_estate_extension.project_api_url")
    project_api_username = fields.Char(config_parameter="real_estate_extension.project_api_username")
    project_api_key = fields.Char(config_parameter="real_estate_extension.project_api_key")
    project_employee_assign_api_url = fields.Char(config_parameter="real_estate_extension.project_employee_assign_api_url")
    project_employee_assign_api_username = fields.Char(config_parameter="real_estate_extension.project_employee_assign_api_username")
    project_employee_assign_api_key = fields.Char(config_parameter="real_estate_extension.project_employee_assign_api_key")
    booking_cancel_api_url = fields.Char(config_parameter="real_estate_extension.booking_cancel_api_url")
    booking_cancel_api_username = fields.Char(config_parameter="real_estate_extension.booking_cancel_api_username")
    booking_cancel_api_key = fields.Char(config_parameter="real_estate_extension.booking_cancel_api_key")
    enable_employee_out_api = fields.Boolean(config_parameter="real_estate_extension.enable_employee_out_api")
    enable_project_out_api = fields.Boolean(config_parameter="real_estate_extension.enable_project_out_api")
    enable_project_employee_assign_api = fields.Boolean(config_parameter="real_estate_extension.enable_project_employee_assign_api")
    enable_booking_cancel_api = fields.Boolean(config_parameter="real_estate_extension.enable_booking_cancel_api")
