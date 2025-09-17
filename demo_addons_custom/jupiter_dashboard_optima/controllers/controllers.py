# -*- coding: utf-8 -*-
import json
import requests
from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime, timedelta, date
from pytz import timezone
import calendar


class JupiterDashboardOptima(http.Controller):
    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(request.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    @http.route('/jupiter_dashboard_optima/call_list_view', auth='public', type='json')
    def jupiter_dashboard_tres_call_list_view(self, domain, model, name):
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'view_mode': 'tree,form',
            'res_model': model,
            'views': [(False, 'list'), (False, 'form')],
            'domain': domain,
            'context': {'create': False}
        }

    @http.route('/jupiter_dashboard_optima/call_report', auth='public', type='json')
    def jupiter_dashboard_tres_call_report(self, report_attr, model='beta.booking.report', region_ids=False,
                                           cluster_ids=False, project_ids=False):
        projects = False
        if region_ids:
            projects = request.env['building'].search([('region_id', 'in', region_ids)])
        if cluster_ids:
            projects = request.env['building'].search([('sub_region_id', 'in', cluster_ids)])
        if project_ids:
            projects = request.env['building'].search([('id', 'in', project_ids)])
        if region_ids or cluster_ids or project_ids:
            full_project_count = request.env['building'].search_count([])
            if len(projects) != full_project_count:
                report_attr['project_filter'] = 'selected'
                report_attr['project_ids'] = projects.ids
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

    @http.route('/jupiter_dashboard_optima/cp_booking_units_region_wise', auth='public', type='json')
    def cp_booking_units_region_wise(self, model='region', frequency='month', custom_start=False, custom_end=False):
        if model == 'region':
            records = request.env['regions'].search([('is_parent', '=', True)], order='name')
        else:
            records = request.env['regions'].search([('is_parent', '=', False)], order='name')

        current_datetime = datetime.today()
        start_date = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_date + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        if custom_start and custom_end:
            start_formatted = self.get_actual_date(str(custom_start) + ' 00:00:00')
            end_formatted = self.get_actual_date(str(custom_end) + ' 23:59:59')
        elif frequency == 'today':
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'week':
            start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
            start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]

            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'year':
            fin_year_obj = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
            start_date = fin_year_obj.strftime('%Y-%m-%d')
            fin_year_end = date.today().strftime('%Y-%m-%d')
            start_formatted = self.get_actual_date(start_date + ' 00:00:00')
        data = {
            'categories': [],
            'data': []
        }
        for record in records:
            domain_str = 'region_id' if model == 'region' else 'sub_region_id'
            booking = request.env['unit.reservation'].search(
                [('date', '<=', end_formatted), ('date', '>=', start_formatted), ('source_of_booking', '=', 'cp'),
                 (f'building.{domain_str}', '=', record.id), ('state', 'in', ('confirmed', 'canceled'))])
            data['categories'].append(record.name)
            data['data'].append(len(booking))
        return data

    @http.route('/jupiter_dashboard_optima/walk_in_data', auth='public', type='json')
    def walk_in_data(self, model='region', frequency='month', region=False, cluster=False):
        config_obj = request.env['ir.config_parameter'].sudo()
        if not config_obj.get_param('jupiter_dashboard_tres.enable_dashboard_walk_in_api'):
            return 'disable'
        username = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_username')
        password = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_key')
        url = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_url')
        data = {
            'params': {
                'login': username,
                'password': password
            }
        }
        api_model_mapping = {
            'region': {},
            'cluster': {},
            'project': {}
        }
        disable = False
        try:
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(url, headers=headers, json=data)
            if response.ok:
                rec = json.loads(response.text)
                api_data = rec.get('data')
                # api_model_mapping['region'] = api_data.get('visited_region')
                # api_model_mapping['cluster'] = api_data.get('visited_cluster')
                # api_model_mapping['project'] = api_data.get('visted_project')
                for item in api_data:
                    for line in item:
                        api_model_mapping['project'][line] = item[line]
            else:
                raise ValidationError(str(response.text))
        except:
            disable = True
        if disable:
            return 'disable'
        api_frequency_mapping = {
            'today': 'today',
            'week': 'week',
            'month': 'month',
            'quarter': 'quarter',
            'half': 'semi',
            'year': 'year'
        }
        data = {
            'categories': [],
            'walk_in': [],
            'booking': [],
            'conversion': [],
            'width': [0.32, 0.40] if model == 'region' else [0.22, 0.32]
        }
        domain = ' where b.active = True '
        if model == 'region':
            pass
            # records = request.env['regions'].search([('is_parent', '=', True)], order='name')
        elif model == 'cluster':
            pass
            # records = request.env['regions'].search([('is_parent', '=', False)], order='name')
        else:
            if region:
                # domain.append(('region_id', '=', int(region)))
                domain += f' and b.region_id = {region}'
            if cluster:
                # domain.append(('sub_region_id', 'in', cluster))
                domain += f' and b.sub_region_id in ({",".join([str(i) for i in cluster])})'
            data = ''
        # records = request.env['building'].search(domain, order='name')
        request.env.cr.execute(f"""
            select b.name, b.code, b.id, b.region_id, b.sub_region_id, r.name as region_name, c.name as cluster_name 
            from building b 
            left join regions r on r.id = b.region_id 
            left join regions c on c.id = b.sub_region_id
            {domain}
        """)
        records = request.env.cr.dictfetchall()
        current_datetime = datetime.today()
        start_date = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_date + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        if frequency == 'today':
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'week':
            start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
            start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]

            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)

            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'year':
            fin_year_obj = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
            start_date = fin_year_obj.strftime('%Y-%m-%d')
            start_formatted = self.get_actual_date(start_date + ' 00:00:00')

        region_data = {}

        for record in records:
            # domain_str = 'region_id' if model == 'region' else 'sub_region_id' if model == 'cluster' else 'id'

            walk_in = 0
            record_name = record['code']
            if record_name in api_model_mapping.get('project'):
                walk_in = api_model_mapping['project'][record_name].get(api_frequency_mapping[frequency])

            booking = request.env['unit.reservation'].search(
                [('date', '<=', end_formatted), ('date', '>=', start_formatted),
                 ('building.id', '=', record['id']), ('state', 'in', ('confirmed', 'canceled'))])
            booking_count = len(booking)
            if model != 'project':
                if model == 'region':
                    region_field = 'region_id'
                    region_name = record['region_name']
                else:
                    region_field = 'sub_region_id'
                    region_name = record['cluster_name']
                if record['region_id'] not in region_data:
                    region_data[record[region_field]] = [walk_in, booking_count, region_name]
                else:
                    region_data[record[region_field]][0] += walk_in
                    region_data[record[region_field]][1] += booking_count

            if model == 'project':
                conversion = "{:,.2f}".format(
                    booking_count * 100 / walk_in if walk_in != 0 else 0 if (
                                booking_count == 0 and walk_in == 0) else 100)
                data += f"""
                    <tr>
                        <td class="pr-0">{record['name']}</td>
                        <td class="text-right">{walk_in}</td>
                        <td class="text-right">{booking_count}</td>
                        <td class="text-right">{conversion}</td>
                    </tr>
                """
            # else:
            #     data['categories'].append(record.name)
            #     data['walk_in'].append(walk_in)
            #     data['booking'].append(booking_count)
            #     data['conversion'].append(conversion)
        if model != 'project':
            for item in region_data:
                walk_in = region_data[item][0]
                booking_count = region_data[item][1]
                name = region_data[item][2]
                conversion = "{:,.2f}".format(
                    booking_count * 100 / walk_in if walk_in != 0 else 0 if (
                            booking_count == 0 and walk_in == 0) else 100)
                data['categories'].append(name)
                data['walk_in'].append(walk_in)
                data['booking'].append(booking_count)
                data['conversion'].append(conversion)
        return data

    # @http.route('/jupiter_dashboard_tres/walk_in_data', auth='public', type='json')
    def walk_in_data_old(self, model='region', frequency='month', region=False, cluster=False):
        config_obj = request.env['ir.config_parameter'].sudo()
        if not config_obj.get_param('jupiter_dashboard_tres.enable_dashboard_walk_in_api'):
            return 'disable'
        username = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_username')
        password = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_key')
        url = config_obj.get_param('jupiter_dashboard_tres.dashboard_walk_in_api_url')
        data = {
            'params': {
                'login': username,
                'password': password
            }
        }
        api_model_mapping = {
            'region': {},
            'cluster': {},
            'project': {}
        }
        disable = False
        try:
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(url, headers=headers, json=data)
            if response.ok:
                rec = json.loads(response.text)
                api_data = rec.get('data')
                api_model_mapping['region'] = api_data.get('visited_region')
                api_model_mapping['cluster'] = api_data.get('visited_cluster')
                api_model_mapping['project'] = api_data.get('visted_project')
            else:
                raise ValidationError(str(response.text))
        except:
            disable = True
        if disable:
            return 'disable'
        api_frequency_mapping = {
            'today': 'Today_Visited',
            'week': 'This_Week_Visted',
            'month': 'This_Month_Visted',
            'quarter': 'Visited_Quarterly',
            'half': 'Semi_Year_Visited',
            'year': 'Annual_Visited'
        }
        data = {
            'categories': [],
            'walk_in': [],
            'booking': [],
            'conversion': [],
            'width': [0.32, 0.40] if model == 'region' else [0.22, 0.32]
        }
        if model == 'region':
            records = request.env['regions'].search([('is_parent', '=', True)], order='name')
        elif model == 'cluster':
            records = request.env['regions'].search([('is_parent', '=', False)], order='name')
        else:
            domain = []
            if region:
                domain.append(('region_id', '=', int(region)))
            if cluster:
                domain.append(('sub_region_id', 'in', cluster))
            records = request.env['building'].search(domain, order='name')
            data = ''
        current_datetime = datetime.today()
        start_date = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_date + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        if frequency == 'today':
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'week':
            start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
            start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]

            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)

            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'year':
            fin_year_obj = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
            start_date = fin_year_obj.strftime('%Y-%m-%d')
            start_formatted = self.get_actual_date(start_date + ' 00:00:00')
        for record in records:
            domain_str = 'region_id' if model == 'region' else 'sub_region_id' if model == 'cluster' else 'id'

            walk_in = 0
            record_name = record.code if model == 'project' else record.name
            if record_name in api_model_mapping.get(model):
                walk_in = api_model_mapping[model][record_name].get(api_frequency_mapping[frequency])

            booking = request.env['unit.reservation'].search(
                [('date', '<=', end_formatted), ('date', '>=', start_formatted),
                 (f'building.{domain_str}', '=', record.id), ('state', 'in', ('confirmed', 'canceled'))])
            booking_count = len(booking)
            conversion = "{:,.2f}".format(
                booking_count * 100 / walk_in if walk_in != 0 else 0 if (booking_count == 0 and walk_in == 0) else 100)
            if model == 'project':
                data += f"""
                    <tr>
                        <td class="pr-0">{record.name}</td>
                        <td class="text-right">{walk_in}</td>
                        <td class="text-right">{booking_count}</td>
                        <td class="text-right">{conversion}</td>
                    </tr>
                """
            else:
                data['categories'].append(record.name)
                data['walk_in'].append(walk_in)
                data['booking'].append(booking_count)
                data['conversion'].append(conversion)
        return data

    @http.route('/jupiter_dashboard_optima/get_top_20_cp', auth='public', type='json')
    def get_top_20_cp(self, frequency='month', custom_start=False, custom_end=False):
        current_datetime = datetime.today()
        start_date = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_date + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        if custom_start and custom_end:
            start_formatted = self.get_actual_date(str(custom_start) + ' 00:00:00')
            end_formatted = self.get_actual_date(str(custom_end) + ' 23:59:59')
        elif frequency == 'today':
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'week':
            start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
            start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]

            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'year':
            fin_year_obj = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
            start_date = fin_year_obj.strftime('%Y-%m-%d')
            start_formatted = self.get_actual_date(start_date + ' 00:00:00')

        booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_formatted),
             ('state', 'in', ('confirmed', 'canceled')), ('source_of_booking', '=', 'cp')])
        cp_dict = {}
        for booking in booking_confirmed:
            if booking.cp_id:
                if booking.cp_id.id in cp_dict:
                    cp_dict[booking.cp_id.id][0] += 1
                else:
                    cp_dict[booking.cp_id.id] = [1, booking.cp_id.name]
        cp_dict = sorted(cp_dict.items(), key=lambda x: x[1][0], reverse=True)[:20]
        cp_data = ''
        for cp in cp_dict:
            cp_data += f"""
                <tr>
                    <td>{cp[1][1]}</td>
                    <td class="text-right">{cp[1][0]}</td>
                </tr>
            """
        return cp_data

    @http.route('/jupiter_dashboard_optima/manpower_productivity', auth='public', type='json')
    def manpower_productivity(self, frequency='month', count_or_value='count', date_from=False, date_to=False):
        def get_productivity(start_date, end_date, project_domain):
            total_manpower = 0
            total_booking_count = 0
            projects = request.env['building'].search(project_domain)
            for project in projects:
                first_assigning = request.env['project.employee.assigning'].search(
                    [('project_id', '=', project.id), ('date', '<=', start_date)], limit=1)
                in_range_assigning = request.env['project.employee.assigning'].search(
                    [('project_id', '=', project.id), ('date', '<=', end_date), ('date', '>=', start_date)], order='id')
                in_range_mapping = {}
                for assign in in_range_assigning:
                    in_range_mapping[assign.date] = assign
                employee_total_count = 0
                no_of_days = 0

                def compute_employee_count(assigning):
                    return (len(assigning.closing_manager_ids.mapped(
                        'employee_id')) + len(assigning.sourcing_manager_ids.mapped(
                        'employee_id')) + len(assigning.closing_tl_ids.mapped(
                        'employee_id')) + len(assigning.sourcing_tl_ids.mapped(
                        'employee_id')) + len(assigning.crm_ids.mapped(
                        'employee_id')) + len(assigning.marketing_ids.mapped(
                        'employee_id')) + len(assigning.business_head_id) + len(
                        assigning.site_head_id) + len(assigning.cluster_head_id))

                employee_count = compute_employee_count(first_assigning) if first_assigning else 0
                current_date = start_date
                while current_date <= end_date:
                    no_of_days += 1
                    if current_date in in_range_mapping:
                        first_assigning = in_range_mapping[current_date]
                        employee_count = compute_employee_count(first_assigning)
                    employee_total_count += employee_count
                    current_date += timedelta(days=1)
                man_power_per_day = employee_total_count / no_of_days if no_of_days != 0 else 0
                end_formatted = end_date.strftime('%Y-%m-%d 23:59:59')
                start_formatted = start_date.strftime('%Y-%m-%d 00:00:00')
                bookings = request.env['unit.reservation'].search([('building', '=', project.id),
                                                                   ('date', '<=', end_formatted),
                                                                   ('date', '>=', start_formatted),
                                                                   ('state', 'in', ('confirmed', 'canceled'))])
                if count_or_value == 'count':
                    booking_count = len(bookings)
                else:
                    booking_count = sum(bookings.mapped('flat_cost')) / 100000
                total_manpower += man_power_per_day
                total_booking_count += booking_count
            total_productivity = total_booking_count / total_manpower if total_manpower != 0 else 0
            return "{:,.2f}".format(total_productivity)

        current_datetime = datetime.today().date()
        start_date = end_date = current_datetime
        if date_from and date_to:
            if date_from > date_to:
                raise ValidationError('Date From should be less than Date To')
            start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        elif frequency == 'week':
            start_date = current_datetime - timedelta(days=current_datetime.weekday())
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1)
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            start_date = start_date.date()
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
            start_date = start_date.date()
        elif frequency == 'year':
            start_date = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
        consolidate = get_productivity(start_date, end_date, [])
        regions = request.env['regions'].search([('is_parent', '=', True)], order='name')
        region_data = {
            'categories': [],
            'data': []
        }
        for region in regions:
            region_data['categories'].append(region.name)
            region_data['data'].append(get_productivity(start_date, end_date, [('region_id', '=', region.id)]))
        cluster_data = {
            'categories': [],
            'data': []
        }
        clusters = request.env['regions'].search([('is_parent', '=', False)], order='name')
        for cluster in clusters:
            cluster_data['categories'].append(cluster.name)
            cluster_data['data'].append(get_productivity(start_date, end_date, [('sub_region_id', '=', cluster.id)]))
        project_data = ''
        projects = request.env['building'].search([], order='name')
        for project in projects:
            project_productivity = get_productivity(start_date, end_date, [('id', '=', project.id)])
            project_data += f"<tr><td>{project.name}</td><td class='text-right'>{project_productivity}</td></tr>"
        return [consolidate, region_data, cluster_data, project_data]

    @http.route('/jupiter_dashboard_optima/walk_in_get_cluster', auth='public', type='json')
    def jupiter_dashboard_walk_in_get_cluster(self, region=False):
        cluster_data = 'Cluster<select id="walk_in_cluster_select" class="controller_selects walk_in_cluster_select" multiple="multiple">'
        domain = ''
        if region:
            domain += f' and region_id = {region}'
        request.env.cr.execute(f"select id, name from regions where is_parent = False {domain}")
        rows = request.env.cr.dictfetchall()
        for row in rows:
            cluster_data += "<option cluster_id='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        cluster_data += '</select>'
        return cluster_data

    @http.route('/jupiter_dashboard_optima/get_cluster', auth='public', type='json')
    def jupiter_dashboard_get_cluster(self, region=False):
        cluster_data = 'Cluster<select id="cluster_select" class="controller_selects cluster_select" multiple="multiple">'
        domain = ''
        if region:
            domain += f' and region_id = {region}'
        request.env.cr.execute(f"select id, name from regions where is_parent = False {domain}")
        rows = request.env.cr.dictfetchall()
        for row in rows:
            cluster_data += "<option cluster_id='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        cluster_data += '</select>'
        return cluster_data

    @http.route('/jupiter_dashboard_optima/get_region', auth='public', type='json')
    def jupiter_dashboard_get_region(self):
        regions = request.env['regions'].search([('is_parent', '=', True)], order='name')
        data = '<a class="dropdown-item" href="#">All</a>'
        for region in regions:
            data += '<a class="dropdown-item" href="#" value="%s">%s</a>' % (str(region.id), str(region.name))
        configuration_data = ''
        request.env.cr.execute("select id, name from building_unit")
        rows = request.env.cr.dictfetchall()
        for row in rows:
            configuration_data += "<option configuration_id='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        return [data, configuration_data]

    @http.route('/jupiter_dashboard_optima/sales_inventory', auth='public', type='json')
    def sales_inventory(self, region_wise, project_wise, project_region, configuration_ids=False, cluster_ids=False):
        region_list = []
        region_booked = []
        region_available = []
        if region_wise:
            regions = request.env['regions'].search([('is_parent', '=', True)], order='name')
            for region in regions:
                available_count = request.env['product.template'].search_count(
                    [('region_id', '=', region.id), ('state', '=', 'free')])
                booked_count = request.env['product.template'].search_count(
                    [('region_id', '=', region.id), ('state', '=', 'reserved')])
                region_list.append(region.name)
                region_booked.append(booked_count)
                region_available.append(available_count)

        project_list = []
        project_booked = []
        project_available = []
        if project_wise:
            region_clause = ''
            configuration_clause = ''
            if project_region:
                region_clause = ' AND b.region_id = %s' % str(project_region)
            if cluster_ids:
                region_clause += f' AND b.sub_region_id = {",".join([str(i) for i in cluster_ids])}'
            if configuration_ids:
                configuration_clause += f' AND pt.flat_type in ({",".join([str(i) for i in configuration_ids])})'
            request.env.cr.execute("""
                SELECT 
                    b.name, 
                    SUM(CASE WHEN pt.state = 'free' THEN 1 ELSE 0 END) AS available_count,
                    SUM(CASE WHEN pt.state = 'reserved' THEN 1 ELSE 0 END) AS reserved_count
                FROM 
                    building b 
                LEFT JOIN 
                    product_template pt ON pt.building_id = b.id %s
                WHERE 
                    b.active = True and pt.active = True
                    %s
                GROUP BY 
                    b.id, b.name
                ORDER BY 
                    available_count DESC
                LIMIT 25;
            """ % (configuration_clause, region_clause))
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

    @http.route('/jupiter_dashboard_optima/get_cluster_select_data', auth='public', type='json')
    def get_cluster_select_data(self, region_ids=False):
        cluster_data = ''
        domain = ''
        if region_ids:
            domain = f" and region_id in ({','.join([str(i) for i in region_ids])}) "
        request.env.cr.execute(f"select id, name from regions where is_parent = False {domain}")
        rows = request.env.cr.dictfetchall()
        for row in rows:
            cluster_data += "<span class='d-flex'><input class='cluster_checkbox mr-2' type='checkbox' checked='checked' cluster_id='" + str(
                row['id']) + "'/>" + str(row['name']) + "</span>"
        return cluster_data

    @http.route('/jupiter_dashboard_optima/get_region_select_data', auth='public', type='json')
    def get_region_select_data(self):
        region_data = ''
        request.env.cr.execute("select id, name from regions where is_parent = True")
        rows = request.env.cr.dictfetchall()
        for row in rows:
            region_data += "<option region_id='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        return region_data

    @http.route('/jupiter_dashboard_optima/get_last_6_month_cp_booking', auth='public', type='json')
    def jupiter_dashboard_tres_get_last_6_month_cp_booking(self, region_ids=False, cluster_ids=False):
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
            domain = [('date', '<=', end_date_formatted), ('date', '>=', start_date_formatted),
                      ('state', '=', 'confirmed'), ('source_of_booking', '=', 'cp')]
            if region_ids:
                domain.append(('building.region_id', 'in', region_ids))
            if cluster_ids:
                domain.append(('building.sub_region_id', 'in', cluster_ids))
            booking_search = request.env['unit.reservation'].search(domain)
            bookings.append(len(booking_search))
        return {
            'months': months,
            'bookings': bookings,
        }

    @http.route('/jupiter_dashboard_optima/get_cp_count', auth='public', type='json')
    def jupiter_dashboard_tres_get_cp_count(self):
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
        quarter_cp_domain = [('is_channel', '=', True), ('create_date', '>=', start_of_quarter_formatted),
                             ('create_date', '<=', end_formatted)]
        half_cp_domain = [('is_channel', '=', True), ('create_date', '>=', start_of_half_formatted),
                          ('create_date', '<=', end_formatted)]
        year_cp_domain = [('is_channel', '=', True), ('create_date', '>=', fin_year_start_formatted),
                          ('create_date', '<=', end_formatted)]

        month_cps = 0
        quarter_cps = 0
        half_cps = 0
        year_cps = 0

        config_obj = request.env['ir.config_parameter'].sudo()
        disable = True
        if config_obj.get_param('jupiter_dashboard_tres.enable_dashboard_new_cp_api'):
            username = config_obj.get_param('jupiter_dashboard_tres.dashboard_new_cp_api_username')
            password = config_obj.get_param('jupiter_dashboard_tres.dashboard_new_cp_api_key')
            url = config_obj.get_param('jupiter_dashboard_tres.dashboard_new_cp_api_url')
            data = {
                'params': {
                    'login': username,
                    'password': password
                }
            }
            try:
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post(url, headers=headers, json=data)
                if response.ok:
                    rec = json.loads(response.text)
                    api_data = rec.get('data')
                    month_cps = api_data.get('ThisMonth')
                    quarter_cps = api_data.get('FinancialYearQuarter')
                    half_cps = api_data.get('Financial_HalfYear')
                    year_cps = api_data.get('Financial_Year')
                    disable = False
                else:
                    raise ValidationError(str(response.text))
            except:
                disable = True

        if disable:
            month_cps = request.env['res.partner'].search_count(month_cp_domain)
            quarter_cps = request.env['res.partner'].search_count(quarter_cp_domain)
            half_cps = request.env['res.partner'].search_count(half_cp_domain)
            year_cps = request.env['res.partner'].search_count(year_cp_domain)

        month_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').filtered(lambda x: x.is_channel)

        quarter_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_quarter_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').filtered(lambda x: x.is_channel)

        half_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_half_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').filtered(lambda x: x.is_channel)

        year_cps_active = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', fin_year_start_formatted),
             ('state', '=', 'confirmed')]).mapped('cp_id').filtered(lambda x: x.is_channel)
        total_cp = request.env['res.partner'].search([('is_channel', '=', True)])
        total_cp_count = len(total_cp)
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

            'month_cps_dormant': total_cp_count - len(month_cps_active),
            'quarter_cps_dormant': total_cp_count - len(quarter_cps_active),
            'half_cps_dormant': total_cp_count - len(half_cps_active),
            'year_cps_dormant': total_cp_count - len(year_cps_active),

            'month_cp_domain': str(month_cp_domain),
            'quarter_cp_domain': str(quarter_cp_domain),
            'half_cp_domain': str(half_cp_domain),
            'year_cp_domain': str(year_cp_domain),

            'month_cp_active_domain': "[('id', 'in', " + str(month_cps_active.ids) + ")]",
            'quarter_cp_active_domain': "[('id', 'in', " + str(quarter_cps_active.ids) + ")]",
            'half_cp_active_domain': "[('id', 'in', " + str(half_cps_active.ids) + ")]",
            'year_cp_active_domain': "[('id', 'in', " + str(year_cps_active.ids) + ")]",

            'month_cps_dormant_domain': "[('id', 'in', " + str(
                (total_cp.filtered(lambda x: x not in month_cps_active)).ids) + ")]",
            'quarter_cps_dormant_domain': "[('id', 'in', " + str(
                (total_cp.filtered(lambda x: x not in quarter_cps_active)).ids) + ")]",
            'half_cps_dormant_domain': "[('id', 'in', " + str(
                (total_cp.filtered(lambda x: x not in half_cps_active)).ids) + ")]",
            'year_cps_dormant_domain': "[('id', 'in', " + str(
                (total_cp.filtered(lambda x: x not in year_cps_active)).ids) + ")]",
        }

    @http.route('/jupiter_dashboard_optima/budget_actual_comparison', auth='public', type='json')
    def jupiter_dashboard_budget_actual_comparison(self, booking_type='number', registration_type='number',
                                                   budget_type='number'):
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
            months.append(start_date.strftime('%b'))
            budget_month = start_date.strftime("%B %Y")
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            start_date_formatted = self.get_actual_date(start_date + " 00:00:00")
            end_date_formatted = self.get_actual_date(end_date + " 23:59:59")
            if booking_type:
                booking_search = request.env['unit.reservation'].search(
                    [('date', '<=', end_date_formatted), ('date', '>=', start_date_formatted),
                     ('state', '=', 'confirmed')])
                if booking_type == 'number':
                    bookings.append(len(booking_search))
                else:
                    bookings.append(sum(booking_search.mapped('flat_cost')) / 100000)
            if registration_type:
                registration_search = request.env['project.registration'].search(
                    [('registration_date', '<=', end_date), ('registration_date', '>=', start_date),
                     ('state', '=', 'confirmed')])
                if registration_type == 'number':
                    registrations.append(len(registration_search))
                else:
                    booking_of_registration = request.env['unit.reservation'].search(
                        [('building_unit', 'in', registration_search.mapped('flat_id').ids),
                         ('state', '=', 'confirmed')])
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

    @http.route('/jupiter_dashboard_optima/get_project_data', auth='public', type='json')
    def get_project_data(self, region=False, cluster=False):
        domain = []
        if region:
            domain.append(('region_id', 'in', region))
        if cluster:
            domain.append(('sub_region_id', 'in', cluster))
        projects = request.env['building'].search([('active', '=', True)] + domain, order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(projects)) if len(projects) != 0 else 0
        degree = 0
        for project in projects:
            degree += angle
            data += f"""
                <div class="col-4 px-0">
                    <div class="project-blocks selectable-block active" project_id="{project.id}">
                        {project.name}
                    </div>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_project_data2', auth='public', type='json')
    def get_project_data2(self, region=False, cluster=False):
        domain = []
        if region:
            domain.append(('region_id', 'in', region))
        if cluster:
            domain.append(('sub_region_id', 'in', cluster))
        projects = request.env['building'].search([('active', '=', True)] + domain, order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(projects)) if len(projects) != 0 else 0
        degree = 0
        for project in projects:
            degree += angle
            data += f"""
                <div class="col-3 px-0">
                    <div class="project-blocks2 selectable-block2 active" project_id="{project.id}">
                        {project.name}
                    </div>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_search_project_data2', type='json', auth='user')
    def get_search_project_data2(self, search_term='', excluded_ids=None, region=False, cluster=False):
        # 1) Ensure excluded_ids is a Python list
        if excluded_ids is None:
            excluded_ids = []

        # 2) Base domain: only parent projects
        domain = [('active', '=', True)]
        # 3) Keep your existing region/cluster filters exactly the same
        if region:
            domain.append(('region_id', 'in', region))
        if cluster:
            domain.append(('sub_region_id', 'in', cluster))
        if search_term:
            domain.append(('name', 'ilike', search_term))

        # 3) Exclude any IDs already in excluded_ids
        if excluded_ids:
            domain.append(('id', 'not in', excluded_ids))
        print("excluded_ids", excluded_ids)
        projects = request.env['building'].search(domain, order='name')
        data2 = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(projects)) if len(projects) != 0 else 0
        degree = 0

        for project in projects:
            degree += angle
            data2 += f"""
                        <div>
                          <label class="d-flex align-items-center project-blocks2 selectable-block2 active"
                                 for="project-checkbox-{project.id}"
                                 data2-project-id="{project.id}"
                                 tabindex="0">
                            <input
                              type="checkbox"
                              id="project-checkbox-{project.id}"
                              name="projects[]"
                              value="{project.id}"
                              class="me-2 project-checkbox"
                              aria-checked="false"
                            />
                            <span style="padding-left: 15px;">{project.name}</span>
                          </label>
                        </div>
                    """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return {
            'data2': data2,
            'count': len(projects),
        }

    @http.route('/jupiter_dashboard_optima/get_cluster_data', auth='public', type='json')
    def get_cluster_data(self, region=False):
        domain = []
        if region:
            domain = [('region_id', 'in', region)]
        clusters = request.env['regions'].search([('is_parent', '=', False)] + domain, order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(clusters)) if len(clusters) != 0 else 0
        degree = 0
        for cluster in clusters:
            degree += angle
            data += f"""
                <div class="col-4 px-0">
                    <div class="cluster-blocks selectable-block active" cluster_id="{cluster.id}">
                        {cluster.name}
                    </div>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_cluster_data2', auth='public', type='json')
    def get_cluster_data2(self, region=False):
        domain = []
        if region:
            domain = [('region_id', 'in', region)]
        clusters = request.env['regions'].search([('is_parent', '=', False)] + domain, order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(clusters)) if len(clusters) != 0 else 0
        degree = 0
        for cluster in clusters:
            degree += angle
            data += f"""
                <div class="col-3 px-0">
                    <div class="cluster-blocks2 selectable-block2 active" cluster_id="{cluster.id}">
                        {cluster.name}
                    </div>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_search_cluster_data2', type='json', auth='user')
    def get_search_cluster_data2(self, search_term='', excluded_ids=None):
        # 1) Ensure excluded_ids is a Python list
        if excluded_ids is None:
            excluded_ids = []

        # 2) Base domain: only parent clusters
        domain = [('is_parent', '=', False)]
        if search_term:
            domain.append(('name', 'ilike', search_term))

        # 3) Exclude any IDs already in excluded_ids
        if excluded_ids:
            domain.append(('id', 'not in', excluded_ids))
        print("excluded_ids", excluded_ids)
        clusters = request.env['regions'].search(domain, order='name')
        data2 = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(clusters)) if len(clusters) != 0 else 0
        degree = 0

        for cluster in clusters:
            degree += angle
            data2 += f"""
                    <div>
                      <label class="d-flex align-items-center cluster-blocks2 selectable-block2 active"
                             for="cluster-checkbox-{cluster.id}"
                             data2-cluster-id="{cluster.id}"
                             tabindex="0">
                        <input
                          type="checkbox"
                          id="cluster-checkbox-{cluster.id}"
                          name="clusters[]"
                          value="{cluster.id}"
                          class="me-2 cluster-checkbox"
                          aria-checked="false"
                        />
                        <span style="padding-left: 15px;">{cluster.name}</span>
                      </label>
                    </div>
                """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return {
            'data2': data2,
            'count': len(clusters),
        }

    @http.route('/jupiter_dashboard_optima/get_region_data', auth='public', type='json')
    def get_region_data(self):
        regions = request.env['regions'].search([('is_parent', '=', True)], order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(regions)) if len(regions) != 0 else 0
        degree = 0
        for region in regions:
            degree += angle
            data += f"""
                <div class="col-4 px-0">
                    <div class="region-blocks selectable-block active" region_id="{region.id}">
                        {region.name}
                    </div>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    #             graph 2 region dashboard iii
    @http.route('/jupiter_dashboard_optima/get_region_data2', auth='public', type='json')
    def get_region_data2(self):
        regions = request.env['regions'].search([('is_parent', '=', True)], order='name')
        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(regions)) if len(regions) != 0 else 0
        degree = 0
        for region in regions:
            degree += angle
            data += f"""
                <div class="col-3 px-0">
                    <div class="region-blocks2 selectable-block2 active" region_id="{region.id}">
                        {region.name}
                    </div>
                </div>

            """

            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_search_region_data2', type='json', auth='user')
    def get_search_region_data2(self, search_term='', excluded_ids=None):
        # 1) Ensure excluded_ids is a Python list
        if excluded_ids is None:
            excluded_ids = []

        # 2) Base domain: only parent regions
        domain = [('is_parent', '=', True)]
        if search_term:
            domain.append(('name', 'ilike', search_term))

        # 3) Exclude any IDs already in excluded_ids
        if excluded_ids:
            domain.append(('id', 'not in', excluded_ids))
        print("excluded_ids", excluded_ids)
        regions = request.env['regions'].search(domain, order='name')
        data2 = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(regions)) if len(regions) != 0 else 0
        degree = 0
        for region in regions:
            degree += angle
            data2 += f"""
                <div>
                  <label class="d-flex align-items-center region-blocks2 selectable-block2 active"
                         for="region-checkbox-{region.id}"
                         data2-region-id="{region.id}"
                         tabindex="0">
                    <input
                      type="checkbox"
                      id="region-checkbox-{region.id}"
                      name="regions[]"
                      value="{region.id}"
                      class="me-2 region-checkbox"
                      aria-checked="false"
                    />
                    <span style="padding-left: 15px;">{region.name}</span>
                  </label>
                </div>
            """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1

        return {
            'data2': data2,
            'count': len(regions),
        }

    @http.route('/jupiter_dashboard_optima/get_cluster_head_data2', auth='public', type='json')
    def get_cluster_head_data2(self, region=False, cluster=False):
        domain = []
        cluster_head_data = request.env['building'].search([('active', 'in', [True, False])], order='name')
        cluster_head = cluster_head_data.mapped('cluster_head_id')
        # Convert Odoo records to a list of dicts
        cluster_head_list = [{'id': ch.id, 'name': ch.name} for ch in cluster_head]

        # Append dummy "Other" entry
        cluster_head_list.append({'id': 0, 'name': 'Other'})

        data = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(cluster_head)) if len(cluster_head) != 0 else 0
        degree = 0
        for ch in cluster_head_list:
            degree += angle
            data += f"""
                    <div class="col-3 px-0">
                        <div class="cluster-head-blocks2 selectable-block2 active" cluster_heads_id="{ch['id']}">
                            {ch['name']}
                        </div>
                    </div>
                """

            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        return data

    @http.route('/jupiter_dashboard_optima/get_search_clusterhead_data2', type='json', auth='user')
    def get_search_clusterhead_data2(self, search_term='', excluded_ids=None):
        # 1) Ensure excluded_ids is a Python list
        if excluded_ids is None:
            excluded_ids = []

        # 2) Base domain: only parent clusterheads
        domain = [('active', 'in', [True, False])]
        if search_term:
            domain.append(('cluster_head_id.name', 'ilike', search_term))

        # 3) Exclude any IDs already in excluded_ids
        if excluded_ids:
            domain.append(('cluster_head_id', 'not in', excluded_ids))
        print("excluded_ids", excluded_ids)
        clusterheads = request.env['building'].search(domain, order='name')
        cluster_heads = clusterheads.mapped('cluster_head_id').filtered(lambda ch: ch)
        # Convert Odoo records to a list of dicts
        cluster_head_list = [{'id': ch.id, 'name': ch.name} for ch in cluster_heads]
        if (search_term in 'other' or not search_term) and 0 not in excluded_ids:
            cluster_head_list.append({'id': 0, 'name': 'Other'})

        data2 = ""
        colors = ['#14b5ff', '#00d58e', '#8950ff', '#ff50ab', '#eb5b30', '#0d7ea9', '#ff1f1f', '#008755', '#e5ac0a',
                  '#00ad95']
        index = 0
        angle = (360 / len(cluster_head_list)) if len(cluster_head_list) != 0 else 0
        degree = 0
        for ch in cluster_head_list:
            degree += angle
            data2 += f"""
                        <div>
                          <label class="d-flex align-items-center clusterhead-blocks2 selectable-block2 active"
                                 for="clusterhead-checkbox-{ch['id']}"
                                 data2-clusterhead-id="{ch['id']}"
                                 tabindex="0">
                            <input
                              type="checkbox"
                              id="clusterhead-checkbox-{ch['id']}"
                              name="clusterheads[]"
                              value="{ch['id']}"
                              class="me-2 clusterhead-checkbox"
                              aria-checked="false"
                            />
                            <span style="padding-left: 15px;">{ch['name']}</span>
                          </label>
                        </div>
                    """
            if index == len(colors) - 1:
                index = 0
            else:
                index += 1
        # print("cluster_heads popup", len(cluster_head_list))
        return {
            'data2': data2,
            'count': len(cluster_head_list),
        }

    @http.route('/jupiter_dashboard_optima/bookings_registrations_region_wise', auth='public', type='json')
    def bookings_registrations_region_wise(self, frequency='today', region_ids=False, count_or_value='count',
                                           region_or_cluster='region', parent_region=False, project_ids=False,
                                           custom_start=False, custom_end=False):
        series = [
            {
                'name': 'Gross',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Cancelled',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Net',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Registration',
                'type': 'line',
                'data': []
            },
        ]
        categories = []
        current_datetime = datetime.today()
        start_date = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_date + timedelta(days=1) - timedelta(microseconds=1)
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d %H:%M:%S'))
        if custom_start and custom_end:
            start_formatted = self.get_actual_date(str(custom_start) + ' 00:00:00')
            end_formatted = self.get_actual_date(str(custom_end) + ' 23:59:59')
            start_date = datetime.strptime(start_formatted, '%Y-%m-%d %H:%M:%S')
            end_of_today = datetime.strptime(end_formatted, '%Y-%m-%d %H:%M:%S')
        elif frequency == 'today':
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'week':
            start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
            start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'month':
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'quarter':
            financial_year_start_month = 4
            quarter_month_starts = [4, 7, 10, 1]

            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
            start_date = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
            next_quarter_index = (quarter_index + 1) % 4
            quarter_end = datetime(current_datetime.year + year_offset, quarter_month_starts[next_quarter_index],
                                   1) - timedelta(days=1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'half':
            financial_year_start_month = 4
            half_year_starts = [4, 10]
            year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
            half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
            start_date = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
            start_formatted = self.get_actual_date(start_date.strftime('%Y-%m-%d %H:%M:%S'))
        elif frequency == 'year':
            fin_year_obj = (
                date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
            start_date = fin_year_obj.strftime('%Y-%m-%d')
            fin_year_end = date.today().strftime('%Y-%m-%d')
            start_formatted = self.get_actual_date(start_date + ' 00:00:00')
        if region_or_cluster == 'project':
            domain = []
            if project_ids:
                domain.append(('id', 'in', project_ids))
            if region_ids:
                domain.append(('sub_region_id', 'in', region_ids))
            if parent_region:
                domain.append(('region_id', 'in', parent_region))
            regions = request.env['building'].search(domain, order='name')
        else:
            if region_or_cluster == 'region':
                domain = [('is_parent', '=', True)]
            else:
                domain = [('is_parent', '=', False)]
                if parent_region:
                    domain.append(('region_id', 'in', parent_region))
            if region_ids:
                domain.append(('id', 'in', region_ids))
            regions = request.env['regions'].search(domain, order='name')
        project_values = {
            'gross': {},
            'cancelled': {},
            'net': {},
            'registration': {}
        }
        for region in regions:
            categories.append(region.name)
            region_string = 'region_id' if region_or_cluster == 'region' else 'sub_region_id' if region_or_cluster == 'cluster' else 'id'
            booking_confirmed = request.env['unit.reservation'].search(
                [('date', '<=', end_formatted), ('date', '>=', start_formatted),
                 ('state', 'in', ('confirmed', 'canceled')), (f'building.{region_string}', '=', region.id)])
            booking_cancelled = request.env['unit.reservation'].search(
                [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', start_formatted),
                 ('state', '=', 'canceled'), (f'building.{region_string}', '=', region.id)])
            registration = request.env['project.registration'].search(
                [('registration_date', '<=', end_of_today), ('registration_date', '>=', start_date),
                 ('state', '=', 'confirmed'), (f'project_id.{region_string}', '=', region.id)])
            if count_or_value == 'count':
                registration_value = len(registration)
                booking_gross_value = len(booking_confirmed)
                booking_cancelled_value = len(booking_cancelled)
                booking_value = booking_gross_value - booking_cancelled_value
            else:
                booking_of_registrations = request.env['unit.reservation'].search(
                    [('building_unit', 'in', registration.mapped('flat_id').ids),
                     ('state', '=', 'confirmed')])
                registration_value = round(sum(booking_of_registrations.mapped('flat_cost')) / 100000, 2)
                booking_gross_value = round(sum(booking_confirmed.mapped('flat_cost')) / 100000, 2)
                booking_cancelled_value = round(sum(booking_cancelled.mapped('flat_cost')) / 100000, 2)
                booking_value = round(booking_gross_value - booking_cancelled_value, 2)
                booking_value = round(booking_value, 2)
                booking_cancelled_value = round(booking_cancelled_value, 2)
            series[0]['data'].append(booking_gross_value)
            series[1]['data'].append(booking_cancelled_value)
            series[2]['data'].append(booking_value)
            series[3]['data'].append(registration_value)
            if region_or_cluster == 'project':
                project_values['gross'][region.name] = booking_gross_value
                project_values['cancelled'][region.name] = booking_cancelled_value
                project_values['net'][region.name] = booking_value
                project_values['registration'][region.name] = registration_value
        if region_or_cluster == 'project':
            def get_top_10_sorted(dictionary):
                sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
                top_10_items = sorted_items[:10]
                categories = [item[0] for item in top_10_items]
                values = [item[1] for item in top_10_items]
                return {'categories': categories, 'values': values}

            project_values['gross'] = get_top_10_sorted(project_values['gross'])
            project_values['cancelled'] = get_top_10_sorted(project_values['cancelled'])
            project_values['net'] = get_top_10_sorted(project_values['net'])
            project_values['registration'] = get_top_10_sorted(project_values['registration'])
        return [series, categories, project_values]

    @http.route('/jupiter_dashboard_optima/get_financial_year', auth='public', type='json')
    def get_financial_year(self):
        print("fgdsfgdsg")
        sequence = request.env['account.journal'].search([('type', '=', 'purchase')], limit=1).sequence_id
        values = []
        for line in sequence.date_range_ids:
            date_from = line.date_from
            date_to = line.date_to
            year_from = line.date_from.year
            year_to = year_from + 1
            label = f"{year_from} - {year_to}"

            values.append(f'''
                <option selected="" value="{str(date_from)+"#"+str(date_to)}">{label}</option>
                        
            ''')
        return values

    # Graph 2 Fetching Data and Returning It via JSON dashboard iii
    @http.route('/jupiter_dashboard_optima/bookings_registrations_region_wise2', auth='public', type='json')
    def bookings_registrations_region_wise2(self, frequency='today', region_ids=False, count_or_value='count',
                                            region_or_cluster='region', parent_region=False, project_ids=False,
                                           custom_start=False, custom_end=False, month_or_quarter='month', financial_year=False, show_booking=True, show_cancel=True, show_net=True, show_reg=True, cluster_ids=False, cluster_head_ids=False):
        unit_reservation_other_domain = []
        project_registration_other_domain = []
        if region_ids:
            region_string = 'region_id'
            unit_reservation_other_domain = [(f'building.{region_string}', 'in', region_ids)]
            project_registration_other_domain = [(f'project_id.{region_string}', 'in', region_ids)]
        elif cluster_ids:
            unit_reservation_other_domain = [(f'building.sub_region_id', 'in', cluster_ids)]
            project_registration_other_domain = [(f'project_id.sub_region_id', 'in', cluster_ids)]
        elif project_ids:
            unit_reservation_other_domain = [(f'building', 'in', project_ids)]
            project_registration_other_domain = [(f'project_id', 'in', project_ids)]
        elif cluster_head_ids:
            if None in cluster_head_ids:
                cluster_head_ids.append(False)
            unit_reservation_other_domain = [(f'building.cluster_head_id', 'in', cluster_head_ids)]
            project_registration_other_domain = [(f'project_id.cluster_head_id', 'in', cluster_head_ids)]

        series = [
            {
                'name': 'Booking',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Cancellation',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Net',
                'type': 'column',
                'data': []
            },
            {
                'name': 'Registration',
                'type': 'column',
                'data': []
            }
        ]
        th_count = 2
        extra_th_count = 0
        table_dict = {
            'Booking':{
                'color':'#aed6f1',
                'datas':[],
                'total':0
                },
            'Cancellation':{
                'color':'#D3D3D3',
                'datas':[],
                'total':0
                },
            'Net':{
                'color':'#82e0aa',
                'datas':[],
                'total':0
                },
            'Registration':{
                'color':'#f1948a',
                'datas':[],
                'total':0
                },
        }

        categories = []  # X-axis labels (quarters)
        current_datetime = datetime.today()
        region_string = 'region_id'
        if not financial_year:
            sequence = request.env['account.journal'].search([('type', '=', 'purchase')], limit=1).sequence_id
            for line in sequence.date_range_ids:
                date_from = line.date_from
                date_to = line.date_to
                label = str(date_from)+"#"+str(date_to)
                financial_year = label
        if financial_year and "#" in financial_year:
            start_date, end_date = financial_year.split("#")

            date_format = "%Y-%m-%d"

            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)

            print("Start Date:", start_date)
            print("End Date:", end_date)


        if month_or_quarter == 'month':
            current_date = start_date

            # Loop from start_date to end_date month by month
            while current_date <= end_date:
                th_count+=1
                extra_th_count+=1
                print("Current Month:", current_date.strftime("%Y-%m"))


            # for i in range(12):
                first_day_of_month = current_date.replace(day=1)

                # Get the last day of the month
                last_day_of_month = first_day_of_month + relativedelta(months=1)  # last day of the month
                last_day_of_month = last_day_of_month - relativedelta(days=1)
                # Set start and end of the month (midnight to 23:59)
                start_of_month2 = first_day_of_month.replace(hour=0, minute=0, second=0)
                end_of_month2 = last_day_of_month.replace(hour=23, minute=59, second=59)
                categories.append(first_day_of_month.strftime('%b %Y'))  # e.g., 'Jan 2024'
                start_of_month = self.get_actual_date(first_day_of_month.strftime('%Y-%m-%d 00:00:00'))
                end_of_month = self.get_actual_date(last_day_of_month.strftime('%Y-%m-%d 23:59:59'))

                # Fetch cancelled bookings within this month
                booking_cancelled = request.env['unit.reservation'].search(
                    [('cancellation_date', '<=', end_of_month2), ('cancellation_date', '>=', start_of_month2),
                     ('state', '=', 'canceled')] + unit_reservation_other_domain
                )
                # Fetch confirmed bookings within this month (only confirmed state)
                booking_confirmed = request.env['unit.reservation'].search(
                    [('date', '<=', end_of_month), ('date', '>=', start_of_month),
                     ('state', 'in', ('confirmed', 'canceled'))] + unit_reservation_other_domain
                )

                # Fetch confirmed registrations within this month
                registration = request.env['project.registration'].search(
                    [('registration_date', '<=', end_of_month2), ('registration_date', '>=', start_of_month2),
                     ('state', '=', 'confirmed')] + project_registration_other_domain
                )
                # if start_of_month.month == 12:
                #     start_of_month
                if count_or_value == 'count':
                    # Count the records
                    booking_cancelled_value = len(booking_cancelled)
                    registration_value = len(registration)
                    booking_confirmed_value = len(booking_confirmed)
                else:
                    # For cancellations, sum the flat_cost of all canceled bookings
                    booking_cancelled_value = round(sum(booking_cancelled.mapped('flat_cost')) / 100000, 2)
                    # For confirmed bookings, sum the flat_cost of all confirmed bookings
                    booking_confirmed_value = round(sum(booking_confirmed.mapped('flat_cost')) / 100000, 2)
                    booking_of_registrations = request.env['unit.reservation'].search(
                        [('building_unit', 'in', registration.mapped('flat_id').ids),
                         ('state', '=', 'confirmed')])
                    registration_value = round(sum(booking_of_registrations.mapped('flat_cost')) / 100000, 2)
                net_value = round(booking_confirmed_value - booking_cancelled_value, 2)

                # Append data to the respective series
                if show_booking:
                    series[0]['data'].append(booking_confirmed_value)  # Bookings (Confirmed)
                    table_dict['Booking']['datas'].append(booking_confirmed_value)
                    table_dict['Booking']['total'] += booking_confirmed_value
                else:
                    series[0]['data'].append(0)  # Bookings (Confirmed)
                    table_dict['Booking']['datas'].append(0)
                    table_dict['Booking']['total'] += 0
                if show_cancel:
                    series[1]['data'].append(booking_cancelled_value)  # Cancellations
                    table_dict['Cancellation']['datas'].append(booking_cancelled_value)
                    table_dict['Cancellation']['total'] += booking_cancelled_value
                else:
                    series[1]['data'].append(0)  # Cancellations
                    table_dict['Cancellation']['datas'].append(0)
                    table_dict['Cancellation']['total'] += 0
                if show_net:
                    series[2]['data'].append(net_value)  # Net
                    table_dict['Net']['datas'].append(net_value)
                    table_dict['Net']['total'] += net_value
                else:
                    series[2]['data'].append(0)  # Net
                    table_dict['Net']['datas'].append(0)
                    table_dict['Net']['total'] += 0
                if show_reg:
                    series[3]['data'].append(registration_value)  # Registrations
                    table_dict['Registration']['datas'].append(registration_value)
                    table_dict['Registration']['total'] += registration_value
                else:
                    series[3]['data'].append(0)  # Registrations
                    table_dict['Registration']['datas'].append(0)
                    table_dict['Registration']['total'] += 0
                current_date += relativedelta(months=1)
        else:
            quarter_label_count = 1

            current_date = start_date

            # Loop from start_date to end_date month by month
            while current_date <= end_date:
                th_count += 1
                extra_th_count += 1
                print("Current Month:", current_date.strftime("%Y-%m"))


            # for i in range(12):
                first_day_of_month = current_date.replace(day=1)
                quarter_start_month = (first_day_of_month.month - 1) // 3 * 3 + 1
                quarter_end_date = first_day_of_month + relativedelta(months=3)
                quarter_end_date = quarter_end_date - relativedelta(days=1)

                # Get the last day of the month
                last_day_of_month = quarter_end_date

                start_of_month = self.get_actual_date(first_day_of_month.strftime('%Y-%m-%d 00:00:00'))
                end_of_month = self.get_actual_date(last_day_of_month.strftime('%Y-%m-%d 23:59:59'))

                # Set start and end of the month (midnight to 23:59)
                start_of_month2 = first_day_of_month.replace(hour=0, minute=0, second=0)
                end_of_month2 = last_day_of_month.replace(hour=23, minute=59, second=59)

                # categories.append(start_of_month.strftime('%b %Y'))  # e.g., 'Jan 2024'
                quarter_label = f'Q{quarter_label_count} {first_day_of_month.year}'
                quarter_label_count+=1
                categories.append(quarter_label)
                # Fetch cancelled bookings within this month
                booking_cancelled = request.env['unit.reservation'].search(
                    [('cancellation_date', '<=', end_of_month2), ('cancellation_date', '>=', start_of_month2),
                     ('state', '=', 'canceled')] + unit_reservation_other_domain
                )
                # Fetch confirmed bookings within this month (only confirmed state)
                booking_confirmed = request.env['unit.reservation'].search(
                    [('date', '<=', end_of_month), ('date', '>=', start_of_month),
                     ('state', 'in', ('confirmed', 'canceled'))] + unit_reservation_other_domain
                )
                # Fetch confirmed registrations within this month
                registration = request.env['project.registration'].search(
                    [('registration_date', '<=', end_of_month2), ('registration_date', '>=', start_of_month2),
                     ('state', '=', 'confirmed')] + project_registration_other_domain
                )

                if count_or_value == 'count':
                    # Count the records
                    booking_cancelled_value = len(booking_cancelled)
                    registration_value = len(registration)
                    booking_confirmed_value = len(booking_confirmed)
                else:
                    # For cancellations, sum the flat_cost of all canceled bookings
                    booking_cancelled_value = round(sum(booking_cancelled.mapped('flat_cost')) / 100000, 2)
                    # For confirmed bookings, sum the flat_cost of all confirmed bookings
                    booking_confirmed_value = round(sum(booking_confirmed.mapped('flat_cost')) / 100000, 2)
                    booking_of_registrations = request.env['unit.reservation'].search(
                        [('building_unit', 'in', registration.mapped('flat_id').ids),
                         ('state', '=', 'confirmed')])
                    registration_value = round(sum(booking_of_registrations.mapped('flat_cost')) / 100000, 2)
                net_value = round(booking_confirmed_value - booking_cancelled_value, 2)

                # Append data to the respective series
                if show_booking:
                    series[0]['data'].append(booking_confirmed_value)  # Bookings (Confirmed)
                    table_dict['Booking']['datas'].append(booking_confirmed_value)
                    table_dict['Booking']['total'] += booking_confirmed_value
                else:
                    series[0]['data'].append(0)
                    table_dict['Booking']['datas'].append(0)
                    table_dict['Booking']['total'] += 0
                if show_cancel:
                    series[1]['data'].append(booking_cancelled_value)  # Cancellations
                    table_dict['Cancellation']['datas'].append(booking_cancelled_value)
                    table_dict['Cancellation']['total'] += booking_cancelled_value
                else:
                    series[1]['data'].append(0)  # Cancellations
                    table_dict['Cancellation']['datas'].append(0)
                    table_dict['Cancellation']['total'] += 0
                if show_net:
                    series[2]['data'].append(net_value)  # Net
                    table_dict['Net']['datas'].append(net_value)
                    table_dict['Net']['total'] += net_value
                else:
                    series[2]['data'].append(0)  # Net
                    table_dict['Net']['datas'].append(0)
                    table_dict['Net']['total'] += 0
                if show_reg:
                    series[3]['data'].append(registration_value)  # Registrations
                    table_dict['Registration']['datas'].append(registration_value)
                    table_dict['Registration']['total'] += registration_value
                else:
                    series[3]['data'].append(0)  # Registrations
                    table_dict['Registration']['datas'].append(0)
                    table_dict['Registration']['total'] += 0
                current_date += relativedelta(months=3)
        th_width = 89/extra_th_count
        head_data = '<th width="'+str(th_width)+'%"></th>'
        head_data = head_data * extra_th_count

        t_body = ''
        for tb in table_dict:
            if not show_booking and tb =="Booking":
                continue
            if not show_cancel and tb =="Cancellation":
                continue
            if not show_net and tb =="Net":
                continue
            if not show_reg and tb =="Registration":
                continue

            t_body += '<tr>'
            t_body += '<td>'+tb+'</td>'
            index = 0
            for tb2 in table_dict[tb]['datas']:
                t_body += '<td class="data-table-'+tb+'-td data_column" month="'+ categories[index] +'" type="'+ f'{tb}' +'">'+ f'{tb2:.2f}' +'</td>'
                index += 1
            t_body += '<td class="data-table-'+tb+'-td tot_td data_column" month="'+ financial_year +'" type="'+ f'{tb}' +'">'+f'{table_dict[tb]["total"]:.2f}'+'</td>'
            t_body += '</tr>'



        table_data = '''
         <table class="data-table-brnc" style="width: 100%;">
                        <thead>
                            <th width="6%"></th>
                            '''+head_data+'''
                            <th width="5%"></th>
                        </thead>
                         '''+t_body+'''
                        </table>
        '''
        # print(table_data)
        return [series, categories,table_data]

    @http.route('/jupiter_dashboard_optima/generate_report_optima', auth='user', type='json')
    def generate_report_optima(self, type, month, region_ids=False, project_ids=False):
        print(f"type: {type}, month: {month}")

        # Define the months for each quarter
        quarter_months = {
            'Q1': ('01-04', '30-06'),  # April - June
            'Q2': ('01-07', '30-09'),  # July - September
            'Q3': ('01-10', '31-12'),  # October - December
            'Q4': ('01-01', '31-03')   # January - March
        }

        # Define month mapping to full month names
        month_map = {
            "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
            "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
            "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
        }
        region_ids_value =[]
        if region_ids:
            # for region in region_ids:
            region_ids_value.append((6,0,region_ids))
        project_ids_value =[]
        if project_ids:
            # for region in region_ids:
            project_ids_value.append((6,0,project_ids))
        try:
            # Handle custom date range (e.g., '2024-04-01#2025-03-31')
            if '#' in month:
                date_parts = month.split('#')
                date_from = datetime.strptime(date_parts[0], '%Y-%m-%d')
                date_to = datetime.strptime(date_parts[1], '%Y-%m-%d')

            elif 'Q' in month:
                quarter, year = month.split(' ')
                quarter = quarter.strip()  # Example: 'Q1'
                year = year.strip()  # Example: '2024'

                if quarter not in quarter_months:
                    return {'error': 'Invalid quarter format'}

                start_month, end_month = quarter_months[quarter]

                # Construct the full date range for the quarter
                date_from = datetime.strptime(f'{start_month}-{year}', '%d-%m-%Y')
                date_to = datetime.strptime(f'{end_month}-{year}', '%d-%m-%Y')

            elif ' ' in month and len(month.split(' ')) == 2:  # Handle Monthly selection
                month_parts = month.split(' ')
                abbreviated_month = month_parts[0]
                year = month_parts[1]

                # Get the full month name
                full_month = month_map.get(abbreviated_month)

                # Combine the full month with the year
                full_month_str = f"{full_month} {year}"
                month_obj = datetime.strptime(full_month_str, '%B %Y')
                date_from = month_obj.replace(day=1)  # Start of the month
                date_to = month_obj.replace(
                    day=calendar.monthrange(month_obj.year, month_obj.month)[1]
                )  # End of the month

            elif len(month.split(' ')) == 1 and month.isdigit():  # Handle Yearly selection
                # If 'month' is just a year like "2024"
                year = month.strip()

                # Create a date range from January 1st to December 31st of the year
                date_from = datetime.strptime(f'01-01-{year}', '%d-%m-%Y')
                date_to = datetime.strptime(f'31-12-{year}', '%d-%m-%Y')

            else:
                return {'error': 'Invalid month or quarter format'}

        except Exception as e:
            return {'error': f'Error parsing date range: {str(e)}'}

        # Map report type to backend state
        if type == 'Booking':
            type = 'confirmed'
        elif type == 'Cancellation':
            type = 'canceled'
        elif type == 'Net':
            type = 'both'
        elif type == 'Registration':
            # For 'Registration', we only need to pass the date range, no state field is required
            report_obj = request.env['beta.registration.report']
            create_vals = {
                'date_from': date_from,
                'date_to': date_to,
                'project_ids': project_ids_value
            }
            # if the user passed project_ids, force project_filter to 'selected'
            if project_ids_value:
                create_vals['project_filter'] = 'selected'

            # Create the registration report record
            report = report_obj.create(create_vals)
            report_data = report.get_html()  # Get the report's HTML
            report_id = report.id
            report.report_id = request.env.ref('registration_report.registration_report_reports_pdf_action').id
            print(f"Calculated Date Range: {date_from} to {date_to}")
            # Return the report ID and HTML data for frontend use
            return {
                'report_id': report_id,
                'report_model': 'beta.registration.report'
            }
        else:
            return {'error': 'Invalid report type'}

        # Generate the report based on the type and date range
        report_obj = request.env['beta.booking.report']
        create_vals = {
            'state': type,
            'date_from': date_from,
            'date_to': date_to,
            'region_ids': region_ids_value,
            'project_ids': project_ids_value,
            'region_wise': True
        }
        # if the user passed project_ids, force project_filter to 'selected'
        if project_ids_value:
            create_vals['project_filter'] = 'selected'

        # Create the report record
        report = report_obj.create(create_vals)
        report.get_html()  # Get the report's HTML
        report_id = report.id

        # Return the report ID and HTML data for frontend use
        return {
            'report_id': report_id,
            'report_model': 'beta.booking.report'
        }

    @http.route('/jupiter_dashboard_optima/cp_booked_count', auth='public', type='json')
    def jupiter_dashboard_tres_cp_booked_count(self):
        current_datetime = datetime.today()
        start_of_today = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_of_today + timedelta(days=1) - timedelta(microseconds=1)
        start_formatted = self.get_actual_date(start_of_today.strftime('%Y-%m-%d 00:00:00'))
        end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d 23:59:59'))
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week_formatted = self.get_actual_date(start_of_week.strftime('%Y-%m-%d 00:00:00'))
        start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_month_formatted = self.get_actual_date(start_of_month.strftime('%Y-%m-%d 00:00:00'))
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
        half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
        half_start = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)

        start_of_quarter_formatted = self.get_actual_date(quarter_start.strftime('%Y-%m-%d 00:00:00'))
        start_of_half_formatted = self.get_actual_date(half_start.strftime('%Y-%m-%d 00:00:00'))
        booking_region_filter = []
        quarter_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_quarter_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        half_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_half_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        year_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', fin_year_end_formatted), ('date', '>=', fin_year_start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        today_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        this_week_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_week_formatted),
             ('date', '>=', start_of_month_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        this_month_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)

        return {
            'today_booking_cp_count': len(today_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'week_booking_cp_count': len(this_week_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'month_booking_cp_count': len(this_month_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'year_booking_cp_count': len(year_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'quarter_booking_cp_count': len(quarter_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'half_booking_cp_count': len(half_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
        }

    @http.route('/jupiter_dashboard_optima/bookings_registrations', auth='public', type='json')
    def jupiter_dashboard_tres_bookings_registrations(self, region=False, cluster=False, project=False):
        currency = request.env.company.currency_id.symbol
        current_datetime = datetime.today()
        # start_of_today = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_today = current_datetime.date()
        end_of_today = start_of_today + timedelta(days=1) - timedelta(microseconds=1)
        # start_formatted = self.get_actual_date(start_of_today.strftime('%Y-%m-%d 00:00:00'))
        start_formatted = start_of_today.strftime('%Y-%m-%d 00:00:00')
        # end_formatted = self.get_actual_date(end_of_today.strftime('%Y-%m-%d 23:59:59'))
        end_formatted = end_of_today.strftime('%Y-%m-%d 23:59:59')
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
        # start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = start_of_week.date()
        # start_of_week_formatted = self.get_actual_date(start_of_week.strftime('%Y-%m-%d 00:00:00'))
        start_of_week_formatted = start_of_week.strftime('%Y-%m-%d 00:00:00')
        start_of_month = current_datetime.replace(day=1).date()
        # start_of_month_formatted = self.get_actual_date(start_of_month.strftime('%Y-%m-%d 00:00:00'))
        start_of_month_formatted = start_of_month.strftime('%Y-%m-%d 00:00:00')
        fin_year_obj = (
            date(date.today().year, 4, 1) if date.today().month >= 4 else date(date.today().year - 1, 4, 1))
        fin_year_start = fin_year_obj.strftime('%Y-%m-%d')
        fin_year_end = date.today().strftime('%Y-%m-%d')
        # fin_year_start_formatted = self.get_actual_date(fin_year_start + ' 00:00:00')
        fin_year_start_formatted = fin_year_start + ' 00:00:00'
        # fin_year_end_formatted = self.get_actual_date(fin_year_end + ' 23:59:59')
        fin_year_end_formatted = fin_year_end + ' 23:59:59'

        financial_year_start_month = 4
        quarter_month_starts = [4, 7, 10, 1]
        half_year_starts = [4, 10]

        year_offset = 0 if current_datetime.month >= financial_year_start_month else -1
        quarter_index = (current_datetime.month - financial_year_start_month) // 3 % 4
        quarter_start = datetime(current_datetime.year + year_offset, quarter_month_starts[quarter_index], 1)
        next_quarter_index = (quarter_index + 1) % 4
        quarter_end = datetime(current_datetime.year + year_offset, quarter_month_starts[next_quarter_index],
                               1) - timedelta(days=1)

        # Adjust the year for the quarter end correctly
        if next_quarter_index == 0:  # If the next quarter is April (the first month of the financial year)
            quarter_end = datetime(current_datetime.year + year_offset + 1, quarter_month_starts[next_quarter_index],
                                   1) - timedelta(days=1)
        if quarter_month_starts[next_quarter_index] == 1:  # If the next quarter is January
            quarter_end = datetime(current_datetime.year + year_offset + 1, quarter_month_starts[next_quarter_index],
                                   1) - timedelta(days=1)
        half_year_index = (current_datetime.month - financial_year_start_month) // 6 % 2
        half_start = datetime(current_datetime.year + year_offset, half_year_starts[half_year_index], 1)
        if current_datetime.month >= half_year_starts[half_year_index]:
            half_end = datetime(current_datetime.year + year_offset + 1, half_year_starts[(half_year_index + 1) % 2],
                                1) - timedelta(days=1)
        else:
            half_end = datetime(current_datetime.year + year_offset, half_year_starts[(half_year_index + 1) % 2],
                                1) - timedelta(days=1)

        # start_of_quarter_formatted = self.get_actual_date(quarter_start.strftime('%Y-%m-%d 00:00:00'))
        start_of_quarter_formatted = quarter_start.strftime('%Y-%m-%d 00:00:00')
        # start_of_half_formatted = self.get_actual_date(half_start.strftime('%Y-%m-%d 00:00:00'))
        start_of_half_formatted = half_start.strftime('%Y-%m-%d 00:00:00')
        booking_region_filter = []
        registration_region_filter = []
        if region:
            booking_region_filter = [('building.region_id', 'in', region)]
            registration_region_filter = [('project_id.region_id', 'in', region)]
        if cluster:
            booking_region_filter = [('building.sub_region_id', 'in', cluster)]
            registration_region_filter = [('project_id.sub_region_id', 'in', cluster)]
        if project:
            booking_region_filter = [('building', 'in', project)]
            registration_region_filter = [('project_id', 'in', project)]
        quarter_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_quarter_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        quarter_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_formatted), ('cancellation_date', '>=', quarter_start),
             ('state', '=', 'canceled')] + booking_region_filter)
        quarter_registration = request.env['project.registration'].search(
            [('registration_date', '<=', current_datetime), ('registration_date', '>=', quarter_start),
             ('state', '=', 'confirmed')] + registration_region_filter)

        quarter_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', quarter_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        quarter_registration_value = sum(quarter_booking_of_registrations.mapped('flat_cost')) / 100000
        quarter_booking_value = sum(quarter_booking_confirmed.mapped('flat_cost')) / 100000

        half_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_half_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        half_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', half_start),
             ('state', '=', 'canceled')] + booking_region_filter)
        half_registration = request.env['project.registration'].search(
            [('registration_date', '<=', current_datetime), ('registration_date', '>=', half_start),
             ('state', '=', 'confirmed')] + registration_region_filter)

        half_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', half_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        half_registration_value = sum(half_booking_of_registrations.mapped('flat_cost')) / 100000
        half_booking_value = sum(half_booking_confirmed.mapped('flat_cost')) / 100000

        year_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', fin_year_end_formatted), ('date', '>=', fin_year_start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        year_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', fin_year_end), ('cancellation_date', '>=', fin_year_start),
             ('state', '=', 'canceled')] + booking_region_filter)
        year_registration = request.env['project.registration'].search(
            [('registration_date', '<=', fin_year_end), ('registration_date', '>=', fin_year_start),
             ('state', '=', 'confirmed')] + registration_region_filter)

        year_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', year_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        year_registration_value = sum(year_booking_of_registrations.mapped('flat_cost')) / 100000
        year_booking_value = sum(year_booking_confirmed.mapped('flat_cost')) / 100000

        today_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        today_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', end_of_today),
             ('state', '=', 'canceled')] + booking_region_filter)

        this_week_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_week_formatted),
             ('date', '>=', start_of_month_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        this_week_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', start_of_week),
             ('cancellation_date', '>=', start_of_month), ('state', '=', 'canceled')] + booking_region_filter)

        this_month_booking_confirmed = request.env['unit.reservation'].search(
            [('date', '<=', end_formatted), ('date', '>=', start_of_month_formatted),
             ('state', 'in', ('confirmed', 'canceled'))] + booking_region_filter)
        this_month_booking_cancelled = request.env['unit.reservation'].search(
            [('cancellation_date', '<=', end_of_today), ('cancellation_date', '>=', start_of_month),
             ('state', '=', 'canceled')] + booking_region_filter)

        today_registration = request.env['project.registration'].search(
            [('registration_date', '=', current_datetime.date()),
             ('state', '=', 'confirmed')] + registration_region_filter)
        today_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', today_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        today_registration_value = sum(today_booking_of_registrations.mapped('flat_cost')) / 100000
        today_booking_value = sum(today_booking_confirmed.mapped('flat_cost')) / 100000

        this_week_registration = request.env['project.registration'].search(
            [('registration_date', '<=', end_of_today), ('registration_date', '>=', start_of_week),
             ('state', '=', 'confirmed')] + registration_region_filter)
        this_week_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', this_week_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        this_week_registration_value = sum(this_week_booking_of_registrations.mapped('flat_cost')) / 100000
        this_week_booking_value = sum(this_week_booking_confirmed.mapped('flat_cost')) / 100000

        this_month_registration = request.env['project.registration'].search(
            [('registration_date', '<=', end_of_today), ('registration_date', '>=', start_of_month),
             ('state', '=', 'confirmed')] + registration_region_filter)
        this_month_booking_of_registrations = request.env['unit.reservation'].search(
            [('building_unit', 'in', this_month_registration.mapped('flat_id').ids),
             ('state', '=', 'confirmed')] + booking_region_filter)
        this_month_registration_value = sum(this_month_booking_of_registrations.mapped('flat_cost')) / 100000
        this_month_booking_value = sum(this_month_booking_confirmed.mapped('flat_cost')) / 100000

        today_booking_cancelled_value = sum(today_booking_cancelled.mapped('flat_cost')) / 100000
        week_booking_cancelled_value = sum(this_week_booking_cancelled.mapped('flat_cost')) / 100000
        month_booking_cancelled_value = sum(this_month_booking_cancelled.mapped('flat_cost')) / 100000
        year_booking_cancelled_value = sum(year_booking_cancelled.mapped('flat_cost')) / 100000
        quarter_booking_cancelled_value = sum(quarter_booking_cancelled.mapped('flat_cost')) / 100000
        half_booking_cancelled_value = sum(half_booking_cancelled.mapped('flat_cost')) / 100000

        today_booking_attrs = {
            "date_from": current_datetime.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        week_booking_attrs = {
            "date_from": start_of_week.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        month_booking_attrs = {
            "date_from": start_of_month.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        year_booking_attrs = {
            "date_from": fin_year_start,
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        quarter_booking_attrs = {
            "date_from": quarter_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
            'consolidate': 'False',
            'project_filter': 'all'
        }
        half_booking_attrs = {
            "date_from": half_start.strftime('%Y-%m-%d'),
            "date_to": current_datetime.strftime('%Y-%m-%d'),
            "state": 'both',
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
            ('date', '>=', start_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        week_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_week_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        month_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_month_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        quarter_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_quarter_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        half_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', start_of_half_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        year_booking_cp_domain = [
            ('source_of_booking', '=', 'cp'), ('date', '<=', end_formatted),
            ('date', '>=', fin_year_start_formatted), ('state', 'in', ('confirmed', 'canceled'))
        ]
        return {

            'today_booking_gross_count': len(today_booking_confirmed),
            'week_booking_gross_count': len(this_week_booking_confirmed),
            'month_booking_gross_count': len(this_month_booking_confirmed),
            'year_booking_gross_count': len(year_booking_confirmed),
            'quarter_booking_gross_count': len(quarter_booking_confirmed),
            'half_booking_gross_count': len(half_booking_confirmed),

            'today_booking_gross_value': currency + "{:,.2f}".format(today_booking_value),
            'week_booking_gross_value': currency + "{:,.2f}".format(this_week_booking_value),
            'month_booking_gross_value': currency + "{:,.2f}".format(this_month_booking_value),
            'year_booking_gross_value': currency + "{:,.2f}".format(year_booking_value),
            'quarter_booking_gross_value': currency + "{:,.2f}".format(quarter_booking_value),
            'half_booking_gross_value': currency + "{:,.2f}".format(half_booking_value),

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

            'today_booking_cancelled_count': len(today_booking_cancelled),
            'week_booking_cancelled_count': len(this_week_booking_cancelled),
            'month_booking_cancelled_count': len(this_month_booking_cancelled),
            'year_booking_cancelled_count': len(year_booking_cancelled),
            'quarter_booking_cancelled_count': len(quarter_booking_cancelled),
            'half_booking_cancelled_count': len(half_booking_cancelled),

            'today_booking_cancelled_value': currency + "{:,.2f}".format(today_booking_cancelled_value),
            'week_booking_cancelled_value': currency + "{:,.2f}".format(week_booking_cancelled_value),
            'month_booking_cancelled_value': currency + "{:,.2f}".format(month_booking_cancelled_value),
            'year_booking_cancelled_value': currency + "{:,.2f}".format(year_booking_cancelled_value),
            'quarter_booking_cancelled_value': currency + "{:,.2f}".format(quarter_booking_cancelled_value),
            'half_booking_cancelled_value': currency + "{:,.2f}".format(half_booking_cancelled_value),

            'today_booking_count': len(today_booking_confirmed) - len(today_booking_cancelled),
            'week_booking_count': len(this_week_booking_confirmed) - len(this_week_booking_cancelled),
            'month_booking_count': len(this_month_booking_confirmed) - len(this_month_booking_cancelled),
            'year_booking_count': len(year_booking_confirmed) - len(year_booking_cancelled),
            'quarter_booking_count': len(quarter_booking_confirmed) - len(quarter_booking_cancelled),
            'half_booking_count': len(half_booking_confirmed) - len(half_booking_cancelled),

            'today_booking_value': currency + "{:,.2f}".format(today_booking_value - today_booking_cancelled_value),
            'week_booking_value': currency + "{:,.2f}".format(this_week_booking_value - week_booking_cancelled_value),
            'month_booking_value': currency + "{:,.2f}".format(
                this_month_booking_value - month_booking_cancelled_value),
            'year_booking_value': currency + "{:,.2f}".format(year_booking_value - year_booking_cancelled_value),
            'quarter_booking_value': currency + "{:,.2f}".format(
                quarter_booking_value - quarter_booking_cancelled_value),
            'half_booking_value': currency + "{:,.2f}".format(half_booking_value - half_booking_cancelled_value),

            'quarter_label': quarter_start.strftime('%b %y') + '-' + quarter_end.strftime('%b %y'),
            'half_label': half_start.strftime('%b %y') + '-' + half_end.strftime('%b %y'),
            'year_label': fin_year_obj.strftime('%Y') + '-' + str(int(fin_year_obj.strftime('%Y')) + 1),

            'today_booking_cp_count': len(today_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'week_booking_cp_count': len(this_week_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'month_booking_cp_count': len(this_month_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'year_booking_cp_count': len(year_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'quarter_booking_cp_count': len(quarter_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),
            'half_booking_cp_count': len(half_booking_confirmed.filtered(lambda x: x.source_of_booking == 'cp')),

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

            'today_booking_cp_domain': str(today_booking_cp_domain),
            'week_booking_cp_domain': str(week_booking_cp_domain),
            'month_booking_cp_domain': str(month_booking_cp_domain),
            'quarter_booking_cp_domain': str(quarter_booking_cp_domain),
            'half_booking_cp_domain': str(half_booking_cp_domain),
            'year_booking_cp_domain': str(year_booking_cp_domain),
        }
