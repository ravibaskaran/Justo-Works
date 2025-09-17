# -*- coding: utf-8 -*-
import calendar

from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaProjectWiseRegistrationReport(models.TransientModel):  # change this
    _name = 'beta.project.wise.registration.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Project Wise Registration Report')  # change this
    date = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaProjectWiseRegistrationReport, self).default_get(fields_list)
        today = datetime.today()
        res['date'] = today
        return res

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('project_wise_registration_report.project_wise_registration_report')._render({
            'doc': doc,
            'date': self.date,
        })

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    def _get_report_data(self):
        projects = self.env['building'].search([], order='name')
        _, last_day = calendar.monthrange(int(self.date.year), int(self.date.month))
        last_day = str(self.date.year) + '-' + str(self.date.month) + '-' + str(last_day)
        first_day = str(self.date.year) + '-' + str(self.date.month) + '-01'
        first_day = datetime.strptime(first_day, '%Y-%m-%d')
        last_day = datetime.strptime(last_day, '%Y-%m-%d')
        month = self.date.strftime("%B %Y")
        doc = {
            'data': [],
            'total_month_target_count': 0,
            'total_day_registration_count': 0,
            'total_month_registration_count': 0,
            'total_day_registration_value': 0,
            'total_month_registration_value': 0,
        }
        for project in projects:
            target = self.env['project.target.line'].search(
                [('month', '=', month), ('target_id.project_id', '=', project.id)])
            registrations = self.env['project.registration'].search(
                [('project_id', '=', project.id), ('state', 'not in', ('draft', 'canceled')),
                 ('registration_date', '<=', last_day), ('registration_date', '>=', first_day)])
            booking_of_registrations = self.env['unit.reservation'].search(
                [('building_unit', 'in', registrations.mapped('flat_id').ids), ('state', '=', 'confirmed')])
            day_registrations = registrations.filtered(lambda x: x.registration_date == self.date)
            booking_of_day_registrations = self.env['unit.reservation'].search(
                [('building_unit', 'in', day_registrations.mapped('flat_id').ids), ('state', '=', 'confirmed')])
            month_target_count = sum(target.mapped('registration'))
            day_registration_count = len(day_registrations)
            month_registration_count = len(registrations)
            achieved_percentage = month_registration_count / month_target_count * 100 if month_target_count != 0 else 100
            day_registration_value = sum(booking_of_day_registrations.mapped('flat_cost'))
            month_registration_value = sum(booking_of_registrations.mapped('flat_cost'))
            doc['data'].append({
                'project': project.name,
                'month_target_count': month_target_count,
                'day_registration_count': day_registration_count,
                'month_registration_count': month_registration_count,
                'achieved_percentage': achieved_percentage,
                'day_registration_value': day_registration_value,
                'month_registration_value': month_registration_value,
            })
            doc['total_month_target_count'] += month_target_count
            doc['total_day_registration_count'] += day_registration_count
            doc['total_month_registration_count'] += month_registration_count
            doc['total_day_registration_value'] += day_registration_value
            doc['total_month_registration_value'] += month_registration_value
        doc['total_achieved_percentage'] = doc['total_month_registration_count'] / doc[
            'total_month_target_count'] * 100 if doc['total_month_target_count'] != 0 else 100
        return {'data': doc}
