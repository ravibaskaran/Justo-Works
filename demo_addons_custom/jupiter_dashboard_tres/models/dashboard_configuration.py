from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DashboardConfiguration(models.Model):
    _name = 'dashboard.configuration'
    _description = 'Dashboard Configuration'

    role = fields.Selection([('crm', 'CRM'),
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
        ('crm_team_lead', 'CRM Team Lead')], 'Role')
    project = fields.Boolean('Project')
    cluster = fields.Boolean('Cluster')
    region = fields.Boolean('Region')
    limit_dashboard_pt = fields.Boolean('Limit dashboard project wise')

    def name_get(self):
        result = []
        for record in self:
            role_display = dict(self._fields['role'].selection).get(record.role)
            name = role_display or 'No Role'
            result.append((record.id, name))
        return result

    @api.constrains('role')
    def _check_unique_role(self):
        for rec in self:
            # count how many records already use this role
            count = self.search_count([('role', '=', rec.role)])
            if count > 1:
                raise ValidationError(
                    f"The role “{dict(self._fields['role'].selection)[rec.role]}” is already assigned.")

    @api.onchange('region')
    def _onchange_region(self):
        if self.region:
            self.cluster = True  # Automatically select Cluster
            self.project = True  # Automatically select Project
            self.limit_dashboard_pt = False
        else:
            self.cluster = False  # Deselect Cluster if Region is not selected
            self.project = False  # Deselect Project if Region is not selected

    @api.onchange('cluster')
    def _onchange_cluster(self):
        if self.cluster:
            self.project = True  # Automatically select Project
            self.limit_dashboard_pt = False
        else:
            self.project = False  # Deselect Project if Region is not selected

    @api.model
    def create(self, values):
        if values.get('region'):
            values['cluster'] = True  # Automatically select Cluster if Region is selected
            values['project'] = True  # Automatically select Project if Region is selected
        if values.get('cluster'):
            values['project'] = True
        return super(DashboardConfiguration, self).create(values)

    def write(self, values):
        if 'region' in values and values['region']:
            values['cluster'] = True  # Automatically select Cluster if Region is selected
            values['project'] = True  # Automatically select Project if Region is selected
        if 'cluster' in values and values['cluster']:
            values['project'] = True
        return super(DashboardConfiguration, self).write(values)

    @api.constrains('region', 'cluster', 'project', 'limit_dashboard_pt')
    def _check_region_dependencies(self):
        for record in self:
            # Rule 1: Region needs Cluster and Project
            if record.region and (not record.cluster or not record.project):
                raise ValidationError(
                    "If 'Region' is selected, 'Cluster' and 'Project' must also be selected."
                )
            # Rule 2: Cluster needs Project
            if record.cluster and not record.project:
                raise ValidationError(
                    "If 'Cluster' is selected, 'Project' must also be selected."
                )
            # Rule 3: limit_dashboard_pt needs Project
            # if record.limit_dashboard_pt and not record.project:
            #     raise ValidationError(
            #         "'Limit dashboard project wise' can only be enabled if 'Project' is selected."
            #     )

            # if record.limit_dashboard_pt and (record.cluster or record.region):
            #     raise ValidationError(
            #         "'Limit dashboard project wise' cannot be selected when "
            #         "'Cluster' or 'Region' is selected."
            #     )


