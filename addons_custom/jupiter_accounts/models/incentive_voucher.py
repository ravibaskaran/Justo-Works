from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError


class EmployeeIncentiveMove(models.Model):
    _name = 'employee.incentive.move'
    _description = 'Employee Incentive Voucher'

    name = fields.Char(compute='compute_name')
    project_id = fields.Many2one('building')
    date = fields.Date(default=date.today())
    closing_manager_amount = fields.Float('Closing Manager Amount')
    sourcing_manager_amount = fields.Float('Sourcing Manager Amount')
    closing_tl_amount = fields.Float('Closing TL Amount')
    sourcing_tl_amount = fields.Float('Sourcing Tl Amount')
    crm_amount = fields.Float('CRM Amount')
    marketing_amount = fields.Float('Marketing Amount')

    def compute_name(self):
        for rec in self:
            rec.name = str(rec.project_id.name) + (('(' + str(rec.date.strftime('%d/%m/%Y')) + ')') if rec.date else '')

    @api.constrains('name', 'project_id', 'date', 'closing_manager_amount', 'sourcing_manager_amount',
                    'closing_tl_amount', 'sourcing_tl_amount', 'crm_amount', 'marketing_amount')
    def block_backdate(self):
        if not self.env.user.has_group('jupiter_accounts.edit_incentive_rate_slab_date'):
            if self.env['project.registration'].search(
                    [('registration_date', '>=', self.date), ('project_id', '=', self.project_id.id), ('state', 'not in', ('draft', 'canceled'))]):
                raise UserError(
                    'Backdate voucher creating or editing not allowed, \nRegistration exists for project after this date!')
