# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields
from datetime import datetime, timedelta

invoice_qry = """
    SELECT COALESCE(SUM(am.amount_total), 0) AS billing
    FROM account_move am
    WHERE 
        state = 'posted'
        AND am.project_invoice_type = 'developer_invoice'
        AND am.project_id in (%s)
        AND am.invoice_date <= '%s'
        AND am.invoice_date >= '%s'
"""
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
        AND am.project_id in (%s)
        %s
"""


class BetaBillingCollectionReport(models.TransientModel):  # change this
    _name = 'beta.billing.collection.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Billing & Collection Report')  # change this
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
        self.template_area = self.env.ref('billing_collection_report.billing_collection_report')._render({
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
        regions = self.env['regions'].search([('is_parent', '=', True)], order='name')
        data = {}
        total_data = {
            'billing': {},
            'collection': {},
        }
        for start, end in month_ranges:
            month = start.strftime('%b-%y')
            data[month] = {
                'billing': {},
                'collection': {},
            }
            total_billing = 0
            total_collection = 0
            for region in regions:
                projects = self.env['building'].search([('region_id', '=', region.id)])
                collection = billing = 0
                if projects:
                    projects = ','.join([str(i) for i in projects.ids])
                    self.env.cr.execute(invoice_qry % (str(projects), end.strftime('%Y-%m-%d'), start.strftime('%Y-%m-%d')))
                    invoice_row = self.env.cr.fetchone()
                    billing = invoice_row[0] / 100000
                    # invoices = self.env['account.move'].search(
                    #     [('project_id.region_id', '=', region.id), ('state', '=', 'posted'),
                    #      ('invoice_date', '<=', end), ('invoice_date', '>=', start),
                    #      ('partner_id.is_owner', '=', True), ('project_invoice_type', '=', 'developer_invoice')])

                    date_clause = """
                        AND ((line_debit.date <= '%s' AND line_debit.date >= '%s') 
                        OR (line_credit.date <= '%s' AND line_credit.date >= '%s'))
                    """ % (
                        end.strftime('%Y-%m-%d'), start.strftime('%Y-%m-%d'),
                        end.strftime('%Y-%m-%d'), start.strftime('%Y-%m-%d')
                    )
                    self.env.cr.execute(payment_qry % (projects, date_clause))
                    # payments = self.env['account.payment'].search(
                    #     [('partner_id.is_owner', '=', True), ('state', '=', 'posted'), ('date', '<=', end),
                    #      ('date', '>=', start)])
                    payment_row = self.env.cr.fetchone()
                    collection = payment_row[1] / 100000
                    # billing = sum(invoices.mapped('amount_untaxed')) / 100000
                # for payment in payments:
                #     reconciled_lines = payment.move_id.line_ids._reconciled_lines()
                #     reconciled_lines = self.env['account.move.line'].browse(reconciled_lines).filtered(
                #         lambda x: x.move_id != payment.move_id and x.move_id.project_id.region_id.id == region.id
                #         and x.move_id.project_invoice_type == 'developer_invoice')
                #     for line in reconciled_lines:
                #         collection += line.debit + line.credit
                # collection = collection / 100000
                # billing = sum(invoices.mapped('amount_untaxed')) / 100000
                data[month]['billing'][region] = billing
                data[month]['collection'][region] = collection
                total_billing += billing
                total_collection += collection
                if region in total_data['billing']:
                    total_data['billing'][region] += billing
                    total_data['collection'][region] += collection
                else:
                    total_data['billing'][region] = billing
                    total_data['collection'][region] = collection
            data[month]['billing']['Total'] = total_billing
            data[month]['collection']['Total'] = total_collection
            if 'Total' in total_data['billing']:
                total_data['billing']['Total'] += total_billing
                total_data['collection']['Total'] += total_collection
            else:
                total_data['billing']['Total'] = total_billing
                total_data['collection']['Total'] = total_collection
        data['Total'] = total_data
        return {'data': data, 'regions': regions}
