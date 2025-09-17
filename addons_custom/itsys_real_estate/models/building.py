# -*- coding: utf-8 -*-
from datetime import datetime, date
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _


class Building(models.Model):
    _name = "building"
    _description = "Project"
    _inherit = ['mail.thread']

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('building')
        new_id = super(Building, self).create(vals)
        return new_id

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            for record in self:
                booking_count = self.env['unit.reservation'].search_count([('building', '=', record.id)])
                if booking_count > 0:
                    raise ValidationError(_("You cannot archive this project because it has active bookings."))

        return super(Building, self).write(vals)

    attach_line = fields.One2many("building.attachment.line", "building_attach_id", "Documents")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    region_id = fields.Many2one('regions', 'Region', )
    account_income = fields.Many2one('account.account', 'Income Account', )
    account_analytic_id = fields.Many2one('account.analytic.account', 'Cost Center')
    active = fields.Boolean('Active',
                            help="If the active field is set to False, it will allow you to hide the top without removing it.",
                            default=True, tracking=True)
    alarm = fields.Boolean('Alarm')
    old_building = fields.Boolean('Old Property')
    constructed = fields.Date('Construction Date')
    no_of_floors = fields.Integer('Floors')
    props_per_floors = fields.Integer('Unit per Floor')
    category = fields.Char('Category', size=16)
    description = fields.Text('Description')
    floor = fields.Char('Floor', size=16)
    pricing = fields.Float('Average Price', )
    balcony = fields.Integer('Balconies Sq.Ft', )
    building_area = fields.Float('Property Area Sq.Ft', )
    land_area = fields.Float('Land Area Sq.Ft', )
    garden = fields.Float('Garden Sq.Ft', )
    terrace = fields.Float('Terraces Sq.Ft', )
    garage = fields.Integer('Garage included')
    carport = fields.Integer('Carport included')
    parking_place_rentable = fields.Boolean('Parking rentable', help="Parking rentable in the location if available")
    handicap = fields.Boolean('Handicap Accessible')
    heating = fields.Selection([('unknown', 'unknown'),
                                ('none', 'none'),
                                ('tiled_stove', 'tiled stove'),
                                ('stove', 'stove'),
                                ('central', 'central heating'),
                                ('self_contained_central', 'self-contained central heating')], 'Heating')
    heating_source = fields.Selection([('unknown', 'unknown'),
                                       ('electricity', 'Electricity'),
                                       ('wood', 'Wood'),
                                       ('pellets', 'Pellets'),
                                       ('oil', 'Oil'),
                                       ('gas', 'Gas'),
                                       ('district', 'District Heating')], 'Heating Source')
    internet = fields.Boolean('Internet')
    lease_target = fields.Integer('Target Lease', )
    lift = fields.Integer('Passenger Elevators')
    lift_f = fields.Integer('Freight Elevators')
    name = fields.Char('Project Name', size=64, required=True)
    code = fields.Char('Code', size=16)
    note = fields.Html('Notes')
    note_sales = fields.Text('Note Sales Folder')
    partner_id = fields.Many2one('res.partner', 'Developer', )
    configuration_ids = fields.Many2many('building.unit', 'project_building_unit_rel', 'project_id', 'config_id')
    type = fields.Many2one('building.type', 'Property Type', )
    residential_commercial = fields.Selection([('residential', 'Residential'), ('commercial', 'Commercial')],
                                              related='type.type')
    status = fields.Many2one('building.status', 'Property Status', )
    purchase_date = fields.Date('Project Starting Date')
    launch_date = fields.Date('Closing Date')

    @api.onchange('purchase_date', 'launch_date')
    def _check_dates(self):
        for record in self:
            if record.purchase_date and record.launch_date:
                if record.purchase_date > record.launch_date:
                    raise ValidationError("The project closing date cannot be before the project starting date.")

    rooms = fields.Char('Rooms', size=32)
    solar_electric = fields.Boolean('Solar Electric System')
    solar_heating = fields.Boolean('Solar Heating System')
    staircase = fields.Char('Staircase', size=8)
    surface = fields.Integer('Surface')
    telephone = fields.Boolean('Telephone')
    tv_cable = fields.Boolean('Cable TV')
    tv_sat = fields.Boolean('SAT TV')
    usage = fields.Selection([('unlimited', 'unlimited'),
                              ('office', 'Office'),
                              ('shop', 'Shop'),
                              ('flat', 'Flat'),
                              ('rural', 'Rural Property'),
                              ('parking', 'Parking')], 'Usage')
    sort = fields.Integer('Sort')
    sequence = fields.Integer('Sequ.')
    air_condition = fields.Selection([('unknown', 'Unknown'),
                                      ('central', 'Central'),
                                      ('partial', 'Partial'),
                                      ('none', 'None'),
                                      ], 'Air Condition')
    address = fields.Text('Address')
    license_code = fields.Char('RERA No.', size=16)
    license_date = fields.Date('License Date')
    date_added = fields.Date('Date Added to Notarization')
    license_location = fields.Char('License Notarization')
    electricity_meter = fields.Char('Electricity meter', size=16)
    water_meter = fields.Char('Water meter', size=16)
    north = fields.Char('Northen border by:')
    south = fields.Char('Southern border by:')
    east = fields.Char('Eastern border  by: ')
    west = fields.Char('Western border by: ')
    unit_ids = fields.Many2many('product.template', string='Properties')
    property_floor_plan_image_ids = fields.One2many('floor.plans', 'building_id', string="Floor Plans", copy=True)
    building_image_ids = fields.One2many('building.images', 'building_id', string="Building Images", copy=True)

    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    sub_region_id = fields.Many2one('regions', string='Cluster')
    remarks = fields.Char()
    wings = fields.Integer()
    promoter_name = fields.Char("Promoter's Name")
    reg_office_address = fields.Text('Registered Office Address')
    site_address = fields.Text()
    cluster_head_id = fields.Many2one('hr.employee', 'Cluster Head')
    business_head_id = fields.Many2one('hr.employee', 'Business Head')
    site_head_id = fields.Many2one('hr.employee', 'Site Head')
    residential_carpet_area = fields.Float('Total Residential Carpet Area')
    commercial_carpet_area = fields.Float('Total Commercial Carpet Area')
    gst_number = fields.Char('GST Number')
    pan_number = fields.Char('PAN Number')
    bank_details = fields.Char()
    apf_details = fields.Char('APF Details')
    residential_saleable_area = fields.Float('Residential Saleable Area')
    commercial_saleable_area = fields.Float('Commercial Saleable Area')
    total_inventory = fields.Integer(compute='compute_inventory_count')
    available_inventory_count = fields.Integer(compute='compute_inventory_count', string='Available Inventory')
    pin_code = fields.Char()

    closing_manager_ids = fields.Many2many('hr.employee', 'project_closing_manager_rel', 'project_id', 'employee_id')
    sourcing_manager_ids = fields.Many2many('hr.employee', 'project_sourcing_manager_rel', 'project_id', 'employee_id')
    closing_tl_ids = fields.Many2many('hr.employee', 'project_closing_tl_rel', 'project_id', 'employee_id', string='Closing TL')
    sourcing_tl_ids = fields.Many2many('hr.employee', 'project_sourcing_tl_rel', 'project_id', 'employee_id', string='Sourcing TL')
    crm_ids = fields.Many2many('hr.employee', 'project_crm_rel', 'project_id', 'employee_id', string='CRM')
    marketing_ids = fields.Many2many('hr.employee', 'project_marketing_rel', 'project_id', 'employee_id')

    sourcing_head_id = fields.Many2one('hr.employee')
    crm_head_id = fields.Many2one('hr.employee', 'CRM Head')
    crm_team_lead_id = fields.Many2one('hr.employee', 'CRM Team Lead')

    employee_count = fields.Integer(compute='compute_employee_count_and_cost')
    employee_cost = fields.Float(compute='compute_employee_count_and_cost')
    danger_project = fields.Boolean(compute='compute_danger_project')
    days_from_start_date = fields.Integer(
        string='Days From Start Date',
        compute='_compute_days_from_start_date'
    )
    days_from_close_date = fields.Integer(
        string='Days From Closing Date',
        compute='_compute_days_from_closing_date'
    )
    project_status = fields.Selection([('active', 'Active'), ('on_hold', 'On Hold'), ('closed', 'Closed')], 'Status', default='active', tracking=True)

    @api.depends('launch_date')
    def _compute_days_from_closing_date(self):
        for project in self:
            if project.launch_date:
                start_date = fields.Date.from_string(project.launch_date)
                today = date.today()
                delta = today - start_date
                project.days_from_close_date = delta.days if delta.days > 0 else 0
            else:
                project.days_from_close_date = 0

    @api.depends('purchase_date')
    def _compute_days_from_start_date(self):
        for project in self:
            if project.purchase_date:
                start_date = fields.Date.from_string(project.purchase_date)
                today = date.today()
                delta = today - start_date
                project.days_from_start_date = delta.days
            else:
                project.days_from_start_date = 0

    @api.depends('launch_date')
    def compute_danger_project(self):
        today = datetime.now().date()
        for rec in self:
            rec.danger_project = False
            if rec.launch_date and rec.launch_date < today:
                inventories = self.env['product.template'].search([('is_property', '=', True), ('building_id', '=', rec.id), ('state', '!=', 'sold')])
                if inventories:
                    rec.danger_project = True

    def compute_inventory_count(self):
        for rec in self:
            rec.total_inventory = 0
            rec.available_inventory_count = 0
            if rec.id:
                inventories = self.env['product.template'].search([('is_property', '=', True), ('building_id', '=', rec.id)])
                rec.total_inventory = len(inventories)
                rec.available_inventory_count = len(inventories.filtered(lambda x: x.state == 'free'))

    @api.depends(
        'closing_manager_ids',
        'sourcing_manager_ids',
        'closing_tl_ids',
        'sourcing_tl_ids',
        'crm_ids',
        'marketing_ids',
        'cluster_head_id',
        'business_head_id',
        'site_head_id'
    )
    def compute_employee_count_and_cost(self):
        for rec in self:
            rec.employee_count = len(rec.closing_manager_ids) + len(rec.sourcing_manager_ids) + len(
                rec.closing_tl_ids) + len(rec.sourcing_tl_ids) + len(rec.crm_ids) + len(rec.marketing_ids) + len(
                rec.cluster_head_id) + len(rec.business_head_id) + len(rec.site_head_id)
            rec.employee_cost = sum(rec.closing_manager_ids.mapped('ctc')) + sum(rec.sourcing_manager_ids.mapped('ctc')) + sum(
                rec.closing_tl_ids.mapped('ctc')) + sum(rec.sourcing_tl_ids.mapped('ctc')) + sum(
                rec.crm_ids.mapped('ctc')) + sum(rec.marketing_ids.mapped('ctc')) + sum(
                rec.cluster_head_id.mapped('ctc')) + sum(rec.business_head_id.mapped('ctc')) + sum(
                rec.site_head_id.mapped('ctc'))

    @api.model
    def default_get(self, fields):
        res = super(Building, self).default_get(fields)
        res['country_id'] = self.env.company.country_id.id
        res['state_id'] = self.env.company.state_id.id
        return res

    def action_create_units(self):
        property_pool = self.env['product.template']
        props = []
        if self.no_of_floors and self.props_per_floors:
            i = 1
            while i <= self.no_of_floors:
                j = 1
                while j <= self.props_per_floors:
                    vals = {
                        'name': self.code + ' - ' + str(i) + ' - ' + str(j),
                        'code': self.code + ' - ' + str(i) + ' - ' + str(j),
                        'building_id': self.id,
                        'floor': str(i),
                        'is_property': True,
                    }
                    prop_id = property_pool.create(vals)
                    props.append(prop_id.id)
                    j += 1
                i += 1

            self.unit_ids = [(6, 0, props)]
        else:
            raise ValidationError(
                _("Please set valid number for number of floors and units per floor"))

    _sql_constraints = [
        ('unique_code_per_project', 'UNIQUE (code)', 'Project code must be unique!'),
        ('unique_name_per_project', 'UNIQUE (name)', 'Project name must be unique!'),
    ]

    def view_sub_properties(self):
        list_view_id = self.env.ref("itsys_real_estate.building_unit_list").id
        kanban_view_id = self.env.ref("itsys_real_estate.building_unit_kanban").id
        form_view_id = self.env.ref("itsys_real_estate.building_unit_form").id
        graph_view_id = self.env.ref("itsys_real_estate.view_unit_graph").id
        search_view_id = self.env.ref("itsys_real_estate.building_unit_filter").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Flats',
            'view_mode': 'tree,kanban,form,graph',
            'res_model': 'product.template',
            'domain': [('building_id', '=', self.id), ('is_property', '=', True)],
            'context': {'search_default_status': 1, 'search_default_flat_state': 1, 'default_is_property': True, 'default_sale_ok': False,
                        'default_purchase_ok': False},
            'views': [(list_view_id, 'list'), (kanban_view_id, 'kanban'), (form_view_id, 'form'),
                      (graph_view_id, 'graph')],
            'search_view_id': [search_view_id, 'search'],
        }


class building_attachment_line(models.Model):
    _name = 'building.attachment.line'

    name = fields.Char('Name', required=True)
    file = fields.Binary('File', required=True)
    building_attach_id = fields.Many2one('building', '', ondelete='cascade', readonly=True)
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
