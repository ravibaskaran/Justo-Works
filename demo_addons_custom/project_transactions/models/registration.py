from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ProjectRegistration(models.Model):
    _name = 'project.registration'
    _inherit = ['mail.thread']
    _description = 'Registration'

    name = fields.Char(default='Draft', string='Reg Number')
    customer_id = fields.Many2one('res.partner', 'Customer Name', domain=[('is_tenant', '=', True)])  # todo add context
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    @api.onchange('customer_id')
    def fill_customer_address(self):
        self.street = self.customer_id.street
        self.street2 = self.customer_id.street2
        self.zip = self.customer_id.zip
        self.city = self.customer_id.city
        self.state_id = self.customer_id.state_id.id
        self.country_id = self.customer_id.country_id.id

    project_id = fields.Many2one('building')
    cp_id = fields.Many2one('res.partner', 'Channel Partner', domain=[('is_channel', '=', True)])
    flat_id = fields.Many2one('product.template')  # todo: add domain and context
    total_saleable_area = fields.Float()
    unit_type = fields.Many2one('building.unit')
    closing_manager = fields.Many2one('hr.employee')
    booking_id = fields.Many2one('unit.reservation')

    # def read(self, fields=None, load='_classic_read'):
    #     res = super(ProjectRegistration, self).read(fields=fields, load=load)
    #     if len(res) == 1:
    #         if not self.env.user.has_group('project_transactions.view_all_projects'):
    #             employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
    #             if employee:
    #                 # project = self.project_id
    #                 booking = self.env['unit.reservation'].search(
    #                     [('building_unit', '=', self.flat_id.id), ('state', 'not in', ('draft', 'cancel'))], limit=1)
    #                 allowed_employees = booking.closing_manager_id + booking.sourcing_manager_id + booking.closing_tl_id \
    #                                     + booking.sourcing_tl_id + booking.crm_id + booking.marketing_id
    #                 # allowed_employees = project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
    #                 #                     + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
    #                 #                     + project.business_head_id + project.site_head_id + project.cluster_head_id
    #                 if employee.id not in allowed_employees.ids:
    #                     raise ValidationError('You have no access to this project!')
    #             else:
    #                 raise ValidationError('You have no access to this project!')
    #     return res

    @api.onchange('customer_id')
    def onchange_customer(self):
        booking = self.env['unit.reservation'].search(
            [('partner_id', '=', self.customer_id.id), ('state', '=', 'confirmed')])
        if not self.flat_id:
            if len(booking) == 1:
                self.flat_id = booking.building_unit.id
        if booking:
            return {'domain': {
                'flat_id': [
                    ('id', 'in', booking.mapped('building_unit').filtered(lambda l: l.state == 'reserved').ids)]}}

    @api.onchange('flat_id')
    def onchange_flat(self):
        if self.flat_id:
            if self.flat_id.flat_state == 'rtb':
                raise UserError('The flat is in RTB status')
            self.project_id = self.flat_id.building_id.id
            booking = self.env['unit.reservation'].search(
                [('building_unit', '=', self.flat_id.id), ('state', '=', 'confirmed')])
            self.total_saleable_area = self.flat_id.saleable_area
            self.unit_type = self.flat_id.flat_type.id
            project_assigning = self.env['project.assigning.flats'].search([('flat_id', '=', self.flat_id.id)],
                                                                           limit=1)
            if project_assigning:
                self.cp_id = project_assigning.project_assigning_id.channel_partner.id
                self.closing_manager = project_assigning.project_assigning_id.closing_manager.id
            if len(booking) == 1:
                self.booking_id = booking.id
                self.cp_id = booking.cp_id.id
                self.customer_id = booking.partner_id.id
                self.co_customer_id = booking.co_partner_id.id
                self.closing_manager = booking.closing_manager_id.id
            else:
                self.booking_id = False
                self.customer_id = False
                self.cp_id = False
                self.co_customer_id = 0
        else:
            self.booking_id = False
            self.customer_id = False
            self.cp_id = False
            self.co_customer_id = 0

    co_customer_id = fields.Many2one('res.partner', 'Customer Name (Co-applicant)',
                                     domain=[('is_tenant', '=', True)])  # todo add context
    co_street = fields.Char()
    co_street2 = fields.Char()
    co_zip = fields.Char(change_default=True)
    co_city = fields.Char()
    co_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                  domain="[('country_id', '=?', co_country_id)]")
    co_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    @api.onchange('co_customer_id')
    def fill_co_customer_address(self):
        self.co_street = self.co_customer_id.street
        self.co_street2 = self.co_customer_id.street2
        self.co_zip = self.co_customer_id.zip
        self.co_city = self.co_customer_id.city
        self.co_state_id = self.co_customer_id.state_id.id
        self.co_country_id = self.co_customer_id.country_id.id

    registration_date = fields.Date()
    registration_document_number = fields.Char()
    notes = fields.Html()
    attach_line = fields.One2many("registration.attachment.line", "registration_id", "Documents")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled'), ('invoiced', 'Invoiced')],
                             default='draft', string='Status')
    invoice_id = fields.Many2one('account.move')

    def action_confirm(self):
        if self.registration_date > datetime.now().date():
            raise UserError('Future dates are not allowed')
        if self.flat_id.state == 'sold':
            raise UserError('The selected flat is already registered')
        if self.flat_id.state == 'free':
            raise UserError('The selected flat is not booked')
        self.flat_id.state = 'sold'
        self.name = self.env['ir.sequence'].next_by_code('sequence.registration')
        not_sold = self.env['product.template'].search(
            [('building_id', '=', self.project_id.id), ('state', '!=', 'sold'), ('is_property', '=', True)])
        if not not_sold:
            self.project_id.project_status = 'closed'
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        if self.flat_id.state == 'sold':
            self.flat_id.state = 'reserved'

        # Reset Spot Booking Invoices to Draft
        booking = self.env['unit.reservation'].search([
            ('building_unit', '=', self.flat_id.id),
            ('state', 'not in', ('draft', 'canceled'))
        ], limit=1)

        if booking:
            # Find the spot booking invoice
            spot_booking_invoices = booking.spot_booking_invoice_id

            # Reset invoices to draft before canceling
            if spot_booking_invoices:
                if spot_booking_invoices.state == 'posted':
                    spot_booking_invoices.button_draft()  # Reset invoice to draft
                if spot_booking_invoices.state == 'draft':
                    spot_booking_invoices.button_cancel_voucher()
                booking.spot_booking_invoice_id = None

                # --- Cancel CP Brokerage Invoice ---
            cp_brokerage_invoices = booking.cp_brokerage_invoice_id

            if cp_brokerage_invoices:
                if cp_brokerage_invoices.state == 'posted':
                    cp_brokerage_invoices.button_draft()  # Reset to draft
                if cp_brokerage_invoices.state == 'draft':
                    cp_brokerage_invoices.button_cancel_voucher()
                booking.cp_brokerage_invoice_id = None

            # ----- Developer Invoice ------
            developer_invoice = self.developer_invoice_id
            if developer_invoice:
                if developer_invoice.state == 'posted':
                    developer_invoice.button_draft()
                # if developer_invoice.state == 'draft':
                #     developer_invoice.button_cancel_voucher()
                # self.developer_invoice_id = None

        self.write({'state': 'canceled'})

            # cp_brokerage_invoices = self.env['account.move'].search([
            #     ('id', 'in', booking.cp_brokerage_invoice_id.ids),  # Ensure correct field for CP invoices
            #     ('state', '=', 'posted')
            # ])
            # for invoice in cp_brokerage_invoices:
            #     invoice.button_draft()  # Reset to draft
            #     invoice.button_cancel_voucher()  # Cancel invoice

        # Cancel Incentive Invoices
        # incentive_invoices = self.env['account.move'].search([
        #     ('project_id', '=', self.project_id.id),
        #     ('move_type', '=', 'out_invoice'),
        #     ('state', '=', 'posted'),
        #     ('is_project_invoice', '=', True)
        # ])
        # for invoice in incentive_invoices:
        #     invoice.button_cancel()  # Cancels posted invoices
        #
        # # Cancel Brokerage & Spot Booking Invoices
        # booking = self.env['unit.reservation'].search([
        #     ('building_unit', '=', self.flat_id.id),
        #     ('state', 'not in', ('draft', 'canceled'))
        # ], limit=1)

        # if booking:
        #     booking.cancel_cp_brokerage_invoice()  # Assuming this method exists
        #     booking.cancel_spot_booking_invoice()  # Assuming this method exists

        # Cancel Developer Invoice
        # if self.developer_invoice_id and self.developer_invoice_id.state == 'posted':
        #     self.developer_invoice_id.button_cancel()

        # Reopen Project if Needed
        # project_flats = self.env['product.template'].search([
        #     ('building_id', '=', self.project_id.id),
        #     ('state', '=', 'sold'),
        #     ('is_property', '=', True)
        # ])
        # if project_flats and self.project_id.project_status == 'closed':
        #     self.project_id.project_status = 'open'




    # def view_invoice(self):
    #     form_view_id = self.env.ref("account.view_move_form").id
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Invoice',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'account.move',
    #         'views': [(form_view_id, 'form')],
    #         'res_id': self.invoice_id.id,
    #     }

    # def _prepare_invoice_values(self, amount, product_id):
    #     invoice_vals = {
    #         'ref': self.flat_id.name,
    #         'move_type': 'out_invoice',
    #         # 'invoice_origin': '',
    #         'invoice_user_id': self.env.uid,
    #         'partner_id': self.project_id.partner_id.id,
    #         'currency_id': self.env.company.currency_id.id,
    #         'partner_bank_id': self.env.company.partner_id.bank_ids[:1].id,
    #         'invoice_line_ids': [(0, 0, {
    #             'name': product_id.name,
    #             'price_unit': amount,
    #             'quantity': 1.0,
    #             'product_id': product_id.id,
    #             'tax_ids': [(6, 0, product_id.taxes_id.ids)],
    #         })],
    #     }
    #
    #     return invoice_vals

    # def action_create_invoice(self):
    #     booking = self.env['unit.reservation'].search([('building_unit', '=', self.flat_id.id),
    #                                                    ('state', '=', 'confirmed')], limit=1)
    #     amount = booking.flat_cost
    #     product_id = int(self.env['ir.config_parameter'].sudo().get_param('project_transactions.incentive_product_id'))
    #     product = self.env['product.product'].browse(product_id)
    #     invoice_vals = self._prepare_invoice_values(amount, product)
    #     invoice = self.env['account.move'].with_company(self.env.company).sudo().create(invoice_vals).with_user(
    #         self.env.uid)
    #     invoice.action_post()
    #     self.invoice_id = invoice.id
    #     self.state = 'invoiced'


class RegistrationAttachmentLine(models.Model):
    _name = 'registration.attachment.line'
    _description = 'Registration Attachments'

    name = fields.Char('Name', required=True)
    file = fields.Binary('File', required=True)
    registration_id = fields.Many2one('project.registration', '', ondelete='cascade')
    view_file_toggle = fields.Boolean()

    def download_file(self):
        self.env.cr.execute(
            "select id from ir_attachment where res_model='" + str(self._name) + "' and res_id=" + str(self.id))
        attachment_id = self.env.cr.fetchone()[0] or None
        if attachment_id:
            attachment = self.env['ir.attachment'].sudo().browse(attachment_id)
            if attachment:
                action = {
                    'type': 'ir.actions.act_url',
                    'url': "web/content/?model=ir.attachment&id=" + str(
                        attachment.id) + "&filename_field=name&field=datas&download=true&name=" + str(
                        attachment.store_fname),
                    'target': 'self'
                }
                return action
