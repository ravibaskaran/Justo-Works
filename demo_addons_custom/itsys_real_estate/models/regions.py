# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Regions(models.Model):
    _name = "regions"
    _description = "Region"
    _parent_name = "region_id"
    _parent_store = True
    _order = 'complete_name'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    @api.depends('name', 'region_id')
    def _compute_complete_name(self):
        """ Forms complete name of region from region to child region. """
        name = self.name
        current = self
        while current.region_id:
            current = current.region_id
            name = '%s/%s' % (current.name, name)
        self.complete_name = name

    @api.depends('name', 'region_id.complete_name')
    def _compute_complete_name(self):
        """ Forms complete name of location from parent location to child location. """
        if self.region_id.complete_name:
            self.complete_name = '%s/%s' % (self.region_id.complete_name, self.name)
        else:
            self.complete_name = self.name

    name = fields.Char('Name', required=True)
    complete_name = fields.Char(
        'Name', compute='_compute_complete_name', recursive=True,
        store=True)
    child_ids = fields.One2many('regions', 'region_id', 'Contains')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)
    account = fields.Many2one('account.account', 'Discount Account', )
    account_me = fields.Many2one('account.account', 'Managerial Expenses Account', )
    region_id = fields.Many2one('regions', ondelete='cascade')
    # region_id = fields.Many2one('regions', 'Parent Region', ondelete='cascade')
    parent_path = fields.Char(index=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    latlng_ids = fields.One2many('latlng.line', 'region_id', string='LatLng List', copy=True)
    map = fields.Text('Map', digits=(9, 6))
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    is_parent = fields.Boolean()
    code = fields.Char('ID')

    @api.constrains('name')
    def validate_unique_name(self):
        if self.is_parent:
            regions = self.env['regions'].search(
                [('name', '=', self.name), ('is_parent', '=', True), ('id', '!=', self.id)])
            if regions:
                raise ValidationError('Region with same name already exists!')
        else:
            clusters = self.env['regions'].search(
                [('name', '=', self.name), ('is_parent', '=', False), ('region_id', '=', self.region_id.id),
                 ('id', '!=', self.id)])
            if clusters:
                raise ValidationError('Cluster with same name already exists under the same region!')

    @api.model
    def create(self, values):
        res = super(Regions, self).create(values)
        print(res,'res')
        if res.is_parent:
            res.code = self.env['ir.sequence'].next_by_code('region.master.sequence')
        else:
            res.code = self.env['ir.sequence'].next_by_code('cluster.master.sequence')
        return res

    @api.model
    def default_get(self, fields):
        res = super(Regions, self).default_get(fields)
        res['country_id'] = self.env.company.country_id.id
        res['state_id'] = self.env.company.state_id.id
        return res

    def unit_status(self, unit_id):
        self.env.cr.execute("select state from building_unit where id = " + str(int(unit_id)))
        res = self.env.cr.dictfetchone()
        if res:
            if res["state"]:
                return res["state"]


class LatlngLine(models.Model):
    _name = "latlng.line"
    lat = fields.Float('Latitude', digits=(9, 6), required=True)
    lng = fields.Float('Longitude', digits=(9, 6), required=True)
    url = fields.Char('URL', digits=(9, 6), required=True)
    region_id = fields.Many2one('regions', 'Region')
    unit_id = fields.Many2one('product.template', 'Unit', domain=[('is_property', '=', True)], required=True)
    state = fields.Selection(string='State', related='unit_id.state', store=True, readonly=True)

    @api.onchange('unit_id')
    def onchange_unit(self):
        action_id = self.env.ref('itsys_real_estate.building_unit_act1').id
        '#id=33&cids=1&action=317&model=product.template&view_type=form&menu_id=205'
        link = '#id=%s&action=%s&model=product.template&view_type=form' % (
            self.unit_id.id, action_id)
        self.url = link

    @api.onchange('url')
    def onchange_url(self):
        if self.url:
            url = self.url
            self.unit_id = int(((url.split("#")[1]).split("&")[0]).split("=")[1])
        else:
            self.unit_id = None
            self.state = None
