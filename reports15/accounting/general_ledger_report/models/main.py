# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import datetime, date
from odoo.exceptions import Warning


class ReportGeneralLedger(models.AbstractModel):
    _name = 'report.general_ledger_report.report_general_ledger'
    _description = 'General Ledger'

    @api.model
    def get_report_values(self, data=None):
        lines = {}
        date_from = date_to = False
        account_obj = self.env['account.account']
        accounts = ''
        if data['date_from']:
            try:
                date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")
        if data['date_to']:
            try:
                date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except:
                raise Warning("Invalid Date Format")
        print("get_report_values data['account_ids']", data['account_ids'])
        if data['account_ids']:
            for account in data['account_ids']:
                accounts += account_obj.browse(account).name + ", "

        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        if data['date_from'] and data['date_to']:
            lines = self.get_general_ledger(data)
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'with_initial_balance': data['with_initial_balance'],
            'day_summary': data['day_summary'],
            'accounts': accounts,
            'lines': lines,
            'branch_name': branch_name,
            'monthSummary': data['monthSummary'],
            'monthTotal': data['monthTotal'],
            'o': self,
            'breadcrumbs': data['breadcrumbs'],
        }

    def get_general_ledger(self, data):
        print("def get_general_ledger(self, data):")
        move_line_obj = self.env['account.move.line']
        domain = [('move_id.state', '=', 'posted')]
        print(data['monthSummary'], data['monthTotal'])
        if data['date_from']:
            domain.append(('move_id.date', '>=', data['date_from']))
        if data['date_to']:
            domain.append(('move_id.date', '<=', data['date_to']))

        if data['account_ids']:
            domain.append(('account_id', 'in', data['account_ids']))
        opening_move = self.env.company.account_opening_move_id
        # acc_ignore_domain = []
        acc_to_ignore = self.env['ir.config_parameter'].sudo().get_param(
            'general_ledger_report.gl_ignore_ac_heads')
        if acc_to_ignore:
            # print(" get_general_ledger acc_to_ignore", acc_to_ignore.strip('][').split(','))
            # .strip('][').split(',')
            acc_to_ignore = tuple(acc_to_ignore.strip('][').split(','))
            domain.append(('account_id', 'not in', [int(a_id) for a_id in acc_to_ignore]))
        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))
            opening_move = self.env['account.move']
            branch_obj = self.env['res.branch']
            branches = branch_obj.search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in branch_obj._fields:
                for branch in branches:
                    account_opening_move_id = branch.account_opening_move_id
                    if account_opening_move_id and account_opening_move_id.state == 'posted':
                        opening_move += account_opening_move_id
                # opening_move = account_move_obj

        if opening_move:
            domain.append(('move_id.id', 'not in', opening_move.ids))

        moves = move_line_obj.search(domain, order="date asc, id asc").sorted(
            key=lambda r: str(r.account_id.name).upper())
        datas = {}
        for moveline in moves:
            move_name = moveline.move_id.name
            move_id = moveline.move_id.id
            model = moveline.move_id._name
            form = False
            if 'direct_journal_type_inx' in moveline.move_id._fields:
                if moveline.move_id.direct_journal_type_inx:
                    if moveline.move_id.direct_journal_type_inx in (
                            'receipt', 'payment_reverse', 'payment', 'receipt_reverse'):
                        form = self.env.ref('inexoft_account_voucher.direct_journal_view_move_form', False)
                    else:
                        form = False
            remarks = ''
            if 'direct_journal_item_ids' in moveline.move_id._fields:
                remarks = moveline.name if moveline.move_id.direct_journal_item_ids else ''
            if 'direct_journal_type_inx' in moveline.move_id._fields:
                if moveline.move_id.direct_journal_type_inx not in (
                        'payment', 'receipt', 'receipt_reverse', 'payment_reverse'):
                    remarks = moveline.name if moveline.move_id.line_ids else ''
            if moveline.move_id.move_type == 'in_invoice':
                remarks = 'Purchase'
                form = self.env.ref('purchase_custom.view_move_form_purchase_custom', False)
            elif moveline.move_id.move_type == 'out_invoice':
                remarks = 'Sales'
                form = self.env.ref('direct_sales_with_lot.view_move_form_direct_sales_with_lot', False)
            elif moveline.move_id.move_type == 'in_refund':
                remarks = 'Purchase Return'
                form = self.env.ref('purchase_custom.view_move_form_purchase_custom', False)
            elif moveline.move_id.move_type == 'out_refund':
                remarks = 'Sales Return'
                form = self.env.ref('direct_sales_with_lot.view_move_form_direct_sales_with_lot', False)
            if moveline.payment_id:
                move_name = moveline.payment_id.name
                move_id = moveline.payment_id.id
                model = moveline.payment_id._name
                if moveline.payment_id.partner_type == 'customer':
                    remarks = 'Customer Reciept'
                if moveline.payment_id.partner_type == 'supplier':
                    remarks = 'Supplier Reciept'

            if data['day_summary']:
                factor = moveline.date
            elif data['monthSummary']:
                date = str(moveline.date)
                d = datetime.strptime(date, "%Y-%m-%d")
                m = d.strftime('%B')
                y = str(d.year)
                factor = m + '-' + y
            else:
                factor = moveline.move_id.id

            partner = moveline.partner_id.name if moveline.partner_id else ''

            if moveline.account_id.id in datas:
                if factor in datas[moveline.account_id.id]['data']:

                    datas[moveline.account_id.id]['data'][factor]['credit'] += moveline.credit
                    datas[moveline.account_id.id]['data'][factor]['debit'] += moveline.debit
                    datas[moveline.account_id.id]['data'][factor][
                        'partner'] += ', ' + partner if moveline.move_id.move_type == 'entry' and \
                                                        datas[moveline.account_id.id]['data'][factor][
                                                            'partner'] != partner else ''
                else:
                    datas[moveline.account_id.id]['data'][factor] = {
                        'date': moveline.date.strftime('%d-%m-%Y') if not data['monthSummary'] else factor,
                        'partner': partner,
                        'move': move_name,
                        'move_id': move_id,
                        'model': model,
                        'form': form.id if form else False,
                        'name': moveline.account_id.name,
                        'credit': moveline.credit,
                        'debit': moveline.debit,
                        'remarks': remarks,
                    }
            else:
                datas[moveline.account_id.id] = {
                    'name': moveline.account_id.name,
                    'data': {
                        factor: {
                            'date': moveline.date.strftime('%d-%m-%Y') if not data['monthSummary'] else factor,
                            'partner': partner,
                            'move': move_name,
                            'move_id': move_id,
                            'model': model,
                            'form': form.id if form else False,
                            'name': moveline.account_id.name,
                            'credit': moveline.credit,
                            'debit': moveline.debit,
                            'remarks': remarks,
                        },
                    },
                    'credit': 0,
                    'debit': 0,
                }

        if data['with_initial_balance']:
            domain = [('code', '!=', str(999999))]
            if data['account_ids']:
                domain.append(('id', 'in', data['account_ids']))
            accounts = self.env['account.account'].search(domain)
            for account in accounts:
                if 'branch' in data:
                    opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], data['branch'])
                else:
                    opening = self.get_ledger_credit_and_debit(account.id, data['date_from'], branch=False)
                if opening[0] or opening[1]:
                    if account.id in datas:
                        datas[account.id]['credit'] = opening[0]
                        datas[account.id]['debit'] = opening[1]
                    else:
                        datas[account.id] = {
                            'name': account.name,
                            'data': [],
                            'credit': opening[0],
                            'debit': opening[1],
                        }
        return datas

    def get_ledger_credit_and_debit(self, account, date_from, branch):
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
                print(domain, 'domain')
            if branch:
                domain.append(('move_id.branch_id', 'in', branch))
            moves = self.env['account.move.line'].search(domain)
            print(moves, 'moves')
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

    @api.model
    def get_html(self, searchDateFrom=False, searchDateTo=False, report_account=False, searchInitial=False,
                 report_branch=False, daySummary=False, breadcrumbs=False, monthSummary=False, monthTotal=False):
        res = self._get_report_data(searchDateFrom=searchDateFrom, searchDateTo=searchDateTo,
                                    report_account=report_account, searchInitial=searchInitial,
                                    report_branch=report_branch, daySummary=daySummary, breadcrumbs=breadcrumbs,
                                    monthSummary=monthSummary, monthTotal=monthTotal)
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('general_ledger_report.report_general_ledger')._render(
            {'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'accounts': res['lines']['accounts'],
             'with_initial_balance': res['lines']['with_initial_balance'],
             'day_summary': res['lines']['day_summary'],
             'branch_name': res['lines']['branch_name'],
             'breadcrumbs': res['lines']['breadcrumbs'],
             'monthSummary': res['lines']['monthSummary'],
             'monthTotal': res['lines']['monthTotal'],
             'o': self,
             })
        return res

    @api.model
    def _get_report_data(self, searchDateFrom=False, searchDateTo=False, report_account=False, searchInitial=False,
                         report_branch=False, daySummary=False, breadcrumbs=False, monthSummary=False,
                         monthTotal=False):
        if searchDateTo and searchDateFrom:
            if searchDateFrom > searchDateTo:
                raise Warning("From date can't be greater than To date")
        acc = []
        domain = []
        acc_to_ignore = self.env['ir.config_parameter'].sudo().get_param(
            'general_ledger_report.gl_ignore_ac_heads')
        if acc_to_ignore:
            domain.append(('id', 'not in', acc_to_ignore.strip('][').split(',')))
        if breadcrumbs:
            if report_account:
                acc.append(int(report_account))
        else:
            if report_account:
                for account in report_account:
                    acc.append(int(account))
        tk = self.env['account.account'].search(domain, order='name')
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
            'account_ids': acc if acc else False,
            'with_initial_balance': searchInitial,
            'day_summary': daySummary,
            'breadcrumbs': breadcrumbs,
            'monthSummary': monthSummary if monthSummary else False,
            'monthTotal': monthTotal if monthTotal else False,
        }

        rep_branch = []
        if report_branch:
            for b in report_branch:
                rep_branch.append(int(b))
            branch_id = self.env['res.branch'].search([('id', 'in', rep_branch)])
            data['branch'] = branch_id.ids
            data['branch_name'] = ', '.join(branch_id.mapped('name'))
        is_branch = self.env['ir.model'].sudo().search([('model', '=', 'res.branch')])
        branches = {}
        branch_exists = False
        default_branch = []
        if is_branch:
            branch = self.env['res.branch'].search([('id', 'in', self.env.user.branch_ids.ids)])
            default_branch_id = self.env['res.branch'].search([('id', '=', self.env.user.branch_id.ids)])
            default_branch = [default_branch_id.id, default_branch_id.name]
            for i in branch:
                if i.id != default_branch_id.id:
                    branches[i.id] = i.name
            branch_exists = True
        dat = self.get_report_values(data=data)
        do = {}
        for i in tk:
            do[i.id] = i.name
        return {
            'lines': dat,
            'variants': do,
            'branches': branches,
            'branch_exists': branch_exists,
            'default_branch': default_branch,
            'breadcrumbs': breadcrumbs,
        }
