# -*- coding: utf-8 -*-
import json
import re

import requests
from pytz import timezone
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class UnitReservation(models.Model):
    _name = "unit.reservation"
    _description = "Booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    name = fields.Char('Booking No.', size=64, readonly=True, tracking=True)
    date = fields.Datetime('Booking Date', tracking=True)
    building = fields.Many2one('building', 'Project', tracking=True)

    @api.model
    def default_get(self, fields_list):
        res = super(UnitReservation, self).default_get(fields_list)
        res['date'] = datetime.now()
        return res

    # def read(self, fields=None, load='_classic_read'):
    #     res = super(UnitReservation, self).read(fields=fields, load=load)
    #     if len(res) == 1:
    #         if not self.env.user.has_group('project_transactions.view_all_projects'):
    #             employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
    #             if employee:
    #                 project = self.building
    #                 # allowed_employees = self.closing_manager_id + self.sourcing_manager_id + self.closing_tl_id \
    #                 #                     + self.sourcing_tl_id + self.crm_id + self.marketing_id
    #                 allowed_employees = project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
    #                                     + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
    #                                     + project.business_head_id + project.site_head_id + project.cluster_head_id
    #                 if employee.id not in allowed_employees.ids:
    #                     raise ValidationError('You have no access to this project!')
    #             else:
    #                 raise ValidationError('You have no access to this project!')
    #     return res

    template_id = fields.Many2one('installment.template', 'Payment Template', )
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user, )

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('contracted', 'Contracted'),
                              ('canceled', 'Canceled')
                              ], 'State', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    building_unit = fields.Many2one('product.template', 'Flat',
                                    domain=[('is_property', '=', True), ('state', '=', 'free')], required=True, tracking=True)
    flat_type = fields.Many2one('building.unit', 'Configuration', tracking=True)
    carpet_area = fields.Float(tracking=True)
    balcony_area = fields.Float(tracking=True)
    total_saleable_area = fields.Float('Total Saleable Sq. Ft', tracking=True)
    parking = fields.Boolean(tracking=True)
    source_of_booking = fields.Selection([('cp', 'CP'), ('direct', 'Direct'), ('referral_partner', 'Referral Partner')], tracking=True)
    source_of_booking_type = fields.Selection(
        [
            ('tele_call', 'Tele Call'),
            ('walk_in', 'Walk In'),
        ],
        string="Type",
        tracking=True,
        default='tele_call',
    )
    referral_partner_name = fields.Char(string="Referral Name", tracking=True)
    referral_partner_mobile = fields.Char(string="Referral Mobile", tracking=True)
    referral_partner_email = fields.Char(string="Referral Email", tracking=True)
    direct_type_id = fields.Many2one('booking.direct.type', 'Sub Source', tracking=True)
    cp_brokerage = fields.Float('CP Brokerage', tracking=True)
    referral_amount = fields.Float(tracking=True)
    referred_person = fields.Many2one('res.partner', domain=[('is_referrer', '=', True)], tracking=True)
    sq_ft_rate = fields.Float(tracking=True)
    flat_cost_real = fields.Float('Flat Cost', tracking=True)
    rom = fields.Boolean('ROM')
    rom_id = fields.Many2one('hr.employee', 'ROM')

    @api.constrains('referral_partner_mobile')
    def contact_fields_validation(self):
        for record in self:
            if record.referral_partner_mobile and not record.referral_partner_mobile.isdigit():
                raise ValidationError('Phone must contain only digits.')
            if record.referral_partner_mobile and not re.match(r'^\d{10}$', record.referral_partner_mobile):
                raise ValidationError('Mobile must be exactly 10 digits.')

    @api.onchange('flat_cost_real')
    def onchange_flat_cost_real(self):
        self.sq_ft_rate = self.flat_cost_real / self.total_saleable_area if self.total_saleable_area != 0 else 0

    @api.onchange('sq_ft_rate')
    def onchange_sq_ft_rate(self):
        self.flat_cost_real = self.total_saleable_area * self.sq_ft_rate

    @api.onchange('building')
    def onchange_project_id(self):
        self.building_unit = False
        self.rera_no = self.building.license_code
        self.developer_id = self.building.partner_id.id

    @api.onchange('building_unit')
    def onchange_flat(self):
        self.flat_type = self.building_unit.flat_type.id
        self.balcony_area = self.building_unit.balcony
        self.carpet_area = self.building_unit.carpet
        self.total_saleable_area = self.building_unit.saleable_area
        self.flat_cost = self.building_unit.flat_cost
        project_assigning = self.env['project.assigning.flats'].search([('flat_id', '=', self.building_unit.id)],
                                                                       limit=1)
        if project_assigning:
            self.cp_id = project_assigning.project_assigning_id.channel_partner
        prev_booking = self.env['unit.reservation'].search([('building_unit', '=', self.building_unit.id), ('id', '!=', self._origin.id), ('state', '=', 'draft')], order='date desc', limit=1)
        if prev_booking:
            booking_draft_checking_hours = self.env['ir.config_parameter'].sudo().get_param('itsys_real_estate.booking_draft_checking_hours')
            if booking_draft_checking_hours:
                booking_draft_checking_hours = int(booking_draft_checking_hours)
                difference = self.date - prev_booking.date
                hours_difference = difference.total_seconds() / 3600
                if booking_draft_checking_hours > hours_difference:
                    raise UserError(f'The flat has already been selected for another draft booking within {booking_draft_checking_hours} hours of the booking date.')
            return {'warning': {'title': _("Alert"), 'message': 'This flat is already selected for another draft booking!'}}

    partner_id = fields.Many2one('res.partner', 'Applicant Name', domain=[('is_tenant', '=', True)], tracking=True)
    attach_line = fields.One2many("reservation.attachment.line", "customer_reservation_id", "Documents")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    @api.onchange('partner_id')
    def fill_applicant_address(self):
        self.street = self.partner_id.street
        self.street2 = self.partner_id.street2
        self.zip = self.partner_id.zip
        self.city = self.partner_id.city
        self.state_id = self.partner_id.state_id.id
        self.country_id = self.partner_id.country_id.id

    co_partner_id = fields.Many2one('res.partner', 'Co-Applicant Name', domain=[('is_tenant', '=', True)], tracking=True)
    co_attach_line = fields.One2many("reservation.attachment.line", "co_customer_reservation_id", "Documents")
    co_street = fields.Char()
    co_street2 = fields.Char()
    co_zip = fields.Char(change_default=True)
    co_city = fields.Char()
    co_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                  domain="[('country_id', '=?', co_country_id)]")
    co_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    @api.onchange('co_partner_id')
    def fill_co_applicant_address(self):
        self.co_street = self.co_partner_id.street
        self.co_street2 = self.co_partner_id.street2
        self.co_zip = self.co_partner_id.zip
        self.co_city = self.co_partner_id.city
        self.co_state_id = self.co_partner_id.state_id.id
        self.co_country_id = self.co_partner_id.country_id.id

    cp_employee_id = fields.Many2one('res.partner', 'CP Employee Name', domain=[('is_channel_employee', '=', True)], tracking=True)
    cp_id = fields.Many2one('res.partner', 'CP Firm Name', domain=[('is_channel', '=', True)], tracking=True)
    developer_id = fields.Many2one('res.partner', 'Developer', domain=[('is_owner', '=', True)], tracking=True)
    rera_no = fields.Char('RERA No.', tracking=True)

    @api.onchange('cp_employee_id')
    def onchange_cp_employee(self):
        self.cp_id = self.cp_employee_id.parent_id.id

    spot_booking = fields.Boolean('CP Employee Spot Incentive', tracking=True)
    spot_percentage = fields.Float(tracking=True)
    spot_amount = fields.Float(tracking=True)

    # @api.depends('spot_booking', 'spot_percentage', 'flat_cost')
    # def compute_spot_amount(self):
    #     for rec in self:
    #         rec.spot_amount = 0
    #         if rec.spot_booking:
    #             rec.spot_amount = rec.flat_cost * rec.spot_percentage / 100

    infra_charge = fields.Float(tracking=True)
    other_charges = fields.Float(tracking=True)
    flat_cost = fields.Float('Agreement Value', tracking=True)
    stamp_duty_percentage = fields.Float(tracking=True, string='Stamp Duty %')
    stamp_duty = fields.Float(compute='compute_stamp_duty', string='Stamp Duty', store=True, tracking=True)
    gst_legal_charge = fields.Float(default=18, tracking=True, string='GST %')
    legal_charge = fields.Float(compute='compute_legal_charge', string='GST', store=True, tracking=True)
    registration_charge = fields.Float(tracking=True)
    net_amount = fields.Float('All Inclusive Amount', compute='compute_net_amount', store=True, tracking=True)

    @api.depends('gst_legal_charge', 'flat_cost')
    def compute_legal_charge(self):
        for rec in self:
            rec.legal_charge = rec.flat_cost * rec.gst_legal_charge / 100

    @api.depends('stamp_duty_percentage', 'flat_cost')
    def compute_stamp_duty(self):
        for rec in self:
            rec.stamp_duty = round(rec.flat_cost * rec.stamp_duty_percentage / 100)

    @api.onchange('sq_ft_rate', 'infra_charge', 'other_charges')
    def compute_agreement_value(self):
        self.flat_cost = self.total_saleable_area * self.sq_ft_rate + self.infra_charge + self.other_charges

    @api.depends('flat_cost', 'stamp_duty', 'legal_charge', 'registration_charge')
    def compute_net_amount(self):
        for rec in self:
            rec.net_amount = rec.flat_cost + rec.stamp_duty + rec.legal_charge + rec.registration_charge

    advance_amount = fields.Float(tracking=True)
    payment_mode = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], default='bank', tracking=True)
    payment_type = fields.Selection([('upi_id', 'UPI ID'), ('neft', 'NEFT'), ('imps', 'IMPS'), ('dd', 'DD')], tracking=True)
    document_number = fields.Char(tracking=True)
    document_date = fields.Date(tracking=True)

    payment_template_id = fields.Many2one('reservation.payment.template')
    payment_schedule_ids = fields.One2many('reservation.payment.schedule', 'reservation_id')

    @api.onchange('payment_template_id')
    def fill_payment_schedule_ids(self):
        self.payment_schedule_ids = False
        payment_data = []
        for line in self.payment_template_id.line_ids:
            installment = self.flat_cost * line.percentage / 100
            tds = installment * line.template_id.tds_percentage / 100
            gst = installment * line.template_id.gst / 100
            payment_data.append((0, 0, {
                'percentage': line.percentage,
                'payment_schedule': line.payment_schedule,
                'installment': installment,
                'tds': tds,
                'gst': gst,
                'net_amount': installment - tds + gst
            }))
        self.payment_schedule_ids = payment_data

    payment_schedule_monitoring_ids = fields.One2many('reservation.payment.schedule', 'monitoring_reservation_id')

    @api.onchange('payment_schedule_monitoring_ids', 'flat_cost')
    def onchange_payment_schedule_monitoring_ids(self):
        balance = self.flat_cost
        for line in self.payment_schedule_monitoring_ids:
            line.balance = balance - line.amount_total
            balance = line.balance

    if_loan = fields.Boolean(tracking=True)
    preferred_bank = fields.Char(tracking=True)
    required_amount = fields.Float(tracking=True)
    bank_person = fields.Char(tracking=True)
    mobile = fields.Char(tracking=True)

    if_offer = fields.Boolean(tracking=True)
    offer_details = fields.Text(tracking=True)

    booking_form_signed = fields.Boolean(tracking=True)
    cost_sheet_signed = fields.Boolean(tracking=True)
    received_photos = fields.Boolean(tracking=True)
    self_attested_pan_card = fields.Boolean('Self-Attested PAN Card', tracking=True)
    self_attested_aadhaar_card = fields.Boolean('Self-Attested Aadhaar Card', tracking=True)
    stamp_duty_collected = fields.Boolean(tracking=True)

    closing_manager_id = fields.Many2one('hr.employee', tracking=True)
    sourcing_manager_id = fields.Many2one('hr.employee', tracking=True)
    closing_tl_id = fields.Many2one('hr.employee', string='Closing TL', tracking=True)
    sourcing_tl_id = fields.Many2one('hr.employee', string='Sourcing TL', tracking=True)
    crm_id = fields.Many2one('hr.employee', string='CRM', tracking=True)
    marketing_id = fields.Many2one('hr.employee', tracking=True)

    @api.depends('building', 'rom')
    def _compute_employee_domain(self):
        for this in self:
            this.closing_manager_domain = json.dumps(([('id', 'in', this.building.closing_manager_ids.ids)]))
            this.closing_tl_domain = json.dumps(([('id', 'in', this.building.closing_tl_ids.ids)]))
            this.crm_domain = json.dumps(([('id', 'in', this.building.crm_ids.ids)]))
            this.marketing_domain = json.dumps(([('id', 'in', this.building.marketing_ids.ids)]))
            this.rom_domain = json.dumps(([('id', 'in', (this.building.sourcing_manager_ids + this.building.sourcing_tl_ids).ids)]))
            if this.rom:
                this.sourcing_manager_domain = json.dumps(([('is_rom', '=', True), ('role', '=', 'sourcing_manager')]))
                this.sourcing_tl_domain = json.dumps(([('is_rom', '=', True), ('role', '=', 'sourcing_tl')]))
            else:
                this.sourcing_manager_domain = json.dumps(([('id', 'in', this.building.sourcing_manager_ids.ids)]))
                this.sourcing_tl_domain = json.dumps(([('id', 'in', this.building.sourcing_tl_ids.ids)]))

    closing_manager_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    sourcing_manager_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    closing_tl_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    sourcing_tl_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    crm_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    marketing_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    rom_domain = fields.Char(compute="_compute_employee_domain", readonly=True, store=False)
    once_confirmed = fields.Boolean()
    flat_state = fields.Selection(related='building_unit.flat_state')
    jv_id = fields.Char()

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('You can not delete a reservation not in draft state'))
        super(UnitReservation, self).unlink()

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Reservation Number record must be unique !')
    ]

    def auto_cancel_reservation(self):
        pass

    def get_hr_partner_ids(self):
        param = self.env['ir.config_parameter'].sudo()
        mail_hr_users = param.get_param('itsys_real_estate.booking_reset_mail_users')
        if mail_hr_users:
            user_ids = mail_hr_users.replace('[', '').replace(']', '').split(',')
            partner_ids = self.env['res.users'].sudo().search([('id', 'in', [int(item) for item in user_ids])]).mapped('partner_id')
            return ','.join([str(item.id) for item in partner_ids])
        return False

    def get_crm_partner_id(self):
        param = self.env['ir.config_parameter'].sudo()
        enable_mail = param.get_param('itsys_real_estate.enable_booking_wo_registration_mail')
        if enable_mail:
            if self.crm_id:
                partner_id = self.crm_id.user_id.partner_id
                if partner_id:
                    return partner_id.id
        return False

    # Booking Form
    def action_draft(self):
        if self.state == 'confirmed':
            registration = self.env['project.registration'].search(
                [('flat_id', '=', self.building_unit.id), ('state', 'not in', ('draft', 'canceled'))])
            if registration:
                raise UserError('The flat is already registered!')
            # self.building_unit.state = 'free'
            self.building_unit.state = 'draft_booking'
            self.building_unit.booking_id = False
            self.once_confirmed = True
        param = self.env['ir.config_parameter'].sudo()
        enable_mail = param.get_param('itsys_real_estate.enable_booking_reset_mail')
        booking_reset_mail_users = param.get_param('itsys_real_estate.booking_reset_mail_users')
        if enable_mail and booking_reset_mail_users:
            template = self.env.ref('itsys_real_estate.booking_reset_alert_mail_template').sudo()
            template.send_mail(self.id, force_send=True)
        self.write({'state': 'draft'})

    # Booking Form
    def action_cancel(self):
        registration = self.env['project.registration'].search(
            [('flat_id', '=', self.building_unit.id), ('state', 'not in', ('draft', 'canceled'))])
        if registration:
            raise UserError('The flat is already registered!')
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Cancellation Reason'),
            'view_mode': 'form',
            'res_model': 'booking.cancellation.popup',
            'context': {'default_booking_id': self.id},
        }

    def get_actual_date_plus(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime - utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    def action_confirm(self):
        current_date = datetime.now()
        if not self.env.user.has_group('itsys_real_estate.group_booking_confirm_backdate') and not self.once_confirmed:
            backdate_allowed_days = self.env['ir.config_parameter'].sudo().get_param('itsys_real_estate.booking_backdate_allowed_days')
            if backdate_allowed_days:
                backdate_allowed_days = int(backdate_allowed_days)
            else:
                backdate_allowed_days = 0
            allowed_days_before = current_date - timedelta(days=backdate_allowed_days)
            booking_date = datetime.strptime(self.get_actual_date_plus(self.date.strftime('%Y-%m-%d %H:%M:%S')), "%Y-%m-%d %H:%M:%S").date()
            allowed_days_before = datetime.strptime(self.get_actual_date_plus(allowed_days_before.strftime('%Y-%m-%d %H:%M:%S')), "%Y-%m-%d %H:%M:%S").date()
            if booking_date < allowed_days_before:
                raise UserError('Booking backdate is not allowed!')
        if self.date > current_date:
            raise UserError('Future Dates are not allowed')
        if self.building_unit.state == 'reserved':
            raise UserError('The selected flat is already booked')
        if self.building_unit.state == 'sold':
            raise UserError('The selected flat is already registered')
        self.building_unit.booking_id = self.id
        self.building_unit.state = 'reserved'
        self.once_confirmed = True
        self.write({'state': 'confirmed', 'cancellation_reason': False})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('unit.reservation')
        new_id = super(UnitReservation, self).create(vals)
        new_id.building_unit.state = 'draft_booking'
        return new_id

    def write(self, vals):
        initial_unit = self.building_unit
        res = super(UnitReservation, self).write(vals)
        if self.state == 'draft':
            if initial_unit != self.building_unit:
                initial_unit.state = 'free'
                self.building_unit.state = 'draft_booking'
        return res

    cancellation_reason = fields.Many2one('booking.cancellation.reason', tracking=True)
    cancellation_notes = fields.Text()
    cancellation_date = fields.Date(tracking=True)

    def get_from_mail(self):
        mail_server = self.env['ir.mail_server'].search([('active', '=', True)], limit=1)
        if mail_server:
            return mail_server.smtp_user
        return False

    def send_mail_to_crm(self):
        param = self.env['ir.config_parameter'].sudo()
        enable_mail = param.get_param('itsys_real_estate.enable_booking_wo_registration_mail')
        frequency = param.get_param('itsys_real_estate.booking_wo_registration_mail_frequency')
        if enable_mail and frequency:
            today = datetime.now().date()
            bookings = self.env['unit.reservation'].search([('state', '=', 'confirmed')])
            for booking in bookings:
                registration = self.env['project.registration'].search(
                    [('flat_id', '=', booking.building_unit.id), ('state', 'not in', ('draft', 'canceled'))])
                if not registration and booking.crm_id.user_id:
                    booking_date = booking.date.date()
                    days_since_booking = (today - booking_date).days
                    if days_since_booking % int(frequency) == 0:
                        template = self.env.ref('itsys_real_estate.booking_wo_registration_mail_template').sudo()
                        template.send_mail(booking.id, force_send=True)


class BookingCancellationPopup(models.TransientModel):
    _name = 'booking.cancellation.popup'

    reason = fields.Many2one('booking.cancellation.reason')
    booking_id = fields.Many2one('unit.reservation')
    notes = fields.Text(' ')
    date = fields.Date()

    @api.model
    def default_get(self, fields):
        res = super(BookingCancellationPopup, self).default_get(fields)
        res['date'] = datetime.today()
        return res

    def action_booking_cancel(self):
        if not self.env.user.has_group('itsys_real_estate.group_booking_cancel_anytime'):
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            day_before_yesterday = today - timedelta(days=2)
            if self.date != today and self.date != yesterday and self.date != day_before_yesterday:
                raise UserError('Date should be today, yesterday or the day before yesterday!')
        self.booking_id.building_unit.state = 'free'
        self.booking_id.building_unit.booking_id = False
        self.booking_id.write({
            'state': 'canceled',
            'cancellation_reason': self.reason,
            'cancellation_notes': self.notes,
            'cancellation_date': self.date,
            'once_confirmed': True
        })
        param = self.env['ir.config_parameter'].sudo()
        out_api = param.get_param('real_estate_extension.enable_booking_cancel_api')
        if out_api:
            booking = self.booking_id
            params = {
                'project': booking.building.code or '',
                'jv_id': booking.jv_id or '',
                'flat': booking.building_unit.name or '',
                'customer': booking.partner_id.jv_cid or '',
                'cancellation_date': self.date.strftime('%d/%m/%Y'),
                'cancellation_reason': self.reason.name or '',
                'cancellation_notes': self.notes or '',
                'booking_no': booking.name or ''
            }
            url = self.env['ir.config_parameter'].sudo().get_param(
                'real_estate_extension.booking_cancel_api_url')
            username = self.env['ir.config_parameter'].sudo().get_param(
                'real_estate_extension.booking_cancel_api_username')
            password = self.env['ir.config_parameter'].sudo().get_param(
                'real_estate_extension.booking_cancel_api_key')

            data = {
                'params': {
                    'login': username,
                    'password': password,
                    'record': params
                }
            }
            code = ''
            try:
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post(url, headers=headers, json=data)
                if response.ok:
                    rec = json.loads(response.text)
                    if rec.get('status') == 200:
                        code = rec.get('status')
                        response = response.content
                        status = 'success'
                        pass
                    else:
                        raise ValidationError(str(rec))
                else:
                    raise ValidationError(str(response.text))
            except Exception as e:
                response = e
                status = 'failed'
                pass
            self.env['api.log'].sudo().create({
                'record': str(booking.id),
                'code': code,
                'response': response,
                'date': datetime.now(),
                'type': 'booking',
                'status': status,
                'name': booking.name,
                'direction': 'out',
                'args': data
            })


class BookingCancellationReason(models.Model):
    _name = 'booking.cancellation.reason'

    name = fields.Char('Reason')


class BookingDirectType(models.Model):
    _name = 'booking.direct.type'

    name = fields.Char()
    code = fields.Char()


class ReservationPaymentSchedule(models.Model):
    _name = 'reservation.payment.schedule'
    _description = 'Payment Schedule'

    reservation_id = fields.Many2one('unit.reservation', ondelete='cascade')
    percentage = fields.Float('% of Payment')
    payment_schedule = fields.Char()
    installment = fields.Float()
    tds = fields.Float('TDS')
    gst = fields.Float('GST')
    net_amount = fields.Float()
    payment_date = fields.Date()

    monitoring_reservation_id = fields.Many2one('unit.reservation', ondelete='cascade')
    date = fields.Date()
    mode = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], default='bank')
    description = fields.Char()
    ocr = fields.Float('OCR')
    bank_payment = fields.Float()
    amount_total = fields.Float('Net Amount', compute='_compute_amount_total')
    balance = fields.Float()

    @api.depends('ocr', 'bank_payment', 'gst')
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = rec.ocr + rec.bank_payment


