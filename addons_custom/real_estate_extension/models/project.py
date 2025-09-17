import json
import requests
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'building'
    #
    # country_id = fields.Many2one('res.country')
    # state_id = fields.Many2one('res.country.state')
    # sub_region_id = fields.Many2one('regions')
    # remarks = fields.Char()

    def process_project_api(self, mode):
        res = self
        crm_email = res.crm_ids.mapped('corporate_email')
        if mode == 'create':
            params = {
                'project_name': res.name,
                'project_code': res.code or '',
                'configuration': [str(item.name) for item in res.configuration_ids],
                'project_starting_date': res.purchase_date.strftime('%Y-%m-%d') if res.purchase_date else '',
                'closing_date': res.launch_date.strftime('%Y-%m-%d') if res.launch_date else '',
                # 'property_type': res.type.name or '',
                'region': res.region_id.name or '',
                # 'cluster': res.sub_region_id.name or '',
                'site_address': res.site_address or '',
                # 'closing_manager': ', '.join(
                #     [str(item.barcode) for item in res.closing_manager_ids]) if res.closing_manager_ids else '',
                # 'sourcing_manager': ', '.join(
                #     [str(item.barcode) for item in res.sourcing_manager_ids]) if res.sourcing_manager_ids else '',
                # 'closing_tl': ', '.join([str(item.barcode) for item in res.closing_tl_ids]) if res.closing_tl_ids else '',
                # 'sourcing_tl': ', '.join(
                #     [str(item.barcode) for item in res.sourcing_tl_ids]) if res.sourcing_tl_ids else '',
                # 'crm': ', '.join([str(item.barcode) for item in res.crm_ids]) if res.crm_ids else '',
                'crm_email': ', '.join([str(item) if item else '' for item in crm_email]) if crm_email else '',
                # 'marketing': ', '.join([str(item.barcode) for item in res.marketing_ids]) if res.marketing_ids else '',
                # 'residential_saleable_area': res.residential_saleable_area,
                'rera_no': res.license_code or '',
                'city': res.region_id.name or '',
                'locality': res.sub_region_id.name or '',
                'property_type': res.type.name or '',
                # 'business_head': res.business_head_id.barcode,
                # 'site_head': res.site_head_id.barcode,
                # 'cluster_head': res.cluster_head_id.barcode,
                'project_status': res.project_status or ''
            }
        else:
            params = {
                'project_name': res.name,
                'project_code': res.code or '',
                'project_starting_date': res.purchase_date.strftime('%Y-%m-%d') if res.purchase_date else '',
                'closing_date': res.launch_date.strftime('%Y-%m-%d') if res.launch_date else '',
                'rera_no': res.license_code or '',

                'configuration': [str(item.name) for item in res.configuration_ids],
                'region': res.region_id.name or '',
                'site_address': res.site_address or '',
                'city': res.region_id.name or '',
                'locality': res.sub_region_id.name or '',
                'property_type': res.type.name or '',
                'project_status': res.project_status or ''
            }
        url = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_api_url')
        username = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_api_username')
        password = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.project_api_key')

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
                if rec.get('status') in (200, 201):
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
            'record': str(res.id),
            'code': code,
            'response': response,
            'date': datetime.now(),
            'type': 'project',
            'status': status,
            'name': res.name,
            'direction': 'out',
            'args': data
        })

    def get_from_mail(self):
        mail_server = self.env['ir.mail_server'].search([('active', '=', True)], limit=1)
        if mail_server:
            return mail_server.smtp_user
        return False

    def get_hr_partner_ids(self):
        param = self.env['ir.config_parameter'].sudo()
        mail_hr_users = param.get_param('itsys_real_estate.mail_hr_users')
        if mail_hr_users:
            user_ids = mail_hr_users.replace('[', '').replace(']', '').split(',')
            partner_ids = self.env['res.users'].sudo().search([('id', 'in', [int(item) for item in user_ids])]).mapped('partner_id')
            return ','.join([str(item.id) for item in partner_ids])
        return False

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        param = self.env['ir.config_parameter'].sudo()
        out_api = param.get_param('real_estate_extension.enable_project_out_api')
        if out_api:
            res.process_project_api('create')
        mail_to_hr = param.get_param('itsys_real_estate.enable_project_creation_mail_to_hr')
        if mail_to_hr:
            mail_hr_users = param.get_param('itsys_real_estate.mail_hr_users')
            if mail_hr_users:
                template = self.env.ref('real_estate_extension.project_creation_alert_mail_template').sudo()
                template.send_mail(res.id, force_send=True)
        return res

    def write(self, vals):
        res = super(Project, self).write(vals)
        out_api = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_project_out_api')
        if out_api:
            # self.process_project_api('create')
            if vals.get('name') or vals.get('code') or vals.get('purchase_date') or vals.get('launch_date') or vals.get('license_code') or vals.get('project_status') or vals.get('configuration_ids') or vals.get('region_id') or vals.get('site_address') or vals.get('sub_region_id') or vals.get('type'):
                self.process_project_api('write')
        return res
