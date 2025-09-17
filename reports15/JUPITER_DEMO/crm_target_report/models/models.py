# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime, timedelta
import calendar


class BetaCrmTarget(models.TransientModel):  # change this
    _name = 'beta.crm.target'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='CRM Target Report')  # change this
    financial_year = fields.Selection(selection=lambda self: self.get_financial_years())
    month = fields.Selection(selection=[
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March')
    ])

    def get_financial_years(self):
        sequence = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).sequence_id
        values = []
        for line in sequence.date_range_ids:
            values.append((str(line.date_from.year),
                           str(line.date_from.strftime('%y')) + ' - ' + str(int(line.date_from.strftime('%y')) + 1)))
        return values

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('crm_target_report.crm_target_report')._render({
            'doc': doc,
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
        data = []
        totals = {
            'booking_count': 0,
            'registered_count': 0,
            'pending_registration_count': 0,
            'sdr_pending_count': 0,
            'projection_count': 0,
            'achieved_count': 0,
            'cancellation_count': 0,
            'projection_av': 0,
            'achieved_av': 0,
            'cancellation_av': 0,
        }
        if int(self.month) > 3:
            date_from = self.financial_year + '-' + self.month + '-01'
            _, last_day = calendar.monthrange(int(self.financial_year), int(self.month))
            date_to = self.financial_year + '-' + self.month + '-' + str(last_day)
        else:
            date_from = str(int(self.financial_year) + 1) + '-' + self.month + '-01'
            _, last_day = calendar.monthrange(int(self.financial_year) + 1, int(self.month))
            date_to = str(int(self.financial_year) + 1) + '-' + self.month + '-' + str(last_day)
        actual_date_from = self.get_actual_date(date_from + " 00:00:00")
        actual_date_to = self.get_actual_date(date_to + " 23:59:59")
        date_from_object = datetime.strptime(date_from, '%Y-%m-%d')
        month = date_from_object.strftime("%B %Y")
        financial_year_start = self.get_actual_date(self.financial_year + '-04-01' + " 00:00:00")
        financial_year_end = self.get_actual_date(str(int(self.financial_year) + 1) + '-03-31' + " 23:59:59")
        for project in projects:
            project_data = {'project_name': project.name}
            all_bookings = self.env['unit.reservation'].search(
                [('building', '=', project.id), ('state', '!=', 'draft'),
                 ('date', '<=', financial_year_end), ('date', '>=', financial_year_start)])
            confirmed_bookings = all_bookings.filtered(lambda x: x.state == 'confirmed')
            booking_count = len(confirmed_bookings)
            registered_count = len(confirmed_bookings.filtered(lambda x: x.registration_status == 'registered'))
            pending_registration_count = booking_count - registered_count
            sdr_pending = len(confirmed_bookings.filtered(lambda x: not x.stamp_duty_collected))

            project_data['booking_count'] = len(confirmed_bookings)
            project_data['registered_count'] = registered_count
            project_data['pending_registration_count'] = pending_registration_count
            project_data['sdr_pending_count'] = sdr_pending

            projection = self.env['project.target.line'].search([('month', '=', month), ('target_id.project_id', '=', project.id)])

            project_data['projection_count'] = sum(projection.mapped('inventory'))

            bookings = all_bookings.filtered(lambda x: actual_date_to >= x.date.strftime("%Y-%m-%d %H:%M:%S") >= actual_date_from)
            achieved_bookings = bookings.filtered(lambda x: x.state == 'confirmed')
            cancelled_bookings = bookings.filtered(lambda x: x.state == 'canceled')
            project_data['achieved_count'] = len(achieved_bookings)
            project_data['cancellation_count'] = len(cancelled_bookings)
            project_data['projection_av'] = sum(projection.mapped('amount'))
            project_data['achieved_av'] = sum(achieved_bookings.mapped('flat_cost'))
            project_data['cancellation_av'] = sum(cancelled_bookings.mapped('flat_cost'))

            data.append(project_data)

            totals['booking_count'] += project_data['booking_count']
            totals['registered_count'] += project_data['registered_count']
            totals['pending_registration_count'] += project_data['pending_registration_count']
            totals['sdr_pending_count'] += project_data['sdr_pending_count']
            totals['projection_count'] += project_data['projection_count']
            totals['achieved_count'] += project_data['achieved_count']
            totals['cancellation_count'] += project_data['cancellation_count']
            totals['projection_av'] += project_data['projection_av']
            totals['achieved_av'] += project_data['achieved_av']
            totals['cancellation_av'] += project_data['cancellation_av']
        return {'data': data, 'totals': totals, 'month': month}
