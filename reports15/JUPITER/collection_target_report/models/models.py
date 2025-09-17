# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime, timedelta


class BetaCollectionTargetReport(models.TransientModel):  # change this
    _name = 'beta.collection.target.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Collection Target Report')  # change this
    financial_year = fields.Selection(selection=lambda self: self.get_financial_years())

    def get_financial_years(self):
        sequence = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).sequence_id
        values = []
        for line in sequence.date_range_ids:
            values.append((str(line.date_from.year),
                           str(line.date_from.strftime('%y')) + ' - ' + str(int(line.date_from.strftime('%y')) + 1)))
        return values

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('collection_target_report.collection_target_report')._render({
            'doc': doc,
        })

    def _get_report_data(self):
        financial_year_start = datetime.strptime(self.financial_year + '-04-01', '%Y-%m-%d')
        financial_year_end = datetime.strptime(str(int(self.financial_year) + 1) + '-03-31', '%Y-%m-%d')
        month_ranges = []
        current_month_start = financial_year_start
        while current_month_start < financial_year_end:
            current_month_end = (current_month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            current_month_end = min(current_month_end, financial_year_end)
            month_ranges.append((current_month_start, current_month_end))
            current_month_start = (current_month_end + timedelta(days=1))
        regions = self.env['regions'].search([('is_parent','=',True)], order='name')
        data = {}
        for start, end in month_ranges:
            print(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
            data[start] = {
                'billing': {},
                'collection': {},
            }
            total_billing = 0
            total_collection = 0
            for region in regions:
                invoices = self.env['account.move'].search(
                    [('project_id.region_id', '=', region.id), ('state', '=', 'posted'),
                     ('invoice_date', '<=', end), ('invoice_date', '>=', start),
                     ('partner_id.is_owner', '=', True), ('project_invoice_type', '=', 'developer_invoice')])
                data[start]['billing'][region] = sum(invoices.mapped('amount_total'))
                data[start]['collection'][region] = 0
                total_billing += data[start]['billing'][region]
                total_collection += data[start]['collection'][region]
            data[start]['billing']['Total'] = total_billing
            data[start]['collection']['Total'] = total_collection
        return {'data': data, 'regions': regions}
