from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_payslip_adjustment_line = fields.Boolean(default=False)