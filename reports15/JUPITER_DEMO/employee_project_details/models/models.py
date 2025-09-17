# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime, timedelta
import calendar


class BetaEmployeeProjectDetails(models.TransientModel):  # change this
    _name = 'beta.employee.project.details'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Employee Project Details')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    type = fields.Selection([('month', 'Month Wise'), ('year', 'Year Wise')], default='month')
    year_from = fields.Selection(selection=lambda self: self.get_years())
    year_to = fields.Selection(selection=lambda self: self.get_years())

    def get_years(self):
        sequence = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).sequence_id
        values = []
        for line in sequence.date_range_ids:
            values.append((str(line.date_from.year), str(line.date_from.year)))
        return values

    @api.model
    def default_get(self, fields_list):
        res = super(BetaEmployeeProjectDetails, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('employee_project_details.employee_project_details_report')._render({
            'doc': doc,
            'date_start': self.date_from,
            'date_end': self.date_to
        })

    def _get_report_data(self):
        date_from = self.date_from
        date_to = self.date_to
        if self.type == 'year':
            date_from = datetime.strptime(self.year_from + '-01-01', '%Y-%m-%d')
            date_to = datetime.strptime(self.year_to + '-12-31', '%Y-%m-%d')
        assigning = self.env['project.employee.assigning'].search([('date', '<=', date_to), ('date', '>=', date_from), ('state', '=', 'assigned')])
        employees = assigning.closing_manager_ids.mapped('employee_id') + \
                    assigning.sourcing_manager_ids.mapped('employee_id') + \
                    assigning.closing_tl_ids.mapped('employee_id') + \
                    assigning.sourcing_tl_ids.mapped('employee_id') + \
                    assigning.crm_ids.mapped('employee_id') + \
                    assigning.marketing_ids.mapped('employee_id') + \
                    assigning.business_head_id + assigning.site_head_id + assigning.cluster_head_id
        data = {}
        date_ranges = []
        if self.type == 'month':
            current_date = date_from
            while current_date <= date_to:
                last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
                if current_date == date_from:
                    month_start = current_date.strftime('%Y-%m-%d')
                else:
                    month_start = current_date.replace(day=1).strftime('%Y-%m-%d')
                if current_date.year == date_to.year and current_date.month == date_to.month:
                    month_end = date_to.strftime('%Y-%m-%d')
                else:
                    month_end = current_date.replace(day=last_day_of_month).strftime('%Y-%m-%d')
                    if month_end > date_to.strftime('%Y-%m-%d'):
                        month_end = date_to.strftime('%Y-%m-%d')
                month_name = current_date.strftime('%B-%Y')
                date_ranges.append((month_start, month_end, month_name))
                current_date = current_date.replace(day=1) + timedelta(days=32)
                current_date = current_date.replace(day=1)
        else:
            for i in range(int(self.year_from), int(self.year_to) + 1):
                date_ranges.append(((str(i) + '-01-01'), (str(i) + '-12-31'), str(i)))
        for employee in employees:
            data[employee.id] = {'name': employee.name, 'project': {}}
            for interval in date_ranges:
                qry = f"""
                    SELECT 
                        a.project_id, 
                        b.name 
                    FROM 
                        project_employee_assigning_line al 
                    LEFT JOIN project_employee_assigning a 
                        ON a.id = al.cm_parent_id 
                        OR a.id = al.sm_parent_id 
                        OR a.id = al.ctl_parent_id 
                        OR a.id = al.stl_parent_id 
                        OR a.id = al.crm_parent_id 
                        OR a.id = al.mkg_parent_id
                    LEFT JOIN building b 
                        ON b.id = a.project_id
                    WHERE 
                        al.employee_id = {employee.id} 
                        AND a.date <= '{interval[1]}' 
                        AND a.date >= '{interval[0]}'
                        AND a.state = 'assigned'
                    GROUP BY 
                        a.id, 
                        b.id
                    
                    UNION ALL
                    
                    SELECT 
                        b.id, 
                        b.name 
                    FROM 
                        project_employee_assigning a 
                    LEFT JOIN building b 
                        ON b.id = a.project_id
                    WHERE 
                        (a.business_head_id = {employee.id} 
                        OR a.site_head_id = {employee.id}
                        OR a.cluster_head_id = {employee.id})
                        AND a.date <= '{interval[1]}' 
                        AND a.date >= '{interval[0]}'
                        AND a.state = 'assigned'
                    GROUP BY 
                        b.id
                """
                self.env.cr.execute(qry)
                data[employee.id]['project'][interval] = ''
                comma = ''
                for line in self.env.cr.dictfetchall():
                    data[employee.id]['project'][interval] += comma + line['name']
                    comma = ', '
            booking_qry = f"""
                SELECT 
                    COALESCE(SUM(ur.flat_cost), 0) AS amount, 
                    COALESCE(SUM(CASE WHEN ur.state = 'canceled' THEN ur.flat_cost ELSE 0 END), 0) AS cancelled_amount,
                    COALESCE(SUM(CASE WHEN ur.state = 'confirmed' THEN ur.flat_cost ELSE 0 END), 0) AS confirmed_amount
                FROM 
                    unit_reservation ur 
                WHERE
                    ur.closing_manager_id = {employee.id} 
                    OR ur.sourcing_manager_id = {employee.id} 
                    OR sourcing_tl_id = {employee.id}
                    OR ur.closing_tl_id = {employee.id} 
                    OR crm_id = {employee.id} 
                    OR marketing_id = {employee.id} 
                    AND ur.state != 'draft'
                """
            self.env.cr.execute(booking_qry)
            values = self.env.cr.fetchone()
            data[employee.id]['active'] = values[0]
            data[employee.id]['cancelled'] = values[1]
            data[employee.id]['net'] = values[2]
        return {'data': data, 'date_ranges': date_ranges}
