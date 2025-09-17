import calendar
from datetime import datetime, timedelta, date
from pytz import timezone
from odoo.http import request
from odoo import http, fields
import logging

_logger = logging.getLogger(__name__)


class RealEstate(http.Controller):

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(request.env.user.tz or 'Asia/Kolkata'))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)
    def add_api_log(self, record, code, response, api_type, status, name, direction, args):
        try:
            request.env['api.log'].sudo().create({
                'record': str(record),
                'code': code,
                'response': response,
                'date': datetime.now(),
                'type': api_type,
                'status': status,
                'name': name,
                'direction': direction,
                'args': str(args)
            })
        except Exception as e:
            _logger.warning(str(e))

    # Api for fetching project details
    # create api key with scope project
    @http.route(['/project/fetch_record_details'], type='json', auth='public', methods=['POST'])
    def project_fetch_record_details(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='project', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'project',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'project',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            try:
                cr = request.env.cr
                query = """
                    SELECT b.name AS "Project Name", 
                        COALESCE(b.code, '') AS "Project Code", 
                        COALESCE(TO_CHAR(b.purchase_date, 'YYYY-MM-DD'), '') AS "Starting Date",
                        COALESCE(TO_CHAR(b.launch_date, 'YYYY-MM-DD'), '') AS "End Date",
                        COALESCE(bt.name, '') AS "Property Type", 
                        COALESCE(b.license_code, '') AS "RERA No.",
                        COALESCE(rcs.name, '') AS "State", 
                        COALESCE(r.name, '') AS "Region",
                        COALESCE(c.name, '') AS "Cluster",
                        COALESCE(CAST(b.residential_saleable_area AS numeric(10, 2)), 0) AS "Residential Saleable Area",
                        COALESCE(CAST(b.commercial_saleable_area AS numeric(10, 2)), 0) AS "Commercial Saleable Area",
                        COALESCE(CAST(b.garden AS numeric(10, 2)), 0) AS "Garden Sq.Ft",
                        COALESCE(b.address, '') AS "Address",
                        COALESCE(STRING_AGG(DISTINCT cm_emp.id::text, ','), '') "CM",
                        COALESCE(STRING_AGG(DISTINCT sm_emp.id::text, ','), '') "SM",
                        COALESCE(STRING_AGG(DISTINCT ctl_emp.id::text, ','), '') "CTL",
                        COALESCE(STRING_AGG(DISTINCT stl_emp.id::text, ','), '') "STL",
                        COALESCE(STRING_AGG(DISTINCT crm_emp.id::text, ','), '') "CRM",
                        COALESCE(STRING_AGG(DISTINCT mk_emp.id::text, ','), '') "Marketing",
                        COALESCE(STRING_AGG(DISTINCT pbu.name::text, ','), '') "Configuration",
                        COALESCE(bh_emp.id::text, '') AS "Business Head", 
                        COALESCE(ch_emp.id::text, '') AS "Cluster Head",
                        COALESCE(sh_emp.id::text, '') AS "Site Head"
                    FROM building b
                    LEFT JOIN building_type bt ON bt.id = b.type
                    LEFT JOIN res_country_state rcs ON rcs.id = b.state_id
                    LEFT JOIN regions r ON r.id = b.region_id
                    LEFT JOIN regions c ON c.id = b.sub_region_id
                    LEFT JOIN project_closing_manager_rel cm_rel ON cm_rel.project_id = b.id
                    LEFT JOIN hr_employee cm_emp ON cm_emp.id = cm_rel.employee_id
                    LEFT JOIN project_sourcing_manager_rel sm_rel ON sm_rel.project_id = b.id
                    LEFT JOIN hr_employee sm_emp ON sm_emp.id = sm_rel.employee_id
                    LEFT JOIN project_closing_tl_rel ctl_rel ON ctl_rel.project_id = b.id
                    LEFT JOIN hr_employee ctl_emp ON ctl_emp.id = ctl_rel.employee_id
                    LEFT JOIN project_sourcing_tl_rel stl_rel ON stl_rel.project_id = b.id
                    LEFT JOIN hr_employee stl_emp ON stl_emp.id = stl_rel.employee_id
                    LEFT JOIN project_crm_rel crm_rel ON crm_rel.project_id = b.id
                    LEFT JOIN hr_employee crm_emp ON crm_emp.id = crm_rel.employee_id
                    LEFT JOIN project_marketing_rel mk_rel ON mk_rel.project_id = b.id
                    LEFT JOIN hr_employee mk_emp ON mk_emp.id = mk_rel.employee_id
                    LEFT JOIN project_building_unit_rel pbu_rel ON pbu_rel.project_id = b.id
                    LEFT JOIN building_unit pbu ON pbu.id = pbu_rel.config_id
                    LEFT JOIN hr_employee bh_emp ON bh_emp.id = b.business_head_id
                    LEFT JOIN hr_employee ch_emp ON ch_emp.id = b.cluster_head_id
                    LEFT JOIN hr_employee sh_emp ON sh_emp.id = b.site_head_id
                    WHERE b.active = True
                    GROUP BY b.name, b.code ,b.purchase_date, b.launch_date, b.license_code, 
                        r.name, bt.name, rcs.name, c.name,b.address, b.residential_saleable_area,
                        b.commercial_saleable_area, b.garden, bh_emp.name, ch_emp.name, 
                        bh_emp.id, ch_emp.id, sh_emp.id
                """
                cr.execute(query)
                data = cr.dictfetchall()
                response = {
                    'data': data,
                    'status': 'Success',
                    'code': 200
                }
                self.add_api_log('', 200, str(response), 'project', 'success', '', 'in',
                                 kwargs)
                return response
            except:
                self.add_api_log('', 201, str(failed_response), 'project',
                                 'failed', '', 'in', kwargs)
                return failed_response

    # Api for fetching flat details
    # create api key with scope inventory
    @http.route(['/inventory/fetch_record_details'], type='json', auth='public', methods=['POST'])
    def fetch_record_details(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='inventory', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'inventory',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'inventory',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            if kwargs.get('project'):
                cr = request.env.cr
                if kwargs.get('type') == '':
                    type_filter = ""
                elif kwargs.get('type'):
                    type_filter = " and bu.name='" + kwargs.get('type').replace("'", "''") + "'"
                else:
                    self.add_api_log('', 201, str(failed_response), 'inventory',
                                     'failed', '', 'in', kwargs)
                    return failed_response
                query = """
                           SELECT b.name as "Project Name", pt.name as "Flat Name", bu.name as "Flat Type", 
                           CAST(pt.saleable_area AS numeric(10, 2)) as "Saleable Area",
                           CAST(pt.carpet AS numeric(10, 2)) as "Carpet Area", pt.floor as "Floor", pt.id, pt.flat_state
                           FROM product_template pt
                           left join building b on b.id=pt.building_id
                           left join building_unit bu on bu.id=pt.flat_type
                           where pt.is_property=True and state='free' and pt.on_hold is not True
                           and b.code='""" + kwargs.get('project').replace("'", "''") + """'
                           """ + type_filter + """
                       """
                cr.execute(query)
                final = []
                data = cr.dictfetchall()
                booking_draft_checking_hours = request.env['ir.config_parameter'].sudo().get_param(
                    'itsys_real_estate.booking_draft_checking_hours')
                if booking_draft_checking_hours:
                    booking_draft_checking_hours = int(booking_draft_checking_hours)
                for item in data:
                    item_data = {
                        'Project Name': item['Project Name'],
                        'Flat Name': item['Flat Name'],
                        'Flat Type': item['Flat Type'],
                        'Saleable Area': item['Saleable Area'],
                        'Carpet Area': item['Carpet Area'],
                        'Floor': item['Floor'],
                        'Status': item['flat_state'].upper() if item['flat_state'] else ''
                    }
                    if booking_draft_checking_hours:
                        prev_booking = request.env['unit.reservation'].sudo().search(
                            [('building_unit', '=', item['id']), ('state', '=', 'draft')],
                            order='date desc', limit=1)
                        if prev_booking:
                            difference = datetime.now() - prev_booking.date
                            hours_difference = difference.total_seconds() / 3600
                            if booking_draft_checking_hours > hours_difference:
                                continue
                    final.append(item_data)
                response = {
                    'data': final,
                    'status': 'Success',
                    'code': 200
                }
                self.add_api_log('', 200, str(response), 'inventory',
                             'success', kwargs.get('project'), 'in', kwargs)
                return response
            else:
                self.add_api_log('', 201, str(failed_response), 'inventory',
                                 'failed', '', 'in', kwargs)
                return failed_response

    @http.route(['/booking_cancel_count/fetch_record_details'], type='json', auth='public', methods=['POST'])
    def booking_cancel_fetch_record_details(self, **kwargs):
        """     Return bookings and cancellations counts by date, month, and financial year.
                If a project_id is provided, return single summary; otherwise, return per-project breakdown.    """
        failed = {'data': 'Access Denied', 'status': 'Failed', 'code': 201}

        # 1) Authenticate
        user_id = request.env['res.users.apikeys']._check_credentials(
            scope='booking_cancel', key=kwargs.get('password'))
        if not user_id or request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed), 'booking_cancel', 'failed', '', 'in', kwargs)
            return failed

        # 2) Parse and validate date
        ondate_str = kwargs.get('date')
        if not ondate_str:
            return {'status': 'Failed', 'code': 400, 'message': 'Error: Received an Invalid Date.'}
        try:
            ondate = fields.Date.from_string(ondate_str)
        except Exception:
            return {'status': 'Failed', 'code': 400, 'message': 'Invalid date format, expected YYYY-MM-DD'}

        project_code = kwargs.get('project_code') or None
        from_date = ondate_str + ' 00:00:00'
        to_date = ondate_str + ' 23:59:59'
        converted_from_date = self.get_actual_date(from_date)
        converted_to_date = self.get_actual_date(to_date)

        # Helper to compute counts for a given domain
        def _count(domain, domain2):
            Book = request.env['unit.reservation'].sudo()
            total = Book.search_count(domain + [('state', 'in', ['confirmed', 'canceled'])])
            canc = Book.search_count(domain2 + [('state', '=', 'canceled')])
            return total, canc

        # 4) Build date, month, and FY domains
        date_dom_booking = [('date', '>=', converted_from_date), ('date', '<=', converted_to_date)]
        date_dom_cancel = [('cancellation_date', '>=', from_date), ('cancellation_date', '<=', to_date)]

        local_date = datetime.strptime(ondate_str, "%Y-%m-%d").date()
        year, month = local_date.year, local_date.month

        # 2) Compute first & last day of that month
        first_day = local_date.replace(day=1)
        last_day_num = calendar.monthrange(year, month)[1]
        last_day = local_date.replace(day=last_day_num)

        # 3) Build your local-time boundary strings
        start_of_month_str = first_day.strftime("%Y-%m-%d") + " 00:00:00"
        end_of_month_str = last_day.strftime("%Y-%m-%d") + " 23:59:59"

        # 4) Convert both back to UTC via your helper
        start_of_month_formatted = self.get_actual_date(start_of_month_str)
        end_of_month_formatted = self.get_actual_date(end_of_month_str)

        month_dom_booking = [('date', '>=', start_of_month_formatted), ('date', '<=', end_of_month_formatted)]
        month_dom_cancel = [('cancellation_date', '>=', first_day), ('cancellation_date', '<=', last_day)]

        fy_year = local_date.year if local_date.month >= 4 else local_date.year - 1
        fy_start_date = date(fy_year, 4, 1)  # Apr 1 of fy_year
        fy_end_date = date(fy_year + 1, 3, 31)  # Mar 31 of the next year

        # 4) Build your local‐time boundary strings
        start_of_fy_str = fy_start_date.strftime("%Y-%m-%d") + " 00:00:00"
        end_of_fy_str = fy_end_date.strftime("%Y-%m-%d") + " 23:59:59"

        # 5) Convert these back to UTC via your helper
        start_of_fy_formatted = self.get_actual_date(start_of_fy_str)
        end_of_fy_formatted = self.get_actual_date(end_of_fy_str)

        fy_dom_booking = [('date', '>=', start_of_fy_formatted), ('date', '<=', end_of_fy_formatted)]
        fy_dom_can = [('cancellation_date', '>=', fy_start_date), ('cancellation_date', '<=', fy_end_date)]

        if project_code:
            # Single project summary
            date_tot, date_can = _count(date_dom_booking + [('building.code', '=', project_code)], date_dom_cancel + [('building.code', '=', project_code)])
            month_tot, month_can = _count(month_dom_booking + [('building.code', '=', project_code)], month_dom_cancel + [('building.code', '=', project_code)])
            fy_tot, fy_can = _count(fy_dom_booking + [('building.code', '=', project_code)], fy_dom_can + [('building.code', '=', project_code)])

            data = {"projects": [{
                'project_code': project_code,
                'date': {'bookings': date_tot, 'cancellations': date_can},
                'month': {'bookings': month_tot, 'cancellations': month_can},
                'financial_year': {'bookings': fy_tot, 'cancellations': fy_can},
            }]}
            response = {'status': 'Success', 'code': 200, 'data': data}
        else:
            # Overall totals (all projects)
            total_date, total_date_can = _count(date_dom_booking, date_dom_cancel)
            total_month, total_month_can = _count(month_dom_booking, month_dom_cancel)
            total_fy, total_fy_can = _count(fy_dom_booking, fy_dom_can)

            # Breakdown by project
            project_codes = request.env['unit.reservation'].sudo().search([]).mapped('building.code')
            results = []

            for code in set(project_codes):
                d_tot, d_can = _count(date_dom_booking + [('building.code', '=', code)], date_dom_cancel + [('building.code', '=', code)])
                m_tot, m_can = _count(month_dom_booking + [('building.code', '=', code)], month_dom_cancel + [('building.code', '=', code)])
                f_tot, f_can = _count(fy_dom_booking + [('building.code', '=', code)], fy_dom_can + [('building.code', '=', code)])
                results.append({
                    'project_code': code,
                    'date': {'bookings': d_tot, 'cancellations': d_can},
                    'month': {'bookings': m_tot, 'cancellations': m_can},
                    'financial_year': {'bookings': f_tot, 'cancellations': f_can},
                })

            data = {
                'total': {
                    'date': {'bookings': total_date, 'cancellations': total_date_can},
                    'month': {'bookings': total_month, 'cancellations': total_month_can},
                    'financial_year': {'bookings': total_fy, 'cancellations': total_fy_can},
                },
                'projects': results
            }
            response = {'status': 'Success', 'code': 200, 'data': data}

        # 5) Log and return
        self.add_api_log('', response['code'], str(response), 'booking_stats', 'success', project_code or '', 'in',
                         kwargs)
        return response


    @http.route('/get_attachment_file_url', type='json', auth="none")
    def get_attachment_file_url(self, line_id=None, model=False, **kw):
        if line_id and model:
            attachment_line = request.env[model].browse(int(line_id))
            request.env.cr.execute(
                "select id from ir_attachment where res_model='" + str(attachment_line._name) + "' and res_id=" + str(
                    attachment_line.id))
            attachment_id = request.env.cr.fetchone()[0] or None
            if attachment_id:
                attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
                if attachment.index_content == 'image':
                    img = """<img id="attachment_img_file_toggle" src='/web/image/""" + str(attachment.id) + """'>"""
                    return img
