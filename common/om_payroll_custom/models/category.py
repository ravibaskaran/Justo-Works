from odoo import models, fields


class HrSalaryRuleCategory(models.Model):
    _inherit = 'hr.salary.rule.category'

    type = fields.Selection([('addition', 'Addition'), ('deduction', 'Deduction'), ('z_adjustment', 'Adjustment')])
