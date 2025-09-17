from odoo import http
from odoo.http import request
from datetime import datetime, timedelta, date
from pytz import timezone


class JupiterDashboard(http.Controller):

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(request.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    @http.route('/jupiter_dashboard/get_financial_year_data', auth='public', type='json')
    def jupiter_dashboard_get_financial_year_data(self, get_selection, fin_year):
        sequence = request.env['account.journal'].search([('type', '=', 'sale')], limit=1).sequence_id
        fin_year_selection = ''
        fin_year_start = (
            date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1)).strftime(
            '%Y-%m-%d')
        fin_year_end = date.today().strftime('%Y-%m-%d')
        if fin_year:
            fin_year_start = str(fin_year) + '-04-01'
            fin_year_end = str(int(fin_year) + 1) + '-03-31'
        else:
            fin_year = date.today().year if date.today().month >= 4 else date.today().year - 1
        if get_selection:
            for line in sequence.date_range_ids:
                selected = ''
                fin_start = datetime.strptime(str(line.date_from.year) + '-04-01', '%Y-%m-%d')
                fin_end = datetime.strptime(str(line.date_from.year + 1) + '-03-31', '%Y-%m-%d')
                if fin_start.date() <= datetime.now().date() <= fin_end.date():
                    selected = 'selected="selected"'
                    fin_year = line.date_from.year
                    fin_year_start = str(line.date_from.year) + '-04-01'
                    fin_year_end = str(line.date_from.year + 1) + '-03-31'
                fin_year_selection += '<option value="%s" %s>%s</option>' % (str(line.date_from.year), selected, str(line.date_from.strftime('%Y')) + ' - ' + str(int(line.date_from.strftime('%y')) + 1))
        start_formatted = self.get_actual_date(fin_year_start + ' 00:00:00')
        end_formatted = self.get_actual_date(fin_year_end + ' 23:59:59')
        year_booking = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))])
        year_registration = request.env['project.registration'].search(
            [('registration_date', '<=', end_formatted), ('registration_date', '>=', start_formatted),
             ('state', '=', 'confirmed')])
        year_registration_count = len(year_registration)

        year_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', year_registration.mapped('flat_id').ids), ('state', '=', 'confirmed')])
        year_registration_value = sum(year_booking_of_registrations.mapped('flat_cost')) / 100000
        year_booking_value = sum(year_booking.mapped('flat_cost')) / 100000
        fin_year_string = str(fin_year) + ' - ' + str(int(fin_year) + 1)[-2:]
        return {
            'fin_year_selection': fin_year_selection,
            'year_booking_gross': len(year_booking),
            'year_booking_cancelled': len(year_booking.filtered(lambda x: x.state == 'canceled')),
            'year_booking_net': len(year_booking.filtered(lambda x: x.state == 'confirmed')),
            'year_registration_count': year_registration_count,
            'year_registration_value': "{:,.2f}".format(year_registration_value),
            'year_booking_value': "{:,.2f}".format(year_booking_value),
            'fin_year_string': fin_year_string
        }

    @http.route('/jupiter_dashboard/get_region', auth='public', type='json')
    def jupiter_dashboard_get_region(self):
        regions = request.env['regions'].search([('is_parent', '=', True)])
        data = '<a class="dropdown-item" href="#">All</a>'
        for region in regions:
            data += '<a class="dropdown-item" href="#" value="%s">%s</a>' % (str(region.id), str(region.name))
        return data

    @http.route('/jupiter_dashboard/row_4', auth='public', type='json')
    def jupiter_dashboard_row_4(self, region_wise, project_wise, project_region):
        region_list = []
        region_booked = []
        region_available = []
        if region_wise:
            regions = request.env['regions'].search([('is_parent', '=', True)])
            for region in regions:
                available_count = request.env['product.template'].search_count([('region_id', '=', region.id), ('state', '=', 'free')])
                booked_count = request.env['product.template'].search_count([('region_id', '=', region.id), ('state', '=', 'reserved')])
                region_list.append(region.name)
                region_booked.append(booked_count)
                region_available.append(available_count)

        project_list = []
        project_booked = []
        project_available = []
        if project_wise:
            region_clause = ''
            if project_region:
                region_clause = ' AND b.region_id = %s' % str(project_region)
            request.env.cr.execute("""
                SELECT 
                    b.name, 
                    SUM(CASE WHEN pt.state = 'free' THEN 1 ELSE 0 END) AS available_count,
                    SUM(CASE WHEN pt.state = 'reserved' THEN 1 ELSE 0 END) AS reserved_count
                FROM 
                    building b 
                LEFT JOIN 
                    product_template pt ON pt.building_id = b.id
                WHERE 
                    b.active = True and pt.active = True
                    %s
                GROUP BY 
                    b.id, b.name
                ORDER BY 
                    available_count DESC
                LIMIT 25;
            """ % region_clause)
            rows = request.env.cr.dictfetchall()
            for row in rows:
                project_list.append(row['name'])
                project_booked.append(row['reserved_count'])
                project_available.append(row['available_count'])

        return {
            'region_booked': region_booked,
            'region_available': region_available,
            'regions': region_list,
            'projects': project_list,
            'project_booked': project_booked,
            'project_available': project_available,
        }

    @http.route('/jupiter_dashboard/row_3', auth='public', type='json')
    def jupiter_dashboard_row_3(self):
        regions = request.env['regions'].search([('is_parent', '=', True)])
        region_list = []
        bookings = []
        for region in regions:
            booking_count = request.env['unit.reservation'].search_count([('building.region_id', '=', region.id), ('state', '=', 'confirmed')])
            if booking_count > 0:
                region_list.append(region.name)
                bookings.append(booking_count)
        return {
            'region': region_list,
            'booking': bookings
        }

    @http.route('/jupiter_dashboard/row_2', auth='public', type='json')
    def jupiter_dashboard_row_2(self, booking_type='number', registration_type='number', budget_type='number'):
        current_date = datetime.now()
        months = []
        bookings = []
        registrations = []
        booking_budgets = []
        registration_budgets = []
        for i in range(11, -1, -1):
            start_month = current_date.month - i
            start_year = current_date.year - 1 if start_month <= 0 else current_date.year
            start_month = (start_month + 12) % 12 or 12
            start_date = datetime(start_year, start_month, 1)
            end_month = start_month % 12 + 1
            end_year = start_year if end_month != 1 else start_year + 1
            end_date = datetime(end_year, end_month, 1) - timedelta(days=1)
            # last_12_months.append(
            #     (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), start_date.strftime('%b')))
            months.append(start_date.strftime('%b'))
            budget_month = start_date.strftime("%B %Y")
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            start_date_formatted = self.get_actual_date(start_date + " 00:00:00")
            end_date_formatted = self.get_actual_date(end_date + " 23:59:59")
            if booking_type:
                booking_search = request.env['unit.reservation'].search([('date', '<=', end_date_formatted), ('date', '>=', start_date_formatted), ('state', '=', 'confirmed')])
                if booking_type == 'number':
                    bookings.append(len(booking_search))
                else:
                    bookings.append(sum(booking_search.mapped('flat_cost')) / 100000)
            if registration_type:
                registration_search = request.env['project.registration'].search([('registration_date', '<=', end_date), ('registration_date', '>=', start_date), ('state', '=', 'confirmed')])
                if registration_type == 'number':
                    registrations.append(len(registration_search))
                else:
                    booking_of_registration = request.env['unit.reservation'].search([('building_unit', 'in', registration_search.mapped('flat_id').ids), ('state', '=', 'confirmed')])
                    registrations.append(sum(booking_of_registration.mapped('flat_cost')) / 100000)
            if budget_type:
                budget = request.env['project.target.line'].search([('month', '=', budget_month)])
                booking_budgets.append(sum(budget.mapped('inventory')))
                registration_budgets.append(sum(budget.mapped('registration')))
        return {
            'months': months,
            'bookings': bookings,
            'registrations': registrations,
            'booking_budgets': booking_budgets,
            'registration_budgets': registration_budgets,
        }

    @http.route('/jupiter_dashboard/row_1', auth='public', type='json')
    def jupiter_dashboard_row_1(self):
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

        today_booking = request.env['unit.reservation'].search([('date', '<=', end_formatted), ('date', '>=', start_formatted), ('state', 'in', ('confirmed', 'canceled'))])
        this_week_booking = request.env['unit.reservation'].search([('date', '<=', end_formatted), ('date', '>=', start_of_week_formatted), ('date', '>=', start_of_month_formatted), ('state', 'in', ('confirmed', 'canceled'))])
        this_month_booking = request.env['unit.reservation'].search([('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted), ('state', 'in', ('confirmed', 'canceled'))])

        today_registration_count = request.env['project.registration'].search_count([('registration_date', '=', current_datetime.date()), ('state', '=', 'confirmed')])
        this_week_registration_count = request.env['project.registration'].search_count([('registration_date', '<=', end_formatted), ('registration_date', '>=', start_of_week_formatted), ('state', '=', 'confirmed')])
        this_month_registration_count = request.env['project.registration'].search_count([('registration_date', '<=', end_formatted), ('registration_date', '>=', start_of_month_formatted), ('state', '=', 'confirmed')])
        return {
            'today_booking_gross': len(today_booking),
            'today_booking_cancelled': len(today_booking.filtered(lambda x: x.state == 'canceled')),
            'today_booking_net': len(today_booking.filtered(lambda x: x.state == 'confirmed')),

            'week_booking_gross': len(this_week_booking),
            'week_booking_cancelled': len(this_week_booking.filtered(lambda x: x.state == 'canceled')),
            'week_booking_net': len(this_week_booking.filtered(lambda x: x.state == 'confirmed')),

            'month_booking_gross': len(this_month_booking),
            'month_booking_cancelled': len(this_month_booking.filtered(lambda x: x.state == 'canceled')),
            'month_booking_net': len(this_month_booking.filtered(lambda x: x.state == 'confirmed')),

            'today_registration_count': today_registration_count,
            'this_week_registration_count': this_week_registration_count,
            'this_month_registration_count': this_month_registration_count,
        }
