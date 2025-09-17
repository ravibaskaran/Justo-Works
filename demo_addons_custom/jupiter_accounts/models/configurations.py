from odoo import models, fields, api, _
from odoo.exceptions import UserError

product_domain = [('detailed_type', '=', 'service'), ('is_property', '!=', True)]


class ProjectConfigurations(models.Model):
    _name = 'project.configurations'
    _description = 'Project Configurations'

    name = fields.Char()
    spot_booking_product = fields.Many2one('product.product', domain=product_domain)
    cp_brokerage_product = fields.Many2one('product.product', domain=product_domain)
    incentive_product = fields.Many2one('product.product', domain=product_domain)
    developer_invoice_product = fields.Many2one('product.product', domain=product_domain)
    activate = fields.Boolean(default=False)
    monthly_minimum_booking = fields.Integer(default=2)
    incentive_interval = fields.Integer(default=3)
    minimum_advance_ids = fields.One2many('minimum.advance.line', 'configuration_id')

    _sql_constraints = [
        ('incentive_interval_validation',
         'CHECK(incentive_interval in (1, 2, 3, 4, 6, 12))',
         'Incentive Interval should be one the values 1, 2, 3, 4, 6, 12')
    ]

    @api.onchange('activate')
    def check_activated(self):
        if self.activate:
            conf = self.env['project.configurations'].search([('activate', '=', True), ('id', '!=', self._origin.id)])
            if conf:
                raise UserError(_('Another configuration(%s) already activated') % conf.name)


class MinimumAdvanceLine(models.Model):
    _name = 'minimum.advance.line'

    configuration_id = fields.Many2one('project.configurations')
    amount_from = fields.Float()
    amount_to = fields.Float()
    advance_amount = fields.Float()
