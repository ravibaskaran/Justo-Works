# -*- coding: utf-8 -*-
from pytz import timezone
import calendar
from odoo import models, fields
from datetime import datetime


class BetaBudgetActualComparison(models.TransientModel):  # change this
    _name = 'beta.budget.actual.comparison'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Budget Actual Comparison')  # change this
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

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('budget_actual_comparison.budget_actual_comparison_report')._render({
            'doc': doc,
        })

    def _get_report_data(self):
        regions = self.env['regions'].search([('is_parent', '=', True)])
        if int(self.month) > 3:
            date_from = self.financial_year + '-' + self.month + '-01'
            _, last_day = calendar.monthrange(int(self.financial_year), int(self.month))
            date_to = self.financial_year + '-' + self.month + '-' + str(last_day)
            prev_date_from = str(int(self.financial_year) - 1) + '-' + self.month + '-01'
            prev_date_to = str(int(self.financial_year) - 1) + '-' + self.month + '-' + str(last_day)
        else:
            date_from = str(int(self.financial_year) + 1) + '-' + self.month + '-01'
            _, last_day = calendar.monthrange(int(self.financial_year) + 1, int(self.month))
            date_to = str(int(self.financial_year) + 1) + '-' + self.month + '-' + str(last_day)
            prev_date_from = self.financial_year + '-' + self.month + '-01'
            prev_date_to = self.financial_year + '-' + self.month + '-' + str(last_day)
        date_from_object = datetime.strptime(date_from, '%Y-%m-%d')
        prev_date_from_object = datetime.strptime(prev_date_from, '%Y-%m-%d')
        month = date_from_object.strftime("%B %Y")
        actual_date_from = self.get_actual_date(date_from + " 00:00:00")
        actual_date_to = self.get_actual_date(date_to + " 23:59:59")
        prev_actual_date_from = self.get_actual_date(prev_date_from + " 00:00:00")
        prev_actual_date_to = self.get_actual_date(prev_date_to + " 23:59:59")
        data = []
        total_budget_booking_count = total_actual_booking_count = total_prev_actual_booking_count = \
            total_booking_count_variance = total_prev_booking_count_variance = total_budget_booking_value = \
            total_actual_booking_value = total_prev_actual_booking_value = total_booking_value_variance = \
            total_prev_booking_value_variance = total_budget_registration_count = total_actual_registration_count = \
            total_prev_actual_registration_count = total_registration_count_variance = \
            total_prev_registration_count_variance = total_budget_registration_value = \
            total_actual_registration_value = total_prev_actual_registration_value = \
            total_registration_value_variance = total_prev_registration_value_variance = 0
        for region in regions:
            projects = self.env['building'].search([('region_id', '=', region.id)])
            budget = self.env['project.target.line'].search(
                [('month', '=', month), ('target_id.project_id', 'in', projects.ids)])
            bookings = self.env['unit.reservation'].search(
                [('building', 'in', projects.ids), ('state', '=', 'confirmed'), ('date', '<=', actual_date_to),
                 ('date', '>=', actual_date_from)])
            registrations = self.env['project.registration'].search(
                [('project_id', 'in', projects.ids), ('state', 'not in', ('draft', 'canceled')), ('registration_date', '<=', date_to),
                 ('registration_date', '>=', date_from)])
            booking_of_registrations = self.env['unit.reservation'].search(
                [('building_unit', 'in', registrations.mapped('flat_id').ids), ('state', '=', 'confirmed')])
            prev_bookings = self.env['unit.reservation'].search(
                [('building', 'in', projects.ids), ('state', '=', 'confirmed'), ('date', '<=', prev_actual_date_to),
                 ('date', '>=', prev_actual_date_from)])
            prev_registrations = self.env['project.registration'].search(
                [('project_id', 'in', projects.ids), ('state', 'not in', ('draft', 'canceled')), ('registration_date', '<=', prev_date_to),
                 ('registration_date', '>=', prev_date_from)])
            booking_of_prev_registrations = self.env['unit.reservation'].search(
                [('building_unit', 'in', prev_registrations.mapped('flat_id').ids), ('state', '=', 'confirmed')])

            budget_booking_count = sum(budget.mapped('inventory'))
            actual_booking_count = len(bookings)
            prev_actual_booking_count = len(prev_bookings)
            booking_count_variance = actual_booking_count - budget_booking_count
            prev_booking_count_variance = actual_booking_count - prev_actual_booking_count

            total_budget_booking_count += budget_booking_count
            total_actual_booking_count += actual_booking_count
            total_prev_actual_booking_count += prev_actual_booking_count
            total_booking_count_variance += booking_count_variance
            total_prev_booking_count_variance += prev_booking_count_variance

            budget_booking_value = sum(budget.mapped('amount')) / 100000
            actual_booking_value = sum(bookings.mapped('flat_cost')) / 100000
            prev_actual_booking_value = sum(prev_bookings.mapped('flat_cost')) / 100000
            booking_value_variance = actual_booking_value - budget_booking_value
            prev_booking_value_variance = actual_booking_value - prev_actual_booking_value

            total_budget_booking_value += budget_booking_value
            total_actual_booking_value += actual_booking_value
            total_prev_actual_booking_value += prev_actual_booking_value
            total_booking_value_variance += booking_value_variance
            total_prev_booking_value_variance += prev_booking_value_variance

            budget_registration_count = sum(budget.mapped('registration'))
            actual_registration_count = len(registrations)
            prev_actual_registration_count = len(prev_registrations)
            registration_count_variance = actual_registration_count - budget_registration_count
            prev_registration_count_variance = actual_registration_count - prev_actual_registration_count

            total_budget_registration_count += budget_registration_count
            total_actual_registration_count += actual_registration_count
            total_prev_actual_registration_count += prev_actual_registration_count
            total_registration_count_variance += registration_count_variance
            total_prev_registration_count_variance += prev_registration_count_variance

            budget_registration_value = sum(budget.mapped('registration_amount')) / 100000
            actual_registration_value = sum(booking_of_registrations.mapped('flat_cost')) / 100000
            prev_actual_registration_value = sum(booking_of_prev_registrations.mapped('flat_cost')) / 100000
            registration_value_variance = actual_registration_value - budget_registration_value
            prev_registration_value_variance = actual_registration_value - prev_actual_registration_value

            total_budget_registration_value += budget_registration_value
            total_actual_registration_value += actual_registration_value
            total_prev_actual_registration_value += prev_actual_registration_value
            total_registration_value_variance += registration_value_variance
            total_prev_registration_value_variance += prev_registration_value_variance

            data.append({
                'region': region.name,

                'budget_booking_count': budget_booking_count,
                'actual_booking_count': actual_booking_count,
                'booking_count_variance': booking_count_variance,
                'prev_actual_booking_count': prev_actual_booking_count,
                'prev_booking_count_variance': prev_booking_count_variance,

                'budget_booking_value': budget_booking_value,
                'actual_booking_value': actual_booking_value,
                'booking_value_variance': booking_value_variance,
                'prev_actual_booking_value': prev_actual_booking_value,
                'prev_booking_value_variance': prev_booking_value_variance,

                'budget_registration_count': budget_registration_count,
                'actual_registration_count': actual_registration_count,
                'registration_count_variance': registration_count_variance,
                'prev_actual_registration_count': prev_actual_registration_count,
                'prev_registration_count_variance': prev_registration_count_variance,

                'budget_registration_value': budget_registration_value,
                'actual_registration_value': actual_registration_value,
                'registration_value_variance': registration_value_variance,
                'prev_actual_registration_value': prev_actual_registration_value,
                'prev_registration_value_variance': prev_registration_value_variance,
            })
        data.append({
            'region': 'Total',

            'budget_booking_count': total_budget_booking_count,
            'actual_booking_count': total_actual_booking_count,
            'booking_count_variance': total_booking_count_variance,
            'prev_actual_booking_count': total_prev_actual_booking_count,
            'prev_booking_count_variance': total_prev_booking_count_variance,

            'budget_booking_value': total_budget_booking_value,
            'actual_booking_value': total_actual_booking_value,
            'booking_value_variance': total_booking_value_variance,
            'prev_actual_booking_value': total_prev_actual_booking_value,
            'prev_booking_value_variance': total_prev_booking_value_variance,

            'budget_registration_count': total_budget_registration_count,
            'actual_registration_count': total_actual_registration_count,
            'registration_count_variance': total_registration_count_variance,
            'prev_actual_registration_count': total_prev_actual_registration_count,
            'prev_registration_count_variance': total_prev_registration_count_variance,

            'budget_registration_value': total_budget_registration_value,
            'actual_registration_value': total_actual_registration_value,
            'registration_value_variance': total_registration_value_variance,
            'prev_actual_registration_value': total_prev_actual_registration_value,
            'prev_registration_value_variance': total_prev_registration_value_variance,
        })
        return {
            'data': data,
            'month': date_from_object.strftime("%b-%y"),
            'prev_month': prev_date_from_object.strftime("%b-%y")
        }
