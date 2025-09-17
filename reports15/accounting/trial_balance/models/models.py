# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
import time
from odoo.exceptions import UserError


class BetaTrialBalance(models.TransientModel):  # change this
    _name = 'beta.trial.balance'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Trial Balance')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    opening = fields.Boolean()
    without_opening = fields.Boolean()
    order = fields.Selection([('alpha', 'Alphabetical'), ('schedule', 'Schedule Wise')], default='alpha', required=True)
    summary = fields.Boolean()

    @api.onchange('order')
    def onchange_order(self):
        self.summary = False

    @api.model
    def default_get(self, fields_list):
        res = super(BetaTrialBalance, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    @api.model
    def get_report_values(self, data=None):
        account_res = ''
        display_account = data['form'].get('display_account')
        accounts = self.env['account.account'].search([])
        head_type_obj = self.env['account.account.type']
        if 'branch' in data:
            branch = data['branch']
        else:
            branch = None
        if data['date_from'] and data['date_to']:
            account_res = self.with_context(
                data['form'].get('used_context'))._get_accounts(accounts,
                                                                display_account, branch, data['date_from'],
                                                                data['date_to'])
        if not data['without_opening']:
            for data_line in account_res:
                if 'branch' in data:
                    opening = self.get_trial_credit_and_debit(data_line['account_id'], data['date_from'],
                                                              data['branch'])
                else:
                    opening = self.get_trial_credit_and_debit(data_line['account_id'], data['date_from'], branch=False)

                if data['opening']:
                    debit = opening[1]
                    credit = opening[0]
                    opening = debit - credit
                    data_line['balance'] = opening + data_line['balance']
                    data_line['opening'] = opening
                else:
                    debit = opening[1]
                    credit = opening[0]
                    opening = debit - credit
                    data_line['balance'] = opening + data_line['balance']
                    if data_line['balance'] >= 0:
                        data_line['debit'] = data_line['balance']
                        data_line['credit'] = 0
                    else:
                        data_line['debit'] = 0
                        data_line['credit'] = data_line['balance'] * -1

        if data['order'] == 'schedule':
            sorted_dict_list = []
            type1 = ''
            sorted_dict_list2 = []
            i = 0
            total = []
            total_debit = 0
            total_credit = 0
            for data_cust in sorted(account_res, key=lambda i: i['type']):
                sorted_dict_list2.append(data_cust)
            if len(sorted_dict_list2) > 0:
                j = 0
                type2 = sorted_dict_list2[0]['type']
                while j < len(sorted_dict_list2):
                    if type2 == sorted_dict_list2[j]['type']:
                        total_debit += sorted_dict_list2[j]['debit']
                        total_credit += sorted_dict_list2[j]['credit']
                    else:
                        total.append({'type': type2, 'total_debit': total_debit, 'total_credit': total_credit})
                        total_debit = 0
                        total_credit = 0
                        type2 = sorted_dict_list2[j]['type']
                        total_debit += sorted_dict_list2[j]['debit']
                        total_credit += sorted_dict_list2[j]['credit']
                    j = j + 1
                total.append({'type': type2, 'total_debit': total_debit, 'total_credit': total_credit})
            if 'sequence' in head_type_obj._fields:
                account_doc = sorted(account_res, key=lambda i: i['sequence'])
            else:
                account_doc = sorted(account_res, key=lambda i: i['type'])
            for data_line2 in account_doc:
                if data_line2['type'] != type1:
                    i = i + 1
                    idf = data_line2['type'][:3]
                    id = idf + str(i)
                    for tot in total:
                        if data_line2['type'] == tot['type']:
                            sorted_dict_list.append(
                                {'type': data_line2['type'], 'id': id, 'total_debit': tot['total_debit'],
                                 'total_credit': tot['total_credit'], 'opening': data['opening'],
                                 'without_opening': data['without_opening']})
                    sorted_dict_list.append(data_line2)
                    type1 = data_line2['type']
                else:
                    sorted_dict_list.append(data_line2)
            account_res = sorted_dict_list
        if data['order'] == 'alpha':
            account_res = sorted(account_res, key=lambda i: i['name'])
        if data['form']['date_from']: data['form']['date_from'] = datetime.strptime(data['form']['date_from'],
                                                                                    '%Y-%m-%d').strftime(
            '%d-%m-%Y')
        if data['form']['date_to']: data['form']['date_to'] = datetime.strptime(data['form']['date_to'],
                                                                                '%Y-%m-%d').strftime(
            '%d-%m-%Y')
        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        docs = {
            'opening': data['opening'],
            'without_opening': data['without_opening'],
            'order': data['order'],
        }
        return {
            'doc_ids': self.ids,
            'doc_model': 'account.move',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
            'auto_unfold': data['auto_unfold'],
            'branch_name': branch_name,
            'order': data['order'],
        }

    def get_trial_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id', '=', account)])
            if not account_id.user_type_id.include_initial_balance:
                today = date.today()
                if today < datetime.strptime('01-04-' + str(today.year), '%d-%m-%Y').date():
                    fin_date = str(today.year - 1) + '-04-01'
                else:
                    fin_date = str(today.year) + '-04-01'
                domain.append(('date', '>=', fin_date))

            if branch:
                domain.append(('move_id.branch_id', 'in', branch))
            moves = self.env['account.move.line'].search(domain)

            opening_move = self.env.company.account_opening_move_id
            if branch:
                branch_id = self.env['res.branch'].search([('id', 'in', branch)])
                if 'account_opening_move_id' in self.env['res.branch']:
                    for b in branch_id:
                        account_opening_move_id = b.account_opening_move_id
                        opening_move = account_opening_move_id
                        if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                                "%Y-%m-%d") == date_from:
                            for openline in opening_move.line_ids:
                                if openline.account_id.id == account:
                                    moves += openline
            else:
                if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                        "%Y-%m-%d") == date_from:
                    for openline in opening_move.line_ids:
                        if openline.account_id.id == account:
                            moves += openline
            for move in moves:
                credit += move.credit
                debit += move.debit
        return (credit, debit)

    def _get_accounts(self, accounts, display_account, branch, date_from, date_to):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """
        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env['account.move.line']._query_get()

        tables = tables.replace('"', '')
        if not tables:
            tables = 'account_move_line'
        tables += ' left join account_move on account_move.id=account_move_line.move_id '
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())

        filters = " AND ".join(wheres)

        opening_move = self.env.company.account_opening_move_id
        moves = None
        if branch:
            branch_id = self.env['res.branch'].search([('id', 'in', branch)])
            if 'account_opening_move_id' in self.env['res.branch']:
                for b in branch_id:
                    account_opening_move_id = b.account_opening_move_id
                    opening_move = account_opening_move_id
                    if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                            "%Y-%m-%d") == date_from:
                        moves = opening_move
        else:
            if opening_move and opening_move.state == 'posted' and opening_move.date.strftime(
                    "%Y-%m-%d") == date_from:
                moves = opening_move
        opening_filter = ""
        if moves:
            opening_filter = "and account_move_line.id not in " + str(tuple(moves.line_ids.ids))
        if branch is not None:
            branch.append(0)
            branch_ids = tuple(branch)
            request = (
                    "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                    " FROM " + tables + " WHERE account_id IN %s " + filters + "AND account_move_line.date<='" + date_to + "' AND account_move_line.date>='" + date_from + "' AND account_move_line__move_id.state = 'posted' AND (account_move_line.branch_id in " + str(
                branch_ids) + ") " + str(opening_filter) + " GROUP BY account_id")
        else:
            # compute the balance, debit and credit for the provided accounts
            request = (
                    "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                    " FROM " + tables + " WHERE account_id IN %s " + filters + "AND account_move_line.date<='" + date_to + "' AND account_move_line.date>='" + date_from + "' AND account_move.state = 'posted'  " + str(
                opening_filter) + "   GROUP BY account_id")

        params = (tuple(accounts.ids),) + tuple(where_params)

        self.env.cr.execute(request, params)

        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row
        account_res = []

        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance', 'type', 'account_id'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            res['type'] = account.user_type_id.name
            res['sequence'] = account.user_type_id.sequence if 'sequence' in account.user_type_id._fields else 0
            res['account_id'] = account.id
            if account.id in account_result:
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(
                    res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (
                    not currency.is_zero(res['debit']) or not currency.is_zero(
                res['credit'])):
                account_res.append(res)
            elif moves and account in moves.line_ids.mapped('account_id') and res not in account_res:
                account_res.append(res)
        return account_res

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'),
                                    date_to=self.date_to.strftime('%Y-%m-%d'),
                                    opening=self.opening, without_opening=self.without_opening,
                                    order=self.order, auto_unfold=self.summary)
        res['lines'] = self.env.ref('trial_balance.report_trial_balance')._render(
            {'doc_ids': res['lines']['doc_ids'],
             'doc_model': res['lines']['doc_model'],
             'data': res['lines']['data'],
             'docs': res['lines']['docs'],
             'Accounts': res['lines']['Accounts'],
             'branch_name': res['lines']['branch_name'],
             'auto_unfold': res['lines']['auto_unfold'],
             'order': res['lines']['order'],
             })
        self.template_area = res['lines']

    def _get_report_data(self, date_from=False, date_to=False, opening=False, without_opening=False, order=False,
                         auto_unfold=False):
        if date_to and date_from:
            if date_from > date_to:
                raise Warning("From date can't be greater than To date")
        form = {
            'display_account': 'movement',
            'date_from': date_from,
            'date_to': date_to,
            'used_context': {
                'date_from': date_from,
                'date_to': date_to,
            }
        }
        data = {
            'form': form,
            'date_from': date_from,
            'date_to': date_to,
            'company_id': self.env.user.company_id.id,
            'without_opening': without_opening,
            'opening': opening,
            'order': order,
            'auto_unfold': auto_unfold,
        }
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
