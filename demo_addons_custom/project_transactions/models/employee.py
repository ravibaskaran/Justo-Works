import json
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    role = fields.Selection([
        ('crm', 'CRM'),
        ('closing_tl', 'Closing TL'),
        ('closing_manager', 'Closing Manager'),
        ('sourcing_tl', 'Sourcing TL'),
        ('sourcing_manager', 'Sourcing Manager'),
        ('marketing', 'Marketing'),
        ('business_head', 'Business Head'),
        ('site_head', 'Site Head'),
        ('cluster_head', 'Cluster Head'),
        ('sourcing_head', 'Sourcing Head'),
        ('closing_head', 'Closing Head'),
        ('admin', 'Admin'),
        ('crm_head', 'CRM Head'),
        ('crm_team_lead', 'CRM Team Lead')
    ])
    parent_domain = fields.Char(compute='compute_employee_parent_domain', readonly=True, store=False)
    is_default_site_head = fields.Boolean(default=False)
    is_rom = fields.Boolean()
    region_ids = fields.Many2many('regions', string='Region')

    @api.depends('role')
    def compute_employee_parent_domain(self):
        for rec in self:
            parent_domain = json.dumps(([]))
            if rec.role == 'sourcing_manager':
                parent_domain = json.dumps(([('role', '=', 'sourcing_tl')]))
            elif rec.role == 'closing_manager':
                parent_domain = json.dumps(([('role', '=', 'closing_tl')]))
            elif rec.role == 'sourcing_tl':
                parent_domain = json.dumps(([('role', 'in', ('site_head', 'cluster_head', 'business_head'))]))
            elif rec.role == 'closing_tl':
                parent_domain = json.dumps(([('role', 'in', ('site_head', 'cluster_head', 'business_head'))]))
            elif rec.role == 'site_head':
                parent_domain = json.dumps(([('role', 'in', ('cluster_head', 'business_head'))]))
            elif rec.role == 'cluster_head':
                parent_domain = json.dumps(([('role', '=', 'business_head')]))
            elif rec.role in ('sourcing_head', 'closing_head', 'admin', 'crm_head', 'crm_team_lead'):
                parent_domain = json.dumps(([('role', '=', 'cluster_head')]))
            rec.parent_domain = parent_domain

    @api.onchange('role')
    def onchange_employee_role(self):
        if self.role:
            self.parent_id = False
