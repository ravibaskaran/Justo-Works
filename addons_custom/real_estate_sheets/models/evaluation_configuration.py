from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EvaluationSheetConfiguration(models.Model):
    _name = 'evaluation.configuration'

    name = fields.Char(required=True)
    walk_ins = fields.Float()
    cp_walk_ins = fields.Float()
    direct_walk_ins = fields.Float()
    digital_walk_ins = fields.Float()
    no_of_digital_leads = fields.Integer()
    activate = fields.Boolean(default=False)
    other_exp_percentage = fields.Float()
    sales_incentive_group_count = fields.Integer('Profit & Loss Sales Incentive Group Count')
    cf_sales_incentive_group_count = fields.Integer('Cash Flow Sales Incentive Group Count')
    reg_month_1 = fields.Float('Reg Month 1 %')
    reg_month_2 = fields.Float('Reg Month 2 %')
    reg_month_3 = fields.Float('Reg Month 3 %')
    reg_month_4 = fields.Float('Reg Month 4 %')
    collection_billing_count = fields.Integer()
    admin_expense = fields.Float()

    @api.onchange('activate')
    def check_activated(self):
        if self.activate:
            conf = self.env['evaluation.configuration'].search([('activate', '=', True), ('id', '!=', self._origin.id)])
            if conf:
                raise UserError(_('Another configuration(%s) already activated') % conf.name)
