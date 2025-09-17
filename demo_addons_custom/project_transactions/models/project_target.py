from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTarget(models.Model):
    _name = 'project.target'
    _inherit = ['mail.thread']
    _description = 'Project Target Form'

    name = fields.Char(compute='compute_name')
    project_id = fields.Many2one('building', tracking=True)
    financial_year = fields.Many2one('ir.sequence.date_range', tracking=True)
    target_line_ids = fields.One2many('project.target.line', 'target_id')

    @api.depends('project_id', 'financial_year')
    def compute_name(self):
        for rec in self:
            rec.name = "%s (%s)" % ((rec.project_id.name if rec.project_id else ''), (rec.financial_year.name if rec.financial_year else ''))

    @api.onchange('financial_year')
    def onchange_financial_year(self):
        if self.financial_year:
            start_date = self.financial_year.date_from
            end_date = self.financial_year.date_to
            line_ids = []
            current_date = start_date
            while current_date <= end_date:
                print(current_date.strftime("%B %Y"))
                line_ids.append((0, 0, {
                    'month': current_date.strftime("%B %Y"),
                    'inventory': 0,
                    'amount': 0
                }))
                current_date = current_date.replace(day=1) + timedelta(days=32)
            self.target_line_ids = False
            self.target_line_ids = line_ids
        else:
            self.target_line_ids = False

    @api.constrains('project_id', 'financial_year')
    def _check_duplicate_target(self):
        for record in self:
            if record.project_id and record.financial_year:
                duplicate = self.search([
                    ('id', '!=', record.id),
                    ('project_id', '=', record.project_id.id),
                    ('financial_year', '=', record.financial_year.id)
                ])
                if duplicate:
                    raise ValidationError(
                        "A project target for the selected financial year already exists for this project!"
                    )

class ProjectTargetLine(models.Model):
    _name = 'project.target.line'
    _description = 'Project Target Line'

    month = fields.Char()
    inventory = fields.Integer('Booking')
    registration = fields.Integer()
    amount = fields.Float('Booking Amount')
    registration_amount = fields.Float()
    target_id = fields.Many2one('project.target', ondelete='cascade')
