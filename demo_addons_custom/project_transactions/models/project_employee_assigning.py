import json
import requests
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectEmployeeAssigning(models.Model):
    _name = 'project.employee.assigning'
    _inherit = ['mail.thread']
    _description = 'Project Employee Assigning'
    _order = "date desc"

    name = fields.Char(compute='compute_name')
    project_id = fields.Many2one('building', 'Project', tracking=True)
    date = fields.Date(tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned')], default='draft', tracking=True)
    closing_manager_ids = fields.One2many('project.employee.assigning.line', 'cm_parent_id')
    sourcing_manager_ids = fields.One2many('project.employee.assigning.line', 'sm_parent_id')
    closing_tl_ids = fields.One2many('project.employee.assigning.line', 'ctl_parent_id')
    closing_tl_id = fields.Many2one('hr.employee')
    closing_tl_date = fields.Date()
    sourcing_tl_ids = fields.One2many('project.employee.assigning.line', 'stl_parent_id')
    sourcing_tl_id = fields.Many2one('hr.employee')
    sourcing_tl_date = fields.Date()
    crm_ids = fields.One2many('project.employee.assigning.line', 'crm_parent_id')
    marketing_ids = fields.One2many('project.employee.assigning.line', 'mkg_parent_id')
    business_head_id = fields.Many2one('hr.employee')
    site_head_id = fields.Many2one('hr.employee')
    cluster_head_id = fields.Many2one('hr.employee')
    business_head_date = fields.Date()
    site_head_date = fields.Date()
    cluster_head_date = fields.Date()
    region_id = fields.Many2one('regions', related='project_id.region_id')
    cluster_id = fields.Many2one('regions', string='Cluster', related='project_id.sub_region_id')

    merge_role = fields.Boolean()

    sourcing_head_id = fields.Many2one('hr.employee')
    crm_head_id = fields.Many2one('hr.employee')
    crm_team_lead_id = fields.Many2one('hr.employee')

    sourcing_head_date = fields.Date()
    crm_head_date = fields.Date()
    crm_team_lead_date = fields.Date()

    @api.onchange('merge_role')
    def clear_scm_managers(self):
        if not self.merge_role:
            if self.closing_manager_ids.filtered(lambda x: x.employee_id.role != 'closing_manager'):
                self.closing_manager_ids = False
            if self.sourcing_manager_ids.filtered(lambda x: x.employee_id.role != 'sourcing_manager'):
                self.sourcing_manager_ids = False

    @api.constrains('closing_manager_ids', 'closing_tl_ids', 'sourcing_manager_ids', 'sourcing_tl_ids', 'crm_ids',
                    'marketing_ids', 'business_head_id', 'site_head_id', 'cluster_head_id', 'project_id')
    def check_required_employee_roles(self):
        msg = ''
        is_or_are = ' is'
        # if not self.closing_tl_ids and self.closing_tl_id:
        #     self.closing_tl_ids = [(0, 0, {'employee_id': self.closing_tl_id.id,'date':self.closing_tl_date})]
        # if not self.sourcing_tl_ids and self.sourcing_tl_id:
        #     self.sourcing_tl_ids = [(0, 0, {'employee_id': self.sourcing_tl_id.id,'date':self.sourcing_tl_date})]
        if not self.closing_manager_ids:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Closing Manager'
        if not self.closing_tl_ids:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Closing TL'
        if not self.sourcing_manager_ids:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Sourcing Manager'
        if not self.sourcing_tl_ids:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Sourcing TL'
        if not self.crm_ids:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'CRM'
        if not self.marketing_ids:
            if msg:
                msg += ', '
            msg += 'Marketing'
        # if not self.business_head_id:
        #     if msg:
        #         msg += ', '
        #         is_or_are = ' are'
        #     msg += 'Business Head'
        if not self.site_head_id:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Site Head'
        if not self.cluster_head_id:
            if msg:
                msg += ', '
                is_or_are = ' are'
            msg += 'Cluster Head'
        if msg:
            msg += is_or_are + ' required'
            raise ValidationError(msg)
        if len(self.crm_ids) != 1:
            raise ValidationError('Only one CRM allowed')

    @api.onchange('closing_tl_ids','closing_tl_date')
    def onchange_closing_tl_id(self):
        sourcing_tl_id = self.sourcing_tl_ids.mapped('employee_id')
        closing_tl_id = self.closing_tl_ids.mapped('employee_id')
        # closing_tl_id = self.closing_tl_id
        # closing_tl_date = self.closing_tl_date
        # self.closing_tl_ids = False
        # if closing_tl_id or closing_tl_date:
        #     self.closing_tl_ids = [(0, 0, {'employee_id': closing_tl_id.id,'date':closing_tl_date})]
        # if not closing_tl_id and self.closing_manager_ids:
        #     raise ValidationError('Need to remove selected Closing Managers before changing Closing TL')
        error_msg = ''
        try:
            for managers in self.closing_manager_ids:
                if self.merge_role:
                    if managers.employee_id.parent_id.id not in (closing_tl_id + sourcing_tl_id).ids:
                        error_msg = 'Selected Closing Manager is not under the Closing or Sourcing TL'
                else:
                    if managers.employee_id.parent_id.id not in closing_tl_id.ids:
                        error_msg = 'Selected Closing Manager is not under the Closing TL'
        except:
            pass
        if error_msg:
            if self.merge_role:
                self.closing_manager_ids = self.closing_manager_ids.filtered(
                    lambda x: x.employee_id.parent_id.id in (closing_tl_id + sourcing_tl_id).ids)
            else:
                self.closing_manager_ids = self.closing_manager_ids.filtered(lambda x: x.employee_id.parent_id.id in closing_tl_id.ids)
            return {'warning': {
                'title': " ",
                'message': error_msg
            }}
            raise ValidationError(error_msg)

    @api.onchange('sourcing_tl_ids','sourcing_tl_date')
    def onchange_sourcing_tl_id(self):
        sourcing_tl_id = self.sourcing_tl_ids.mapped('employee_id')
        closing_tl_id = self.closing_tl_ids.mapped('employee_id')
        # sourcing_tl_date = self.sourcing_tl_date
        # self.sourcing_tl_ids = False
        # if sourcing_tl_id or sourcing_tl_date:
        #     self.sourcing_tl_ids = [(0, 0, {'employee_id': sourcing_tl_id.id,'date':sourcing_tl_date})]
        # if not sourcing_tl_id and self.sourcing_manager_ids:
        #     raise ValidationError('Need to remove selected Sourcing Managers before changing Sourcing TL')
        error_msg = ''
        try:
            for managers in self.sourcing_manager_ids:
                if self.merge_role:
                    if managers.employee_id.parent_id.id not in (sourcing_tl_id + closing_tl_id).ids:
                        error_msg = 'Selected Closing Manager is not under the Closing or Sourcing TL'
                else:
                    if managers.employee_id.parent_id.id not in sourcing_tl_id.ids:
                        error_msg = 'Selected Sourcing Manager is not under the Sourcing TL'
        except:
            pass
        if error_msg:
            if self.merge_role:
                self.sourcing_manager_ids = self.sourcing_manager_ids.filtered(
                    # lambda x: x.employee_id.parent_id.id in (sourcing_tl_id + self.closing_tl_id).ids)
                    lambda x: x.employee_id.parent_id.id in (sourcing_tl_id + closing_tl_id).ids)
            else:
                self.sourcing_manager_ids = self.sourcing_manager_ids.filtered(
                    lambda x: x.employee_id.parent_id.id in sourcing_tl_id.ids)
            return {'warning': {
                'title': " ",
                'message': error_msg
            }}
            raise ValidationError(error_msg)

    # commented to prevent wrong data filling process. told to do so
    @api.onchange('project_id')
    def onchange_project(self):
        self.closing_manager_ids = False
        self.sourcing_manager_ids = False
        self.closing_tl_ids = False
        self.sourcing_tl_ids = False
        self.crm_ids = False
        self.marketing_ids = False

        self.sourcing_head_id = False
        self.crm_head_id = False
        self.crm_team_lead_id = False

        if self.project_id:
            # self.closing_tl_id = self.project_id.closing_tl_ids[0].id if self.project_id.closing_tl_ids else False
            # self.sourcing_tl_id = self.project_id.sourcing_tl_ids[0].id if self.project_id.sourcing_tl_ids else False
            self.closing_manager_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.closing_manager_ids]
            self.sourcing_manager_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.sourcing_manager_ids]
            # self.closing_tl_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.closing_tl_ids]
            self.closing_tl_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.closing_tl_ids]
            self.sourcing_tl_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.sourcing_tl_ids]

            self.crm_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.crm_ids]
            self.marketing_ids = [(0, 0, {'employee_id': l.id}) for l in self.project_id.marketing_ids]
            self.business_head_id = self.project_id.business_head_id
            self.site_head_id = self.project_id.site_head_id
            self.cluster_head_id = self.project_id.cluster_head_id

            self.sourcing_head_id = self.project_id.sourcing_head_id
            self.crm_head_id = self.project_id.crm_head_id
            self.crm_team_lead_id = self.project_id.crm_team_lead_id
            last_assigning_record = self.env['project.employee.assigning'].search(
                [('state', '=', 'assigned'), ('project_id', '=', self.project_id.id)], order="id desc", limit=1)
            if last_assigning_record:
                self.merge_role = last_assigning_record.merge_role


    def compute_name(self):
        self.name = 'Project Employee Assigning'
        if self.project_id and self.date:
            self.name = str(self.project_id.name) + " (" + str(self.date.strftime('%d/%m/%Y')) + ")"

    def action_assign(self):
        if self.closing_manager_ids and not self.closing_tl_ids:
            raise ValidationError('Closing TL is required since Closing Manager is selected')
        if self.sourcing_manager_ids and not self.sourcing_tl_ids:
            raise ValidationError('Sourcing TL is required since Sourcing Manager is selected')
        if not self.crm_ids:
            raise ValidationError('CRM is required')
        values = {
            'closing_manager_ids': [(6, 0, self.closing_manager_ids.mapped('employee_id').ids)],
            'sourcing_manager_ids': [(6, 0, self.sourcing_manager_ids.mapped('employee_id').ids)],
            'closing_tl_ids': [(6, 0, self.closing_tl_ids.mapped('employee_id').ids)],
            'sourcing_tl_ids': [(6, 0, self.sourcing_tl_ids.mapped('employee_id').ids)],
            'crm_ids': [(6, 0, self.crm_ids.mapped('employee_id').ids)],
            'marketing_ids': [(6, 0, self.marketing_ids.mapped('employee_id').ids)],
            'business_head_id': self.business_head_id.id,
            'site_head_id': self.site_head_id.id,
            'cluster_head_id': self.cluster_head_id.id,

            'sourcing_head_id': self.sourcing_head_id.id,
            'crm_head_id': self.crm_head_id.id,
            'crm_team_lead_id': self.crm_team_lead_id.id,
        }

        # Write to the project_id record
        self.project_id.write(values)
        out_api = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_project_employee_assign_api')
        if out_api:

            params = {
                'project': self.project_id.code or '',
                'date': self.date.strftime('%d/%m/%Y') if self.date else '',
                'closing_tl_manager': ','.join(
                    [(str(item.id or '')) for item in self.closing_tl_ids.mapped('employee_id')]),
                'closing_manager': ','.join(
                    [(str(item.id or '')) for item in self.closing_manager_ids.mapped('employee_id')]),
                'sourcing_tl_manager': ','.join(
                    [(str(item.id or '')) for item in self.sourcing_tl_ids.mapped('employee_id')]),
                'sourcing_manager': ','.join(
                    [(str(item.id or '')) for item in self.sourcing_manager_ids.mapped('employee_id')]),
                'crm': ','.join([(str(item.id or '')) for item in self.crm_ids.mapped('employee_id')]),
                'marketing': ','.join([(str(item.id or '')) for item in self.marketing_ids.mapped('employee_id')]),
                'business_head': str(self.business_head_id.id or ''),
                'site_head': str(self.site_head_id.id or ''),
                'cluster_head': str(self.cluster_head_id.id or ''),

                'sourcing_head_id': str(self.sourcing_head_id.id or ''),
                'crm_head_id': str(self.crm_head_id.id or ''),
                'crm_team_lead_id': str(self.crm_team_lead_id.id or ''),
            }
            # params = {
            #     'project': self.project_id.code or '',
            #     'date': self.date.strftime('%d/%m/%Y') if self.date else '',
            #     'closing_manager': [(item.id or '') for item in self.closing_manager_ids.mapped('employee_id')],
            #     'sourcing_manager': [(item.id or '') for item in self.sourcing_manager_ids.mapped('employee_id')],
            #     'closing_tl_manager': [(item.id or '') for item in self.closing_tl_ids.mapped('employee_id')],
            #     'sourcing_tl_manager': [(item.id or '') for item in self.sourcing_tl_ids.mapped('employee_id')],
            #     'crm': [(item.id or '') for item in self.crm_ids.mapped('employee_id')],
            #     'marketing': [(item.id or '') for item in self.marketing_ids.mapped('employee_id')],
            #     'business_head': [self.business_head_id.id or ''],
            #     'site_head': [self.site_head_id.id or ''],
            #     'cluster_head': [self.cluster_head_id.id or ''],
            # }
            url = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_employee_assign_api_url')
            username = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_employee_assign_api_username')
            password = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_employee_assign_api_key')

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
                'record': str(self.id),
                'code': code,
                'response': response,
                'date': datetime.now(),
                'type': 'employee_assign',
                'status': status,
                'name': self.name,
                'direction': 'out',
                'args': data
            })
        emp_out_api = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_employee_out_api')
        if emp_out_api:
            for manager in self.closing_manager_ids.mapped('employee_id'):
                if manager in self.sourcing_manager_ids.mapped('employee_id'):
                    manager.process_employee_api(role='scm')
        # self.project_id.closing_manager_ids = self.closing_manager_ids.mapped('employee_id')
        # self.project_id.sourcing_manager_ids = self.sourcing_manager_ids.mapped('employee_id')
        # self.project_id.closing_tl_ids = self.closing_tl_ids.mapped('employee_id')
        # self.project_id.sourcing_tl_ids = self.sourcing_tl_ids.mapped('employee_id')
        # self.project_id.crm_ids = self.crm_ids.mapped('employee_id')
        # self.project_id.marketing_ids = self.marketing_ids.mapped('employee_id')
        # self.project_id.business_head_id = self.business_head_id
        # self.project_id.site_head_id = self.site_head_id
        # self.project_id.cluster_head_id = self.cluster_head_id
        self.state = 'assigned'

    @api.model
    def default_get(self, fields_list):
        res = super(ProjectEmployeeAssigning, self).default_get(fields_list)
        res['date'] = datetime.today()
        default_site_head = self.env['hr.employee'].search([('is_default_site_head', '=', True), ('role', '=', 'site_head')], limit=1)
        if default_site_head:
            res['site_head_id'] = default_site_head.id
        return res


