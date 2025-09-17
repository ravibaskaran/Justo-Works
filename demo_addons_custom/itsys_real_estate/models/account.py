# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountVoucher(models.Model):
    _inherit = "account.payment"

    reservation_id = fields.Many2one('unit.reservation', 'Reservation')
    real_estate_ref = fields.Char('Real Estate Ref.')
    ownership_line_id = fields.Many2one('loan.line.rs.own', 'Ownership Installment')
    rental_line_id = fields.Many2one('loan.line.rs.rent', 'Rental Contract Installment')


class AccountMove(models.Model):
    _inherit = "account.move"

    real_estate_ref = fields.Char('Real Estate Ref.')
    ownership_line_id = fields.Many2one('loan.line.rs.own', 'Ownership Installment')
    rental_line_id = fields.Many2one('loan.line.rs.rent', 'Rental Contract Installment')
    property_owner_id = fields.Many2one('res.partner', string="Owner")
    building = fields.Many2one('building', 'Building')
    building_unit = fields.Many2one('product.template', 'Building Unit')


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    commissioned = fields.Boolean('Commissioned')
