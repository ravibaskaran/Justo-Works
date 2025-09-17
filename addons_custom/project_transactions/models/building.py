# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import ValidationError


class Building(models.Model):
    _inherit = 'building'

    def read(self, fields=None, load='_classic_read'):
        res = super(Building, self).read(fields=fields, load=load)
        if len(res) == 1:
            if not self.env.user.has_group('project_transactions.view_all_projects'):
                employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
                if employee:
                    allowed_employees = self.closing_manager_ids + self.sourcing_manager_ids + self.closing_tl_ids \
                                        + self.sourcing_tl_ids + self.crm_ids + self.marketing_ids \
                                        + self.business_head_id + self.site_head_id + self.cluster_head_id
                    if employee.id not in allowed_employees.ids:
                        raise ValidationError('You have no access to this project!')
                else:
                    raise ValidationError('You have no access to this project!')
        return res

    def action_create_inventory(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Inventory'),
            'res_model': 'building.create.inventory',
            'target': 'new',
            'view_id': self.env.ref('project_transactions.building_create_inventory_view_form').id,
            'view_mode': 'form',
            'context': {'default_project_id': self.id}
        }
