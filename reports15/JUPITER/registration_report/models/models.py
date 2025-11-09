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
        # ----------------------------
        # CHANGE 1 — from_clause definition (unchanged from original, kept as is)
        # ----------------------------
        from_clause = """
            FROM project_registration pr
            LEFT JOIN product_template pt ON pt.id = pr.flat_id
            LEFT JOIN unit_reservation ur ON ur.building_unit = pt.id AND ur.state = 'confirmed'
            LEFT JOIN res_partner rp ON rp.id = pr.customer_id
            LEFT JOIN building b ON b.id = pr.project_id
            WHERE pr.state = 'confirmed'
              AND pr.registration_date >= '%s'
              AND pr.registration_date <= '%s'
        """ % (self.date_from.strftime('%Y-%m-%d'), self.date_to.strftime('%Y-%m-%d'))

        if self.project_filter == 'selected':
            from_clause += " and b.id in " + str(tuple(self.project_ids.ids) or '(0)').replace(',)', ')')

        # ----------------------------
        # CHANGE 2 — Removed Project Totals block entirely
        # We removed the section that added:
        # UNION ALL
        # SELECT 'Total' as customer, b.name as project_name, ...
        # This was producing the "Project Total" row in output.
        # Now only Detailed rows + Grand Total remain.
        # ----------------------------
        qry = """
            WITH grand_total AS (
                SELECT 'Grand Total' as customer,
                       NULL as project_name,
                       NULL as registration,
                       NULL as inventory,
                       max(pr.registration_date) as registration_date,
                       max(ur.date) as booking_date,
                       sum(ur.flat_cost) as agreement_value,
                       4000 as sequence
                %s
            )
            SELECT * FROM (
                -- Detailed rows only
                SELECT rp.name as customer,
                       b.name as project_name,
                       pr.name as registration,
                       pt.name as inventory,
                       pr.registration_date,
                       ur.date as booking_date,
                       ur.flat_cost as agreement_value,
                       2000 as sequence
                %s
            ) AS result

            UNION ALL
            SELECT * FROM grand_total

            ORDER BY registration_date NULLS LAST, sequence
        """ % (from_clause, from_clause)

        # ----------------------------
        # CHANGE 3 — Execute query and return results (unchanged)
        # ----------------------------
        self.env.cr.execute(qry)
        return self.env.cr.dictfetchall()
