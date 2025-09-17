# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaClusterHeadReport(models.TransientModel):  # change this
    _name = 'beta.cluster.head.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Cluster Head Wise Booking Report')  # change this
    date = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaClusterHeadReport, self).default_get(fields_list)
        today = datetime.today()
        res['date'] = today
        return res

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('cluster_head_report.cluster_head_report')._render({
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
        projects = self.env['building'].search([])
        data = {
            'data': {},
            'target': 0,
            'booking_count': 0,
            'day_gross_bookings_count': 0,
            'day_cancelled_bookings_count': 0,
            'day_net_bookings_count': 0,
            'day_gross_bookings_value': 0,
            'day_cancelled_bookings_value': 0,
            'day_net_bookings_value': 0,
            'month_gross_bookings_count': 0,
            'month_cancelled_bookings_count': 0,
            'month_net_bookings_count': 0,
            'month_gross_bookings_value': 0,
            'month_cancelled_bookings_value': 0,
            'month_net_bookings_value': 0,
        }
        if self.date.month > 3:
            year = str(self.date.year)
        else:
            year = str(self.date.year - 1)

        financial_year_start = self.get_actual_date(year + '-04-01' + " 00:00:00")
        financial_year_end = self.get_actual_date(str(int(year) + 1) + '-03-31' + " 23:59:59")
        for project in projects:
            target = self.env['project.target'].search([('project_id', '=', project.id), ('financial_year.date_from', '=', year + '-04-01')])
            target_booking_count = sum(target.target_line_ids.mapped('inventory'))
            bookings = self.env['unit.reservation'].search(
                [('building', '=', project.id), ('state', '!=', 'draft'),
                 ('date', '<=', financial_year_end), ('date', '>=', financial_year_start)])
            booking_count = len(bookings.filtered(lambda x: x.state == 'confirmed'))
            achieved_percentage = booking_count / target_booking_count * 100 if target_booking_count != 0 else 100

            day_bookings = bookings.filtered(lambda x: x.date.date() == self.date)
            day_gross_bookings = day_bookings.filtered(lambda x: x.state == 'confirmed')
            day_cancelled_bookings = day_bookings.filtered(lambda x: x.state == 'canceled')
            day_gross_bookings_count = len(day_gross_bookings)
            day_cancelled_bookings_count = len(day_cancelled_bookings)
            day_net_bookings_count = day_gross_bookings_count - day_cancelled_bookings_count
            day_gross_bookings_value = sum(day_gross_bookings.mapped('flat_cost')) / 100000000
            day_cancelled_bookings_value = sum(day_cancelled_bookings.mapped('flat_cost')) / 100000000
            day_net_bookings_value = day_gross_bookings_value - day_cancelled_bookings_value
            month_bookings = bookings.filtered(lambda x: x.date.month == self.date.month)
            month_gross_bookings = month_bookings.filtered(lambda x: x.state == 'confirmed')
            month_cancelled_bookings = month_bookings.filtered(lambda x: x.state == 'canceled')
            month_gross_bookings_count = len(month_gross_bookings)
            month_cancelled_bookings_count = len(month_cancelled_bookings)
            month_net_bookings_count = month_gross_bookings_count - month_cancelled_bookings_count
            month_gross_bookings_value = sum(month_gross_bookings.mapped('flat_cost')) / 100000000
            month_cancelled_bookings_value = sum(month_cancelled_bookings.mapped('flat_cost')) / 100000000
            month_net_bookings_value = month_gross_bookings_value - month_cancelled_bookings_value
            line_details = {
                'name': project.name,
                'target': target_booking_count,
                'achieved_percentage': "{:.2f}".format(achieved_percentage),
                'day_gross_bookings_count': day_gross_bookings_count,
                'day_cancelled_bookings_count': day_cancelled_bookings_count,
                'day_net_bookings_count': day_net_bookings_count,
                'day_gross_bookings_value': day_gross_bookings_value,
                'day_cancelled_bookings_value': day_cancelled_bookings_value,
                'day_net_bookings_value': day_net_bookings_value,
                'month_gross_bookings_count': month_gross_bookings_count,
                'month_cancelled_bookings_count': month_cancelled_bookings_count,
                'month_net_bookings_count': month_net_bookings_count,
                'month_gross_bookings_value': month_gross_bookings_value,
                'month_cancelled_bookings_value': month_cancelled_bookings_value,
                'month_net_bookings_value': month_net_bookings_value,
            }
            data['target'] += target_booking_count
            data['booking_count'] += booking_count
            data['day_gross_bookings_count'] += day_gross_bookings_count
            data['day_cancelled_bookings_count'] += day_cancelled_bookings_count
            data['day_net_bookings_count'] += day_net_bookings_count
            data['day_gross_bookings_value'] += day_gross_bookings_value
            data['day_cancelled_bookings_value'] += day_cancelled_bookings_value
            data['day_net_bookings_value'] += day_net_bookings_value
            data['month_gross_bookings_count'] += month_gross_bookings_count
            data['month_cancelled_bookings_count'] += month_cancelled_bookings_count
            data['month_net_bookings_count'] += month_net_bookings_count
            data['month_gross_bookings_value'] += month_gross_bookings_value
            data['month_cancelled_bookings_value'] += month_cancelled_bookings_value
            data['month_net_bookings_value'] += month_net_bookings_value

            if project.cluster_head_id in data['data']:
                data['data'][project.cluster_head_id]['data'][project.id] = line_details
                data['data'][project.cluster_head_id]['target'] += target_booking_count
                data['data'][project.cluster_head_id]['booking_count'] += booking_count
                data['data'][project.cluster_head_id]['day_gross_bookings_count'] += day_gross_bookings_count
                data['data'][project.cluster_head_id]['day_cancelled_bookings_count'] += day_cancelled_bookings_count
                data['data'][project.cluster_head_id]['day_net_bookings_count'] += day_net_bookings_count
                data['data'][project.cluster_head_id]['day_gross_bookings_value'] += day_gross_bookings_value
                data['data'][project.cluster_head_id]['day_cancelled_bookings_value'] += day_cancelled_bookings_value
                data['data'][project.cluster_head_id]['day_net_bookings_value'] += day_net_bookings_value
                data['data'][project.cluster_head_id]['month_gross_bookings_count'] += month_gross_bookings_count
                data['data'][project.cluster_head_id]['month_cancelled_bookings_count'] += month_cancelled_bookings_count
                data['data'][project.cluster_head_id]['month_net_bookings_count'] += month_net_bookings_count
                data['data'][project.cluster_head_id]['month_gross_bookings_value'] += month_gross_bookings_value
                data['data'][project.cluster_head_id]['month_cancelled_bookings_value'] += month_cancelled_bookings_value
                data['data'][project.cluster_head_id]['month_net_bookings_value'] += month_net_bookings_value
            else:
                data['data'][project.cluster_head_id] = {
                    'data': {
                        project.id: line_details
                    },
                    'target': target_booking_count,
                    'booking_count': booking_count,
                    'day_gross_bookings_count': day_gross_bookings_count,
                    'day_cancelled_bookings_count': day_cancelled_bookings_count,
                    'day_net_bookings_count': day_net_bookings_count,
                    'day_gross_bookings_value': day_gross_bookings_value,
                    'day_cancelled_bookings_value': day_cancelled_bookings_value,
                    'day_net_bookings_value': day_net_bookings_value,
                    'month_gross_bookings_count': month_gross_bookings_count,
                    'month_cancelled_bookings_count': month_cancelled_bookings_count,
                    'month_net_bookings_count': month_net_bookings_count,
                    'month_gross_bookings_value': month_gross_bookings_value,
                    'month_cancelled_bookings_value': month_cancelled_bookings_value,
                    'month_net_bookings_value': month_net_bookings_value,
                }
        return {'data': data}
