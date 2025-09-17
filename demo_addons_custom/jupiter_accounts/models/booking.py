from odoo import models, fields, api
from odoo.exceptions import UserError


class Booking(models.Model):
    _inherit = 'unit.reservation'

    spot_booking_invoice_id = fields.Many2one('account.move')
    cp_brokerage_invoice_id = fields.Many2one('account.move')
    registration_status = fields.Selection([('not_registered', 'Not Registered'), ('registered', 'Registered')], compute='compute_registration_status')
    developer_commission_percentage = fields.Float(tracking=True)

    @api.onchange('building')
    def fill_developer_commission_percentage(self):
        self.developer_commission_percentage = 0
        if self.building:
            self.developer_commission_percentage = self.building.developer_commission_percentage

    def compute_registration_status(self):
        for rec in self:
            rec.registration_status = 'not_registered'
            if rec.state == 'confirmed':
                registration = self.env['project.registration'].search([('flat_id', '=', rec.building_unit.id), ('state', 'not in', ['draft', 'canceled'])])
                if registration:
                    rec.registration_status = 'registered'

    @api.onchange('building', 'flat_cost_real', 'source_of_booking')
    def fill_cp_brokerage(self):
        if self.source_of_booking == 'cp':
            self.cp_brokerage = self.flat_cost_real * self.building.cp_brokerage_percentage / 100
        else:
            self.cp_brokerage = 0

    def view_registration(self):
        registration = self.env['project.registration'].search(
            [('flat_id', '=', self.building_unit.id), ('state', 'not in', ('draft', 'canceled'))], limit=1)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registration',
            'view_mode': 'form',
            'res_id': registration.id,
            'res_model': 'project.registration',
            'context': {'create': False},
            'views': [(False, 'form')],
        }
    # ('state', 'not in', ['draft', 'canceled'])

    def view_spot_booking_invoice(self):
        form_view_id = self.env.ref("account.view_move_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Spot Booking Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [(form_view_id, 'form')],
            'res_id': self.spot_booking_invoice_id.id,
        }

    def view_cp_brokerage_invoice(self):
        form_view_id = self.env.ref("account.view_move_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'CP Brokerage Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [(form_view_id, 'form')],
            'res_id': self.cp_brokerage_invoice_id.id,
        }

    @api.onchange('building', 'spot_booking')
    def onchange_project(self):
        self.spot_amount = 0
        if self.building and self.spot_booking:
            self.spot_amount = self.building.spot_booking_amount

    @api.onchange('flat_cost')
    def onchange_flat_cost_fill_advance_amount(self):
        config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
        if config:
            for line in config.minimum_advance_ids:
                if line.amount_from <= self.flat_cost <= line.amount_to:
                    self.advance_amount = line.advance_amount

    def action_confirm(self):
        if self.building_unit.flat_state != 'rtb':
            minimum_advance_percentage = self.building.minimum_advance_percentage
            minimum_advance_amount = self.flat_cost * minimum_advance_percentage / 100
            config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
            if config:
                for line in config.minimum_advance_ids:
                    if line.amount_from <= self.flat_cost <= line.amount_to:
                        minimum_advance_amount = line.advance_amount
            if self.advance_amount < minimum_advance_amount:
                raise UserError('Advance amount is less than minimum required amount!')
        if self.developer_commission_percentage <= 0:
            raise UserError('Developer Commission should should be greater than zero!')
        res = super(Booking, self).action_confirm()
        return res

    def create_cp_brokerage_invoice(self):
        if self.source_of_booking == 'cp':
            if self.building.cp_brokerage_accountable:
                journal_id = self.env['account.journal'].search([('type', '=', 'cp_brokerage')], limit=1)
                if not journal_id:
                    raise UserError('CP Brokerage Journal not found!')
                if not journal_id.profit_account_id or not journal_id.loss_account_id:
                    raise UserError('Account configurations missing in CP Brokerage journal!')
                vals = {
                    'project_invoice_type': 'cp_brokerage',
                    'ref': '',
                    'move_type': 'entry',
                    'currency_id': self.env.company.currency_id.id,
                    'payment_reference': '',
                    'invoice_origin': self.name,
                    'company_id': self.env.company.id,
                    'l10n_in_gst_treatment': False,
                    'is_project_invoice': True,
                    'project_id': self.building.id,
                    'journal_id': journal_id.id,
                    'line_ids': [(0, 0, {
                        'account_id': journal_id.loss_account_id.id,
                        'partner_id': self.cp_id.id,
                        'debit': self.cp_brokerage,
                        'credit': 0,
                        'currency_id': self.env.company.currency_id.id
                    }), (0, 0, {
                        'account_id': journal_id.profit_account_id.id,
                        'partner_id': self.cp_id.id,
                        'debit': 0,
                        'credit': self.cp_brokerage,
                        'currency_id': self.env.company.currency_id.id
                    })]
                }
                invoice_id = self.env['account.move'].create(vals)
                self.cp_brokerage_invoice_id = invoice_id.id
                invoice_id.action_post()

    # spot booking invoice creation on registration confirm - this function is called in registration.py/action_confirm
    # changed because user can't cancel booking because of spot booking invoice
    def create_spot_booking_invoice(self):
        if self.source_of_booking == 'cp':
            if self.spot_booking:
                journal_id = self.env['account.journal'].search([('type', '=', 'spot_booking')], limit=1)
                if not journal_id:
                    raise UserError('Spot Booking Journal not found!')
                if not journal_id.profit_account_id or not journal_id.loss_account_id:
                    raise UserError('Account configurations missing in spot booking journal!')
                vals = {
                    'project_invoice_type': 'spot_booking',
                    'ref': '',
                    'move_type': 'entry',
                    'currency_id': self.env.company.currency_id.id,
                    'payment_reference': '',
                    'invoice_origin': self.name,
                    'company_id': self.env.company.id,
                    'l10n_in_gst_treatment': False,
                    'is_project_invoice': True,
                    'project_id': self.building.id,
                    'journal_id': journal_id.id,
                    'line_ids': [(0, 0, {
                        'account_id': journal_id.loss_account_id.id,
                        'partner_id': self.cp_employee_id.id,
                        'debit': self.spot_amount,
                        'credit': 0,
                        'currency_id': self.env.company.currency_id.id
                    }), (0, 0, {
                        'account_id': journal_id.profit_account_id.id,
                        'partner_id': self.cp_employee_id.id,
                        'debit': 0,
                        'credit': self.spot_amount,
                        'currency_id': self.env.company.currency_id.id
                    })]
                }
                invoice_id = self.env['account.move'].create(vals)
                self.spot_booking_invoice_id = invoice_id.id
                invoice_id.action_post()

    def action_draft(self):
        if self.state == 'confirmed':
            if self.env['project.registration'].search(
                    [('flat_id', '=', self.building_unit.id), ('state', 'not in', ['draft', 'canceled'])]):
                raise UserError('You cannot reset this booking since the flat is registered')
            if self.spot_booking_invoice_id or self.cp_brokerage_invoice_id:
                if self.spot_booking_invoice_id.invoice_payments_widget != 'false' or self.cp_brokerage_invoice_id.invoice_payments_widget != 'false':
                    raise UserError('You cannot reset this booking since payments exists for the invoices!')
        return super(Booking, self).action_draft()

    def action_cancel(self):
        if self.env['project.registration'].search([('flat_id', '=', self.building_unit.id), ('state', 'not in', ['draft', 'canceled'])]):
            raise UserError('You cannot cancel this booking since the flat is registered')
        if self.spot_booking_invoice_id or self.cp_brokerage_invoice_id:
            if self.spot_booking_invoice_id.invoice_payments_widget != 'false' or self.cp_brokerage_invoice_id.invoice_payments_widget != 'false':
                raise UserError('You cannot cancel this booking since payments exists for the invoices!')
        return super(Booking, self).action_cancel()

class BookingCancellationPopup(models.TransientModel):
    _inherit = 'booking.cancellation.popup'

    def action_booking_cancel(self):
        res = super(BookingCancellationPopup, self).action_booking_cancel()
        if self.booking_id.spot_booking_invoice_id:
            self.booking_id.spot_booking_invoice_id.button_draft()
            self.booking_id.spot_booking_invoice_id.button_cancel_inx()
        if self.booking_id.cp_brokerage_invoice_id:
            self.booking_id.cp_brokerage_invoice_id.button_draft()
            self.booking_id.cp_brokerage_invoice_id.button_cancel_inx()
        return res