class ReservationAttachmentLine(models.Model):
    _name = 'reservation.attachment.line'
    _description = 'Customer Attachments'

    name = fields.Char('Name', required=True)
    file = fields.Binary('File', required=True)
    customer_reservation_id = fields.Many2one('unit.reservation', '', ondelete='cascade', readonly=True)
    co_customer_reservation_id = fields.Many2one('unit.reservation', '', ondelete='cascade', readonly=True)
    view_file_toggle = fields.Boolean()
    editable = fields.Boolean(compute='check_line_editable')

    @api.depends('customer_reservation_id', 'co_customer_reservation_id')
    def check_line_editable(self):
        for rec in self:
            rec.editable = True
            if rec.id:
                if rec.customer_reservation_id and rec.customer_reservation_id.state == 'confirmed':
                    rec.editable = False
                if rec.co_customer_reservation_id and rec.co_customer_reservation_id.state == 'confirmed':
                    rec.editable = False

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


class ReservationPaymentTemplate(models.Model):
    _name = 'reservation.payment.template'
    _description = 'Reservation Payment Template'

    name = fields.Char()
    line_ids = fields.One2many('reservation.template.line', 'template_id')
    tds_percentage = fields.Float('TDS %')
    gst = fields.Float('GST')

    @api.model
    def create(self, values):
        res = super(ReservationPaymentTemplate, self).create(values)
        if sum(res.line_ids.mapped('percentage')) != 100:
            raise UserError('Total % of payment should be 100')
        return res

    def write(self, vals):
        res = super(ReservationPaymentTemplate, self).write(vals)
        if sum(self.line_ids.mapped('percentage')) != 100:
            raise UserError('Total % of payment should be 100')
        return res


class ReservationTemplateLine(models.Model):
    _name = 'reservation.template.line'
    _description = 'Reservation Payment Template Lines'

    template_id = fields.Many2one('reservation.payment.template')
    percentage = fields.Float('% of Payment')
    payment_schedule = fields.Char()


class LoanLineRs(models.Model):
    _name = 'loan.line.rs'
    _order = 'serial'

    date = fields.Date('Date')
    name = fields.Char('Name')
    serial = fields.Integer('#')
    empty_col = fields.Char(' ', readonly=True)
    amount = fields.Float('Payment', digits=(16, 4), )
    paid = fields.Boolean('Paid')
    contract_partner_id = fields.Many2one(related='loan_id.partner_id', string="Partner")
    contract_building = fields.Many2one(related='loan_id.building', string="Building")
    contract_building_unit = fields.Many2one(related='loan_id.building_unit', string="Building Unit")
    loan_id = fields.Many2one('unit.reservation', '', ondelete='cascade', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
