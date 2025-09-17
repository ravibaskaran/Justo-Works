# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta

invoice_qry = """
    SELECT COALESCE(SUM(am.amount_total), 0) AS billing
    FROM account_move am
    WHERE 
        state = 'posted'
        AND am.project_invoice_type = 'developer_invoice'
        AND am.project_id = %s
        AND am.invoice_date <= '%s'
        %s
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
        AND am.project_id = %s
        %s
"""


class BetaDebtorsOutstandingStatement(models.TransientModel):  # change this
    _name = 'beta.debtors.outstanding.statement'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Debtors Outstanding Statement')  # change this
    date_from = fields.Date()
    date_to = fields.Date()

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('debtors_outstanding_statement.debtors_outstanding_statement_report')._render({
            'doc': doc,
            'date_from': self.date_from.strftime('%d/%m/%Y'),
            'date_to': self.date_to.strftime('%d/%m/%Y'),
        })

    @api.model
    def default_get(self, fields_list):
        res = super(BetaDebtorsOutstandingStatement, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def _get_report_data(self):
        projects = self.env['building'].search([], order='name')
        data = {}
        opening_total = billing_total = collection_total = closing_total = 0
        for project in projects:
            self.env.cr.execute(invoice_qry % (str(project.id), self.date_to.strftime('%Y-%m-%d'), "AND am.invoice_date >= '" + self.date_from.strftime('%Y-%m-%d') + "'"))
            invoice_row = self.env.cr.fetchone()
            billing = invoice_row[0]
            date_clause = """
                AND ((line_debit.date <= '%s' AND line_debit.date >= '%s') 
                OR (line_credit.date <= '%s' AND line_credit.date >= '%s'))
            """ % (
                self.date_to.strftime('%Y-%m-%d'), self.date_from.strftime('%Y-%m-%d'),
                self.date_to.strftime('%Y-%m-%d'), self.date_from.strftime('%Y-%m-%d')
            )
            self.env.cr.execute(payment_qry % (str(project.id), date_clause))
            payment_row = self.env.cr.fetchone()
            collection = payment_row[1]

            self.env.cr.execute(invoice_qry % (str(project.id), self.date_from.strftime('%Y-%m-%d'), ''))
            opening_invoice_row = self.env.cr.fetchone()
            opening_billing = opening_invoice_row[0]
            date_clause = """
                AND (line_debit.date <= '%s' OR line_credit.date <= '%s')
            """ % (
                (self.date_from - timedelta(days=1)).strftime('%Y-%m-%d'), (self.date_from - timedelta(days=1)).strftime('%Y-%m-%d')
            )
            self.env.cr.execute(payment_qry % (str(project.id), date_clause))
            opening_payment_row = self.env.cr.fetchone()
            opening_collection = opening_payment_row[1]

            opening = opening_billing - opening_collection
            closing = opening + billing - collection
            data[project.name] = {
                'opening': opening,
                'billing': billing,
                'collection': collection,
                'closing': closing,
            }
            opening_total += opening
            billing_total += billing
            collection_total += collection
            closing_total += closing
        data['Total'] = {
            'opening': opening_total,
            'billing': billing_total,
            'collection': collection_total,
            'closing': closing_total,
        }
        return {'data': data}
