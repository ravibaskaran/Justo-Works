# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class BetaClusterHeadReport(models.TransientModel):  # change this
    _name = 'beta.cluster.head.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Cluster Head Wise Booking Report')  # change this
    date = fields.Date()
    month_wise = fields.Boolean()
    summary_wise = fields.Boolean()
    from_date = fields.Date()
    to_date = fields.Date()
    gross = fields.Boolean("Gross")
    cancelled = fields.Boolean("Cancelled")
    net = fields.Boolean("Net")

    @api.constrains('gross', 'cancelled', 'net')
    def _check_only_two_selected(self):
        for record in self:
            selected_count = sum([record.gross, record.cancelled, record.net])
            if selected_count > 2:
                raise ValidationError("You can only select up to two checkboxes (Gross, Cancelled, or Net).")

    @api.constrains('from_date', 'to_date')
    def _check_date_diff_and_financial_year(self):
        for record in self:
            if record.month_wise:
                if record.from_date and record.to_date:
                    # Convert fields to datetime objects
                    from_date = fields.Date.from_string(record.from_date)
                    to_date = fields.Date.from_string(record.to_date)

                    # Calculate the difference in months using relativedelta
                    delta = relativedelta(to_date, from_date)

                    # Ensure that the difference does not exceed 12 months
                    if delta.years * 12 + delta.months > 12:
                        raise ValidationError("The date range should not exceed 12 months.")

                    # Check if both dates fall within the same financial year
                    if record.from_date.month > 3:
                        year = from_date.year
                    else:
                        year = from_date.year - 1
                    financial_year_start = datetime(year, 4, 1).date()
                    financial_year_end = datetime(year + 1, 3, 31).date()
                    if not (financial_year_start <= from_date <= financial_year_end) or not (
                            financial_year_start <= to_date <= financial_year_end):
                        raise ValidationError(
                            "The selected dates must fall within the same financial year (April 1st to March 31st).")

    @api.model
    def default_get(self, fields_list):
        res = super(BetaClusterHeadReport, self).default_get(fields_list)
        today = datetime.today()
        res['date'] = today
        res['from_date'] = today
        res['to_date'] = today
        return res

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('cluster_head_report.cluster_head_report')._render({
            'doc': doc,
            'date': self.date,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'month_wise': self.month_wise,
            'summary_wise': self.summary_wise,
            'gross': self.gross,  # Pass the Gross checkbox value (True/False)
            'cancelled': self.cancelled,  # Pass the Cancelled checkbox value (True/False)
            'net': self.net,
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

    def get_current_inv_date(self, tz_datetime):
        fmt = "%d/%m/%Y %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_timezone.strftime(fmt), fmt) - datetime.strptime(
            now_utc.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime

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

        if self.month_wise:
            if self.from_date.month > 3:
                year = str(self.from_date.year)
            else:
                year = str(self.from_date.year - 1)
        else:
            if self.date.month > 3:
                year = str(self.date.year)
            else:
                year = str(self.date.year - 1)
        month_keys = []
        month_vals = []
        financial_year_start = self.get_actual_date(year + '-04-01' + " 00:00:00")
        financial_year_end = self.get_actual_date(str(int(year) + 1) + '-03-31' + " 23:59:59")

        financial_year_start2 = datetime(int(year), 4, 1).date()  # April 1st of the financial year
        financial_year_end2 = datetime(int(year) + 1, 3, 31).date()
        for project in projects:
            target = self.env['project.target'].search([
                ('project_id', '=', project.id),
                ('financial_year.date_from', '<=', self.from_date),
                ('financial_year.date_to', '>=', self.from_date)
            ])
            target_booking_count = sum(target.target_line_ids.mapped('inventory'))
            bookings = self.env['unit.reservation'].search(
                [('building', '=', project.id), ('state', '!=', 'draft'),
                 ('date', '<=', financial_year_end), ('date', '>=', financial_year_start)])
            booking_count = len(bookings.filtered(lambda x: x.state == 'confirmed'))
            achieved_percentage = booking_count / target_booking_count * 100 if target_booking_count != 0 else 100
            booking_cancelled = self.env['unit.reservation'].search(
                [('building', '=', project.id), ('state', '=', 'canceled'),
                 ('cancellation_date', '<=', financial_year_end2), ('cancellation_date', '>=', financial_year_start2),
                 ]
            )
            if not self.month_wise:
                month_list = [self.date.strftime("%B %Y")]
                target_booking_count = sum(self.env['project.target.line'].search([
                ('target_id.project_id', '=', project.id),
                ('month', 'in', month_list)]).mapped('inventory'))
                day_bookings = bookings.filtered(lambda x: self.get_current_inv_date(x.date.strftime('%d/%m/%Y %H:%M:%S')).date() == self.date)
                day_cancel = booking_cancelled.filtered(
                    lambda x: x.cancellation_date and x.cancellation_date == self.date)
                day_gross_bookings = day_bookings.filtered(lambda x: x.state in ['confirmed', 'canceled'])
                day_cancelled_bookings = day_cancel.filtered(lambda x: x.state == 'canceled')

                current_month = self.date.replace(day=1)
                day_gross_bookings_count = len(day_gross_bookings)
                day_cancelled_bookings_count = len(day_cancelled_bookings)
                day_net_bookings_count = day_gross_bookings_count - day_cancelled_bookings_count
                day_gross_bookings_value = sum(day_gross_bookings.mapped('flat_cost')) / 10000000
                day_cancelled_bookings_value = sum(day_cancelled_bookings.mapped('flat_cost')) / 10000000
                day_net_bookings_value = day_gross_bookings_value - day_cancelled_bookings_value
                month_bookings = bookings.filtered(lambda x: self.get_current_inv_date(x.date.strftime('%d/%m/%Y %H:%M:%S')).month == self.date.month)
                month_cancel = booking_cancelled.filtered(lambda x: x.cancellation_date.month == current_month.month)

                month_gross_bookings = month_bookings.filtered(lambda x: x.state in ['confirmed', 'canceled'])
                month_cancelled_bookings = month_cancel.filtered(lambda x: x.state == 'canceled')
                month_gross_bookings_count = len(month_gross_bookings)
                month_cancelled_bookings_count = len(month_cancelled_bookings)
                month_net_bookings_count = month_gross_bookings_count - month_cancelled_bookings_count
                month_gross_bookings_value = sum(month_gross_bookings.mapped('flat_cost')) / 10000000
                month_cancelled_bookings_value = sum(month_cancelled_bookings.mapped('flat_cost')) / 10000000
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

                sub_region_id = project.sub_region_id  # Assuming sub_region_id represents the cluster
                cluster_head_id = project.cluster_head_id
                if sub_region_id in data['data']:
                    data['data'][sub_region_id]['target'] += target_booking_count
                    data['data'][sub_region_id]['booking_count'] += booking_count
                    data['data'][sub_region_id][
                        'day_gross_bookings_count'] += day_gross_bookings_count
                    data['data'][sub_region_id][
                        'day_cancelled_bookings_count'] += day_cancelled_bookings_count
                    data['data'][sub_region_id][
                        'day_net_bookings_count'] += day_net_bookings_count
                    data['data'][sub_region_id][
                        'day_gross_bookings_value'] += day_gross_bookings_value
                    data['data'][sub_region_id][
                        'day_cancelled_bookings_value'] += day_cancelled_bookings_value
                    data['data'][sub_region_id][
                        'day_net_bookings_value'] += day_net_bookings_value
                    data['data'][sub_region_id][
                        'month_gross_bookings_count'] += month_gross_bookings_count
                    data['data'][sub_region_id][
                        'month_cancelled_bookings_count'] += month_cancelled_bookings_count
                    data['data'][sub_region_id][
                        'month_net_bookings_count'] += month_net_bookings_count
                    data['data'][sub_region_id][
                        'month_gross_bookings_value'] += month_gross_bookings_value
                    data['data'][sub_region_id][
                        'month_cancelled_bookings_value'] += month_cancelled_bookings_value
                    data['data'][sub_region_id][
                        'month_net_bookings_value'] += month_net_bookings_value
                    if project.cluster_head_id in data['data'][sub_region_id]['data']:
                        data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id] = line_details
                        data['data'][sub_region_id]['data'][project.cluster_head_id]['target'] += target_booking_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id]['booking_count'] += booking_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_gross_bookings_count'] += day_gross_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_cancelled_bookings_count'] += day_cancelled_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_net_bookings_count'] += day_net_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_gross_bookings_value'] += day_gross_bookings_value
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_cancelled_bookings_value'] += day_cancelled_bookings_value
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'day_net_bookings_value'] += day_net_bookings_value
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_gross_bookings_count'] += month_gross_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_cancelled_bookings_count'] += month_cancelled_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_net_bookings_count'] += month_net_bookings_count
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_gross_bookings_value'] += month_gross_bookings_value
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_cancelled_bookings_value'] += month_cancelled_bookings_value
                        data['data'][sub_region_id]['data'][project.cluster_head_id][
                            'month_net_bookings_value'] += month_net_bookings_value
                    else:
                        data['data'][sub_region_id]['data'][project.cluster_head_id] = {
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

                if sub_region_id not in data['data']:
                    data['data'][sub_region_id] = {
                        # 'name': project.sub_region_id.name,
                        'data': {
                            project.cluster_head_id: {
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
                        },  # Stores Cluster Heads
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
            else:
                slno = 1
                sub_region_id = project.sub_region_id
                cluster_head_id = project.cluster_head_id

                data['booking_count'] += booking_count
                if project.cluster_head_id in data['data']:

                    if data['data'][project.cluster_head_id]['booking_count']:
                        data['data'][project.cluster_head_id]['booking_count'] += booking_count
                current_month = self.from_date.replace(day=1)
                end_date = self.to_date.replace(day=1)
                while current_month <= end_date:
                    month_list = [current_month.strftime("%B %Y")]
                    target_booking_count = sum(self.env['project.target.line'].search([
                        ('target_id.project_id', '=', project.id),
                        ('month', 'in', month_list),
                    ]).mapped('inventory'))
                    data['target'] += target_booking_count

                    if project.cluster_head_id in data['data']:
                        if data['data'][project.cluster_head_id]['target']:
                            data['data'][project.cluster_head_id]['target'] += target_booking_count

                    month_bookings = bookings.filtered(lambda x: self.get_current_inv_date(x.date.strftime('%d/%m/%Y %H:%M:%S')).month == current_month.month)
                    month_cancel = booking_cancelled.filtered(lambda x: x.cancellation_date.month == current_month.month)
                    month_gross_bookings = month_bookings.filtered(lambda x: x.state in ['confirmed', 'canceled'])
                    month_cancelled_bookings = month_cancel.filtered(lambda x: x.state == 'canceled')


                    month_gross_bookings_count = len(month_gross_bookings)
                    month_cancelled_bookings_count = len(month_cancelled_bookings)
                    month_net_bookings_count = month_gross_bookings_count - month_cancelled_bookings_count
                    month_gross_bookings_value = sum(month_gross_bookings.mapped('flat_cost')) / 10000000
                    month_cancelled_bookings_value = sum(month_cancelled_bookings.mapped('flat_cost')) / 10000000
                    month_net_bookings_value = month_gross_bookings_value - month_cancelled_bookings_value
                    line_details = {
                        'name': project.name,
                        'target': target_booking_count,
                        'achieved_percentage': "{:.2f}".format(achieved_percentage),
                        f'month_{slno}_gross_bookings_count': month_gross_bookings_count,
                        f'month_{slno}_cancelled_bookings_count': month_cancelled_bookings_count,
                        f'month_{slno}_net_bookings_count': month_net_bookings_count,
                        f'month_{slno}_gross_bookings_value': month_gross_bookings_value,
                        f'month_{slno}_cancelled_bookings_value': month_cancelled_bookings_value,
                        f'month_{slno}_net_bookings_value': month_net_bookings_value,
                    }
                    if f'month_{slno}' in month_keys:
                        pass
                    else:
                        month_keys.append(f'month_{slno}')
                    if current_month in month_vals:
                        pass
                    else:
                        month_vals.append(current_month)

                    if f'month_{slno}_gross_bookings_count' in data:
                        data[f'month_{slno}_gross_bookings_count'] += month_gross_bookings_count
                    else:
                        data[f'month_{slno}_gross_bookings_count'] = month_gross_bookings_count
                    if f'month_{slno}_cancelled_bookings_count' in data:
                        data[f'month_{slno}_cancelled_bookings_count'] += month_cancelled_bookings_count
                    else:
                        data[f'month_{slno}_cancelled_bookings_count'] = month_cancelled_bookings_count
                    if f'month_{slno}_net_bookings_count' in data:
                        data[f'month_{slno}_net_bookings_count'] += month_net_bookings_count
                    else:
                        data[f'month_{slno}_net_bookings_count'] = month_net_bookings_count
                    if f'month_{slno}_gross_bookings_value' in data:
                        data[f'month_{slno}_gross_bookings_value'] += month_gross_bookings_value
                    else:
                        data[f'month_{slno}_gross_bookings_value'] = month_gross_bookings_value
                    if f'month_{slno}_cancelled_bookings_value' in data:
                        data[f'month_{slno}_cancelled_bookings_value'] += month_cancelled_bookings_value
                    else:
                        data[f'month_{slno}_cancelled_bookings_value'] = month_cancelled_bookings_value
                    if f'month_{slno}_net_bookings_value' in data:
                        data[f'month_{slno}_net_bookings_value'] += month_net_bookings_value
                    else:
                        data[f'month_{slno}_net_bookings_value'] = month_net_bookings_value

                    if sub_region_id in data['data']:
                        if f'month_{slno}_gross_bookings_count' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_gross_bookings_count'] += month_gross_bookings_count
                        else:
                            data['data'][sub_region_id][
                                f'month_{slno}_gross_bookings_count'] = month_gross_bookings_count
                        if f'month_{slno}_cancelled_bookings_count' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_cancelled_bookings_count'] += month_cancelled_bookings_count
                        else:
                            data['data'][sub_region_id][
                                f'month_{slno}_cancelled_bookings_count'] = month_cancelled_bookings_count
                        if f'month_{slno}_net_bookings_count' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_net_bookings_count'] += month_net_bookings_count
                        else:
                            data['data'][sub_region_id][
                                f'month_{slno}_net_bookings_count'] = month_net_bookings_count
                        if f'month_{slno}_gross_bookings_value' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_gross_bookings_value'] += month_gross_bookings_value
                        else:
                            data['data'][sub_region_id][
                                f'month_{slno}_gross_bookings_value'] = month_gross_bookings_value
                        if f'month_{slno}_cancelled_bookings_value' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_cancelled_bookings_value'] += month_cancelled_bookings_value
                        else:
                            data['data'][sub_region_id][
                                f'month_{slno}_cancelled_bookings_value'] = month_cancelled_bookings_value
                        if f'month_{slno}_net_bookings_value' in data['data'][sub_region_id]:
                            data['data'][sub_region_id][
                                f'month_{slno}_net_bookings_value'] += month_net_bookings_value
                        else:
                            data['data'][sub_region_id][f'month_{slno}_net_bookings_value'] = month_net_bookings_value

                        if project.cluster_head_id in data['data'][sub_region_id]['data']:
                            if project.id in data['data'][sub_region_id]['data'][project.cluster_head_id]['data']:
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_gross_bookings_count'] = month_gross_bookings_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_cancelled_bookings_count'] = month_cancelled_bookings_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_net_bookings_count'] = month_net_bookings_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_gross_bookings_value'] = month_gross_bookings_value
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_cancelled_bookings_value'] = month_cancelled_bookings_value
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id][
                                    f'month_{slno}_net_bookings_value'] = month_net_bookings_value
                                data['data'][sub_region_id]['target'] += target_booking_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    'target'] += target_booking_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id]['target'] += target_booking_count
                            else:
                                data['data'][sub_region_id]['target'] += target_booking_count
                                data['data'][sub_region_id]['booking_count'] += booking_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['target'] += target_booking_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['booking_count'] += booking_count
                                data['data'][sub_region_id]['data'][project.cluster_head_id]['data'][project.id] = line_details

                            if f'month_{slno}_gross_bookings_count' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_gross_bookings_count'] += month_gross_bookings_count
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_gross_bookings_count'] = month_gross_bookings_count
                            if f'month_{slno}_cancelled_bookings_count' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_cancelled_bookings_count'] += month_cancelled_bookings_count
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_cancelled_bookings_count'] = month_cancelled_bookings_count
                            if f'month_{slno}_net_bookings_count' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_net_bookings_count'] += month_net_bookings_count
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_net_bookings_count'] = month_net_bookings_count
                            if f'month_{slno}_gross_bookings_value' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_gross_bookings_value'] += month_gross_bookings_value
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_gross_bookings_value'] = month_gross_bookings_value
                            if f'month_{slno}_cancelled_bookings_value' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_cancelled_bookings_value'] += month_cancelled_bookings_value
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_cancelled_bookings_value'] = month_cancelled_bookings_value
                            if f'month_{slno}_net_bookings_value' in data['data'][sub_region_id]['data'][project.cluster_head_id]:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_net_bookings_value'] += month_net_bookings_value
                            else:
                                data['data'][sub_region_id]['data'][project.cluster_head_id][
                                    f'month_{slno}_net_bookings_value'] = month_net_bookings_value
                        else:
                            data['data'][sub_region_id]['target'] += target_booking_count
                            data['data'][sub_region_id]['booking_count'] += booking_count
                            data['data'][sub_region_id]['data'][project.cluster_head_id] = {
                                'data': {
                                    project.id: line_details
                                },
                                'target': target_booking_count,
                                'booking_count': booking_count,
                                f'month_{slno}_gross_bookings_count': month_gross_bookings_count,
                                f'month_{slno}_cancelled_bookings_count': month_cancelled_bookings_count,
                                f'month_{slno}_net_bookings_count': month_net_bookings_count,
                                f'month_{slno}_gross_bookings_value': month_gross_bookings_value,
                                f'month_{slno}_cancelled_bookings_value': month_cancelled_bookings_value,
                                f'month_{slno}_net_bookings_value': month_net_bookings_value,
                            }


                    else:
                        data['data'][sub_region_id] = {

                            'data': {
                                project.cluster_head_id: {
                                    'data': {
                                        project.id: line_details
                                    },
                                    'target': target_booking_count,
                                    'booking_count': booking_count,
                                    f'month_{slno}_gross_bookings_count': month_gross_bookings_count,
                                    f'month_{slno}_cancelled_bookings_count': month_cancelled_bookings_count,
                                    f'month_{slno}_net_bookings_count': month_net_bookings_count,
                                    f'month_{slno}_gross_bookings_value': month_gross_bookings_value,
                                    f'month_{slno}_cancelled_bookings_value': month_cancelled_bookings_value,
                                    f'month_{slno}_net_bookings_value': month_net_bookings_value,
                                }
                            },
                            'target': target_booking_count,
                            'booking_count': booking_count,
                            f'month_{slno}_gross_bookings_count': month_gross_bookings_count,
                            f'month_{slno}_cancelled_bookings_count': month_cancelled_bookings_count,
                            f'month_{slno}_net_bookings_count': month_net_bookings_count,
                            f'month_{slno}_gross_bookings_value': month_gross_bookings_value,
                            f'month_{slno}_cancelled_bookings_value': month_cancelled_bookings_value,
                            f'month_{slno}_net_bookings_value': month_net_bookings_value,
                        }
                    slno += 1
                    current_month = current_month + relativedelta(months=1)
        data
        return {'data': data, 'month_keys': month_keys, 'month_vals': month_vals}
