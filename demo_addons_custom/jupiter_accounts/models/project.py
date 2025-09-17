from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'building'

    spot_booking_amount = fields.Float()
    cp_brokerage_accountable = fields.Boolean()
    cp_brokerage_percentage = fields.Float()
    incentive_type = fields.Selection([('1', 'Type 1'), ('2', 'Type 2')])
    developer_commission_percentage = fields.Float()
    minimum_advance_percentage = fields.Float()

    @api.onchange('region_id')
    def onchange_region_id(self):
        self.incentive_type = self.region_id.incentive_type
