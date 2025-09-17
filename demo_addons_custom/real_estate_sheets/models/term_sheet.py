from odoo import models, fields, api
from odoo.exceptions import UserError


class TermSheet(models.Model):
    _name = 'term.sheet'
    _inherit = ['mail.thread']
    _description = 'Term Sheet'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')
    form_editable = fields.Boolean(compute='compute_form_editable', default=True)

    @api.depends('state')
    def compute_form_editable(self):
        for rec in self:
            rec.form_editable = True
            if rec.state == 'confirmed' and not self.env.user.has_group(
                    'real_estate_sheets.group_evaluation_budgeting_confirm'):
                rec.form_editable = False

    def get_from_mail(self):
        mail_server = self.env['ir.mail_server'].search([('active', '=', True)], limit=1)
        if mail_server:
            return mail_server.smtp_user
        return False

    def get_hr_partner_ids(self):
        param = self.env['ir.config_parameter'].sudo()
        mail_hr_users = param.get_param('itsys_real_estate.term_sheet_mail_users')
        if mail_hr_users:
            user_ids = mail_hr_users.replace('[', '').replace(']', '').split(',')
            partner_ids = self.env['res.users'].sudo().search([('id', 'in', [int(item) for item in user_ids])]).mapped('partner_id')
            return ','.join([str(item.id) for item in partner_ids])
        return False

    def action_confirm(self):
        param = self.env['ir.config_parameter'].sudo()
        enable_mail = param.get_param('itsys_real_estate.enable_term_sheet_mail')
        term_sheet_mail_users = param.get_param('itsys_real_estate.term_sheet_mail_users')
        for rec in self:
            if enable_mail and term_sheet_mail_users:
                template = self.env.ref('real_estate_sheets.term_sheet_alert_mail_template').sudo()
                template.send_mail(rec.id, force_send=True)
            rec.state = 'confirmed'

    developer_id = fields.Many2one('res.partner', 'Name of Developer', domain=[('is_owner', '=', True)])
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    promoter = fields.Char()
    name = fields.Char('Project Name', required=True)
    site_address = fields.Text('Project Site Address')
    average_price = fields.Float()
    date = fields.Date()
    signing_amount = fields.Float()
    retainer_fee = fields.Float()
    duration = fields.Integer()
    template_head = fields.Html(compute='compute_template_head')
    template = fields.Html()
    director_justo = fields.Char('Director (JUSTO)')
    director_developer = fields.Char('Director (Developer)')
    template_id = fields.Many2one('term.sheet.template')
    evaluation_sheet_id = fields.Many2one('evaluation.sheet', domain="[('developer_id', '=?', developer_id)]")
    market_budgeting_percentage = fields.Float('Marketing Budgeting %')
    tenure = fields.Integer()
    extend = fields.Integer()
    crm_fees_applicable = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    avg_rate_sq_ft = fields.Integer()

    @api.depends('name', 'developer_id', 'site_address', 'street', 'street2', 'zip', 'city', 'state_id', 'country_id',
                 'promoter')
    def compute_template_head(self):
        for rec in self:
            rec.template_head = self.env.ref('real_estate_sheets.term_sheet_header_template')._render({
                'o': rec
            })

    @api.onchange('evaluation_sheet_id')
    def onchange_evaluation_sheet(self):
        if self.evaluation_sheet_id:
            if self.env['term.sheet'].search([('evaluation_sheet_id', '=', self.evaluation_sheet_id.id)]):
                self.evaluation_sheet_id = False
                raise UserError('Term Sheet with evaluation sheet already exists!')
        self.name = self.evaluation_sheet_id.project_name
        self.developer_id = self.evaluation_sheet_id.developer_id
        self.average_price = self.evaluation_sheet_id.tentative_unit_sales_price
        self.retainer_fee = self.evaluation_sheet_id.retainer_fee
        self.signing_amount = self.evaluation_sheet_id.signing_amount

    @api.onchange('developer_id')
    def onchange_developer(self):
        self.street = self.developer_id.street
        self.street2 = self.developer_id.street2
        self.zip = self.developer_id.zip
        self.city = self.developer_id.city
        if self.developer_id:
            self.state_id = self.developer_id.state_id
            self.country_id = self.developer_id.country_id
        else:
            self.state_id = self.env.company.state_id
            self.country_id = self.env.company.country_id

    @api.onchange('template_id')
    def apply_template(self):
        self.template = False
        if self.template_id:
            self.template = self.template_id.template
