from odoo import http
from odoo.http import request
from datetime import datetime, timedelta, date
from pytz import timezone


class JupiterDashboardDeux(http.Controller):

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(request.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    @http.route('/jupiter_dashboard_deux/call_list_view', auth='public', type='json')
    def jupiter_dashboard_deux_call_list_view(self, domain, model, name):
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'view_mode': 'tree,form',
            'res_model': model,
            'views': [(False, 'list'), (False, 'form')],
            'domain': domain,
            'context': {'create': False}
        }

    @http.route('/jupiter_dashboard_deux/call_report', auth='public', type='json')
    def jupiter_dashboard_deux_call_report(self, report_attr, model):
        report_obj = request.env[model].create(report_attr)
        report_obj.get_html()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Report',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': model,
            'views': [(False, 'form')],
            'res_id': report_obj.id,
        }

    @http.route('/jupiter_dashboard_deux/get_cp_count', auth='public', type='json')
    def jupiter_dashboard_deux_get_cp_count(self):
        current_datetime = datetime.now()
        months = []
        create_cps_list = []
        active_cps_list = []
        for i in range(5, -1, -1):
            start_month = current_datetime.month - i
            start_year = current_datetime.year - 1 if start_month <= 0 else current_datetime.year
            start_month = (start_month + 12) % 12 or 12
            start_date = datetime(start_year, start_month, 1)
            end_month = start_month % 12 + 1
            end_year = start_year if end_month != 1 else start_year + 1
            end_date = datetime(end_year, end_month, 1) - timedelta(days=1)
            months.append(start_date.strftime('%b %y'))
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            start_date_formatted = self.get_actual_date(start_date + " 00:00:00")
            end_date_formatted = self.get_actual_date(end_date + " 23:59:59")
            cps = request.env['res.partner'].search_count(
                [('is_channel', '=', True), ('create_date', '<=', end_date_formatted),
                 ('create_date', '>=', start_date_formatted)])
            bookings = request.env['unit.reservation'].search(
                [('date', '<=', end_date_formatted), ('date', '>=', start_date_formatted),
                 ('state', '=', 'confirmed')])
            cps_active = len(bookings.mapped('cp_id'))
            create_cps_list.append(cps)
            active_cps_list.append(cps_active)
        start_of_today = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_of_today + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_month_formatted = self.get_actual_date(start_of_month.strftime('%Y-%m-%d %H:%M:%S'))
        fin_year_obj = (
            date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
        fin_year_start = fin_year_obj.strftime('%Y-%m-%d')
        fin_year_start_formatted = self.get_actual_date(fin_year_start + ' 00:00:00')
        financial_year_start_month = 4
        quarter_month_starts = [4, 7, 10, 1]
        half_year_starts = [4, 10]

        year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
        quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
        quarter_start = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
        half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
        half_start = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)

        start_of_quarter_formatted = self.get_actual_date(quarter_start.strftime('%Y-%m-%d %H:%M:%S'))
        start_of_half_formatted = self.get_actual_date(half_start.strftime('%Y-%m-%d %H:%M:%S'))

        month_cp_domain = [('is_channel', '=', True), ('create_date', '>=', start_of_month_formatted),
                           ('create_date', '<=', end_formatted)]
        month_cps = request.env['res.partner'].search_count(month_cp_domain)

        quarter_cp_domain = [('is_channel', '=', True), ('create_date', '>=', start_of_quarter_formatted),
                             ('create_date', '<=', end_formatted)]
        quarter_cps = request.env['res.partner'].search_count(quarter_cp_domain)

        half_cp_domain = [('is_channel', '=', True), ('create_date', '>=', start_of_half_formatted),
                          ('create_date', '<=', end_formatted)]
        half_cps = request.env['res.partner'].search_count(half_cp_domain)

        year_cp_domain = [('is_channel', '=', True), ('create_date', '>=', fin_year_start_formatted),
                          ('create_date', '<=', end_formatted)]
        year_cps = request.env['res.partner'].search_count(year_cp_domain)

        month_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').ids

        quarter_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_quarter_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').ids

        half_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_half_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').ids

        year_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', fin_year_start_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').ids
        return {
            'months': months,
            'create_cps_list': create_cps_list,
            'active_cps_list': active_cps_list,
            'month_cps': month_cps,
            'quarter_cps': quarter_cps,
            'half_cps': half_cps,
            'year_cps': year_cps,

            'month_cps_active': len(month_cps_active),
            'quarter_cps_active': len(quarter_cps_active),
            'half_cps_active': len(half_cps_active),
            'year_cps_active': len(year_cps_active),

            'month_cp_domain': str(month_cp_domain),
            'quarter_cp_domain': str(quarter_cp_domain),
            'half_cp_domain': str(half_cp_domain),
            'year_cp_domain': str(year_cp_domain),

            'month_cp_active_domain': "[('id', 'in', " + str(month_cps_active) + ")]",
            'quarter_cp_active_domain': "[('id', 'in', " + str(quarter_cps_active) + ")]",
            'half_cp_active_domain': "[('id', 'in', " + str(half_cps_active) + ")]",
            'year_cp_active_domain': "[('id', 'in', " + str(year_cps_active) + ")]",
        }

    @http.route('/jupiter_dashboard_deux/get_last_6_month_cp_booking', auth='public', type='json')
    def jupiter_dashboard_deux_get_last_6_month_cp_booking(self):
        current_date = datetime.now()
        months = []
        bookings = []
        for i in range(5, -1, -1):
            start_month = current_date.month - i
            start_year = current_date.year - 1 if start_month <= 0 else current_date.year
            start_month = (start_month + 12) % 12 or 12
            start_date = datetime(start_year, start_month, 1)
            end_month = start_month % 12 + 1
            end_year = start_year if end_month != 1 else start_year + 1
            end_date = datetime(end_year, end_month, 1) - timedelta(days=1)
            months.append(start_date.strftime('%b %y'))
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            start_date_formatted = self.get_actual_date(start_date + " 00:00:00")
            end_date_formatted = self.get_actual_date(end_date + " 23:59:59")
            booking_search = request.env['unit.reservation'].search(
                [('date', '<=', end_date_formatted), ('date', '>=', start_date_formatted),
                 ('state', '=', 'confirmed'), ('source_of_booking', '=', 'cp')])
            bookings.append(len(booking_search))
        return {
            'months': months,
            'bookings': bookings,
        }

    @http.route('/jupiter_dashboard_deux/collections_billings', auth='public', type='json')
    def jupiter_dashboard_deux_collections_billings(self):
        currency = request.env.company.currency_id.symbol
        current_datetime = datetime.today()
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).date()
        start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0).date()
        fin_year_start = (
            date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
        financial_year_start_month = 4
        quarter_month_starts = [4, 7, 10, 1]
        half_year_starts = [4, 10]

        year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
        quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
        quarter_start = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
        half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
        half_start = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)

        current_datetime = current_datetime.strftime('%Y-%m-%d')
        start_of_week = start_of_week.strftime('%Y-%m-%d')
        start_of_month = start_of_month.strftime('%Y-%m-%d')
        fin_year_start = fin_year_start.strftime('%Y-%m-%d')
        quarter_start = quarter_start.strftime('%Y-%m-%d')
        half_start = half_start.strftime('%Y-%m-%d')
        invoice_qry = """
            SELECT COALESCE(SUM(am.amount_total), 0) AS billing
            FROM account_move am
            WHERE 
                state = 'posted'
                AND am.move_type = 'out_invoice'
                AND am.project_invoice_type = 'developer_invoice'
                AND am.invoice_date <= '%s'
                AND am.invoice_date >= '%s'
        """
        request.env.cr.execute(invoice_qry % (current_datetime, current_datetime))
        invoice_row = request.env.cr.fetchone()
        today_billing = invoice_row[0] / 100000

        request.env.cr.execute(invoice_qry % (current_datetime, start_of_week))
        invoice_row = request.env.cr.fetchone()
        week_billing = invoice_row[0] / 100000

        request.env.cr.execute(invoice_qry % (current_datetime, start_of_month))
        invoice_row = request.env.cr.fetchone()
        month_billing = invoice_row[0] / 100000

        request.env.cr.execute(invoice_qry % (current_datetime, quarter_start))
        invoice_row = request.env.cr.fetchone()
        quarter_billing = invoice_row[0] / 100000

        request.env.cr.execute(invoice_qry % (current_datetime, half_start))
        invoice_row = request.env.cr.fetchone()
        half_billing = invoice_row[0] / 100000

        request.env.cr.execute(invoice_qry % (current_datetime, fin_year_start))
        invoice_row = request.env.cr.fetchone()
        year_billing = invoice_row[0] / 100000

        payment_qry = """
            SELECT 
                COALESCE(SUM(am.amount_total), 0) AS billing,
                COALESCE(SUM(match_debit.amount), 0) + COALESCE(SUM(match_credit.amount), 0) AS collection
            FROM account_move am
            LEFT JOIN account_move_line aml ON aml.move_id = am.id
            LEFT JOIN account_account aa ON aml.account_id = aa.id
            LEFT JOIN account_account_type aat ON aat.id = aa.user_type_id 
            LEFT JOIN account_partial_reconcile match_debit ON match_debit.credit_move_id = aml.id
            LEFT JOIN account_partial_reconcile match_credit ON match_credit.debit_move_id = aml.id
            LEFT JOIN account_move_line line_debit on line_debit.id = match_debit.debit_move_id
            LEFT JOIN account_move_line line_credit on line_credit.id = match_credit.credit_move_id
            WHERE 
                state = 'posted'
                AND aat.type IN ('receivable', 'payable')
                AND am.project_invoice_type = 'developer_invoice'
                AND ((line_debit.date <= '%s' AND line_debit.date >= '%s') 
                OR (line_credit.date <= '%s' AND line_credit.date >= '%s'))
        """
        print(payment_qry % (current_datetime, current_datetime, current_datetime, current_datetime))
        request.env.cr.execute(payment_qry % (current_datetime, current_datetime, current_datetime, current_datetime))
        payment_row = request.env.cr.fetchone()
        today_collection = payment_row[1] / 100000

        request.env.cr.execute(payment_qry % (current_datetime, start_of_week, current_datetime, start_of_week))
        payment_row = request.env.cr.fetchone()
        week_collection = payment_row[1] / 100000

        request.env.cr.execute(payment_qry % (current_datetime, start_of_month, current_datetime, start_of_month))
        payment_row = request.env.cr.fetchone()
        month_collection = payment_row[1] / 100000

        request.env.cr.execute(payment_qry % (current_datetime, quarter_start, current_datetime, quarter_start))
        payment_row = request.env.cr.fetchone()
        quarter_collection = payment_row[1] / 100000

        request.env.cr.execute(payment_qry % (current_datetime, half_start, current_datetime, half_start))
        payment_row = request.env.cr.fetchone()
        half_collection = payment_row[1] / 100000

        request.env.cr.execute(payment_qry % (current_datetime, fin_year_start, current_datetime, fin_year_start))
        payment_row = request.env.cr.fetchone()
        year_collection = payment_row[1] / 100000

        today_billing_attrs = {
            "date_from": current_datetime,
            "date_to": current_datetime,
            "report_type": 'all',
        }
        week_billing_attrs = {
            "date_from": start_of_week,
            "date_to": current_datetime,
            "report_type": 'all',
        }
        month_billing_attrs = {
            "date_from": start_of_month,
            "date_to": current_datetime,
            "report_type": 'all',
        }
        quarter_billing_attrs = {
            "date_from": quarter_start,
            "date_to": current_datetime,
            "report_type": 'all',
        }
        half_billing_attrs = {
            "date_from": half_start,
            "date_to": current_datetime,
            "report_type": 'all',
        }
        year_billing_attrs = {
            "date_from": fin_year_start,
            "date_to": current_datetime,
            "report_type": 'all',
        }

        today_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', current_datetime)
        ]
        week_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', start_of_week)
        ]
        month_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', start_of_month)
        ]
        quarter_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', quarter_start)
        ]
        half_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', half_start)
        ]
        year_collection_domain = [
            ('partner_id.is_owner', '=', True),
            ('date', '<=', current_datetime),
            ('date', '>=', fin_year_start)
        ]

        return {
            'today_collection': currency + "{:,.2f}".format(today_collection),
            'week_collection': currency + "{:,.2f}".format(week_collection),
            'month_collection': currency + "{:,.2f}".format(month_collection),
            'quarter_collection': currency + "{:,.2f}".format(quarter_collection),
            'half_collection': currency + "{:,.2f}".format(half_collection),
            'year_collection': currency + "{:,.2f}".format(year_collection),

            'today_billing': currency + "{:,.2f}".format(today_billing),
            'week_billing': currency + "{:,.2f}".format(week_billing),
            'month_billing': currency + "{:,.2f}".format(month_billing),
            'quarter_billing': currency + "{:,.2f}".format(quarter_billing),
            'half_billing': currency + "{:,.2f}".format(half_billing),
            'year_billing': currency + "{:,.2f}".format(year_billing),

            'today_billing_attrs': str(today_billing_attrs),
            'week_billing_attrs': str(week_billing_attrs),
            'month_billing_attrs': str(month_billing_attrs),
            'quarter_billing_attrs': str(quarter_billing_attrs),
            'half_billing_attrs': str(half_billing_attrs),
            'year_billing_attrs': str(year_billing_attrs),

            'today_collection_domain': str(today_collection_domain),
            'week_collection_domain': str(week_collection_domain),
            'month_collection_domain': str(month_collection_domain),
            'quarter_collection_domain': str(quarter_collection_domain),
            'half_collection_domain': str(half_collection_domain),
            'year_collection_domain': str(year_collection_domain),
        }

    @http.route('/jupiter_dashboard_deux/bookings_registrations', auth='public', type='json')
    def jupiter_dashboard_deux_bookings_registrations(self):
        currency = request.env.company.currency_id.symbol
        current_datetime = datetime.today()
        start_of_today = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_of_today + timedelta(days=1) - timedelta(microseconds=1)
        start_formatted = self.get_actual_date(start_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week_formatted = self.get_actual_date(start_of_week.strftime('%Y-%m-%d %H:%M:%S'))
        start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_month_formatted = self.get_actual_date(start_of_month.strftime('%Y-%m-%d %H:%M:%S'))
        fin_year_obj = (
            date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
        fin_year_start = fin_year_obj.strftime('%Y-%m-%d')
        fin_year_end = date.today().strftime('%Y-%m-%d')
        fin_year_start_formatted = self.get_actual_date(fin_year_start + ' 00:00:00')
        fin_year_end_formatted = self.get_actual_date(fin_year_end + ' 23:59:59')

        financial_year_start_month = 4
        quarter_month_starts = [4, 7, 10, 1]
        half_year_starts = [4, 10]

        year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
        quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
        quarter_start = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
        next_quarter_index = (quarter_index + 1) % 4
        quarter_end = datetime(current_datetime.year + year_offset, quarter_month_starts[next_quarter_index],
                               1) - timedelta(days=1)
        half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
        half_start = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
        if current_datetime.month >= half_year_starts[half_year_index]:
            half_end = datetime(current_datetime.year + year_offset, half_year_starts[(half_year_index + 1) % 2],
                                1) - timedelta(days=1)
        else:
            half_end = datetime(current_datetime.year + year_offset - 1, half_year_starts[(half_year_index + 1) % 2],
                                1) - timedelta(days=1)

        start_of_quarter_formatted = self.get_actual_date(quarter_start.strftime('%Y-%m-%d %H:%M:%S'))
        start_of_half_formatted = self.get_actual_date(half_start.strftime('%Y-%m-%d %H:%M:%S'))
        quarter_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_quarter_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        quarter_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_formatted), ('cancellation_date', '>=', quarter_start),
             ('state', '=', 'canceled')])
        quarter_registration = request.env['project.registration'].search(
            [('registration_date', '<=', current_datetime), ('registration_date', '>=', quarter_start),
             ('state', '=', 'confirmed')])

        quarter_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', quarter_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        quarter_registration_value = sum(quarter_booking_of_registrations.mapped('flat_cost')) / 100000
        quarter_booking_value = sum(quarter_booking_confirmed.mapped('flat_cost')) / 100000

        half_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_half_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        half_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', half_start),
             ('state', '=', 'canceled')])
        half_registration = request.env['project.registration'].search(
            [('registration_date', '<=', current_datetime), ('registration_date', '>=', half_start),
             ('state', '=', 'confirmed')])

        half_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', half_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        half_registration_value = sum(half_booking_of_registrations.mapped('flat_cost')) / 100000
        half_booking_value = sum(half_booking_confirmed.mapped('flat_cost')) / 100000

        year_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', fin_year_end_formatted), ('date', '>=', fin_year_start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        year_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', fin_year_end), ('cancellation_date', '>=', fin_year_start),
             ('state', '=', 'canceled')])
        year_registration = request.env['project.registration'].search(
            [('registration_date', '<=', fin_year_end), ('registration_date', '>=', fin_year_start),
             ('state', '=', 'confirmed')])

        year_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', year_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        year_registration_value = sum(year_booking_of_registrations.mapped('flat_cost')) / 100000
        year_booking_value = sum(year_booking_confirmed.mapped('flat_cost')) / 100000

        today_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        today_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', end_of_today),
             ('state', '=', 'canceled')])

        this_week_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_week_formatted),
             ('date', '>=', start_of_month_formatted), ('state', 'in', ('confirmed', 'canceled'))])
        this_week_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', start_of_week),
             ('date', '>=', start_of_month), ('state', '=', 'canceled')])

        this_month_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        this_month_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', start_of_month),
             ('state', '=', 'canceled')])

        today_registration = request.env['project.registration'].search(
            [('registration_date', '=', current_datetime.date()), ('state', '=', 'confirmed')])
        today_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', today_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        today_registration_value = sum(today_booking_of_registrations.mapped('flat_cost')) / 100000
        today_booking_value = sum(today_booking_confirmed.mapped('flat_cost')) / 100000

        this_week_registration = request.env['project.registration'].search(
            [('registration_date', '<=', end_of_today), ('registration_date', '>=', start_of_week),
             ('state', '=', 'confirmed')])
        this_week_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', this_week_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        this_week_registration_value = sum(this_week_booking_of_registrations.mapped('flat_cost')) / 100000
        this_week_booking_value = sum(this_week_booking_confirmed.mapped('flat_cost')) / 100000

        this_month_registration = request.env['project.registration'].search(
            [('registration_date', '<=', end_of_today), ('registration_date', '>=', start_of_month),
             ('state', '=', 'confirmed')])
        this_month_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', this_month_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        this_month_registration_value = sum(this_month_booking_of_registrations.mapped('flat_cost')) / 100000
        this_month_booking_value = sum(this_month_booking_confirmed.mapped('flat_cost')) / 100000

        today_booking_attrs = {
            "date_from": current_datetime.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        week_booking_attrs = {
            "date_from": start_of_week.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        month_booking_attrs = {
            "date_from": start_of_month.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        year_booking_attrs = {
            "date_from": fin_year_start,
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        quarter_booking_attrs = {
            "date_from": quarter_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        half_booking_attrs = {
            "date_from": half_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'confirmed',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        today_registration_attrs = {
            "date_from": current_datetime.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }
        week_registration_attrs = {
            "date_from": start_of_week.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }
        month_registration_attrs = {
            "date_from": start_of_month.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }
        year_registration_attrs = {
            "date_from": fin_year_start,
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }
        quarter_registration_attrs = {
            "date_from": quarter_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }
        half_registration_attrs = {
            "date_from": half_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
        }

        today_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_formatted), ('state', '=', 'confirmed')
        ]
        week_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_week_formatted), ('state', '=', 'confirmed')
        ]
        month_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_month_formatted), ('state', '=', 'confirmed')
        ]
        quarter_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_quarter_formatted), ('state', '=', 'confirmed')
        ]
        half_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_half_formatted), ('state', '=', 'confirmed')
        ]
        year_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', fin_year_start_formatted), ('state', '=', 'confirmed')
        ]

        today_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', start_formatted), ('state', '=', 'confirmed')
        ]
        week_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_week_formatted), ('state', '=', 'confirmed')
        ]
        month_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_month_formatted), ('state', '=', 'confirmed')
        ]
        quarter_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_quarter_formatted), ('state', '=', 'confirmed')
        ]
        half_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_half_formatted), ('state', '=', 'confirmed')
        ]
        year_direct_domain = [
            ('source_of_booking', '=', 'direct'), ('date', '<=', end_formatted),
            ('date', '>=', fin_year_start_formatted), ('state', '=', 'confirmed')
        ]
        return {
            'today_booking_count': len(today_booking_confirmed),
            'week_booking_count': len(this_week_booking_confirmed),
            'month_booking_count': len(this_month_booking_confirmed),
            'year_booking_count': len(year_booking_confirmed),
            'quarter_booking_count': len(quarter_booking_confirmed),
            'half_booking_count': len(half_booking_confirmed),

            'today_booking_value': currency + "{:,.2f}".format(today_booking_value),
            'week_booking_value': currency + "{:,.2f}".format(this_week_booking_value),
            'month_booking_value': currency + "{:,.2f}".format(this_month_booking_value),
            'year_booking_value': currency + "{:,.2f}".format(year_booking_value),
            'quarter_booking_value': currency + "{:,.2f}".format(quarter_booking_value),
            'half_booking_value': currency + "{:,.2f}".format(half_booking_value),

            'today_registration_count': len(today_registration),
            'week_registration_count': len(this_week_registration),
            'month_registration_count': len(this_month_registration),
            'year_registration_count': len(year_registration),
            'quarter_registration_count': len(quarter_registration),
            'half_registration_count': len(half_registration),

            'today_registration_value': currency + "{:,.2f}".format(today_registration_value),
            'week_registration_value': currency + "{:,.2f}".format(this_week_registration_value),
            'month_registration_value': currency + "{:,.2f}".format(this_month_registration_value),
            'year_registration_value': currency + "{:,.2f}".format(year_registration_value),
            'quarter_registration_value': currency + "{:,.2f}".format(quarter_registration_value),
            'half_registration_value': currency + "{:,.2f}".format(half_registration_value),

            'today_booking_attrs': str(today_booking_attrs),
            'week_booking_attrs': str(week_booking_attrs),
            'month_booking_attrs': str(month_booking_attrs),
            'year_booking_attrs': str(year_booking_attrs),
            'quarter_booking_attrs': str(quarter_booking_attrs),
            'half_booking_attrs': str(half_booking_attrs),

            'today_registration_attrs': str(today_registration_attrs),
            'week_registration_attrs': str(week_registration_attrs),
            'month_registration_attrs': str(month_registration_attrs),
            'year_registration_attrs': str(year_registration_attrs),
            'quarter_registration_attrs': str(quarter_registration_attrs),
            'half_registration_attrs': str(half_registration_attrs),

            'today_booking_cancelled_count': len(today_booking_cancelled),
            'week_booking_cancelled_count': len(this_week_booking_cancelled),
            'month_booking_cancelled_count': len(this_month_booking_cancelled),
            'year_booking_cancelled_count': len(year_booking_cancelled),
            'quarter_booking_cancelled_count': len(quarter_booking_cancelled),
            'half_booking_cancelled_count': len(half_booking_cancelled),

            'today_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(today_booking_cancelled.mapped('flat_cost')) / 100000),
            'week_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(this_week_booking_cancelled.mapped('flat_cost')) / 100000),
            'month_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(this_month_booking_cancelled.mapped('flat_cost')) / 100000),
            'year_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(year_booking_cancelled.mapped('flat_cost')) / 100000),
            'quarter_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(quarter_booking_cancelled.mapped('flat_cost')) / 100000),
            'half_booking_cancelled_value': currency + "{:,.2f}".format(
                sum(half_booking_cancelled.mapped('flat_cost')) / 100000),

            'today_booking_cancelled_attrs': str(today_booking_attrs).replace('confirmed', 'canceled'),
            'week_booking_cancelled_attrs': str(week_booking_attrs).replace('confirmed', 'canceled'),
            'month_booking_cancelled_attrs': str(month_booking_attrs).replace('confirmed', 'canceled'),
            'year_booking_cancelled_attrs': str(year_booking_attrs).replace('confirmed', 'canceled'),
            'quarter_booking_cancelled_attrs': str(quarter_booking_attrs).replace('confirmed', 'canceled'),
            'half_booking_cancelled_attrs': str(half_booking_attrs).replace('confirmed', 'canceled'),

            'quarter_label': quarter_start.strftime('%b %y') + '-' + quarter_end.strftime('%b %y'),
            'half_label': half_start.strftime('%b %y') + '-' + half_end.strftime('%b %y'),
            'year_label': fin_year_obj.strftime('%Y') + '-' + str(int(half_end.strftime('%y')) + 1),

            'today_booking_cp_count': len(today_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'week_booking_cp_count': len(this_week_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'month_booking_cp_count': len(this_month_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'year_booking_cp_count': len(year_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'quarter_booking_cp_count': len(quarter_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'half_booking_cp_count': len(half_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),

            'today_booking_cp_domain': str(today_booking_cp_domain),
            'week_booking_cp_domain': str(week_booking_cp_domain),
            'month_booking_cp_domain': str(month_booking_cp_domain),
            'quarter_booking_cp_domain': str(quarter_booking_cp_domain),
            'half_booking_cp_domain': str(half_booking_cp_domain),
            'year_booking_cp_domain': str(year_booking_cp_domain),

            'today_direct': len(today_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),
            'week_direct': len(this_week_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),
            'month_direct': len(this_month_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),
            'year_direct': len(year_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),
            'quarter_direct': len(quarter_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),
            'half_direct': len(half_booking_confirmed.filtered(lambda x: x.source_of_booking == 'direct')),

            'today_direct_domain': str(today_direct_domain),
            'week_direct_domain': str(week_direct_domain),
            'month_direct_domain': str(month_direct_domain),
            'quarter_direct_domain': str(quarter_direct_domain),
            'half_direct_domain': str(half_direct_domain),
            'year_direct_domain': str(year_direct_domain),

            'today_average_av': currency + "{:,.2f}".format(today_registration_value / len(
                today_booking_of_registrations) if today_booking_of_registrations else 0),
            'week_average_av': currency + "{:,.2f}".format(this_week_registration_value / len(
                this_week_booking_of_registrations) if this_week_booking_of_registrations else 0),
            'month_average_av': currency + "{:,.2f}".format(this_month_registration_value / len(
                this_month_booking_of_registrations) if this_month_booking_of_registrations else 0),
            'quarter_average_av': currency + "{:,.2f}".format(quarter_registration_value / len(
                quarter_booking_of_registrations) if quarter_booking_of_registrations else 0),
            'half_average_av': currency + "{:,.2f}".format(
                half_registration_value / len(half_booking_of_registrations) if half_booking_of_registrations else 0),
            'year_average_av': currency + "{:,.2f}".format(
                year_registration_value / len(year_booking_of_registrations) if year_booking_of_registrations else 0),
        }
