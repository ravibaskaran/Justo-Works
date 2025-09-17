# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import date
from odoo.exceptions import UserError
from odoo.tools.translate import _


class LatePaymentPenalties(models.Model):
    _name = "late.payment.penalties"

    region = fields.Many2one('regions', 'Region', )
    percent = fields.Integer('Penalty Percentage')
    account = fields.Many2one('account.account', 'Account', )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def get_account(self):
        penalty_account = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([])[-1].id).penalty_account.id if self.env[
            'res.config.settings'].search([]) else ""
        if not penalty_account:
            raise UserError(_('Please set default Discount Account!'))
        return penalty_account

    def get_penalties(self, line):
        line_date = line.date
        diff = (date.today().year - line_date.year) * 12 + date.today().month - line_date.month
        if diff > 0:
            penalty_percent = self.env['res.config.settings'].browse(
                self.env['res.config.settings'].search([])[-1].id).penalty_percent if self.env[
                'res.config.settings'].search([]) else ""
            if not penalty_percent:
                raise UserError(_('Please set default Penalty Percentage!'))

            result = line.amount * penalty_percent * diff / 100.0
            return result
        else:
            return 0