class ProjectEmployeeAssigningLine(models.Model):
    _name = 'project.employee.assigning.line'

    date = fields.Date("Date Upto")
    cm_parent_id = fields.Many2one('project.employee.assigning')
    sm_parent_id = fields.Many2one('project.employee.assigning')
    ctl_parent_id = fields.Many2one('project.employee.assigning')
    stl_parent_id = fields.Many2one('project.employee.assigning')
    crm_parent_id = fields.Many2one('project.employee.assigning')
    mkg_parent_id = fields.Many2one('project.employee.assigning')
    employee_id = fields.Many2one('hr.employee')

    sm_domain = fields.Char(compute='compute_sm_domain')
    cm_domain = fields.Char(compute='compute_cm_domain')

    @api.depends('sm_parent_id')
    def compute_sm_domain(self):
        for rec in self:
            if rec.sm_parent_id.merge_role:
                rec.sm_domain = json.dumps(([('role', 'in', ('closing_manager', 'sourcing_manager')), ('active_status', '=', True), ('parent_id', 'in', (rec.sm_parent_id.sourcing_tl_ids.mapped('employee_id') + rec.sm_parent_id.closing_tl_ids.mapped('employee_id')).ids), ('parent_id', '!=', False)]))
            else:
                rec.sm_domain = json.dumps(([('role', '=', 'sourcing_manager'), ('active_status', '=', True), ('parent_id', 'in', rec.sm_parent_id.sourcing_tl_ids.mapped('employee_id').ids), ('parent_id', '!=', False)]))

    @api.depends('cm_parent_id')
    def compute_cm_domain(self):
        for rec in self:
            if rec.cm_parent_id.merge_role:
                rec.cm_domain = json.dumps(([('role', 'in', ('closing_manager', 'sourcing_manager')), ('active_status', '=', True), ('parent_id', 'in', (rec.cm_parent_id.sourcing_tl_ids.mapped('employee_id') + rec.cm_parent_id.closing_tl_ids.mapped('employee_id')).ids), ('parent_id', '!=', False)]))
            else:
                rec.cm_domain = json.dumps(([('role', '=', 'closing_manager'), ('active_status', '=', True), ('parent_id', 'in', rec.cm_parent_id.closing_tl_ids.mapped('employee_id').ids), ('parent_id', '!=', False)]))
