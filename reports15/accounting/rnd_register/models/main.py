# ♦ Import ♦

from odoo import models, api, fields
from datetime import datetime, date
from odoo.exceptions import Warning, UserError


# ♦ R & D Report ♦
class ReportRndRegister(models.TransientModel):
    _name = 'rnd.register'
    _inherit = 'beta.reports'
    _description = 'R&D Register'

    date_from = fields.Date()
    date_to = fields.Date()
    order = fields.Selection([('alpha', 'Alphabetical'), ('schedule', 'Schedulewise')], default='alpha')
    with_balance = fields.Boolean()
    summary = fields.Boolean()
    two_side_report = fields.Boolean()
    fin_open = fields.Boolean()

    @api.onchange('with_balance','order')
    def onchange_with_balance(self):
        if not self.with_balance:
            self.fin_open = False
        if self.order == 'alpha':
            self.summary = False

    @api.model
    def default_get(self, fields_list):
        res = super(ReportRndRegister, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    def get_report_values(self, data=None):
        date_from = ''
        date_to = ''
        if data['date_from'] and data['date_to']:
            date_from = datetime.strptime(data['date_from'],"%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'],"%Y-%m-%d")
            date_from = date_from.strftime('%d/%m/%Y')
            date_to = date_to.strftime('%d/%m/%Y')
        if 'branch' in data:
            branch_name = data['branch_name']
        else:
            branch_name = ''
        return {
            'date_from': date_from,
            'date_to': date_to,
            'details': self.get_rnd_details(data),
            'with_balance': data['with_balance'],
            'branch_name': branch_name,
            'order': data['order'],
            'summary': data['summary'],
            'report': data['report'],
            'fin_open': data['fin_open'],
        }

        # ▼ Fully Settlement ▼
    def paid_or_not(self, inv):
        paid_or_not = False
        if inv.invoice_payments_widget != 'false' and inv.payment_state == 'paid':
            pay_json_value = inv.sudo()._get_reconciled_info_JSON_values()
            bill_type = True

            # ▼ if bill type is credit then fully settlement is False ▼
            if 'bill_type' in self.env['account.move']._fields:
                if inv.bill_type == 'credit':
                    bill_type = False

            type = "Cash"
            for pay in pay_json_value:
                if inv.invoice_date == pay['date'] and type == pay['journal_name'] and len(
                        pay_json_value) == 1 and bill_type:
                    self.env.cr.execute("select amount from account_payment where id=" + str(pay['account_payment_id']))
                    payment_amt = self.env.cr.fetchall()[0][0]
                    if inv.amount_total == payment_amt:
                        type = pay['journal_name']
                        paid_or_not = True
                    else:
                        paid_or_not = False
                else:
                    paid_or_not = False
                    break
        return paid_or_not

    def check_payment_invoice(self, payment):
        paid_or_not = False
        if len(payment.reconciled_invoice_ids) == 1:
            for inv in payment.reconciled_invoice_ids:
                paid_or_not = self.paid_or_not(inv)
        return paid_or_not

    def get_rnd_details(self, data):
        account_move_line_obj = self.env['account.move.line']
        cash_credit = cash_debit = debit_total = credit_total = 0
        records = {}
        domain = [('move_id.state', '=', 'posted'), ('move_id.date', '>=', data['date_from']), ('move_id.date', '<=', data['date_to'])]
        opening_move = self.env.company.account_opening_move_id
        if 'branch' in data:
            branch = self.env['res.branch'].search([('id', 'in', data['branch'])])
            if 'account_opening_move_id' in self.env['res.branch']:
                for branches in branch:
                    account_opening_move_id = branches.account_opening_move_id
                    if account_opening_move_id and account_opening_move_id.state == 'posted':
                        opening_move += account_opening_move_id

        if opening_move:
            domain.append(('move_id.id', 'not in', opening_move.ids))

        if 'branch' in data:
            domain.append(('move_id.branch_id', 'in', data['branch']))

        movelines = account_move_line_obj.search(domain)
        for line in movelines:
            type = line.move_id.move_type
            debit = line.debit
            credit = line.credit
            if type not in ['in_invoice','in_refund']:
                if line.payment_id:
                    fully_settled = self.check_payment_invoice(line.payment_id)
                    if fully_settled:
                        continue
                    else:
                        pass
                else:
                    fully_settled = self.paid_or_not(line.move_id)

                    if 'is_freight' in line._fields:
                        opo = not line.is_rounding_line and not line.is_freight
                    else:
                        opo = not line.is_rounding_line

                    if opo and (fully_settled and ((debit > 0 and type == "out_invoice") or (credit > 0 and type in ["out_refund","in_invoice"]))):
                        if line.is_rounding_line:
                            print("voucher no:", line.move_id.name, debit, credit, fully_settled)
                        if 'is_discount_line' in line._fields:
                            if not line.is_discount_line:
                                continue
                        else:
                            continue
            if line.account_id.id in data['cash_account_ids']:
                cash_credit += credit
                cash_debit += debit
            else:
                if line.account_id.id in records:
                    records[line.account_id.id]['credit'] += credit
                    records[line.account_id.id]['debit'] += debit
                else:
                    records[line.account_id.id] = {
                        'name': line.account_id.name,
                        'credit': credit,
                        'debit': debit,
                        'opening_credit': 0,
                        'opening_debit': 0,
                        'parent': line.account_id.user_type_id.name,
                    }
                credit_total += credit
                debit_total += debit
        details = {
            'debit_total': debit_total,
            'credit_total': credit_total,
            'cash_debit_opening': 0,
            'cash_credit_opening': 0,
            'cash_opening': 0,
            'cash_first_opening': 0,
        }
        if data['with_balance']:
            domain = [('code', '!=', str(999999)),('id', 'not in', data['cash_account_ids'])]
            accounts = self.env['account.account'].search(domain)
            for account in accounts:
                if 'branch' in data:
                    opening = self.get_rnd_credit_and_debit(account.id, data['date_from'],data['fin_open'],data['branch'])
                else:
                    opening = self.get_rnd_credit_and_debit(account.id, data['date_from'],data['fin_open'],branch=False,)
                if opening[0] or opening[1]:
                    if account.id in records:
                        records[account.id]['opening_credit'] = opening[1]
                        records[account.id]['opening_debit'] = opening[0]
                    else:
                        records[account.id] = {
                            'name': account.name,
                            'data': [],
                            'credit': 0,
                            'debit': 0,
                            'opening_credit': opening[1],
                            'opening_debit': opening[0],
                            'parent': account.user_type_id.name,
                        }
        for cash_account in data['cash_account_ids']:
            if 'branch' in data:
                cash_opening = self.get_rnd_credit_and_debit(cash_account, data['date_from'],True,data['branch'])
            else:
                cash_opening = self.get_rnd_credit_and_debit(cash_account, data['date_from'],True, branch=False)
            details['cash_credit_opening'] += cash_opening[1]
            details['cash_debit_opening'] += cash_opening[0]
        details['cash_first_opening'] = self.get_first_cash_opening(data['cash_account_ids'],data['date_from'],data['fin_open'],data)
        details['cash_opening'] = abs(details['cash_credit_opening'] - details['cash_debit_opening'])
        details['cash_closing'] = (credit_total - debit_total + details['cash_opening'])
        sorted_dict = {}
        if data['order'] == 'alpha':
            sorted_values = sorted(records, key=lambda x: (records[x]['name']))
            for i in sorted_values:
                sorted_dict[i] = records[i]
        else:
            sorted_values = sorted(records, key=lambda x: (records[x]['parent'],records[x]['name']))
            parent = []

            total = []
            a = 0

            for i in sorted_values:
                if records[i]['parent'] not in sorted_dict:
                    if records[i]['parent'] not in parent:
                        parent.append(records[i]['parent'])
            for a in parent:
                total_debit = 0
                total_credit = 0
                tot_opening_credit = 0
                tot_opening_debit = 0
                l = 0
                while l < len(sorted_values):
                    s = str(sorted_values[l]).strip("[]")
                    h = int(s)
                    if a == records[h]['parent']:
                        total_debit += records[h]['debit']
                        total_credit += records[h]['credit']
                        tot_opening_debit += records[h]['opening_debit']
                        tot_opening_credit += records[h]['opening_credit']
                        head = records[h]['parent']
                    else:
                        pass
                    l = l + 1

                total.append({
                    'head': head,
                    'total_debit': total_debit,
                    'total_credit': total_credit,
                    'tot_opening_credit': tot_opening_credit,
                    'tot_opening_debit': tot_opening_debit
                })
            k = 0
            for i in sorted_values:
                if records[i]['parent'] not in sorted_dict:
                    k = k + 1
                    id1 = "debit" + str(k)
                    id2 = "credit" + str(k)
                    for ma in total:
                        if ma['head'] == records[i]['parent']:
                            sorted_dict[records[i]['parent']] = {
                                    'name': records[i]['parent'],
                                    'credit': ma['total_credit'],
                                    'debit': ma['total_debit'],
                                    'opening_credit':ma['tot_opening_credit'],
                                    'opening_debit':ma['tot_opening_debit'],
                                    'linetotal_debit': ma['tot_opening_credit'] + ma['total_debit'],
                                    'linetotal_credit': ma['tot_opening_debit'] + ma['total_credit'],
                                    'id1': id1,
                                    'id2':id2,
                                    'parent': 'NIL'}
                sorted_dict[i] = records[i]
        details['records'] = sorted_dict
        return details

    def get_rnd_credit_and_debit(self, account, date_from,fin_open,branch):
        credit = debit = 0

        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id','=',account)])
            selected_year = datetime.strptime(str(date_from), '%Y-%m-%d')
            date_f = datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            date_fr = datetime.strptime(str(date_f), '%d-%m-%Y').date()
            if fin_open:
                if not account_id.user_type_id.include_initial_balance:
                    if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                        fin_date = str(selected_year.year-1) + '-04-01'
                    else:
                        fin_date = str(selected_year.year) + '-04-01'
                    domain.append(('date','>=',fin_date))
            else:
                if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                    fin_date = str(selected_year.year - 1) + '-04-01'
                else:
                    fin_date = str(selected_year.year) + '-04-01'
                domain.append(('date', '>=', fin_date))
            if branch:
                domain.append(('move_id.branch_id', 'in', branch))
            moves = self.env['account.move.line'].search(domain)
            if fin_open:
                opening_move = self.env.company.account_opening_move_id
                if branch:
                    branch_id = self.env['res.branch'].search([('id','in',branch)])
                    if 'account_opening_move_id' in self.env['res.branch']:
                        for b in branch_id:
                            account_opening_move_id = b.account_opening_move_id
                            opening_move = account_opening_move_id
                            if opening_move and opening_move.state == 'posted' and opening_move.date.strftime("%Y-%m-%d") == date_from:
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

    def get_opening_credit_debit(self, account, date_from,data):
        credit = debit = 0
        if date_from:
            opening_move = self.env.company.account_opening_move_id
            if 'branch' in data:
                branch = self.env['res.branch'].search([('id', 'in', data['branch'])])
                if 'account_opening_move_id' in self.env['res.branch']:
                    for branches in branch:
                        account_opening_move_id = branches.account_opening_move_id
                        opening_move += account_opening_move_id

            domain = [('move_id.id','not in',opening_move.ids),('move_id.state', '=', 'posted'),('move_id.date','<',date_from),('account_id','=', account)]

            if 'branch' in data:
                domain.append(('move_id.branch_id', 'in', data['branch']))
            moves = self.env['account.move.line'].search(domain)
            for move in moves:
                credit += move.credit
                debit += move.debit
        return (credit, debit)

    def get_first_cash_opening(self, cash_accounts, date_from, fin_open, data):

        credit = debit = 0
        if date_from:
            opening_move = self.env.company.account_opening_move_id
            selected_year = datetime.strptime(str(date_from), '%Y-%m-%d')
            date_f = datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            date_fr = datetime.strptime(str(date_f), '%d-%m-%Y').date()
            if 'branch' in data:
                branch = self.env['res.branch'].search([('id', 'in', data['branch'])])
                if 'account_opening_move_id' in self.env['res.branch']:
                    for branches in branch:
                        account_opening_move_id = branches.account_opening_move_id
                        opening_move += account_opening_move_id

            domain = [('move_id.id','in',opening_move.ids),('move_id.state', '=', 'posted'), ('account_id', 'in', cash_accounts),('date','!=', date_from)]
            if not fin_open:
                if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                    fin_date = str(selected_year.year - 1) + '-04-01'
                else:
                    fin_date = str(selected_year.year) + '-04-01'
                domain.append(('date', '>=', fin_date))
            if 'branch' in data:
                domain.append(('move_id.branch_id', 'in', data['branch']))
            moves = self.env['account.move.line'].search(domain)
            for move in moves:
                credit += move.credit
                debit += move.debit
        return abs(credit - debit)

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(
            searchDateFrom=self.date_from.strftime('%Y-%m-%d'),
            searchDateTo=self.date_to.strftime('%Y-%m-%d'),
            searchOrder=self.order,
            withBalance=self.with_balance,
            report_branch=False,
            summary=self.summary,
            report=self.two_side_report,
            fin_open=self.fin_open,
        )
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('rnd_register.report_rnd_register')._render({
            'date_from': res['lines']['date_from'],
            'date_to': res['lines']['date_to'],
            'details': res['lines']['details'],
            'with_balance': res['lines']['with_balance'],
            'branch_name': res['lines']['branch_name'],
            'order': res['lines']['order'],
            'summary': res['lines']['summary'],
            'report': res['lines']['report'],
            'fin_open':res['lines']['fin_open'],
        })

        self.template_area = res['lines']

    def _get_report_data(self, searchDateFrom=False, searchDateTo=False, searchOrder=False, withBalance=False, report_branch=False, summary=False, report=False, fin_open=False):
        if searchDateTo and searchDateFrom:
            if searchDateFrom > searchDateTo:
                raise Warning("From date can't be greater than To date")
        cash_journal_ids = self.env['account.journal'].search([('type', '=', 'cash')])
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
            'cash_account_ids': cash_journal_ids.ids,
            'order': searchOrder,
            'with_balance': withBalance,
            'summary': summary,
            'report': report,
            'fin_open': fin_open,
        }
        cash_journal_ids = self.env['account.journal'].search([('type', '=', 'cash')])
        cash_ids = []
        for journal in cash_journal_ids:
            cash_ids.append(journal.default_account_id.id)
            cash_ids.append(journal.loss_account_id.id)
            cash_ids.append(journal.profit_account_id.id)
        data['cash_account_ids'] = cash_ids

        rep_branch = []
        if report_branch:
            for b in report_branch:
                rep_branch.append(int(b))
            branch_id = self.env['res.branch'].search([('id', 'in', rep_branch)])
            data['branch'] = branch_id.ids
            data['branch_name'] = ', '.join(branch_id.mapped('name'))
        is_branch = self.env['ir.model'].search([('model', '=', 'res.branch')])
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
        return {
            'lines': dat,
        }

