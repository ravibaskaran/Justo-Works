# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval


class RealEstateSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reservation_hours = fields.Integer(string='Hours to release units reservation',
                                       config_parameter='itsys_real_estate.reservation_hours')

    penalty_percent = fields.Integer('Penalty Percentage')
    penalty_account = fields.Many2one('account.account',
                                      'Late Payments Penalty Account',
                                      config_parameter='itsys_real_estate.penalty_account')
    discount_account = fields.Many2one('account.account',
                                       'Discount Account',
                                       config_parameter='itsys_real_estate.discount_account')
    income_account = fields.Many2one('account.account',
                                     'Income Account',
                                     config_parameter='itsys_real_estate.income_account')
    me_account = fields.Many2one('account.account',
                                 'Managerial Expenses Account',
                                 config_parameter='itsys_real_estate.me_account')
    analytic_account = fields.Many2one('account.analytic.account',
                                       'Analytic Account',
                                       config_parameter='itsys_real_estate.analytic_account')
    security_deposit_account = fields.Many2one('account.account',
                                               'Security Deposit Account',
                                               config_parameter='itsys_real_estate.security_deposit_account')

    revenue_account = fields.Many2one('account.account',
                                      'Revenue Account',
                                      config_parameter='itsys_real_estate.revenue_account')
    booking_backdate_allowed_days = fields.Integer(config_parameter='itsys_real_estate.booking_backdate_allowed_days')
    booking_draft_checking_hours = fields.Integer(config_parameter='itsys_real_estate.booking_draft_checking_hours')

    # MAIL CONFIGURATIONS
    enable_project_creation_mail_to_hr = fields.Boolean(config_parameter="itsys_real_estate.enable_project_creation_mail_to_hr")
    mail_hr_users = fields.Many2many('res.users', 'mail_hr_users')
    enable_term_sheet_mail = fields.Boolean(config_parameter="itsys_real_estate.enable_term_sheet_mail")
    term_sheet_mail_users = fields.Many2many('res.users', 'term_sheet_mail_users')
    enable_booking_reset_mail = fields.Boolean(config_parameter="itsys_real_estate.enable_booking_reset_mail")
    booking_reset_mail_users = fields.Many2many('res.users', 'booking_reset_mail_users')
    enable_booking_wo_registration_mail = fields.Boolean(config_parameter="itsys_real_estate.enable_booking_wo_registration_mail")
    booking_wo_registration_mail_frequency = fields.Integer(config_parameter="itsys_real_estate.booking_wo_registration_mail_frequency")

    def set_values(self):
        res = super(RealEstateSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('itsys_real_estate.mail_hr_users', self.mail_hr_users.ids)
        self.env['ir.config_parameter'].sudo().set_param('itsys_real_estate.term_sheet_mail_users', self.term_sheet_mail_users.ids)
        self.env['ir.config_parameter'].sudo().set_param('itsys_real_estate.booking_reset_mail_users', self.booking_reset_mail_users.ids)
        return res

    @api.model
    def get_values(self):
        res = super(RealEstateSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        mail_hr_users = with_user.get_param('itsys_real_estate.mail_hr_users')
        term_sheet_mail_users = with_user.get_param('itsys_real_estate.term_sheet_mail_users')
        booking_reset_mail_users = with_user.get_param('itsys_real_estate.booking_reset_mail_users')
        res.update(
            mail_hr_users=[(6, 0, literal_eval(mail_hr_users))] if mail_hr_users else False,
            term_sheet_mail_users=[(6, 0, literal_eval(term_sheet_mail_users))] if term_sheet_mail_users else False,
            booking_reset_mail_users=[(6, 0, literal_eval(booking_reset_mail_users))] if booking_reset_mail_users else False,
        )
        return res



class Config(models.TransientModel):
    _name = 'gmap.config'

    @api.model
    def get_key_api(self):
        return self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
