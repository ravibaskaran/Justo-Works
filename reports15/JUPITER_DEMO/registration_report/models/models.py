# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaRegistrationReport(models.TransientModel):  # change this
    _name = 'beta.registration.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Registration Report')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    project_ids = fields.Many2many('building')
    line_wise = fields.Boolean(string="Line wise", default=False)
    project_filter = fields.Selection([('all', 'All Projects'), ('selected', 'Selected Project')], default='all')

    @api.model
    def default_get(self, fields_list):
        res = super(BetaRegistrationReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def get_html(self):
        data = self._get_report_data()
        self.template_area = self.env.ref('registration_report.report_registration_report')._render({
            'data': data,
            'date_start': self.date_from,
            'date_end': self.date_to,
            'line_wise': self.line_wise
        })

    def _get_report_data(self):
        from_clause = """
            FROM project_registration pr
            LEFT JOIN product_template pt ON pt.id = pr.flat_id
            LEFT JOIN unit_reservation ur ON ur.building_unit = pt.id AND ur.state = 'confirmed'
            LEFT JOIN res_partner rp ON rp.id = pr.customer_id
            LEFT JOIN building b ON b.id = pr.project_id
            WHERE pr.state = 'confirmed' and pr.registration_date >= '%s' and pr.registration_date <= '%s'
        """ % (self.date_from.strftime('%Y-%m-%d'), self.date_to.strftime('%Y-%m-%d'))
        if self.project_filter == 'selected':
            from_clause += " and b.id in " + str(tuple(self.project_ids.ids) or '(0)').replace(',)', ')')
        qry = """
            WITH grand_total AS (
                SELECT 0 as project_id, 'Grand Total' as customer, null as project_name, null as registration, null as inventory, max(pr.registration_date) as registration_date, 
                    max(ur.date) as booking_date, sum(ur.flat_cost) as agreement_value, 4000 as sequence
                    %s
            )
            SELECT * FROM (
                SELECT pr.project_id, rp.name as customer, b.name as project_name, pr.name as registration, pt.name as inventory, pr.registration_date, 
                ur.date as booking_date, ur.flat_cost as agreement_value, 2000 as sequence
                %s
                
                UNION ALL
                
                SELECT b.id, 'Total' as customer, b.name as project_name, null as registration, null as inventory, null as registration_date, 
                null as booking_date, sum(ur.flat_cost) as agreement_value, 3000 as sequence
                %s
                GROUP BY b.id
            
                UNION ALL
            
                SELECT b.id as project_id, null as customer, b.name as project_name, null as registration, null as inventory, null as registration_date,
                null as booking_date, null as agreement_value, 1000 as sequence
                FROM building b
                WHERE b.id IN (
                    SELECT pr.project_id
                    %s
                )
                ORDER BY project_name, project_id, sequence, registration
            ) AS result 
            
            UNION ALL
            
            SELECT * FROM grand_total
        """ % (from_clause, from_clause, from_clause, from_clause)
        self.env.cr.execute(qry)
        return self.env.cr.dictfetchall()
