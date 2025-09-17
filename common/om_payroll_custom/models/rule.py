from odoo import models
from odoo.exceptions import Warning


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def write(self, vals):
        res = super(HrSalaryRule, self).write(vals)
        if vals and self.id == self.env.ref('om_payroll_custom.round_off_payroll').id:
            for val in vals:
                if val not in ('account_debit','account_credit'):
                    raise Warning('You cannot change round off rule fields except accounts')
        return res
