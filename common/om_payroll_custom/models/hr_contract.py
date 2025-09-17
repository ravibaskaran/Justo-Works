from odoo import fields, models, api


class InheritHRContract(models.Model):
    _inherit = 'hr.contract'

    schedule_pay = fields.Selection(selection='_get_new_selection', required=True)

    @api.model
    def _get_new_selection(self):
        selection = [
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Biweekly'),
            ('monthly', 'Monthly')
        ]
        return selection

