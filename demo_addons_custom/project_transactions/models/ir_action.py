# -*- coding: utf-8 -*-

from odoo import models


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    # function to show only users allowed projects, booking, registration - based on project's employees
    def read(self, fields=None, load='_classic_read'):
        result = super(IrActionsActWindow, self).read(fields, load=load)
        xml_ids = (
            'itsys_real_estate.unit_reservation_form_action',
            'project_transactions.project_registration_action',
            'itsys_real_estate.building_act1',
        )
        if self.xml_id in ('itsys_real_estate.unit_reservation_form_action', 'project_transactions.project_registration_action', 'itsys_real_estate.building_act1'):
            if self in (self.env.ref('itsys_real_estate.unit_reservation_form_action'), self.env.ref('project_transactions.project_registration_action'), self.env.ref('itsys_real_estate.building_act1')):
                if not self.env.user.has_group('project_transactions.view_all_projects'):
                    if self.xml_id in xml_ids and not self.env.user.has_group('project_transactions.view_all_projects'):
                        # only for Booking-By-Region users
                        if self.env.user.has_group('project_transactions.group_region_booking_user'):
                            emp = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
                            rec_ids = []
                            if emp:
                                regions = emp.region_ids.ids  # the set of allowed region IDs
                                if self.xml_id == 'itsys_real_estate.unit_reservation_form_action':
                                    model = 'unit.reservation'
                                elif self.xml_id == 'project_transactions.project_registration_action':
                                    model = 'project.registration'
                                else:
                                    model = 'building'
                                records = self.env[model].search([])
                                for record in records:
                                    if self.xml_id == 'itsys_real_estate.unit_reservation_form_action':
                                        project = record.building
                                        if project.region_id.id in regions:
                                            rec_ids.append(record.id)
                                    elif self.xml_id == 'project_transactions.project_registration_action':
                                        project = record.project_id
                                        if project.region_id.id in regions:
                                            rec_ids.append(record.id)
                                    else:
                                        project = record
                                        if project.region_id.id in regions:
                                            rec_ids.append(record.id)

                            domain = [('id', 'in', rec_ids)]
                            for values in result:
                                values['domain'] = domain
                        else:
                            employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
                            rec_ids = []
                            if self.xml_id == 'itsys_real_estate.unit_reservation_form_action':
                                model = 'unit.reservation'
                            elif self.xml_id == 'project_transactions.project_registration_action':
                                model = 'project.registration'
                            else:
                                model = 'building'
                            if employee:
                                records = self.env[model].search([])
                                for record in records:
                                    if self.xml_id == 'itsys_real_estate.unit_reservation_form_action':
                                        project = record.building
                                        allowed_employees = record.closing_manager_id + record.sourcing_manager_id + record.closing_tl_id \
                                                            + record.sourcing_tl_id + record.crm_id + record.marketing_id + \
                                                            project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
                                                            + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
                                                            + project.business_head_id + project.site_head_id + project.cluster_head_id
                                    elif self.xml_id == 'project_transactions.project_registration_action':
                                        project = record.project_id
                                        booking = self.env['unit.reservation'].search(
                                            [('building_unit', '=', record.flat_id.id),
                                             ('state', 'not in', ('draft', 'cancel'))], limit=1)
                                        allowed_employees = booking.closing_manager_id + booking.sourcing_manager_id + booking.closing_tl_id \
                                                            + booking.sourcing_tl_id + booking.crm_id + booking.marketing_id + \
                                                            project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
                                                            + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
                                                            + project.business_head_id + project.site_head_id + project.cluster_head_id
                                    else:
                                        project = record
                                        allowed_employees = project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
                                                            + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
                                                            + project.business_head_id + project.site_head_id + project.cluster_head_id
                                    if employee.id in allowed_employees.ids:
                                        rec_ids.append(record.id)

                            domain = [('id', 'in', rec_ids)]
                            for values in result:
                                values['domain'] = domain
        return result
