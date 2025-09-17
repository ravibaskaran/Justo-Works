# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InstallmentTemplate(models.Model):
    _name = "installment.template"
    _description = "Installment Template"
    _inherit = ['mail.thread']

    name = fields.Char('Name', size=64, required=True)
    duration_month = fields.Integer('Month')
    duration_year = fields.Integer('Year')
    annual_raise = fields.Integer('Annual Raise %')
    repetition_rate = fields.Integer('Repetition Rate (month)', default=1)
    adv_payment_rate = fields.Integer('Advance Payment %')
    deduct = fields.Boolean('Deducted from amount?')
    note = fields.Html('Note')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.constrains('duration_month', 'duration_year')
    def _check_rule_duration_year_month(self):
        if not self.duration_month and not self.duration_year:
            raise ValidationError(_('Please set template duration; either by months or years!'))
