from odoo import models, fields, api


class LoanStatusMarking(models.Model):
    _name = 'loan.status.marking'
    _inherit = ['mail.thread']
    _description = 'Loan Status Marking'

    name = fields.Char(default='Loan Status Marking')
    project_id = fields.Many2one('building', 'Project Name')
    flat_id = fields.Many2one('product.template')
    booking_id = fields.Many2one('unit.reservation')
    developer_id = fields.Many2one('res.partner', domain=[('is_owner', '=', True)])
    customer_id = fields.Many2one('res.partner', domain=[('is_tenant', '=', True)])
    bank_name = fields.Char()
    loan_amount = fields.Float()
    status = fields.Many2one('loan.stage')
    is_completed = fields.Boolean(related='status.completed')

    @api.onchange('project_id')
    def onchange_project_id(self):
        self.developer_id = self.project_id.partner_id.id
        if self.flat_id.building_id != self.project_id:
            self.flat_id = False

    @api.onchange('customer_id')
    def onchange_customer(self):
        booking = self.env['unit.reservation'].search(
            [('partner_id', '=', self.customer_id.id), ('state', '=', 'confirmed')])
        if not self.flat_id:
            if len(booking) == 1:
                self.flat_id = booking.building_unit.id
        if booking:
            return {'domain': {'flat_id': [('id', 'in', booking.mapped('building_unit').ids)]}}

    @api.onchange('flat_id')
    def onchange_flat(self):
        if self.flat_id:
            self.project_id = self.flat_id.building_id.id
            booking = self.env['unit.reservation'].search(
                [('building_unit', '=', self.flat_id.id), ('state', '=', 'confirmed')])
            if len(booking) == 1:
                self.booking_id = booking.id
                self.customer_id = booking.partner_id.id
                self.bank_name = booking.preferred_bank
                self.loan_amount = booking.required_amount
            else:
                self.booking_id = False
                self.customer_id = False
                self.bank_name = False
                self.loan_amount = 0
        else:
            self.booking_id = False
            self.customer_id = False
            self.bank_name = False
            self.loan_amount = 0


class LoanStage(models.Model):
    _name = 'loan.stage'

    name = fields.Char()
    completed = fields.Boolean()
