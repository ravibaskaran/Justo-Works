# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import datetime
from odoo.exceptions import Warning, UserError


# Partner Ledger Report
class ReportPartnerLedger(models.TransientModel):
    _name = 'beta.partner.ledger'
    _inherit = 'beta.reports'

    date_from = fields.Date()
    date_to = fields.Date()
    account_ids = fields.Many2many('account.account', string='Accounts')
    partner_ids = fields.Many2many('res.partner', string='Partner')
    consolidate = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(ReportPartnerLedger, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        if not self.env.context.get('default_date_from') and not self.env.context.get('default_date_to'):
            res['date_from'] = fin_start
            res['date_to'] = today
        return res

    def get_report_values(self, data=None):
        lines = {}
        account_obj = self.env['account.account']
        partner_obj = self.env['res.partner']
        date_from = date_to = False
        accounts = partners = ''
        if data['date_from']:
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
        if data['date_to']:
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
        if data['account_ids']:
            for account in data['account_ids']:
                accounts += account_obj.browse(account).name + ", "
        if data['partner_ids']:
            for partner in data['partner_ids']:
                partners += partner_obj.browse(partner).name + ", "
        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        if data['account_ids']:
            lines = self.get_partner_ledger(data)
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'accounts': accounts,
            'partners': partners,
            'lines': lines,
            'with_initial_balance': data['with_initial_balance'],
            'branch_name': branch_name
        }

    def get_partner_ledger(self, data):
        move_line_obj = self.env['account.move.line']
        domain = [('move_id.state', '=', 'posted')]
        if data['date_from']:
            domain.append(('move_id.date', '>=', data['date_from']))
        if data['date_to']:
            domain.append(('move_id.date', '<=', data['date_to']))
        if data['account_ids']:
            domain.append(('account_id', 'in', data['account_ids']))
        if data['partner_ids']:
            domain.append(('partner_id', 'in', data['partner_ids']))
        else:
            domain.append(('partner_id', '!=', False))

        opening_move = self.env.company.account_opening_move_id

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

        moves = move_line_obj.search(domain, order="partner_id asc, date asc, id asc")
        datas = {}
        if data['consolidate']:
            for move in moves:
                move_name = move.move_id.name
                if move.payment_id:
                    move_name = move.payment_id.name
                if 'all' in datas:
                    if move.partner_id.id in datas['all']['data']:
                        datas['all']['data'][move.partner_id.id]['data'].append(
                            (move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit))
                    else:
                        # opening = self.get_partner_credit_and_debit(move.partner_id.id, move.account_id.id,
                        #                                             data['date_from'])
                        datas['all']['data'][move.partner_id.id] = {
                            'name': move.partner_id.name,
                            'data': [(move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit)],
                            'credit': 0,
                            'debit': 0,
                        }
                else:
                    # opening = self.get_partner_credit_and_debit(move.partner_id.id, move.account_id.id, data['date_from'])
                    datas['all'] = {
                        'name': ','.join(data['account_names']),
                        'data': {
                            move.partner_id.id: {
                                'name': move.partner_id.name,
                                'data': [
                                    (move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit)],
                                'credit': 0,
                                'debit': 0,
                            }
                        }
                    }
        else:
            for move in moves:
                move_name = move.move_id.name
                if move.payment_id:
                    move_name = move.payment_id.name
                if move.account_id.id in datas:
                    if move.partner_id.id in datas[move.account_id.id]['data']:
                        datas[move.account_id.id]['data'][move.partner_id.id]['data'].append(
                            (move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit))
                    else:
                        # opening = self.get_partner_credit_and_debit(move.partner_id.id, move.account_id.id,
                        #                                             data['date_from'])
                        datas[move.account_id.id]['data'][move.partner_id.id] = {
                            'name': move.partner_id.name,
                            'data': [(move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit)],
                            'credit': 0,
                            'debit': 0,
                        }
                else:
                    # opening = self.get_partner_credit_and_debit(move.partner_id.id, move.account_id.id, data['date_from'])
                    datas[move.account_id.id] = {
                        'name': move.account_id.name,
                        'data': {
                            move.partner_id.id: {
                                'name': move.partner_id.name,
                                'data': [
                                    (move.date.strftime('%d-%m-%Y'), move_name, move.name, move.credit, move.debit)],
                                'credit': 0,
                                'debit': 0,
                            }
                        }
                    }

        if data['with_initial_balance']:
            partner_domain = []
            account_domain = []
            if data['partner_ids']:
                partner_domain.append(('id', 'in', data['partner_ids']))
            partners = self.env['res.partner'].search(partner_domain)
            if data['account_ids']:
                account_domain.append(('id', 'in', data['account_ids']))
            accounts = self.env['account.account'].search(account_domain)
            for partner in partners:
                for account in accounts:
                    if 'branch' in data:
                        opening = self.get_partner_credit_and_debit(partner.id, account.id, data['date_from'],data['branch'],data)
                    else:
                        opening = self.get_partner_credit_and_debit(partner.id, account.id, data['date_from'],branch=False,data=False)
                    if opening[0] or opening[1]:
                        if data['consolidate']:
                            if 'all' in datas:
                                if partner.id in datas['all']['data']:
                                    datas['all']['data'][partner.id]['credit'] += opening[0]
                                    datas['all']['data'][partner.id]['debit'] += opening[1]
                                else:
                                    datas['all']['data'][partner.id] = {
                                        'name': partner.name,
                                        'data': [],
                                        'credit': opening[0],
                                        'debit': opening[1],
                                    }
                            else:
                                datas['all'] = {
                                    'name': '',
                                    'data': {
                                        partner.id: {
                                            'name': partner.name,
                                            'data': [],
                                            'credit': opening[0],
                                            'debit': opening[1],
                                        }
                                    }
                                }
                        else:
                            if account.id in datas:
                                if partner.id in datas[account.id]['data']:
                                    datas[account.id]['data'][partner.id]['credit'] = opening[0]
                                    datas[account.id]['data'][partner.id]['debit'] = opening[1]
                                else:
                                    datas[account.id]['data'][partner.id] = {
                                        'name': partner.name,
                                        'data': [],
                                        'credit': opening[0],
                                        'debit': opening[1],
                                    }
                            else:
                                datas[account.id] = {
                                    'name': account.name,
                                    'data': {
                                        partner.id: {
                                            'name': partner.name,
                                            'data': [],
                                            'credit': opening[0],
                                            'debit': opening[1],
                                        }
                                    }
                                }

        return datas

    def get_partner_credit_and_debit(self, partner, account, date_from,branch,data):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            if partner:
                domain.append(('partner_id', '=', partner))
            if branch:
                domain.append(('move_id.branch_id', 'in', data['branch']))
            moves = self.env['account.move.line'].search(domain)
            opening_moves = self.env.company.account_opening_move_id
            if branch:
                opening_moves = self.env['account.move']
                branch_obj = self.env['res.branch']
                branches = branch_obj.search([('id', 'in', data['branch'])])
                if 'account_opening_move_id' in branch_obj._fields:
                    for branch in branches:
                        account_opening_move_id = branch.account_opening_move_id
                        if account_opening_move_id and account_opening_move_id.state == 'posted':
                            opening_moves += account_opening_move_id

            for opening_move in opening_moves:
                if opening_move and opening_move.date.strftime("%Y-%m-%d") == date_from:
                    for openline in opening_move.line_ids:
                        if openline.account_id.id == account and openline.partner_id.id == partner:
                            moves += openline
            for move in moves:
                credit += move.credit
                debit += move.debit
        return (credit, debit)

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(
            searchDateFrom=self.date_from.strftime('%Y-%m-%d'),
            searchDateTo=self.date_to.strftime('%Y-%m-%d'),
            report_account=self.account_ids.ids if self.account_ids else False,
            report_partner=self.partner_ids.ids if self.partner_ids else False,
            searchConsolidate=self.consolidate,
            report_branch=False
        )
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('partner_ledger.report_partner_ledger')._render({
            'lines': res['lines']['lines'],
            'date_from': res['lines']['date_from'],
            'date_to': res['lines']['date_to'],
            'data': res['lines']['data'],
            'accounts': res['lines']['accounts'],
            'partners': res['lines']['partners'],
            'with_initial_balance': res['lines']['with_initial_balance'],
            'branch_name': res['lines']['branch_name'],
        })
        self.template_area = res['lines']

    def _get_report_data(self, searchDateFrom=False, searchDateTo=False, report_account=False,report_partner=False, searchConsolidate=False,report_branch=False):
        if searchDateTo and searchDateFrom:
            if searchDateFrom > searchDateTo:
                raise Warning("From date can't be greater than To date")
        acc = []
        part = []
        if report_account:
            for account in report_account:
                acc.append(int(account))
        if report_partner:
            for partner in report_partner:
                part.append(int(partner))
        tk = self.env['account.account'].search([], order='name')
        partner = self.env['res.partner'].search([],order='name')
        account_name = self.env['account.account'].search([('id','in',acc)]).mapped('name')
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
            'account_ids': acc if acc else False,
            'partner_ids': part if part else False,
            'with_initial_balance': True,
            'account_names' : account_name,
            'consolidate': searchConsolidate
        }
        rep_branch = []
        if report_branch:
            for b in report_branch:
                rep_branch.append(int(b))
            branch_id = self.env['res.branch'].search([('id','in',rep_branch)])
            data['branch'] = branch_id.ids
            data['branch_name'] = ', '.join(branch_id.mapped('name'))
        is_branch = self.env['ir.model'].search([('model', '=', 'res.branch')])
        branches = {}
        branch_exists = False
        default_branch = []
        if is_branch:
            branch = self.env['res.branch'].search([('id','in',self.env.user.branch_ids.ids)])
            default_branch_id = self.env['res.branch'].search([('id','=',self.env.user.branch_id.ids)])
            default_branch = [default_branch_id.id,default_branch_id.name]
            for i in branch:
                if i.id != default_branch_id.id:
                    branches[i.id] = i.name
            branch_exists = True
        dat = self.get_report_values(data=data)
        do = {}
        for i in tk:
            do[i.id] = i.name
        partners = {}
        for i in partner:
            partners[i.id] = i.name
        return {
            'lines': dat,
        }

