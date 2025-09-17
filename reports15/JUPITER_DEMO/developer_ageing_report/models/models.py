# -*- coding: utf-8 -*-
from odoo.tools import float_is_zero
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, _


class BetaDeveloperAgeingReport(models.TransientModel):  # change this
    _name = 'beta.developer.ageing.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Developer Ageing Report')  # change this
    date_from = fields.Date()
    period = fields.Integer(default=30)
    summary = fields.Boolean()

    def get_html(self):
        doc = self._get_report_data()
        self.template_area = self.env.ref('developer_ageing_report.developer_ageing_report')._render({
            'doc': doc,
            'date_from': self.date_from,
            'header': doc.get('header'),
            'account_total': doc.get('account_total'),
            'lines': doc.get('lines'),
            'type': doc.get('type'),
            'branch_name': doc.get('branch_name'),
            'summary': self.summary
        })

    @api.model
    def default_get(self, fields_list):
        res = super(BetaDeveloperAgeingReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = today
        return res

    def _get_billwise_move_lines(self, account_type, date_from, target_move, period_length, branch):
        # This method can receive the context key 'include_nullified_amount' {Boolean}
        # Do an invoice and a payment and unreconcile. The amount will be nullified
        # By default, the partner wouldn't appear in this report.
        # The context key allow it to appear
        periods = {}
        start = date_from
        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length)
            periods[str(i)] = {
                'name': (i != 0 and (str((5 - (i + 1)) * period_length) + '-' + str((5 - i) * period_length)) or (
                            '+' + str(4 * period_length))),
                'stop': start.strftime('%Y-%m-%d'),
                'start': (i != 0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop - relativedelta(days=1)
        res = []
        total = []
        cr = self.env.cr
        company_ids = self.env.context.get('company_ids', (self.env.user.company_id.id,))
        user_company = self.env.user.company_id
        user_currency = user_company.currency_id
        ResCurrency = self.env['res.currency'].with_context(date=date_from)
        move_state = ['draft', 'posted']
        if target_move == 'posted':
            move_state = ['posted']
        arg_list = (tuple(move_state), tuple(account_type))
        # build the reconciliation clause to see what partner needs to be printed
        reconciliation_clause = '(l.reconciled IS FALSE)'
        cr.execute('SELECT debit_move_id, credit_move_id FROM account_partial_reconcile where create_date > %s',
                   (date_from,))
        reconciled_after_date = []
        for row in cr.fetchall():
            reconciled_after_date += [row[0], row[1]]
        if reconciled_after_date:
            reconciliation_clause = '(l.reconciled IS FALSE OR l.id IN %s)'
            arg_list += (tuple(reconciled_after_date),)
        arg_list += (date_from, tuple(company_ids))
        branch_clause = ''
        if branch:
            branch_clause = " and am.branch_id in " + str(tuple(branch)).replace(",)", ")") + " "
        query = '''
            SELECT DISTINCT l.partner_id, UPPER(res_partner.name)
            FROM account_move_line AS l left join res_partner on l.partner_id = res_partner.id, account_account, account_move am
            WHERE (l.account_id = account_account.id)
                AND (l.move_id = am.id)
                AND (am.state IN %s)
                AND (account_account.internal_type IN %s)
                AND ''' + reconciliation_clause + '''
                AND (l.date <= %s)
                AND l.company_id IN %s
                and am.move_type in ('in_invoice','out_invoice')
                and res_partner.is_owner = True
                ''' + str(branch_clause) + '''
            ORDER BY UPPER(res_partner.name)'''
        cr.execute(query, arg_list)
        partners = cr.dictfetchall()
        # put a total of 0
        for i in range(7):
            total.append(0)

        # Build a string like (1,2,3) for easy use in SQL query
        partner_ids = [partner['partner_id'] for partner in partners if partner['partner_id']]
        lines = dict((partner['partner_id'] or False, []) for partner in partners)
        if not partner_ids:
            return [], [], {}, periods

        # This dictionary will store the not due amount of all partners
        undue_amounts = {}
        query = '''SELECT l.id
                FROM account_move_line AS l, account_account, account_move am
                WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                    AND (am.state IN %s)
                    AND (account_account.internal_type IN %s)
                    AND (COALESCE(l.date_maturity,l.date) >= %s)\
                    AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                    and am.move_type in ('in_invoice','out_invoice')
                    ''' + str(branch_clause) + '''
                AND (l.date <= %s)
                AND l.company_id IN %s'''
        cr.execute(query, (
        tuple(move_state), tuple(account_type), date_from, tuple(partner_ids), date_from, tuple(company_ids)))
        aml_ids = cr.fetchall()
        aml_ids = aml_ids and [x[0] for x in aml_ids] or []
        for line in self.env['account.move.line'].browse(aml_ids):
            partner_id = line.partner_id.id or False
            if partner_id not in undue_amounts:
                undue_amounts[partner_id] = 0.0
            line_amount = line.balance
            if line.balance == 0:
                continue
            for partial_line in line.matched_debit_ids:
                if partial_line.max_date <= datetime.strptime(date_from, "%Y-%m-%d").date():
                    line_amount += partial_line.amount
            for partial_line in line.matched_credit_ids:
                if partial_line.max_date <= datetime.strptime(date_from, "%Y-%m-%d").date():
                    line_amount -= partial_line.amount
            if not self.env.user.company_id.currency_id.is_zero(line_amount):
                undue_amounts[partner_id] += line_amount
                lines[partner_id].append({
                    'line': line,
                    'amount': line_amount,
                    'period': 6,
                })

        # Use one query per period and store results in history (a list variable)
        # Each history will contain: history[1] = {'<partner_id>': <partner_debit-credit>}
        history = []
        aml_ids_t = str(tuple(aml_ids if aml_ids else [0])).replace(',)', ')')
        for i in range(5):
            args_list = (tuple(move_state), tuple(account_type), tuple(partner_ids),)
            dates_query = '(COALESCE(l.date_maturity,l.date)'
            if periods[str(i)]['start'] and periods[str(i)]['stop']:
                dates_query += ' BETWEEN %s AND %s)'
                args_list += (periods[str(i)]['start'], periods[str(i)]['stop'])
            elif periods[str(i)]['start']:
                dates_query += ' >= %s)'
                args_list += (periods[str(i)]['start'],)
            else:
                dates_query += ' <= %s)'
                args_list += (periods[str(i)]['stop'],)
            args_list += (date_from, tuple(company_ids))

            query = '''SELECT l.id
                    FROM account_move_line AS l, account_account, account_move am
                    WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                        AND (am.state IN %s) and l.id not in ''' + aml_ids_t + '''
                        AND (account_account.internal_type IN %s)
                        AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                        AND ''' + dates_query + '''
                        and am.move_type in ('in_invoice','out_invoice')
                        ''' + str(branch_clause) + '''
                    AND (l.date <= %s)
                    AND l.company_id IN %s'''
            cr.execute(query, args_list)
            partners_amount = {}
            aml_ids = cr.fetchall()
            aml_ids = aml_ids and [x[0] for x in aml_ids] or []
            for line in self.env['account.move.line'].browse(aml_ids).with_context(prefetch_fields=False):
                partner_id = line.partner_id.id or False
                if partner_id not in partners_amount:
                    partners_amount[partner_id] = 0.0
                line_amount = ResCurrency._compute(line.company_id.currency_id, user_currency, line.balance)
                if user_currency.is_zero(line_amount):
                    continue
                for partial_line in line.matched_debit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount += ResCurrency._compute(partial_line.company_id.currency_id, user_currency,
                                                            partial_line.amount)
                for partial_line in line.matched_credit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount -= ResCurrency._compute(partial_line.company_id.currency_id, user_currency,
                                                            partial_line.amount)
                if not self.env.user.company_id.currency_id.is_zero(line_amount):
                    partners_amount[partner_id] += line_amount
                    lines[partner_id].append({
                        'line': line,
                        'amount': line_amount,
                        'period': i + 1,
                    })
            history.append(partners_amount)
        for partner in partners:
            if partner['partner_id'] is None:
                partner['partner_id'] = False
            at_least_one_amount = False
            values = {}
            undue_amt = 0.0
            if partner['partner_id'] in undue_amounts:  # Making sure this partner actually was found by the query
                undue_amt = undue_amounts[partner['partner_id']]

            total[6] = total[6] + undue_amt
            values['direction'] = undue_amt
            if not float_is_zero(values['direction'], precision_rounding=self.env.user.company_id.currency_id.rounding):
                at_least_one_amount = True

            for i in range(5):
                during = False
                if partner['partner_id'] in history[i]:
                    during = [history[i][partner['partner_id']]]
                # Adding counter
                total[(i)] = total[(i)] + (during and during[0] or 0)
                values[str(i)] = during and during[0] or 0.0
                if not float_is_zero(values[str(i)], precision_rounding=self.env.user.company_id.currency_id.rounding):
                    at_least_one_amount = True
            values['total'] = sum([values['direction']] + [values[str(i)] for i in range(5)])
            ## Add for total
            total[(i + 1)] += values['total']
            values['partner_id'] = partner['partner_id']
            if partner['partner_id']:
                browsed_partner = self.env['res.partner'].browse(partner['partner_id'])
                values['name'] = browsed_partner.name and len(browsed_partner.name) >= 45 and browsed_partner.name[
                                                                                              0:40] + '...' or browsed_partner.name
                values['trust'] = browsed_partner.trust
            else:
                values['name'] = _('Unknown Partner')
                values['trust'] = False

            if at_least_one_amount or (self._context.get('include_nullified_amount') and lines[partner['partner_id']]):
                res.append(values)
        return res, total, lines, periods

    def _get_report_data(self):
        # currency = self.env.user.company_id.currency_id.symbol or ''
        header = account_total = ['', '', '', '', '', '', '', '']
        doc_list = {}
        partner_type = 'Partner Ageing'
        if self.date_from:
            account_type = ['receivable']
            partner_type = 'Developer Ageing'
            branch = False
            movelines, total, dummy, periods = self._get_billwise_move_lines(account_type, self.date_from, 'posted',
                                                                             self.period, branch)
            for partner in dummy:
                for line in dummy[partner]:
                    line['intervals'] = {
                        '0': 0,
                        '1': 0,
                        '2': 0,
                        '3': 0,
                        '4': 0,
                        '5': 0,
                        'total': 0
                    }
                    line['intervals'][str(line['period'] - 1)] = line['amount']
                    line['intervals']['total'] += line['amount']

            header = ["Partners", "Not Due", periods['4']['name'], periods['3']['name'], periods['2']['name'],
                      periods['1']['name'], periods['0']['name'], "Total"]
            if total:
                account_total = [
                    "Grand Total",
                    total[6] and str('{:.2f}'.format(abs(total[6]))) + " " or '__',
                    total[4] and str('{:.2f}'.format(abs(total[4]))) + " " or '__',
                    total[3] and str('{:.2f}'.format(abs(total[3]))) + " " or '__',
                    total[2] and str('{:.2f}'.format(abs(total[2]))) + " " or '__',
                    total[1] and str('{:.2f}'.format(abs(total[1]))) + " " or '__',
                    total[0] and str('{:.2f}'.format(abs(total[0]))) + " " or '__',
                    total[5] and str('{:.2f}'.format(abs(total[5]))) + " " or '__',
                ]
            doc_list = {}
            for partner in movelines:
                # doc_list[partner['name']] = [
                #     partner['direction'] and str('{:.2f}'.format(abs(partner['direction']))) + " " or '__',
                #     partner['4'] and str('{:.2f}'.format(abs(partner['4']))) + " " or '__',
                #     partner['3'] and str('{:.2f}'.format(abs(partner['3']))) + " " or '__',
                #     partner['2'] and str('{:.2f}'.format(abs(partner['2']))) + " " or '__',
                #     partner['1'] and str('{:.2f}'.format(abs(partner['1']))) + " " or '__',
                #     partner['0'] and str('{:.2f}'.format(abs(partner['0']))) + " " or '__',
                #     partner['total'] and str('{:.2f}'.format(abs(partner['total']))) + " " or '__',
                #     []
                # ]
                for line in dummy[partner['partner_id']]:
                    region = line['line'].move_id.project_id.region_id
                    if region not in doc_list:
                        doc_list[region] = {
                            'partner_doc': {
                                partner['partner_id']: {
                                    'name': partner['name'],
                                    'invoices': [],
                                    '1': 0,
                                    '2': 0,
                                    '3': 0,
                                    '4': 0,
                                    '5': 0,
                                    '6': 0,
                                    '7': 0,
                                },
                            },
                            '1': 0,
                            '2': 0,
                            '3': 0,
                            '4': 0,
                            '5': 0,
                            '6': 0,
                            '7': 0,
                        }
                    if partner['partner_id'] not in doc_list[region]['partner_doc']:
                        doc_list[region]['partner_doc'][partner['partner_id']] = {
                            'name': partner['name'],
                            'invoices': [],
                            '1': 0,
                            '2': 0,
                            '3': 0,
                            '4': 0,
                            '5': 0,
                            '6': 0,
                            '7': 0,
                        }
                    interval_1 = line['intervals'].get('5') and abs(line['intervals'].get('5')) or 0
                    interval_2 = line['intervals'].get('4') and abs(line['intervals'].get('4')) or 0
                    interval_3 = line['intervals'].get('3') and abs(line['intervals'].get('3')) or 0
                    interval_4 = line['intervals'].get('2') and abs(line['intervals'].get('2')) or 0
                    interval_5 = line['intervals'].get('1') and abs(line['intervals'].get('1')) or 0
                    interval_6 = line['intervals'].get('0') and abs(line['intervals'].get('0')) or 0
                    interval_7 = line['intervals'].get('total') and abs(line['intervals'].get('total')) or 0

                    doc_list[region]['partner_doc'][partner['partner_id']]['1'] += interval_1
                    doc_list[region]['partner_doc'][partner['partner_id']]['2'] += interval_2
                    doc_list[region]['partner_doc'][partner['partner_id']]['3'] += interval_3
                    doc_list[region]['partner_doc'][partner['partner_id']]['4'] += interval_4
                    doc_list[region]['partner_doc'][partner['partner_id']]['5'] += interval_5
                    doc_list[region]['partner_doc'][partner['partner_id']]['6'] += interval_6
                    doc_list[region]['partner_doc'][partner['partner_id']]['7'] += interval_7

                    doc_list[region]['1'] += interval_1
                    doc_list[region]['2'] += interval_2
                    doc_list[region]['3'] += interval_3
                    doc_list[region]['4'] += interval_4
                    doc_list[region]['5'] += interval_5
                    doc_list[region]['6'] += interval_6
                    doc_list[region]['7'] += interval_7

                    doc_list[region]['partner_doc'][partner['partner_id']]['invoices'].append([
                        line['line'].move_id.name,
                        '{:.2f}'.format(interval_1) + ' ' if interval_1 != 0 else '__',
                        '{:.2f}'.format(interval_2) + ' ' if interval_2 != 0 else '__',
                        '{:.2f}'.format(interval_3) + ' ' if interval_3 != 0 else '__',
                        '{:.2f}'.format(interval_4) + ' ' if interval_4 != 0 else '__',
                        '{:.2f}'.format(interval_5) + ' ' if interval_5 != 0 else '__',
                        '{:.2f}'.format(interval_6) + ' ' if interval_6 != 0 else '__',
                        '{:.2f}'.format(interval_7) + ' ' if interval_7 != 0 else '__',
                    ])
        branch_name = ''
        return {
            'date_from': self.date_from,
            'header': header,
            'account_total': account_total,
            'lines': doc_list,
            'type': partner_type,
            'branch_name': branch_name
        }
