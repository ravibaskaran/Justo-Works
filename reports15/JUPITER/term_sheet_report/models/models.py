# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaTermSheetReport(models.TransientModel):  # change this
    _name = 'beta.term.sheet.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Term Sheet Report')  # change this
    date_from = fields.Date()
    date_to = fields.Date()

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
        fmt = "%d/%m/%Y"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_timezone.strftime(fmt), fmt) - datetime.strptime(
            now_utc.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    @api.model
    def default_get(self, fields_list):
        res = super(BetaTermSheetReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def get_html(self):
        res = self._get_report_data()
        self.template_area = self.env.ref('term_sheet_report.report_term_sheet_report')._render({
            'table': res,
            'date_start': self.date_from,
            'date_end': self.date_to
        })

    def _get_report_data(self):
        table = """<table id="tableId" rules="groups" frame="hsides" border="1"
                   class="table table-bordered table-striped"
                   style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px;">
                <style>.table td{ padding: .8px !important;}</style>
                <thead>
                    <th class="text-center">SNo.</th>
                    <th class="text-center">Project</th>
                    <th class="text-center">Project Start Date</th>
                    <th class="text-center">Region</th>
                    <th class="text-center">Cluster</th>
                    <th class="text-center">Location</th>
                    <th class="text-center">Developer</th>
                    <th class="text-center">Units</th>
                    <th class="text-center">Av.Rate/SqFt</th>
                    <th class="text-center">Ticket Size</th>
                    <th class="text-center">AV Cr.</th>
                    <th class="text-center">Marketing Budget %</th>
                    <th class="text-center">Justo Fees %</th>
                    <th class="text-center">Signing Amount</th>
                    <th class="text-center">Monthly Retainer</th>
                    <th class="text-center">Tenure</th>
                    <th class="text-center">Extend</th>
                    <th class="text-center">CRM Fees Applicable</th>
                </thead>
                <tbody>"""
        term_sheets = self.env['term.sheet'].search([('date', '<=', self.date_to), ('date', '>=', self.date_from)])
        form = self.env.ref('real_estate_sheets.term_sheet_view_form', False)
        sl_no = 0
        for sheet in term_sheets:
            sl_no += 1
            project = self.env['building'].search([('term_sheet_id', '=', sheet.id)], limit=1)
            table += """
            <tr>
                <td class="text-right">%s</td>
                <td class="text-left">
                    <a href="#" class="o_beta_report_action"
                       data-res-id="%s"
                       data-model="term.sheet"
                       data-form="%s">%s
                    </a>
                </td>
                <td class="text-left">%s</td>
                <td class="text-left">%s</td>
                <td class="text-left">%s</td>
                <td class="text-left">%s</td>
                <td class="text-left">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
                <td class="text-right">%s</td>
            </tr>
            """ % (
                sl_no,
                sheet.id,
                form.id,
                sheet.name or '',
                project.purchase_date.strftime('%d/%m/%Y') if project.purchase_date else '',
                project.region_id.name or '',
                project.sub_region_id.name or '',
                (project.address or '') if project else (sheet.site_address or ''),
                (project.partner_id.name or '') if project else (sheet.developer_id.name or ''),
                sheet.evaluation_sheet_id.apartments_no_best or 0,
                sheet.avg_rate_sq_ft,
                '{:.2f}'.format(sheet.evaluation_sheet_id.tentative_unit_sales_price or 0),
                '{:.2f}'.format(sheet.evaluation_sheet_id.apartments_no_best * sheet.evaluation_sheet_id.tentative_unit_sales_price) or '0.00',
                sheet.market_budgeting_percentage or 0,
                '{:.2f}'.format(sheet.evaluation_sheet_id.gross_justo_commission or 0),
                '{:.2f}'.format(sheet.signing_amount or 0),
                '{:.2f}'.format(sheet.retainer_fee or 0),
                sheet.tenure or 0,
                sheet.extend or 0,
                (sheet.crm_fees_applicable or '').capitalize()
            )
        return table
