import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = fields.Date('D.O.B')
    rera_number = fields.Char('RERA No')
    is_channel = fields.Boolean(default=False)
    is_channel_employee = fields.Boolean(default=False)
    # is_developer = fields.Boolean(default=False)
    is_vendor = fields.Boolean(default=False)
    developer_code = fields.Char('Developer ID')
    pan_number = fields.Char()
    aadhar_number = fields.Char()
    declaration = fields.Char()
    contact_person_name = fields.Char('Contact Person')
    # service_type = fields.Char()
    owner_name = fields.Char()
    channel_id = fields.Char()
    parent_channel_id = fields.Char()
    bank_name = fields.Char()
    ifsc_code = fields.Char('IFSC Code')
    account_number = fields.Char()
    income = fields.Float('Income per Annum')
    cp_employee_id = fields.Char('CP Employee Id')
    service_type = fields.Char()
    vendor_code = fields.Char('Vendor ID')
    tds_applicable = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'TDS Applicable', default='no')
    customer_code = fields.Char('Customer ID')
    credit_days = fields.Integer()
    region_id = fields.Many2many('regions')
    is_employee = fields.Boolean(compute='compute_is_employee', search='_search_is_employee', store=True)
    msmf_registered = fields.Boolean()
    msmf_value = fields.Char()
    jv_cid = fields.Char()
    jv_cp_id = fields.Char()
    jv_cpe_id = fields.Char()

    @api.constrains('phone', 'mobile')
    def contact_fields_validation(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError('Phone must contain only digits.')
            if record.mobile and not re.match(r'^\d{10}$', record.mobile):
                raise ValidationError('Mobile must be exactly 10 digits.')

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = partner.name

    def compute_is_employee(self):
        for rec in self:
            rec.is_employee = False
            if rec.id:
                employee_count = self.env['hr.employee'].search_count([('partner_id', '=', rec.id)])
                if employee_count > 0:
                    rec.is_employee = True

    def _search_is_employee(self, operator, value):
        employees = self.env['hr.employee'].search([('partner_id', '!=', False)])
        partner_ids = employees.mapped('partner_id')
        return [('id', 'in', partner_ids.ids)]

    _sql_constraints = [
        ('channel_id_unique', 'unique (channel_id)', 'The channel id already exists!'),
    ]

    @api.model
    def default_get(self, fields_list):
        res = super(Customer, self).default_get(fields_list)
        res['country_id'] = self.env.company.country_id.id
        res['state_id'] = self.env.company.state_id.id
        return res

    def _fields_sync(self, values):
        if self.is_channel_employee:
            return
        return super(Customer, self)._fields_sync(values)

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        if self.is_channel_employee:
            return
        return super(Customer, self).onchange_parent_id()

    @api.onchange('parent_id')
    def fill_parent_channel_id(self):
        if self.is_channel_employee:
            self.parent_channel_id = self.parent_id.channel_id

    @api.model
    def setting_init_bank_account_action(self):
        """ Called by the 'Bank Accounts' button of the setup bar."""
        view_id = self.env.ref('account.setup_bank_account_wizard').id
        return {'type': 'ir.actions.act_window',
                'name': _('Create a Bank Account'),
                'res_model': 'account.setup.bank.manual.config',
                'target': 'new',
                'view_mode': 'form',
                'views': [[view_id, 'form']],
                }
