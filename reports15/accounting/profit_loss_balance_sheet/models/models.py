# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import pytz


class BetaProfitLossBalanceSheet(models.TransientModel):  # change this
    _name = 'beta.profit.loss.balance.sheet'  # change this
    _inherit = 'beta.reports'

    name = fields.Char()  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    with_opening = fields.Boolean()
    summary = fields.Boolean()
    month_wise = fields.Boolean()
    report_type = fields.Selection([('profit_loss', 'Profit & Loss'), ('balance_sheet', 'Balance Sheet')])

    @api.model
    def default_get(self, fields_list):
        res = super(BetaProfitLossBalanceSheet, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today
        return res

    def get_report_values(self, data=None):
        months = []
        date_prev = data['date_from']
        if data['monthwise']:
            if data['date_from']:
                start_d = data['date_from']
                end_d = data['date_to']
                date10 = str(start_d)
                date11 = str(end_d)
                d10 = datetime.strptime(date10, "%Y-%m-%d")
                d11 = datetime.strptime(date11, "%Y-%m-%d")
                if d10.year == d11.year:
                    months_count = abs(int(d10.month) - int(d11.month))
                else:
                    months_count = abs(int(d10.month) - (12 + int(d11.month)))
                m = 1
                for i in range(months_count + 1):
                    if m != 1:
                        d10 = d10 + relativedelta(months=1)
                    m10 = d10.strftime('%B')
                    y10 = str(d10.year)
                    month10 = m10 + '-' + y10
                    months.append(month10)
                    m += 1
        ctx = {
            'data': None,
            'account_report': data['context']['default_account_report_id'],
            'tot': None,
            'rows': None,
            'g_tot': None,
            'final_list': None,
            'table': None,
            'table2': None,
            'branch_name': None,
            'monthwise': data['monthwise'],
            'summary': data['summary'],
            'order': data['order'],
            'months': months
        }

        if data['date_from'] and data['date_to']:
            account_report = self.env['account.financial.report'].search([
                ('id', '=', data['context']['default_account_report_id'])
            ])
            data['report_name'] = account_report.name
            childs = self.get_child(account_report, account_report.account_type_ids)
            dom = [('move_id.state', '=', 'posted')]
            if data['date_from']:
                dom.append(('move_id.date', '>=', data['date_from']))
            if data['date_to']:
                dom.append(('move_id.date', '<=', data['date_to']))
            if data.get('allowed_company_ids'):
                dom.append(('company_id', 'in', data.get('allowed_company_ids')))
            if 'branch' in data:
                dom.append(('move_id.branch_id', 'in', data['branch']))
            r_type = data['context']['default_account_report_id']
            if 'branch' in data:
                if data['order']:
                    linedata = self.get_report_template_data(set(childs), account_report, dom, r_type,
                                                             data['date_from'], data['without_opening'],
                                                             data['monthwise'], data['branch'], data['order'])
                else:
                    linedata = self.get_report_template_data(set(childs), account_report, dom, r_type,
                                                             data['date_from'], data['without_opening'],
                                                             data['monthwise'], data['branch'], False)
            else:
                linedata = self.get_report_template_data(set(childs), account_report, dom, r_type, data['date_from'],
                                                         data['without_opening'], data['monthwise'], False, False)
            typ = ['Gross Profit B/d', 'Gross Loss B/d']
            debit_data = linedata[0]  # +ve
            credit_data = linedata[1]  # -ve
            deb_row, cre_row = linedata[4], linedata[5]
            debit_tot = linedata[2]  # +ve
            credit_tot = linedata[3]  # -ve
            data['months'] = months
            trading_data = self.get_trad_acc_dat(dom, data)
            prev_rep_val = trading_data or 0
            if data['context']['default_account_report_id'] == 8:
                typ = ['Net Profit', 'Net Loss']
                profit_data = self.get_prof_acc_dat(dom)
                if data['date_to']:
                    inv_closing = self.get_opening_closing(data['date_to'], data)
                    debit_data['cl_stk'] = {'name': 'Closing Stock A/C', 'balance': inv_closing, 'child': {}}
                    debit_tot += inv_closing
                prev_rep_val += profit_data

            if not data['monthwise']:
                if prev_rep_val > 0:
                    debit_data['gp'] = {'name': typ[1], 'balance': prev_rep_val, 'child': {}}
                    debit_tot += prev_rep_val
                    deb_row += 1
                elif prev_rep_val < 0:
                    credit_data['gl'] = {'name': typ[0], 'balance': prev_rep_val, 'child': {}}
                    credit_tot += prev_rep_val
                    cre_row += 1
            else:
                val = {}
                val['profit'] = {}
                val['loss'] = {}
                profit = False
                loss = False
                for i in prev_rep_val:
                    val['profit'][i] = {'i': 0}
                    val['loss'][i] = {'i': 0}
                    if prev_rep_val[i]['month_total'] > 0:
                        profit = True
                        if 'profit' in val:
                            if i in val['profit']:
                                val['profit'][i]['i'] += prev_rep_val[i]['month_total']
                    else:
                        loss = True
                        if 'loss' in val:
                            if i in val['loss']:
                                val['loss'][i]['i'] += prev_rep_val[i]['month_total']
                if profit:
                    debit_data['gp'] = {'name': typ[1], 'balance': val['profit'], 'child': {}}
                    for m in months:
                        if m in debit_tot:
                            if m in val['profit']:
                                debit_tot[m]['month_debit'] += val['profit'][m]['i']
                            else:
                                debit_tot[m]['month_debit'] += 0
                        else:
                            if m in val['profit']:
                                debit_tot[m] = {'month_debit': val['profit'][m]['i']}
                            else:
                                debit_tot[m] = {'month_debit': 0}
                    deb_row += 1
                if loss:
                    credit_data['gl'] = {'name': typ[0], 'balance': val['loss'], 'child': {}}
                    for m in months:
                        if m in credit_tot:
                            if m in val['loss']:
                                credit_tot[m]['month_credit'] += val['loss'][m]['i']
                            else:
                                credit_tot[m]['month_credit'] += 0
                        else:
                            if m in val['loss']:
                                credit_tot[m] = {'month_credit': val['loss'][m]['i']}
                            else:
                                credit_tot[m] = {'month_credit': 0}
                    cre_row += 1
            table = []
            table2 = []
            ii = 0
            j = 0
            h = 0
            k = 0
            r = 0
            y = 0

            if data['summary']:
                direction = 'right'
            else:
                direction = 'down'

            credit_total = []
            debit_total = []
            bc_total = []
            bd_total = []
            for credit_key in list(credit_data.keys()):
                c_total = 0
                cm_total = {}
                if credit_data[credit_key].get('child'):
                    for child in credit_data[credit_key]['child']:
                        if 'branch' in data:
                            if len(data['branch']) == 1:
                                if not data['monthwise']:
                                    c_total += credit_data[credit_key]['child'][child]['balance'] * -1
                                else:
                                    for m in months:
                                        if m in credit_data[credit_key]['child'][child]:
                                            if credit_key in cm_total:
                                                if m in cm_total[credit_key]:
                                                    cm_total[credit_key][m]['month_bal'] += (
                                                            credit_data[credit_key]['child'][child][m][
                                                                'month_balance'] * -1) if \
                                                        credit_data[credit_key]['child'][child][m][
                                                            'month_balance'] * -1 > 0 else 0
                                                else:
                                                    cm_total[credit_key][m] = {
                                                        'month_bal': (credit_data[credit_key]['child'][child][m][
                                                                          'month_balance'] * -1) if
                                                        credit_data[credit_key]['child'][child][m][
                                                            'month_balance'] * -1 > 0 else 0}
                                            else:
                                                cm_total[credit_key] = {m: {'month_bal': (
                                                        credit_data[credit_key]['child'][child][m][
                                                            'month_balance'] * -1) if
                                                credit_data[credit_key]['child'][child][m][
                                                    'month_balance'] * -1 > 0 else 0}}

                            else:
                                if data['order'] == 'branch_account':
                                    cb_total = 0
                                    cbm_total = {}
                                    for i in credit_data[credit_key]['child'][child]:
                                        if not data['monthwise']:
                                            c_total += credit_data[credit_key]['child'][child][i]['balance'] * -1
                                            cb_total += credit_data[credit_key]['child'][child][i]['balance'] * -1
                                        else:
                                            for m in months:
                                                if m in credit_data[credit_key]['child'][child][i]:
                                                    if credit_key in cm_total:
                                                        if m in cm_total[credit_key]:
                                                            cm_total[credit_key][m]['month_bal'] += (
                                                                    credit_data[credit_key]['child'][child][i][m][
                                                                        'month_balance'] * -1) if \
                                                                credit_data[credit_key]['child'][child][i][m][
                                                                    'month_balance'] * -1 > 0 else 0.00
                                                        else:
                                                            cm_total[credit_key][m] = {
                                                                'month_bal': (
                                                                        credit_data[credit_key]['child'][child][i][
                                                                            m]['month_balance'] * -1) if
                                                                credit_data[credit_key]['child'][child][i][m][
                                                                    'month_balance'] * -1 > 0 else 0.00}
                                                    else:
                                                        cm_total[credit_key] = {m: {'month_bal': (
                                                                credit_data[credit_key]['child'][child][i][m][
                                                                    'month_balance'] * -1) if
                                                        credit_data[credit_key]['child'][child][i][m][
                                                            'month_balance'] * -1 > 0 else 0.00}}
                                                    if credit_key in cbm_total:
                                                        if m in cbm_total[credit_key]:
                                                            cbm_total[credit_key][m]['month_bal'] += (
                                                                    credit_data[credit_key]['child'][child][i][m][
                                                                        'month_balance'] * -1) if \
                                                                credit_data[credit_key]['child'][child][i][m][
                                                                    'month_balance'] * -1 > 0 else 0.00
                                                        else:
                                                            cbm_total[credit_key][m] = {'month_bal': (
                                                                    credit_data[credit_key]['child'][child][i][m][
                                                                        'month_balance'] * -1) if
                                                            credit_data[credit_key]['child'][child][i][m][
                                                                'month_balance'] * -1 > 0 else 0.00}
                                                    else:

                                                        cbm_total[credit_key] = {m: {'month_bal': (
                                                                credit_data[credit_key]['child'][child][i][m][
                                                                    'month_balance'] * -1) if
                                                        credit_data[credit_key]['child'][child][i][m][
                                                            'month_balance'] * -1 > 0 else 0.00}}
                                    if not data['monthwise']:
                                        bc_total.append({'type': credit_data[credit_key]['name'], 'branch': child,
                                                         'total': cb_total})
                                    else:
                                        cmb = []
                                        for m in months:
                                            if m in cbm_total[credit_key]:
                                                cmb.append(cbm_total[credit_key][m]['month_bal'])
                                            else:
                                                cmb.append(0.00)
                                        bc_total.append(
                                            {'type': credit_data[credit_key]['name'], 'branch': child, 'total': cmb})
                                else:
                                    if not data['monthwise']:
                                        c_total += credit_data[credit_key]['child'][child]['balance'] * -1
                                    else:
                                        for m in months:
                                            if m in credit_data[credit_key]['child'][child]:
                                                if credit_key in cm_total:
                                                    if m in cm_total[credit_key]:

                                                        cm_total[credit_key][m]['month_bal'] += (
                                                                credit_data[credit_key]['child'][child][m][
                                                                    'month_balance'] * -1) if \
                                                            credit_data[credit_key]['child'][child][m][
                                                                'month_balance'] * -1 > 0 else 0
                                                    else:
                                                        cm_total[credit_key][m] = {
                                                            'month_bal': (credit_data[credit_key]['child'][child][m][
                                                                              'month_balance'] * -1) if
                                                            credit_data[credit_key]['child'][child][m][
                                                                'month_balance'] * -1 > 0 else 0}
                                                else:
                                                    cm_total[credit_key] = {m: {
                                                        'month_bal': (credit_data[credit_key]['child'][child][m][
                                                                          'month_balance'] * -1) if
                                                        credit_data[credit_key]['child'][child][m][
                                                            'month_balance'] * -1 > 0 else 0}}

                        else:
                            if not data['monthwise']:
                                c_total += credit_data[credit_key]['child'][child]['balance'] * -1
                            else:
                                for m in months:
                                    if m in credit_data[credit_key]['child'][child]:
                                        if credit_key in cm_total:
                                            if m in cm_total[credit_key]:
                                                cm_total[credit_key][m]['month_bal'] += (
                                                        credit_data[credit_key]['child'][child][m][
                                                            'month_balance'] * -1) if \
                                                    credit_data[credit_key]['child'][child][m][
                                                        'month_balance'] * -1 > 0 else 0
                                            else:
                                                cm_total[credit_key][m] = {
                                                    'month_bal': (credit_data[credit_key]['child'][child][m][
                                                                      'month_balance'] * -1) if
                                                    credit_data[credit_key]['child'][child][m][
                                                        'month_balance'] * -1 > 0 else 0}
                                        else:
                                            cm_total[credit_key] = {m: {
                                                'month_bal': (credit_data[credit_key]['child'][child][m][
                                                                  'month_balance'] * -1) if
                                                credit_data[credit_key]['child'][child][m][
                                                    'month_balance'] * -1 > 0 else 0}}

                    if not data['monthwise']:
                        credit_total.append({'type': credit_data[credit_key]['name'], 'total': c_total})
                    else:
                        cml = []
                        for m in months:
                            if m in cm_total[credit_key]:
                                cml.append(cm_total[credit_key][m]['month_bal'])
                            else:
                                cml.append(0.00)
                        credit_total.append({'type': credit_data[credit_key]['name'], 'total': cml})

            for credit_key in list(credit_data.keys()):
                if credit_data[credit_key].get('child'):
                    ii = ii + 1
                    id1 = "credit" + str(ii)

                    balance = 0
                    for cr in credit_total:
                        if cr['type'] == credit_data[credit_key]['name']:
                            balance = cr['total']
                    if not data['monthwise']:
                        table.append([
                            '<td class="parent" id="' + id1 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 15px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' + credit_data[credit_key]['name'] + '</td>',
                            '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str("{:.2f}".format(balance)) + '</td>'
                        ])
                    else:
                        b = ''
                        for i in balance:

                            if i > 0:
                                b += '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str("{:.2f}".format(i)) + '</td>'
                            else:
                                b += '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">&#160;</td>'
                        table.append(
                            [
                                '<td class="parent" id="' + id1 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 15px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' + credit_data[credit_key]['name'] + '</td>', b
                            ])

                    for child in credit_data[credit_key]['child']:
                        if 'branch' in data:
                            if len(data['branch']) == 1:
                                res_id = str(credit_data[credit_key]['child'][child]['account_id'])
                                if data['summary']:
                                    if not data['monthwise']:
                                        table.append(
                                            [
                                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                                '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' +
                                                str("{:.2f}".format(
                                                    credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                                        )
                                    else:
                                        q = ''
                                        for m in months:
                                            if m in credit_data[credit_key]['child'][child]:
                                                if credit_data[credit_key]['child'][child][m]['month_balance'] * -1 > 0:
                                                    q += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' + str(
                                                        "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                            'month_balance'] * -1)) + '</td>'
                                                else:
                                                    q += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                            else:
                                                q += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'

                                        table.append(
                                            [
                                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                credit_data[credit_key]['child'][child]['name'] + '</a></td>', q
                                            ]
                                        )


                                else:
                                    if not data['monthwise']:
                                        table.append(
                                            [
                                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                                '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">' +
                                                str("{:.2f}".format(
                                                    credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                                        )
                                    else:
                                        d = ''
                                        for m in months:
                                            if m in credit_data[credit_key]['child'][child]:
                                                if credit_data[credit_key]['child'][child][m]['month_balance'] * -1 > 0:
                                                    d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">' + str(
                                                        "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                            'month_balance'] * -1)) + '</td>'
                                                else:
                                                    d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                            else:
                                                d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                        table.append(
                                            [
                                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                credit_data[credit_key]['child'][child]['name'] + '</a></td>', d
                                            ]
                                        )

                            else:
                                if data['order'] == 'branch_account':
                                    h = h + 1
                                    id3 = "bcredit" + str(h)
                                    branch = self.env['res.branch'].search([('id', '=', child)]).name
                                    branch_tot = 0
                                    for cb in bc_total:
                                        if cb['type'] == credit_data[credit_key]['name']:
                                            if cb['branch'] == child:
                                                branch_tot = cb['total']
                                    if data['summary']:
                                        if not data['monthwise']:
                                            table.append([
                                                '<td class="parent child-' + id1 + '" id="' + id3 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                branch + '</td>',
                                                '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">' + str(
                                                    "{:.2f}".format(branch_tot)) + '</td>'])
                                        else:
                                            f = ''
                                            for i in branch_tot:
                                                if i > 0:
                                                    f += '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">' + str(
                                                        "{:.2f}".format(i)) + '</td>'
                                                else:
                                                    f += '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">&#160;</td>'
                                            table.append([
                                                '<td class="parent child-' + id1 + '" id="' + id3 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                branch + '</td>', f
                                            ])

                                    else:
                                        if not data['monthwise']:
                                            table.append([
                                                '<td class="parent child-' + id1 + '" id="' + id3 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                branch + '</td>',
                                                '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                                    "{:.2f}".format(branch_tot)) + '</td>'])
                                        else:
                                            f = ''
                                            for i in branch_tot:
                                                if i > 0:
                                                    f += '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                                        "{:.2f}".format(i)) + '</td>'
                                                else:
                                                    f += '<td class="text-right child-' + id1 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">&#160;</td>'
                                            table.append([
                                                '<td class="parent child-' + id1 + '" id="' + id3 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                branch + '</td>', f
                                            ])

                                    for i in credit_data[credit_key]['child'][child]:
                                        res_id = str(credit_data[credit_key]['child'][child][i]['account_id'])
                                        if data['summary']:

                                            if not data['monthwise']:
                                                table.append(
                                                    [
                                                        '<td class="child-' + id3 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action"   data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        credit_data[credit_key]['child'][child][i][
                                                            'name'] + '</a></td>',
                                                        '<td class="text-right child-' + id3 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' +
                                                        str("{:.2f}".format(
                                                            credit_data[credit_key]['child'][child][i][
                                                                'balance'] * -1)) + '</td>']
                                                )
                                            else:
                                                g = ''
                                                for m in months:
                                                    if m in credit_data[credit_key]['child'][child][i]:
                                                        if credit_data[credit_key]['child'][child][i][m][
                                                            'month_balance'] * -1 > 0.00:
                                                            g += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' + str(
                                                                "{:.2f}".format(
                                                                    credit_data[credit_key]['child'][child][i][m][
                                                                        'month_balance'] * -1)) + '</td>'
                                                        else:
                                                            g += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                                    else:
                                                        g += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'

                                                table.append(
                                                    [
                                                        '<td class="child-' + id3 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action"   data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        credit_data[credit_key]['child'][child][i][
                                                            'name'] + '</a></td>', g
                                                    ]
                                                )

                                        else:
                                            if not data['monthwise']:
                                                table.append(
                                                    [
                                                        '<td class="child-' + id3 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        credit_data[credit_key]['child'][child][i][
                                                            'name'] + '</a></td>',
                                                        '<td class="text-right child-' + id3 + '"style="padding-right: 10px;border-right:1px solid;">' +
                                                        str("{:.2f}".format(
                                                            credit_data[credit_key]['child'][child][i][
                                                                'balance'] * -1)) + '</td>']
                                                )
                                            else:
                                                e = ''
                                                for m in months:
                                                    if m in credit_data[credit_key]['child'][child][i]:
                                                        if credit_data[credit_key]['child'][child][i][m][
                                                            'month_balance'] * -1 > 0:
                                                            e += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;border-right:1px solid;">' + str(
                                                                "{:.2f}".format(
                                                                    credit_data[credit_key]['child'][child][i][m][
                                                                        'month_balance'] * -1)) + '</td>'
                                                        else:
                                                            e += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                                    else:
                                                        e += '<td class="text-right child-' + id3 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                                table.append(
                                                    [
                                                        '<td class="child-' + id3 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        credit_data[credit_key]['child'][child][i][
                                                            'name'] + '</a></td>', e
                                                    ]
                                                )

                                else:
                                    res_id = str(credit_data[credit_key]['child'][child]['account_id'])
                                    r = r + 1
                                    id5 = "bcredit2" + str(r)
                                    if data['summary']:
                                        if not data['monthwise']:
                                            table.append(
                                                [
                                                    '<td class="parent child-' + id1 + '" id="' + id5 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                                    '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;cursor: pointer;">' +
                                                    str("{:.2f}".format(
                                                        credit_data[credit_key]['child'][child][
                                                            'balance'] * -1)) + '</td>']
                                            )
                                        else:
                                            h = ''
                                            for m in months:
                                                if m in credit_data[credit_key]['child'][child]:
                                                    if credit_data[credit_key]['child'][child][m][
                                                        'month_balance'] * -1 > 0:
                                                        h += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;cursor: pointer;">' + str(
                                                            "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                                'month_balance'] * -1)) + '</td>'
                                                    else:
                                                        h += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;cursor: pointer;">&#160;</td>'
                                                else:
                                                    h += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;cursor: pointer;">&#160;</td>'
                                            table.append(
                                                [
                                                    '<td class="parent child-' + id1 + '" id="' + id5 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    credit_data[credit_key]['child'][child]['name'] + '</a></td>', h
                                                ]
                                            )

                                    else:
                                        if not data['monthwise']:
                                            table.append(
                                                [
                                                    '<td class="parent child-' + id1 + '" id="' + id5 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-right" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                                    '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;cursor: pointer;">' +
                                                    str("{:.2f}".format(
                                                        credit_data[credit_key]['child'][child][
                                                            'balance'] * -1)) + '</td>']
                                            )
                                        else:
                                            t = ''
                                            for m in months:
                                                if m in credit_data[credit_key]['child'][child]:
                                                    if credit_data[credit_key]['child'][child][m][
                                                        'month_balance'] * -1 > 0:
                                                        t += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;cursor: pointer;">' + str(
                                                            "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                                'month_balance'] * -1)) + '</td>'
                                                    else:
                                                        t += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;cursor: pointer;">&#160;</td>'
                                                else:
                                                    t += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;cursor: pointer;">&#160;</td>'
                                            table.append(
                                                [
                                                    '<td class="parent child-' + id1 + '" id="' + id5 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-right" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    credit_data[credit_key]['child'][child]['name'] + '</a></td>', t
                                                ]
                                            )

                                    for z in credit_data[credit_key]['child'][child]['branch']:
                                        if data['summary']:
                                            if not data['monthwise']:
                                                table.append(
                                                    [
                                                        '<td class="child-' + id5 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;">' +
                                                        credit_data[credit_key]['child'][child]['branch'][z][
                                                            'branch_name'] + '</td>',
                                                        '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;">' +
                                                        str("{:.2f}".format(
                                                            credit_data[credit_key]['child'][child]['branch'][z][
                                                                'branch_balance'] * -1)) + '</td>']
                                                )
                                            else:
                                                e = ''
                                                for m in months:
                                                    if m in credit_data[credit_key]['child'][child]['branch'][z]:
                                                        if credit_data[credit_key]['child'][child]['branch'][z][m][
                                                            'month_balance'] * -1 > 0:
                                                            e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;">' + str(
                                                                "{:.2f}".format(
                                                                    credit_data[credit_key]['child'][child]['branch'][
                                                                        z][m]['month_balance'] * -1)) + '</td>'
                                                        else:
                                                            e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                                    else:
                                                        e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                                table.append(
                                                    [
                                                        '<td class="child-' + id5 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;">' +
                                                        credit_data[credit_key]['child'][child]['branch'][z][
                                                            'branch_name'] + '</td>', e
                                                    ]
                                                )
                                        else:
                                            e = ''
                                            for m in months:
                                                if m in credit_data[credit_key]['child'][child]['branch'][z]:
                                                    if credit_data[credit_key]['child'][child]['branch'][z][m]['month_balance'] * -1 > 0:
                                                        e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;display:none;padding-right: 10px;border-right:1px solid;">' + str(
                                                            "{:.2f}".format(
                                                                credit_data[credit_key]['child'][child]['branch'][z][m][
                                                                    'month_balance'] * -1)) + '</td>'
                                                    else:
                                                        e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;display:none;padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                                else:
                                                    e += '<td class="text-right child-' + id5 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;display:none;padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                            table.append(
                                                [
                                                    '<td class="child-' + id5 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;display:none;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                                                    credit_data[credit_key]['child'][child]['branch'][z][
                                                        'branch_name'] + '</td>', e
                                                ]
                                            )


                        else:
                            res_id = str(credit_data[credit_key]['child'][child]['account_id'])
                            if data['summary']:
                                if not data['monthwise']:
                                    table.append(
                                        [
                                            '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                            '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' +
                                            str("{:.2f}".format(
                                                credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                                    )
                                else:
                                    d = ''
                                    for m in months:
                                        if m in credit_data[credit_key]['child'][child]:
                                            if credit_data[credit_key]['child'][child][m]['month_balance'] * -1 > 0:
                                                d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">' + str(
                                                    "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                        'month_balance'] * -1)) + '</td>'
                                            else:
                                                d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                        else:
                                            d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right:1px solid;">&#160;</td>'
                                    table.append(
                                        [
                                            '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action"  data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data['date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            credit_data[credit_key]['child'][child]['name'] + '</a></td>', d
                                        ]
                                    )

                            else:
                                if not data['monthwise']:
                                    table.append(
                                        [
                                            '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                            '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">' +
                                            str("{:.2f}".format(
                                                credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                                    )
                                else:
                                    d = ''
                                    for m in months:
                                        if m in credit_data[credit_key]['child'][child]:
                                            if credit_data[credit_key]['child'][child][m]['month_balance'] * -1 > 0:
                                                d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">' + str(
                                                    "{:.2f}".format(credit_data[credit_key]['child'][child][m][
                                                                        'month_balance'] * -1)) + '</td>'
                                            else:
                                                d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'
                                        else:
                                            d += '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right:1px solid;">&#160;</td>'

                                    table.append(
                                        [
                                            '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            credit_data[credit_key]['child'][child]['name'] + '</a></td>', d
                                        ]
                                    )


                else:
                    if not data['monthwise']:
                        table.append([
                            '<td style="font-weight:bold;padding-left: 15px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                            credit_data[credit_key]['name'],
                            '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">' +
                            str("{:.2f}".format(credit_data[credit_key]['balance'] * -1)) if credit_data[
                                credit_key].get(
                                'balance') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">0.00</td>'
                        ])
                    else:
                        c = ''
                        for m in months:
                            if m in val['loss']:
                                c += '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">' + str(
                                    "{:.2f}".format(val['loss'][m]['i'] * -1)) if val['loss'][m].get(
                                    'i') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">&#160;</td>'
                            else:
                                c += '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">;&#160;</td>'

                        table.append([
                            '<td style="font-weight:bold;padding-left: 15px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                            credit_data[credit_key]['name'], c

                        ])
            for debit_key in list(debit_data.keys()):
                d_total = 0
                dm_total = {}
                if debit_data[debit_key].get('child'):
                    for child2 in debit_data[debit_key]['child']:
                        if 'branch' in data:
                            if len(data['branch']) == 1:
                                if not data['monthwise']:
                                    d_total += debit_data[debit_key]['child'][child2]['balance']
                                else:
                                    for m in months:
                                        if m in debit_data[debit_key]['child'][child2]:
                                            if debit_key in dm_total:
                                                if m in dm_total[debit_key]:
                                                    dm_total[debit_key][m]['month_bal'] += \
                                                        debit_data[debit_key]['child'][child2][m]['month_balance'] if \
                                                            debit_data[debit_key]['child'][child2][m][
                                                                'month_balance'] > 0 else 0
                                                else:
                                                    dm_total[debit_key][m] = {
                                                        'month_bal': debit_data[debit_key]['child'][child2][m][
                                                            'month_balance'] if
                                                        debit_data[debit_key]['child'][child2][m][
                                                            'month_balance'] > 0 else 0}
                                            else:
                                                dm_total[debit_key] = {m: {
                                                    'month_bal': debit_data[debit_key]['child'][child2][m][
                                                        'month_balance'] if debit_data[debit_key]['child'][child2][m][
                                                                                'month_balance'] > 0 else 0}}

                            else:
                                if data['order'] == 'branch_account':
                                    db_total = 0
                                    dmb_total = {}
                                    for i in debit_data[debit_key]['child'][child2]:
                                        if not data['monthwise']:
                                            d_total += debit_data[debit_key]['child'][child2][i]['balance']
                                            db_total += debit_data[debit_key]['child'][child2][i]['balance']
                                        else:
                                            for m in months:
                                                if m in debit_data[debit_key]['child'][child2][i]:
                                                    if debit_key in dm_total:
                                                        if m in dm_total[debit_key]:
                                                            dm_total[debit_key][m]['month_bal'] += \
                                                                debit_data[debit_key]['child'][child2][i][m][
                                                                    'month_balance'] if \
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] > 0 else 0
                                                        else:
                                                            dm_total[debit_key][m] = {
                                                                'month_bal':
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] if
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] > 0 else 0}
                                                    else:
                                                        dm_total[debit_key] = {m: {
                                                            'month_bal': debit_data[debit_key]['child'][child2][i][m][
                                                                'month_balance'] if
                                                            debit_data[debit_key]['child'][child2][i][m][
                                                                'month_balance'] > 0 else 0}}

                                                    if debit_key in dmb_total:
                                                        if m in dmb_total[debit_key]:

                                                            dmb_total[debit_key][m]['month_bal'] += \
                                                                debit_data[debit_key]['child'][child2][i][m][
                                                                    'month_balance'] if \
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] > 0 else 0
                                                        else:

                                                            dmb_total[debit_key][m] = {
                                                                'month_bal':
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] if
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'] > 0 else 0}
                                                    else:

                                                        dmb_total[debit_key] = {m: {
                                                            'month_bal': debit_data[debit_key]['child'][child2][i][m][
                                                                'month_balance'] if
                                                            debit_data[debit_key]['child'][child2][i][m][
                                                                'month_balance'] > 0 else 0}}

                                    if not data['monthwise']:
                                        bd_total.append({'type': debit_data[debit_key]['name'], 'branch': child2,
                                                         'total': db_total})
                                    else:
                                        dmb = []
                                        for m in months:
                                            if m in dmb_total[debit_key]:
                                                dmb.append(dmb_total[debit_key][m]['month_bal'])
                                            else:
                                                dmb.append(0.00)
                                        bd_total.append(
                                            {'type': debit_data[debit_key]['name'], 'branch': child2, 'total': dmb})
                                else:
                                    if not data['monthwise']:
                                        d_total += debit_data[debit_key]['child'][child2]['balance']
                                    else:
                                        for m in months:
                                            if m in debit_data[debit_key]['child'][child2]:
                                                if debit_key in dm_total:
                                                    if m in dm_total[debit_key]:
                                                        dm_total[debit_key][m]['month_bal'] += \
                                                            debit_data[debit_key]['child'][child2][m][
                                                                'month_balance'] if \
                                                                debit_data[debit_key]['child'][child2][m][
                                                                    'month_balance'] > 0 else 0
                                                    else:
                                                        dm_total[debit_key][m] = {
                                                            'month_bal': debit_data[debit_key]['child'][child2][m][
                                                                'month_balance'] if
                                                            debit_data[debit_key]['child'][child2][m][
                                                                'month_balance'] > 0 else 0}
                                                else:
                                                    dm_total[debit_key] = {m: {
                                                        'month_bal': debit_data[debit_key]['child'][child2][m][
                                                            'month_balance'] if
                                                        debit_data[debit_key]['child'][child2][m][
                                                            'month_balance'] > 0 else 0}}
                        else:

                            if not data['monthwise']:
                                d_total += debit_data[debit_key]['child'][child2]['balance']
                            else:
                                for m in months:
                                    if m in debit_data[debit_key]['child'][child2]:
                                        if debit_key in dm_total:
                                            if m in dm_total[debit_key]:
                                                dm_total[debit_key][m]['month_bal'] += \
                                                    debit_data[debit_key]['child'][child2][m]['month_balance'] if \
                                                        debit_data[debit_key]['child'][child2][m][
                                                            'month_balance'] > 0 else 0
                                            else:
                                                dm_total[debit_key][m] = {
                                                    'month_bal': debit_data[debit_key]['child'][child2][m][
                                                        'month_balance'] if debit_data[debit_key]['child'][child2][m][
                                                                                'month_balance'] > 0 else 0}
                                        else:
                                            dm_total[debit_key] = {m: {
                                                'month_bal': debit_data[debit_key]['child'][child2][m][
                                                    'month_balance'] if
                                                debit_data[debit_key]['child'][child2][m]['month_balance'] > 0 else 0}}
                    if not data['monthwise']:
                        debit_total.append({'type': debit_data[debit_key]['name'], 'total': d_total})
                    else:
                        dml = []
                        for m in months:
                            if m in dm_total[debit_key]:
                                dml.append(dm_total[debit_key][m]['month_bal'])
                            else:
                                dml.append(0.00)

                        debit_total.append({'type': debit_data[debit_key]['name'], 'total': dml})
            for debit_key in list(debit_data.keys()):

                if debit_data[debit_key].get('child'):
                    j = j + 1
                    id2 = "debit" + str(j)

                    balance = 0
                    for dr in debit_total:
                        if dr['type'] == debit_data[debit_key]['name']:
                            balance = dr['total']

                    if not data['monthwise']:
                        table2.append(
                            [
                                '<td class="parent" id="' + id2 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 15px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                debit_data[debit_key]['name'] + '</td>',
                                '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                    "{:.2f}".format(balance)) + '</td>'])
                    else:
                        v = ''
                        for i in balance:
                            if i > 0:
                                v += '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                    "{:.2f}".format(i)) + '</td>'
                            else:
                                v += '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right:1px solid;">&#160;</td>'

                        table2.append(
                            [
                                '<td class="parent" id="' + id2 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 15px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                debit_data[debit_key]['name'] + '</td>', v
                            ])

                    for child2 in debit_data[debit_key]['child']:
                        if 'branch' in data:
                            if len(data['branch']) == 1:
                                res_id = str(debit_data[debit_key]['child'][child2]['account_id'])
                                if data['summary']:
                                    if not data['monthwise']:
                                        table2.append(
                                            [
                                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                                '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' +
                                                str("{:.2f}".format(
                                                    debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                    else:
                                        s = ''
                                        for m in months:
                                            if m in debit_data[debit_key]['child'][child2]:
                                                if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                    s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' + str(
                                                        "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                            'month_balance'])) + '</td>'
                                                else:
                                                    s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                            else:
                                                s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'

                                        table2.append(
                                            [
                                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>', s
                                            ])

                                else:
                                    if not data['monthwise']:
                                        table2.append(
                                            [
                                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                                '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' +
                                                str("{:.2f}".format(
                                                    debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                    else:
                                        s = ''
                                        for m in months:
                                            if m in debit_data[debit_key]['child'][child2]:
                                                if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                    s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' + str(
                                                        "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                            'month_balance'])) + '</td>'
                                                else:
                                                    s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                            else:
                                                s += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                        table2.append(
                                            [
                                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                    data['date_from']) + '" data-date-to="' + str(
                                                    data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                       'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                                s])


                            else:
                                if data['order'] == 'branch_account':
                                    k = k + 1
                                    id4 = "bdebit" + str(k)
                                    branch_tot2 = 0
                                    for db in bd_total:
                                        if db['type'] == debit_data[debit_key]['name']:
                                            if db['branch'] == child2:
                                                branch_tot2 = db['total']
                                    branch = self.env['res.branch'].search([('id', '=', child2)]).name
                                    if data['summary']:
                                        if not data['monthwise']:
                                            table2.append(
                                                [
                                                    '<td class="parent child-' + id2 + '" id="' + id4 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                    branch + '</td>',
                                                    '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">' + str(
                                                        "{:.2f}".format(branch_tot2)) + '</td>'])
                                        else:
                                            s = ''
                                            for i in branch_tot2:
                                                if i > 0:
                                                    s += '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">' + str(
                                                        "{:.2f}".format(i)) + '</td>'
                                                else:
                                                    s += '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;display:none">&#160;</td>'
                                            table2.append(
                                                [
                                                    '<td class="parent child-' + id2 + '" id="' + id4 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                    branch + '</td>', s
                                                ])

                                    else:
                                        if not data['monthwise']:
                                            table2.append(
                                                [
                                                    '<td class="parent child-' + id2 + '" id="' + id4 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                    branch + '</td>',
                                                    '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                                        "{:.2f}".format(branch_tot2)) + '</td>'])
                                        else:
                                            s = ''
                                            for i in branch_tot2:
                                                if i > 0:
                                                    s += '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">' + str(
                                                        "{:.2f}".format(i)) + '</td>'
                                                else:
                                                    s += '<td class="text-right child-' + id2 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;cursor: pointer;border-right:1px solid;">&#160;</td>'

                                            table2.append(
                                                [
                                                    '<td class="parent child-' + id2 + '" id="' + id4 + '" title="Click to expand/collapse" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                                                    branch + '</td>', s
                                                ])

                                    for i in debit_data[debit_key]['child'][child2]:
                                        res_id = str(debit_data[debit_key]['child'][child2][i]['account_id'])

                                        if data['summary']:
                                            if not data['monthwise']:
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id4 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child2) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        debit_data[debit_key]['child'][child2][i]['name'] + '</a></td>',
                                                        '<td class="text-right child-' + id4 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' +
                                                        str("{:.2f}".format(
                                                            debit_data[debit_key]['child'][child2][i][
                                                                'balance'])) + '</td>'])
                                            else:
                                                d = ''
                                                for m in months:
                                                    if m in debit_data[debit_key]['child'][child2][i]:
                                                        if debit_data[debit_key]['child'][child2][i][m][
                                                            'month_balance'] > 0:
                                                            d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' + str(
                                                                "{:.2f}".format(
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'])) + '</td>'
                                                        else:
                                                            d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id4 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child2) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        debit_data[debit_key]['child'][child2][i]['name'] + '</a></td>',
                                                        d
                                                    ])

                                        else:
                                            if not data['monthwise']:
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id4 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child2) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        debit_data[debit_key]['child'][child2][i]['name'] + '</a></td>',
                                                        '<td class="text-right child-' + id4 + '"style="padding-right: 10px;border-right:1px solid;" >' +
                                                        str("{:.2f}".format(
                                                            debit_data[debit_key]['child'][child2][i][
                                                                'balance'])) + '</td>'])
                                            else:
                                                d = ''
                                                for m in months:
                                                    if m in debit_data[debit_key]['child'][child2][i]:
                                                        if debit_data[debit_key]['child'][child2][i][m][
                                                            'month_balance'] > 0:
                                                            d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;border-right:1px solid;" >' + str(
                                                                "{:.2f}".format(
                                                                    debit_data[debit_key]['child'][child2][i][m][
                                                                        'month_balance'])) + '</td>'
                                                        else:
                                                            d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id4 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id4 + '" style="padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                            data['date_from']) + '" data-date-to="' + str(
                                                            data['date_to']) + '" data-branch-ids="[' + str(
                                                            child2) + ']" style="text-decoration: none !important;color: inherit !important;">' +
                                                        debit_data[debit_key]['child'][child2][i]['name'] + '</a></td>',
                                                        d
                                                    ])

                                else:
                                    res_id = str(debit_data[debit_key]['child'][child2]['account_id'])
                                    y = y + 1
                                    id6 = "bdebit2" + str(y)
                                    if data['summary']:
                                        if not data['monthwise']:
                                            table2.append(
                                                [
                                                    '<td  class="parent child-' + id2 + '" id="' + id6 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                                    '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' +
                                                    str("{:.2f}".format(
                                                        debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                        else:
                                            d = ''
                                            for m in months:
                                                if m in debit_data[debit_key]['child'][child2]:
                                                    if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                        d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' + str(
                                                            "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                                'month_balance'])) + '</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                                else:
                                                    d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                            table2.append(
                                                [
                                                    '<td  class="parent child-' + id2 + '" id="' + id6 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    debit_data[debit_key]['child'][child2]['name'] + '</a></td>', d
                                                ])
                                    else:
                                        if not data['monthwise']:
                                            table2.append(
                                                [
                                                    '<td  class="parent child-' + id2 + '" id="' + id6 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-right" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                                    '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' +
                                                    str("{:.2f}".format(
                                                        debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                        else:

                                            d = ''

                                            for m in months:
                                                if m in debit_data[debit_key]['child'][child2]:
                                                    if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                        d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' + str(
                                                            "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                                'month_balance'])) + '</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                                else:
                                                    d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'

                                            table2.append(
                                                [
                                                    '<td  class="parent child-' + id2 + '" id="' + id6 + '" title="Click to expand/collapse" style="padding-left: 20px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-right" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                        data['date_from']) + '" data-date-to="' + str(
                                                        data['date_to']) + '" data-branch-ids="' + str(data[
                                                                                                           'branch']) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                                    debit_data[debit_key]['child'][child2]['name'] + '</a></td>', d
                                                ])

                                    for n in debit_data[debit_key]['child'][child2]['branch']:
                                        if data['summary']:
                                            if not data['monthwise']:
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id6 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;">' +
                                                        debit_data[debit_key]['child'][child2]['branch'][n][
                                                            'branch_name'] + '</td>',
                                                        '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;" >' +
                                                        str("{:.2f}".format(
                                                            debit_data[debit_key]['child'][child2]['branch'][n][
                                                                'branch_balance'])) + '</td>'])
                                            else:
                                                d = ''
                                                for m in months:
                                                    if m in debit_data[debit_key]['child'][child2]['branch'][n]:
                                                        if debit_data[debit_key]['child'][child2]['branch'][n][m][
                                                            'month_balance'] > 0:
                                                            d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;" >' + str(
                                                                "{:.2f}".format(
                                                                    debit_data[debit_key]['child'][child2]['branch'][n][
                                                                        m]['month_balance'])) + '</td>'
                                                        else:
                                                            d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id6 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;">' +
                                                        debit_data[debit_key]['child'][child2]['branch'][n][
                                                            'branch_name'] + '</td>', d
                                                    ])

                                        else:
                                            if not data['monthwise']:
                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id6 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;display:none;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                                                        debit_data[debit_key]['child'][child2]['branch'][n][
                                                            'branch_name'] + '</td>',
                                                        '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;border-right:1px solid;display:none;" >' +
                                                        str("{:.2f}".format(
                                                            debit_data[debit_key]['child'][child2]['branch'][n][
                                                                'branch_balance'])) + '</td>'])
                                            else:
                                                d = ''
                                                for m in months:
                                                    if m in debit_data[debit_key]['child'][child2]['branch'][n]:
                                                        if debit_data[debit_key]['child'][child2]['branch'][n][m][
                                                            'month_balance'] > 0:
                                                            d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;border-right:1px solid;display:none;" >' + str(
                                                                "{:.2f}".format(
                                                                    debit_data[debit_key]['child'][child2]['branch'][n][
                                                                        m]['month_balance'])) + '</td>'
                                                        else:
                                                            d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;border-right:1px solid;display:none;" >&#160;</td>'
                                                    else:
                                                        d += '<td class="text-right child-' + id6 + '"style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-right: 10px;border-right:1px solid;display:none;" >&#160;</td>'

                                                table2.append(
                                                    [
                                                        '<td  class="child-' + id6 + '" style="color:#00A09D;border-right-color: black !important;font-style: italic;padding-left: 30px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;display:none;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                                                        debit_data[debit_key]['child'][child2]['branch'][n][
                                                            'branch_name'] + '</td>', d
                                                    ])


                        else:
                            res_id = str(debit_data[debit_key]['child'][child2]['account_id'])
                            if data['summary']:
                                if not data['monthwise']:
                                    table2.append(
                                        [
                                            '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                            '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' +
                                            str("{:.2f}".format(
                                                debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                else:
                                    d = ''
                                    for m in months:
                                        if m in debit_data[debit_key]['child'][child2]:
                                            if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >' + str(
                                                    "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                        'month_balance'])) + '</td>'
                                            else:
                                                d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'
                                        else:
                                            d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right:1px solid;" >&#160;</td>'

                                    table2.append(
                                        [
                                            '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            debit_data[debit_key]['child'][child2]['name'] + '</a></td>', d
                                        ])

                            else:
                                if not data['monthwise']:

                                    table2.append(
                                        [
                                            '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                            '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' +
                                            str("{:.2f}".format(
                                                debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                                else:
                                    d = ''
                                    for m in months:
                                        if m in debit_data[debit_key]['child'][child2]:
                                            if debit_data[debit_key]['child'][child2][m]['month_balance'] > 0:
                                                d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >' + str(
                                                    "{:.2f}".format(debit_data[debit_key]['child'][child2][m][
                                                                        'month_balance'])) + '</td>'
                                            else:
                                                d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                        else:
                                            d += '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right:1px solid;" >&#160;</td>'
                                    table2.append(
                                        [
                                            '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                                data['date_from']) + '" data-date-to="' + str(data[
                                                                                                  'date_to']) + '" data-branch-ids="false" style="text-decoration: none !important;color: inherit !important;">' +
                                            debit_data[debit_key]['child'][child2]['name'] + '</a></td>', d
                                        ])

                else:
                    if not data['monthwise']:
                        table2.append([
                            '<td style="font-weight:bold;padding-left: 15px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                            debit_data[debit_key]['name'],
                            '<td class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">' +
                            str("{:.2f}".format(debit_data[debit_key]['balance']))
                            if debit_data[debit_key].get(
                                'balance') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">0.00</td>'
                        ])
                    else:
                        c = ''
                        for m in months:
                            if m in val['profit']:
                                c += '<td class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">' + str(
                                    "{:.2f}".format(val['profit'][m]['i'])) if val['profit'][m].get(
                                    'i') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">&#160;</td>'
                            else:
                                c += '<td class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right:1px solid;">&#160;</td>'

                        table2.append([
                            '<td style="font-weight:bold;padding-left: 15px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;border-right:1px solid;">' +
                            debit_data[debit_key]['name'], c

                        ])

            final_list = []
            maxlen = len(table) if len(table) > len(table2) else len(table2)
            if data['context']['default_account_report_id'] == 8:
                for integer_val in range(maxlen):
                    temp = []
                    if len(table) > integer_val:
                        temp.append(table[integer_val][0])
                        temp.append(table[integer_val][1])
                    else:
                        temp.append('<td></td>')
                        temp.append('<td></td>')
                    if len(table2) > integer_val:
                        temp.append(table2[integer_val][0])
                        temp.append(table2[integer_val][1])
                    else:
                        temp.append('<td></td>')
                        temp.append('<td></td>')
                    final_list.append(temp)
            elif data['context']['default_account_report_id'] == 1:
                for integer_val in range(maxlen):
                    temp = []
                    if len(table2) > integer_val:
                        temp.append(table2[integer_val][0])
                        temp.append(table2[integer_val][1])
                    else:
                        temp.append('<td></td>')
                        temp.append('<td></td>')
                    if len(table) > integer_val:
                        temp.append(table[integer_val][0])
                        temp.append(table[integer_val][1])
                    else:
                        temp.append('<td></td>')
                        temp.append('<td></td>')

                    final_list.append(temp)
            if 'branch' in data:
                branch_name = data['branch_name']
            else:
                branch_name = ''

            if data['monthwise']:
                tot = {}
                g_tot = {}
                for m in months:
                    if m in debit_tot and m in credit_tot:
                        tot[m] = {'month_tot': round(debit_tot[m]['month_debit'] + credit_tot[m]['month_credit'], 2)}
                        g_tot[m] = {'debit_tot': debit_tot[m]['month_debit'] if debit_tot[m]['month_debit'] >= (
                                credit_tot[m]['month_credit'] * -1) else 0,
                                    'credit_tot': credit_tot[m]['month_credit'] * -1 if (credit_tot[m][
                                                                                             'month_credit'] * -1) > (
                                                                                            debit_tot[m][
                                                                                                'month_debit']) else 0}
                    elif m in debit_tot and m not in credit_tot:
                        tot[m] = {'month_tot': round(debit_tot[m]['month_debit'], 2)}
                        g_tot[m] = {'debit_tot': debit_tot[m]['month_debit'], 'credit_tot': 0}
                    elif m in credit_tot:
                        tot[m] = {'month_tot': round(credit_tot[m]['month_credit'], 2)}
                        g_tot[m] = {'debit_tot': 0, 'credit_tot': credit_tot[m]['month_credit'] * -1}
            ctx = {
                'data': data,
                'account_report': data['context']['default_account_report_id'],
                'tot': round(debit_tot + credit_tot, 2) if not data['monthwise'] else tot,
                'rows': deb_row - cre_row,
                'g_tot': (debit_tot if debit_tot >= (credit_tot * -1) else credit_tot * -1) if not data[
                    'monthwise'] else g_tot,
                'final_list': final_list,
                'table': table,
                'table2': table2,
                'branch_name': branch_name,
                'summary': data['summary'],
                'order': data['order'],
                'monthwise': data['monthwise'],
                'months': months
            }
        return ctx

    def get_child(self, account, acc_type):
        if not account.children_ids:
            return account.account_type_ids
        else:
            for child in account.children_ids:
                acc_type += self.get_child(child, acc_type)

        return acc_type

    def get_report_template_data(self, account_types, account, dom, rtype, date_from, wopening, monthwise, branch, order):
        account_movelines = self.env['account.move.line']
        credit_data = {}
        debit_data = {}
        deb_row, cre_row, debit_tot, credit_tot = 0, 0, 0, 0
        if branch and len(branch) > 1 and order:
            months_list = []

            debit_list = {}
            credit_list = {}
            if order == 'branch_account':
                for account_type in account_types:
                    movelines = account_movelines.search([('account_id.user_type_id', '=', account_type.id)] + dom)
                    child = {}
                    for moveline in movelines:
                        if monthwise:
                            date = str(moveline.date)
                            d = datetime.strptime(date, "%Y-%m-%d")

                            m = d.strftime('%B')
                            y = str(d.year)
                            month = m + '-' + y
                            if month in months_list:
                                pass
                            else:
                                months_list.append(month)
                        if moveline.move_id.branch_id.id in child:
                            if moveline.account_id.id in child[moveline.move_id.branch_id.id]:
                                child[moveline.move_id.branch_id.id][moveline.account_id.id]['balance'] += moveline.debit - moveline.credit

                                if monthwise:
                                    if month in child[moveline.move_id.branch_id.id][moveline.account_id.id]:
                                        child[moveline.move_id.branch_id.id][moveline.account_id.id][month]['month_balance'] += moveline.debit - moveline.credit
                                    else:
                                        child[moveline.move_id.branch_id.id][moveline.account_id.id][month] = {'month_balance': moveline.debit - moveline.credit}
                            else:
                                tot_open = 0
                                if wopening:
                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from, moveline.move_id.branch_id.ids)

                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit
                            if monthwise:
                                if moveline.account_id.id not in child[moveline.move_id.branch_id.id]:
                                    child[moveline.move_id.branch_id.id][moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'type': moveline.account_id.internal_group,
                                        'branch_id': moveline.move_id.branch_id.id,
                                        'branch_name': moveline.move_id.branch_id.name,
                                        'account_id': moveline.account_id.id,
                                         month: {'month_balance': (moveline.debit - moveline.credit) + tot_open},
                                    }
                            else:

                                if moveline.account_id.id not in child[moveline.move_id.branch_id.id]:
                                    child[moveline.move_id.branch_id.id][moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'type': moveline.account_id.internal_group,
                                        'branch_id': moveline.move_id.branch_id.id,
                                        'branch_name': moveline.move_id.branch_id.name,
                                        'account_id': moveline.account_id.id,

                                    }



                        else:
                            if rtype == 8:
                                tot_open = 0
                                if wopening:
                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from,
                                                                                      moveline.move_id.branch_id.ids)

                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit
                                child[moveline.move_id.branch_id.id] = {moveline.account_id.id: {
                                    'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                    'balance': (moveline.debit - moveline.credit) + tot_open,
                                    'type': moveline.account_id.internal_group,
                                    'branch_id': moveline.move_id.branch_id.id,
                                    'branch_name': moveline.move_id.branch_id.name,
                                    'account_id': moveline.account_id.id,

                                }}

                            else:
                                tot_open = 0
                                if wopening:
                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id,
                                                                                      date_from,
                                                                                      moveline.move_id.branch_id.ids)

                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit
                                if monthwise:

                                    child[moveline.move_id.branch_id.id] = {moveline.account_id.id: {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'branch_id': moveline.move_id.branch_id.id,
                                        'branch_name': moveline.move_id.branch_id.name,
                                        'account_id': moveline.account_id.id,
                                        month: {'month_balance': (moveline.debit - moveline.credit) + tot_open},
                                    }}
                                else:

                                    child[moveline.move_id.branch_id.id] = {moveline.account_id.id: {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'branch_id': moveline.move_id.branch_id.id,
                                        'branch_name': moveline.move_id.branch_id.name,
                                        'account_id': moveline.account_id.id,
                                    }}

                    if child:
                        for d in child:
                            for data in child[d]:
                                if rtype == 8:
                                    if child[d][data]['balance'] != 0:
                                        if child[d][data]['type'] == 'asset':
                                            if account_type.id in debit_data:
                                                if d in debit_data[account_type.id]['child']:
                                                    debit_data[account_type.id]['child'][d][data] = child[d][data]
                                                    debit_tot += child[d][data]['balance']
                                                    deb_row += 1
                                                else:
                                                    debit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                    debit_tot += child[d][data]['balance']
                                                    deb_row += 1
                                            else:

                                                debit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {d: {data: child[d][data]}}
                                                }
                                                debit_tot += child[d][data]['balance']
                                                deb_row += 2
                                        else:
                                            if account_type.id in credit_data:
                                                if d in credit_data[account_type.id]['child']:
                                                    credit_data[account_type.id]['child'][d][data] = child[d][data]
                                                    credit_tot += child[d][data]['balance']
                                                    cre_row += 1
                                                else:
                                                    credit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                    credit_tot += child[d][data]['balance']
                                                    cre_row += 1
                                            else:

                                                credit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {d: {data: child[d][data]}}
                                                }
                                                credit_tot += child[d][data]['balance']
                                                cre_row += 2
                                else:
                                    if not monthwise:
                                        if child[d][data]['balance'] != 0:
                                            if child[d][data]['balance'] > 0:
                                                if account_type.id in debit_data:
                                                    if d in debit_data[account_type.id]['child']:
                                                        debit_data[account_type.id]['child'][d][data] = child[d][data]
                                                        debit_tot += child[d][data]['balance']
                                                        deb_row += 1
                                                    else:
                                                        debit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                        debit_tot += child[d][data]['balance']
                                                        deb_row += 1
                                                else:
                                                    debit_data[account_type.id] = {
                                                        'name': account_type.name,
                                                        'child': {d: {data: child[d][data]}}
                                                    }
                                                    debit_tot += child[d][data]['balance']
                                                    deb_row += 2
                                            else:
                                                if account_type.id in credit_data:
                                                    if d in credit_data[account_type.id]['child']:
                                                        credit_data[account_type.id]['child'][d][data] = child[d][data]
                                                        credit_tot += child[d][data]['balance']
                                                        cre_row += 1
                                                    else:
                                                        credit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                        credit_tot += child[d][data]['balance']
                                                        cre_row += 1
                                                else:
                                                    credit_data[account_type.id] = {
                                                        'name': account_type.name,
                                                        'child': {d: {data: child[d][data]}}
                                                    }
                                                    credit_tot += child[d][data]['balance']
                                                    cre_row += 2
                                    else:
                                        for m in reversed(months_list):
                                            if m in child[d][data]:
                                                if child[d][data][m]['month_balance'] != 0:
                                                    if child[d][data][m]['month_balance'] > 0:
                                                        if account_type.id in debit_data:
                                                            if d in debit_data[account_type.id]['child']:
                                                                debit_data[account_type.id]['child'][d][data] = child[d][data]
                                                                debit_tot += child[d][data][m]['month_balance']
                                                                if m in debit_list:
                                                                    debit_list[m]['month_debit'] += child[d][data][m]['month_balance']
                                                                else:
                                                                    debit_list[m] = {'month_debit':child[d][data][m]['month_balance']}
                                                                deb_row += 1
                                                            else:
                                                                debit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                                debit_tot += child[d][data][m]['month_balance']
                                                                if m in debit_list:
                                                                    debit_list[m]['month_debit'] += child[d][data][m]['month_balance']
                                                                else:
                                                                    debit_list[m] = {'month_debit':child[d][data][m]['month_balance']}
                                                                deb_row += 1
                                                        else:
                                                            debit_data[account_type.id] = {
                                                                'name': account_type.name,
                                                                'child': {d: {data: child[d][data]}}
                                                            }
                                                            debit_tot += child[d][data][m]['month_balance']
                                                            if m in debit_list:
                                                                debit_list[m]['month_debit'] += child[d][data][m]['month_balance']
                                                            else:
                                                                debit_list[m] = {
                                                                    'month_debit': child[d][data][m]['month_balance']}
                                                            deb_row += 2
                                                    else:
                                                        if account_type.id in credit_data:
                                                            if d in credit_data[account_type.id]['child']:
                                                                credit_data[account_type.id]['child'][d][data] = child[d][data]
                                                                credit_tot += child[d][data][m]['month_balance']
                                                                if m in credit_list:
                                                                    credit_list[m]['month_credit'] += child[d][data][m]['month_balance']
                                                                else:
                                                                    credit_list[m] = {'month_credit':child[d][data][m]['month_balance']}
                                                                cre_row += 1
                                                            else:
                                                                credit_data[account_type.id]['child'][d] = {data: child[d][data]}
                                                                credit_tot += child[d][data][m]['month_balance']
                                                                if m in credit_list:
                                                                    credit_list[m]['month_credit'] += child[d][data][m]['month_balance']
                                                                else:
                                                                    credit_list[m] = {'month_credit': child[d][data][m]['month_balance']}
                                                                cre_row += 1
                                                        else:
                                                            credit_data[account_type.id] = {
                                                                'name': account_type.name,
                                                                'child': {d: {data: child[d][data]}}
                                                            }
                                                            credit_tot += child[d][data][m]['month_balance']
                                                            if m in credit_list:
                                                                credit_list[m]['month_credit'] += child[d][data][m]['month_balance']
                                                            else:
                                                                credit_list[m] = {'month_credit': child[d][data][m]['month_balance']}
                                                            cre_row += 2

            else:
                for account_type in account_types:

                    movelines = account_movelines.search([('account_id.user_type_id', '=', account_type.id)] + dom)
                    child = {}
                    for moveline in movelines:

                        if monthwise:
                            date = str(moveline.date)
                            d = datetime.strptime(date, "%Y-%m-%d")
                            m = d.strftime('%B')
                            y = str(d.year)
                            month = m + '-' + y
                            if month in months_list:
                                pass
                            else:
                                months_list.append(month)

                        if moveline.account_id.id in child:
                            child[moveline.account_id.id]['balance'] += moveline.debit - moveline.credit

                            if moveline.move_id.branch_id.id in child[moveline.account_id.id]['branch']:

                                child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id]['branch_balance'] += moveline.debit - moveline.credit

                                if monthwise:
                                    if month in child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id]:
                                        child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id][month]['month_balance'] += moveline.debit - moveline.credit
                                    else:
                                        child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id][month] = {'month_balance': moveline.debit - moveline.credit}

                            else:
                                tot_open = 0
                                if wopening:
                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from, moveline.move_id.branch_id.ids)
                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit

                            if monthwise:

                                if moveline.move_id.branch_id.id not in child[moveline.account_id.id]['branch']:
                                    child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id] = {
                                        'branch_name':moveline.move_id.branch_id.name,
                                        'branch_balance': (moveline.debit - moveline.credit) + tot_open,
                                        month: {'month_balance': (moveline.debit - moveline.credit) + tot_open},
                                    }

                                if month in child[moveline.account_id.id]:
                                    child[moveline.account_id.id][month]['month_balance'] += moveline.debit - moveline.credit
                                else:
                                    child[moveline.account_id.id][month] = {'month_balance': moveline.debit - moveline.credit}
                            else:

                                if moveline.move_id.branch_id.id not in child[moveline.account_id.id]['branch']:

                                    child[moveline.account_id.id]['branch'][moveline.move_id.branch_id.id] = {
                                        'branch_name': moveline.move_id.branch_id.name,
                                        'branch_balance': (moveline.debit - moveline.credit) + tot_open,
                                    }


                        else:
                            if rtype == 8:
                                tot_open = 0
                                if wopening:
                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from, branch)

                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit
                                child[moveline.account_id.id] = {
                                    'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                    'balance': (moveline.debit - moveline.credit) + tot_open,
                                    'type': moveline.account_id.internal_group,
                                    'account_id': moveline.account_id.id,
                                    'branch': {moveline.move_id.branch_id.id:{'branch_name':moveline.move_id.branch_id.name,'branch_balance': moveline.debit - moveline.credit}}
                                }
                            else:
                                tot_open = 0
                                if wopening:

                                    opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id,
                                                                                          date_from,
                                                                                          branch)

                                    if opening[0] or opening[1]:
                                        debit = opening[1]
                                        credit = opening[0]
                                        tot_open = debit - credit
                                if monthwise:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'account_id': moveline.account_id.id,
                                        month: {'month_balance': (moveline.debit - moveline.credit) + tot_open},
                                        'branch': {moveline.move_id.branch_id.id: {'branch_name':moveline.move_id.branch_id.name,
                                        'branch_balance': (moveline.debit - moveline.credit) + tot_open, month: {'month_balance': moveline.debit - moveline.credit},
                                                                                   }}
                                    }
                                else:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'account_id': moveline.account_id.id,
                                        'branch': {moveline.move_id.branch_id.id: {
                                            'branch_name': moveline.move_id.branch_id.name,
                                            'branch_balance': (moveline.debit - moveline.credit) + tot_open,
                                            }}
                                    }

                    if child:
                        for data in child:

                            if rtype == 8:
                                if child[data]['balance'] != 0:
                                    if child[data]['type'] == 'asset':
                                        if account_type.id in debit_data:
                                            debit_data[account_type.id]['child'][data] = child[data]
                                            debit_tot += child[data]['balance']
                                            deb_row += 1
                                        else:
                                            debit_data[account_type.id] = {
                                                'name': account_type.name,
                                                'child': {data: child[data]}
                                            }
                                            debit_tot += child[data]['balance']
                                            deb_row += 2
                                    else:
                                        if account_type.id in credit_data:
                                            credit_data[account_type.id]['child'][data] = child[data]
                                            credit_tot += child[data]['balance']
                                            cre_row += 1
                                        else:
                                            credit_data[account_type.id] = {
                                                'name': account_type.name,
                                                'child': {data: child[data]}
                                            }
                                            credit_tot += child[data]['balance']
                                            cre_row += 2
                            else:
                                if not monthwise:
                                    if child[data]['balance'] != 0:
                                        if child[data]['balance'] > 0:
                                            if account_type.id in debit_data:
                                                debit_data[account_type.id]['child'][data] = child[data]
                                                debit_tot += child[data]['balance']
                                                deb_row += 1
                                            else:
                                                debit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {data: child[data]}
                                                }
                                                debit_tot += child[data]['balance']
                                                deb_row += 2
                                        else:
                                            if account_type.id in credit_data:
                                                credit_data[account_type.id]['child'][data] = child[data]
                                                credit_tot += child[data]['balance']
                                                cre_row += 1
                                            else:
                                                credit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {data: child[data]}
                                                }
                                                credit_tot += child[data]['balance']
                                                cre_row += 2
                                else:
                                    for m in reversed(months_list):
                                        if m in child[data]:
                                            if child[data][m]['month_balance'] != 0:
                                                if child[data][m]['month_balance'] > 0:
                                                    if account_type.id in debit_data:
                                                        debit_data[account_type.id]['child'][data] = child[data]
                                                        debit_tot += child[data][m]['month_balance']
                                                        if m in debit_list:
                                                            debit_list[m]['month_debit'] += child[data][m]['month_balance']
                                                        else:
                                                            debit_list[m] = {
                                                                'month_debit':child[data][m]['month_balance']}
                                                        deb_row += 1
                                                    else:
                                                        debit_data[account_type.id] = {
                                                            'name': account_type.name,
                                                            'child': {data: child[data]}
                                                        }
                                                        debit_tot += child[data][m]['month_balance']
                                                        if m in debit_list:
                                                            debit_list[m]['month_debit'] += child[data][m]['month_balance']
                                                        else:
                                                            debit_list[m] = {
                                                                'month_debit':child[data][m]['month_balance']}
                                                        deb_row += 2
                                                else:
                                                    if account_type.id in credit_data:
                                                        credit_data[account_type.id]['child'][data] = child[data]
                                                        credit_tot += child[data][m]['month_balance']
                                                        if m in credit_list:
                                                            credit_list[m]['month_credit'] += child[data][m]['month_balance']
                                                        else:
                                                            credit_list[m] = {
                                                                'month_credit':child[data][m]['month_balance']}
                                                        cre_row += 1
                                                    else:
                                                        credit_data[account_type.id] = {
                                                            'name': account_type.name,
                                                            'child': {data: child[data]}
                                                        }
                                                        credit_tot += child[data][m]['month_balance']
                                                        if m in credit_list:
                                                            credit_list[m]['month_credit'] += child[data][m][
                                                                'month_balance']
                                                        else:
                                                            credit_list[m] = {
                                                                'month_credit': child[data][m]['month_balance']}
                                                        cre_row += 2
            if monthwise:
                debit_tot = debit_list
                credit_tot = credit_list
            return [debit_data, credit_data, debit_tot, credit_tot, deb_row, cre_row, account]

        else:
            credit_data = {}
            debit_data = {}
            months_list = []
            debit_list = {}
            credit_list = {}

            deb_row, cre_row, debit_tot, credit_tot = 0, 0, 0, 0
            for account_type in account_types:
                if wopening:
                    print("fdsfsdfdfsdddddd")
                    movelines = account_movelines.search([('account_id.user_type_id', '=', account_type.id)] + dom)
                else:
                    print("sssssssssssssss")
                    movelines = account_movelines.search(
                        [('account_id.user_type_id', '=', account_type.id),
                         ('move_id', 'not in', self.env.company.account_opening_move_id.ids)] + dom)

                child = {}

                for moveline in movelines:
                    if monthwise:
                        date = str(moveline.date)
                        d = datetime.strptime(date, "%Y-%m-%d")
                        m = d.strftime('%B')
                        y = str(d.year)
                        month = m + '-' + y
                        if month in months_list:
                            pass
                        else:
                            months_list.append(month)

                    if moveline.account_id.id in child:
                        if moveline.move_id.id not in self.env.company.account_opening_move_id.ids:
                            child[moveline.account_id.id]['balance'] += moveline.debit - moveline.credit
                            if monthwise and rtype == 1:
                                if month in child[moveline.account_id.id]:
                                    child[moveline.account_id.id][month]['month_balance'] += moveline.debit - moveline.credit
                                else:

                                    child[moveline.account_id.id][month] = {'month_balance': moveline.debit - moveline.credit}
                    else:
                        if rtype == 8:
                            tot_open = 0
                            if wopening:

                                opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from,
                                                                                  False)

                                if opening[0] or opening[1]:
                                    debit = opening[1]
                                    credit = opening[0]
                                    tot_open = debit - credit
                            if moveline.move_id.id in self.env.company.account_opening_move_id.ids:
                                child[moveline.account_id.id] = {
                                    'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                    'balance': tot_open,
                                    'type': moveline.account_id.internal_group,
                                    'account_id': moveline.account_id.id,
                                }
                            else:
                                child[moveline.account_id.id] = {
                                    'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                    'balance': (moveline.debit - moveline.credit) + tot_open,
                                    'type': moveline.account_id.internal_group,
                                    'account_id': moveline.account_id.id,
                                }
                        else:
                            tot_open = 0

                            if wopening:

                                opening = self.get_balance_sheet_credit_and_debit(moveline.account_id.id, date_from, False)
                                if opening[0] or opening[1]:
                                    debit = opening[1]
                                    credit = opening[0]
                                    tot_open = debit - credit
                            if not monthwise:
                                if moveline.move_id.id in self.env.company.account_opening_move_id.ids:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': tot_open,
                                        'account_id': moveline.account_id.id,
                                    }
                                else:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'account_id': moveline.account_id.id,
                                    }
                            else:
                                if moveline.move_id.id in self.env.company.account_opening_move_id.ids:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': tot_open,
                                        'account_id': moveline.account_id.id,
                                         month: {'month_balance': tot_open},
                                    }
                                else:
                                    child[moveline.account_id.id] = {
                                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                                        'balance': (moveline.debit - moveline.credit) + tot_open,
                                        'account_id': moveline.account_id.id,
                                        month: {'month_balance': (moveline.debit - moveline.credit) + tot_open},
                                    }

                if child:

                    for data in child:

                            if rtype == 8:
                                if child[data]['balance'] != 0:
                                    if child[data]['type'] == 'asset':
                                        if account_type.id in debit_data:
                                            debit_data[account_type.id]['child'][data] = child[data]
                                            debit_tot += child[data]['balance']
                                            deb_row += 1
                                        else:
                                            if child[data]['balance'] != 0:

                                                debit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {data: child[data]}
                                                }
                                                debit_tot += child[data]['balance']
                                                deb_row += 2
                                    else:
                                        if account_type.id in credit_data:
                                            credit_data[account_type.id]['child'][data] = child[data]
                                            credit_tot += child[data]['balance']
                                            cre_row += 1
                                        else:
                                            if child[data]['balance'] != 0:
                                                credit_data[account_type.id] = {
                                                    'name': account_type.name,
                                                    'child': {data: child[data]}
                                                }
                                                credit_tot += child[data]['balance']
                                                cre_row += 2
                            else:
                                if not monthwise:
                                    if child[data]['balance'] != 0:
                                        if child[data]['balance'] > 0:
                                            if account_type.id in debit_data:
                                                debit_data[account_type.id]['child'][data] = child[data]
                                                debit_tot += child[data]['balance']
                                                deb_row += 1
                                            else:
                                                if child[data]['balance'] != 0:
                                                    debit_data[account_type.id] = {
                                                        'name': account_type.name,
                                                        'child': {data: child[data]}
                                                    }
                                                    debit_tot += child[data]['balance']
                                                    deb_row += 2
                                        else:
                                            if account_type.id in credit_data:
                                                credit_data[account_type.id]['child'][data] = child[data]
                                                credit_tot += child[data]['balance']
                                                cre_row += 1
                                            else:
                                                if child[data]['balance'] != 0:
                                                    credit_data[account_type.id] = {
                                                        'name': account_type.name,
                                                        'child': {data: child[data]}
                                                    }
                                                    credit_tot += child[data]['balance']
                                                    cre_row += 2
                                else:

                                    for m in reversed(months_list):
                                        if m in child[data]:
                                            if child[data][m]['month_balance'] != 0:
                                                if child[data][m]['month_balance'] > 0:
                                                    if account_type.id in debit_data:
                                                        debit_data[account_type.id]['child'][data] = child[data]
                                                        debit_tot += child[data][m]['month_balance']
                                                        if m in debit_list:
                                                            debit_list[m]['month_debit'] += child[data][m]['month_balance']
                                                        else:
                                                            debit_list[m] = {'month_debit': child[data][m]['month_balance']}
                                                        deb_row += 1
                                                    else:
                                                        if child[data][m]['month_balance'] != 0:
                                                            debit_data[account_type.id] = {
                                                                'name': account_type.name,
                                                                'child': {data: child[data]}
                                                            }
                                                            if m in debit_list:
                                                                debit_list[m]['month_debit'] += child[data][m]['month_balance']
                                                            else:
                                                                debit_list[m] = {'month_debit': child[data][m]['month_balance']}
                                                            debit_tot += child[data][m]['month_balance']
                                                            deb_row += 2
                                                else:
                                                    if account_type.id in credit_data:
                                                        credit_data[account_type.id]['child'][data] = child[data]
                                                        if m in credit_list:
                                                            credit_list[m]['month_credit'] += child[data][m]['month_balance']
                                                        else:
                                                            credit_list[m] = {'month_credit': child[data][m]['month_balance']}
                                                        credit_tot += child[data][m]['month_balance']
                                                        cre_row += 1
                                                    else:
                                                        if child[data]['balance'] != 0:
                                                            credit_data[account_type.id] = {
                                                                'name': account_type.name,
                                                                'child': {data: child[data]}
                                                            }
                                                            if m in credit_list:
                                                                credit_list[m]['month_credit'] += child[data][m]['month_balance']
                                                            else:
                                                                credit_list[m] = {'month_credit': child[data][m]['month_balance']}
                                                            credit_tot += child[data][m]['month_balance']
                                                            cre_row += 2
            if monthwise:
                debit_tot = debit_list
                credit_tot = credit_list
            return [debit_data, credit_data, debit_tot, credit_tot, deb_row, cre_row, account]

    def get_balance_sheet_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id', '=', account)])
            selected_year = datetime.strptime(str(date_from), '%Y-%m-%d')
            date_f = datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            date_fr = datetime.strptime(str(date_f), '%d-%m-%Y').date()
            if not account_id.user_type_id.include_initial_balance:
                if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                    fin_date = str(selected_year.year - 1) + '-04-01'
                else:
                    fin_date = str(selected_year.year) + '-04-01'
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

    def get_trad_acc_dat(self, dom, data):
        account = self.env.ref("manufacturing_trading.data_trading_account")
        account_types = self.get_child(account, account.account_type_ids)
        account_types = list(set(account_types.ids))
        movelines = self.env['account.move.line'].search([('account_id.user_type_id', 'in', account_types)] + dom)
        if not data['monthwise']:
            debit_tot = sum(movelines.mapped('debit'))
            credit_tot = sum(movelines.mapped('credit'))
            if data['date_from']:
                opening_date = datetime.strptime(data['date_from'], '%Y-%m-%d') - timedelta(days=1)
                inv_opening = self.get_opening_closing(opening_date.strftime("%Y-%m-%d"), data)
                debit_tot += inv_opening
            if data['date_to']:
                inv_closing = self.get_opening_closing(data['date_to'], data)
                credit_tot += inv_closing
            return debit_tot - credit_tot
        else:
            debit_tot = {}
            credit_tot = {}
            for i in movelines:
                date = str(i.date)
                d = datetime.strptime(date, "%Y-%m-%d")
                m = d.strftime('%B')
                y = str(d.year)
                month = m + '-' + y

                if month in debit_tot:
                    debit_tot[month]['month_debit'] += i.debit
                else:
                    debit_tot[month] = {'month_debit': i.debit}
                if month in credit_tot:
                    credit_tot[month]['month_credit'] += i.credit
                else:
                    credit_tot[month] = {'month_credit': i.credit}

            start_d = data['date_from']
            end_d = data['date_to']
            date10 = str(start_d)
            date11 = str(end_d)

            d10 = datetime.strptime(date10, "%Y-%m-%d")
            d11 = datetime.strptime(date11, "%Y-%m-%d")
            m = d10.strftime('%B')
            y = str(d10.year)
            month = m + '-' + y
            if d10.year == d11.year:
                months_count = abs(int(d10.month) - int(d11.month))
            else:
                months_count = abs(int(d10.month) - (12 + int(d11.month)))

            if data['date_from']:
                opening_date = datetime.strptime(data['date_from'], '%Y-%m-%d') - timedelta(days=1)
                inv_opening = self.get_opening_closing(opening_date.strftime("%Y-%m-%d"), data)
                if month in debit_tot:
                    debit_tot[month]['month_debit'] += inv_opening
                else:
                    debit_tot[month] = {'month_debit': inv_opening}

            for i in range(months_count + 1):

                d10 = d10 + relativedelta(day=1, months=1)
                mdate = d10 - timedelta(days=1)
                m10 = mdate.strftime('%B')
                y10 = str(mdate.year)
                month10 = m10 + '-' + y10
                m12 = d10.strftime('%B')
                y12 = str(d10.year)
                month22 = m12 + '-' + y12

                if mdate.month != d11.month:
                    inv_closing = self.get_opening_closing(
                        str(datetime.strptime(str(mdate), "%Y-%m-%d %H:%M:%S").date()), data)
                    if month10 in credit_tot:
                        credit_tot[month10]['month_credit'] += inv_closing
                    else:
                        credit_tot[month10] = {'month_credit': inv_closing}
                    if month22 in debit_tot:
                        debit_tot[month22]['month_debit'] += inv_closing
                    else:
                        debit_tot[month22] = {'month_debit': inv_closing}
                else:
                    if data['date_to']:
                        inv_closing = self.get_opening_closing(data['date_to'], data)
                        # credit_tot[month10] = {'month_credit': inv_closing}
                        if month10 in credit_tot:
                            credit_tot[month10]['month_credit'] += inv_closing
                        else:
                            credit_tot[month10] = {'month_credit': inv_closing}

            dc_tot = {}
            for d in data['months']:
                if d in credit_tot and d in debit_tot:
                    dc_tot[d] = {'month_total': debit_tot[d]['month_debit'] - credit_tot[d]['month_credit']}
                elif d in credit_tot and d not in debit_tot:
                    dc_tot[d] = {'month_total': 0 - credit_tot[d]['month_credit']}
                elif d not in credit_tot and d in debit_tot:
                    dc_tot[d] = {'month_total': debit_tot[d]['month_debit'] - 0}

            return dc_tot


    def get_opening_closing(self, date, data):
        if self.env['ir.model'].sudo().search([('model', '=', 'stock.move.line')]):
            doc = []
            if date:
                closing_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
                stock_line = self.env['stock.move.line']
                company = self.env.user.company_id
                wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)])
                location = wh.mapped('lot_stock_id').ids
                move_l = stock_line.sudo().search([('date', '<=', closing_date), ('company_id', 'in', company.ids), ('state', '=', 'done')]).ids
                transfer_out = self.env['stock.move.line'].search(
                    [('date', '<=', closing_date), ('company_id', 'not in', company.ids),
                     ('location_id', 'in', location),
                     ('state', '=', 'done')]).ids
                transfer_in = self.env['stock.move.line'].search(
                    [('date', '<=', closing_date), ('company_id', 'not in', company.ids),
                     ('location_dest_id', 'in', location),
                     ('state', '=', 'done')]).ids
                ids = move_l + transfer_out + transfer_in
                move_lines = self.env['stock.move.line'].search([('id', 'in', ids)], order="product_id, lot_id").sorted(
                    lambda line: line.product_id.name)
                if move_lines:
                    for line in move_lines:
                        if line.date:
                            try:
                                date = line.date.astimezone(pytz.timezone(self.env.context.get('tz')))
                            except:
                                raise Warning("Please set User Time Zone")
                            tax = 0
                            for i in line.product_id.taxes_id:
                                for j in i.children_tax_ids:
                                    tax += j.amount
                        doc.append({
                            'product_id': line.product_id.id,
                            'date': date,
                            'lot_id': line.lot_id.id,
                            'qty': float(line.qty_done),
                            'location': line.location_id.id,
                            'dest_location': line.location_dest_id.id,
                            'prate': line.lot_id.p_rate if line.lot_id else line.product_id.list_price,
                            'rate': line.lot_id.sales_rate if line.lot_id else line.product_id.list_price,
                            'tax': tax,
                            'pcs': line.lot_id.packing.name if line.lot_id else line.product_id.uom_id.name,
                            'unit_rate': line.lot_id.mrp if line.lot_id else line.product_id.list_price,
                            'factor': line.lot_id.packing.factor if line.lot_id else line.product_id.uom_id.factor,
                            'uom_type': line.lot_id.packing.uom_type if line.lot_id else line.product_id.uom_id.uom_type,
                        })

                if len(doc) > 0:
                    i = 0
                    pid = doc[0]['product_id']
                    lot_id = doc[0]['lot_id']
                    out_qty = 0
                    in_qty = 0
                    qty = 0
                    count = 0
                    rate_update = False
                    taxable_value_total = 0
                    tax_value_total = 0
                    mrp_value_total = 0
                    cost_value_total = 0

                    while i < len(doc):
                        if pid == doc[i]['product_id']:
                            if lot_id == doc[i]['lot_id']:
                                if doc[i]['uom_type'] == 'smaller':
                                    factor = 1
                                else:
                                    factor = doc[i]['factor']
                                if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                                    out_qty += doc[i]['qty']
                                elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                                    in_qty += doc[i]['qty']
                                qty = in_qty - out_qty
                                tax = doc[i]['tax']
                                prate = doc[i]['prate']
                                unit_rate = doc[i]['unit_rate']
                            else:
                                if qty < 1:
                                    count += 1
                                if qty != 0:
                                    if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                                        rate_update = self.env['rate.update.line'].search(
                                            [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', closing_date),
                                             ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')],
                                            order='id',
                                            limit=1)

                                    if rate_update:
                                        ur = rate_update.c_mrp * factor
                                        taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                                    else:
                                        # print(factor, doc[i]['product_name'], "484585")
                                        taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)

                                    tax_value = (taxable * tax) / 100
                                    mrp_value = taxable + tax_value
                                    cost_value = (prate / (1 / factor)) * qty
                                    taxable_value_total += taxable
                                    tax_value_total += tax_value
                                    mrp_value_total += mrp_value
                                    cost_value_total += cost_value


                                lot_id = doc[i]['lot_id']
                                out_qty = 0
                                in_qty = 0
                                qty = 0
                                if doc[i]['uom_type'] == 'smaller':
                                    factor = 1
                                else:
                                    factor = doc[i]['factor']
                                if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                                    out_qty += doc[i]['qty']
                                elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                                    in_qty += doc[i]['qty']
                                qty = in_qty - out_qty
                                tax = doc[i]['tax']
                                prate = doc[i]['prate']
                                unit_rate = doc[i]['unit_rate']

                        else:

                            if qty < 1:
                                count += 1
                            if qty != 0:
                                if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                                    rate_update = self.env['rate.update.line'].search(
                                        [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', closing_date),
                                         ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')],
                                        order='id',
                                        limit=1)

                                if rate_update:
                                    ur = rate_update.c_mrp * factor
                                    taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                                else:
                                    taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                                tax_value = (taxable * tax) / 100
                                mrp_value = taxable + tax_value
                                cost_value = (prate / (1 / factor)) * qty
                                taxable_value_total += taxable
                                tax_value_total += tax_value
                                mrp_value_total += mrp_value
                                cost_value_total += cost_value



                            pid = doc[i]['product_id']
                            lot_id = doc[i]['lot_id']
                            out_qty = 0
                            in_qty = 0
                            qty = 0
                            if lot_id == doc[i]['lot_id']:
                                if doc[i]['uom_type'] == 'smaller':
                                    factor = 1
                                else:
                                    factor = doc[i]['factor']
                                if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                                    out_qty += doc[i]['qty']
                                elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                                    in_qty += doc[i]['qty']
                                qty = in_qty - out_qty
                                tax = doc[i]['tax']
                                prate = doc[i]['prate']
                                unit_rate = doc[i]['unit_rate']
                            else:
                                if qty < 1:
                                    count += 1
                                if qty != 0:
                                    if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                                        rate_update = self.env['rate.update.line'].search(
                                            [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', closing_date),
                                             ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')],
                                            order='id',
                                            limit=1)

                                    if rate_update:
                                        ur = rate_update.c_mrp * factor
                                        taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                                    else:
                                        taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                                    tax_value = (taxable * tax) / 100
                                    mrp_value = taxable + tax_value
                                    cost_value = (prate / (1 / factor)) * qty
                                    taxable_value_total += taxable
                                    tax_value_total += tax_value
                                    mrp_value_total += mrp_value
                                    cost_value_total += cost_value


                                lot_id = doc[i]['lot_id']
                                out_qty = 0
                                in_qty = 0
                                qty = 0
                                if doc[i]['uom_type'] == 'smaller':
                                    factor = 1
                                else:
                                    factor = doc[i]['factor']
                                sales_rate = doc[i]['rate']
                                if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                                    out_qty += doc[i]['qty']
                                elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                                    in_qty += doc[i]['qty']
                                qty = in_qty - out_qty
                                tax = doc[i]['tax']
                                prate = doc[i]['prate']
                                unit_rate = doc[i]['unit_rate']

                        i = i + 1

                    if qty != 0:
                        if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                            rate_update = self.env['rate.update.line'].search(
                                [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', closing_date),
                                 ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')], order='id',
                                limit=1)

                        if rate_update:
                            ur = rate_update.c_mrp * factor
                            taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                        else:
                            taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                        tax_value = (taxable * tax) / 100
                        mrp_value = taxable + tax_value
                        cost_value = (prate / (1 / factor)) * qty

                        taxable_value_total += taxable
                        tax_value_total += tax_value
                        mrp_value_total += mrp_value
                        cost_value_total += cost_value

                    return cost_value_total
                else:
                    return 0
            else:
                return 0
        else:
            return 0


    # def get_opening_closing(self, date, data):
    #     final_data = []
    #     if self.env['ir.model'].sudo().search([('model', '=', 'stock.move.line')]):
    #         closing_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
    #         products = self.env['product.product'].search([('type', 'in', ['product', 'consu'])], order='name')
    #         stock_line = self.env['stock.move.line']
    #         company = self.env.user.company_id
    #         if 'branch' in data:
    #             wh = self.env['stock.warehouse'].search([('branch_id', 'in', data['branch'])])
    #             loc = wh.mapped('lot_stock_id').ids
    #         else:
    #             wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)])
    #             loc = [wh.lot_stock_id.id]
    #         for product in products:
    #             in_moves = stock_line.search(
    #                 [('location_dest_id', 'in', loc), ('product_id', '=', product.id), ('date', '<', closing_date),
    #                  ('state', '=', 'done')])
    #             out_moves = stock_line.search(
    #                 [('location_id', 'in', loc), ('product_id', '=', product.id), ('date', '<', closing_date),
    #                  ('state', '=', 'done')])
    #             qty_in = 0
    #             qty_out = 0
    #             lot_list = {}
    #             for in_move in in_moves:
    #                 in_q = in_move.product_uom_id._compute_quantity(in_move.qty_done, in_move.product_id.uom_id)
    #                 qty_in += in_q
    #                 if in_move.lot_id:
    #                     if in_move.lot_id.id not in lot_list:
    #                         lot_list[in_move.lot_id.id] = {
    #                             'quantity_in': in_q,
    #                             'quantity_out': 0,
    #                             'balance': in_q,
    #                         }
    #                     else:
    #                         lot_list[in_move.lot_id.id]['quantity_in'] += in_q
    #                         lot_list[in_move.lot_id.id]['balance'] += in_q
    #             for out_move in out_moves:
    #                 out_q = out_move.product_uom_id._compute_quantity(out_move.qty_done, out_move.product_id.uom_id)
    #                 qty_out += out_q
    #                 if out_move.lot_id:
    #                     if out_move.lot_id.id not in lot_list:
    #                         lot_list[out_move.lot_id.id] = {
    #                             'quantity_out': out_q,
    #                             'quantity_in': 0,
    #                             'balance': out_q,
    #                         }
    #                     else:
    #                         lot_list[out_move.lot_id.id]['quantity_out'] += out_q
    #                         lot_list[out_move.lot_id.id]['balance'] -= out_q
    #             qty = qty_in - qty_out
    #             lot = [key for key, values in lot_list.items() if values['balance'] > 0]
    #             # qty=product.with_context({'to_date': closing_date}).qty_available
    #             if qty != 0:
    #                 cost_value = self.get_product_cost_value(lot,product, qty, closing_date, [], data)
    #                 final_data.append(cost_value)
    #         return sum(final_data)
    #     return 0

    # def get_product_cost_value(self,lot, product, qty, date, moveid_list, data, moveid=None, ):
    #     value = 0
    #     stock_production_lot_obj = self.env['stock.production.lot'].sudo().search([('id', 'in', lot)])
    #     domain = [('product_id', '=', product.id), ('move_id.move_type', '=', 'in_invoice'),
    #               ('move_id.state', '=', 'posted'),
    #               ('exclude_from_invoice_tab', '=', False)]
    #     if 'direct_move_type' in self.env['account.move']._fields:
    #         domain.append(('move_id.direct_move_type', '=', 'incoming'))
    #     if date:
    #         domain.append(('date', '<', date))
    #     if moveid:
    #         moveid_list.append(moveid)
    #         domain.append(('id', 'not in', moveid_list))
    #     if 'branch' in data:
    #         domain.append(('move_id.branch_id', 'in', data['branch']))
    #
    #     moveline = self.env['account.move.line'].search(domain, order='date desc,id desc', limit=1)
    #     if moveline:
    #
    #         if moveline.quantity >= qty:
    #             value += qty * moveline.price_unit
    #         else:
    #             if 'generate_serial_number' in product._fields and product.generate_serial_number:
    #                 if stock_production_lot_obj:
    #                     total_purchase_rate = sum(stock_production_lot_obj.mapped('p_rate'))
    #                     average_purchase_rate = total_purchase_rate / len(stock_production_lot_obj) if len(stock_production_lot_obj) > 0 else 0
    #                     value += qty * average_purchase_rate
    #                 else:
    #                     value += qty * moveline.price_unit
    #             else:
    #                 value += moveline.quantity * moveline.price_unit
    #                 value += self.get_product_cost_value(product, qty - moveline.quantity, moveline.date, moveid_list, data,
    #                                                      moveid=moveline.id)
    #     else:
    #         value += qty * product.standard_price
    #     return value

    def get_prof_acc_dat(self, dom):
        account = self.env['account.financial.report'].search([
            ('id', '=', 1)
        ])
        account_types = self.get_child(account, account.account_type_ids)
        account_types = list(set(account_types.ids))
        movelines = self.env['account.move.line'].search([('account_id.user_type_id', 'in', account_types)] + dom)
        debit_tot = sum(movelines.mapped('debit'))
        credit_tot = sum(movelines.mapped('credit'))
        return debit_tot - credit_tot

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(searchDateFrom=self.date_from.strftime('%Y-%m-%d'),
                                    searchDateTo=self.date_to.strftime('%Y-%m-%d'),
                                    report_type=self.report_type,
                                    searchWithoutOpening=self.with_opening, summary=self.summary,
                                    monthwise=self.month_wise)
        res['lines'] = self.env.ref('profit_loss_balance_sheet.report_financial')._render(
            {
                'data': res['lines']['data'],
                'account_report': res['lines']['account_report'],
                'tot': res['lines']['tot'],
                'rows': res['lines']['rows'],
                'g_tot': res['lines']['g_tot'],
                'final_list': res['lines']['final_list'],
                'table': res['lines']['table'],
                'table2': res['lines']['table2'],
                'branch_name': res['lines']['branch_name'],
                'summary': res['lines']['summary'],
                'order': res['lines']['order'],
                'monthwise': res['lines']['monthwise'],
                'months': res['lines']['months'],
            })
        self.template_area = res['lines']

    def _get_report_data(self, searchDateFrom=False, searchDateTo=False, report_type=False,
                         searchWithoutOpening=False, summary=False, order='account_branch', monthwise=False):
        if report_type == 'balance_sheet':
            rep_id = 8
        else:
            rep_id = 1
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
            'without_opening': searchWithoutOpening,
            'context': {},
            'summary': summary,
            'monthwise': monthwise if monthwise else False,
            'order': order
        }
        data['context']['default_account_report_id'] = rep_id
        if searchDateTo and searchDateFrom:
            DateFrom = datetime.strptime(searchDateFrom, '%Y-%m-%d').date()
            DateTo = datetime.strptime(searchDateTo, '%Y-%m-%d').date()
            data['nonopendate'] = searchDateFrom
            date_from = DateFrom
            date_to = DateTo
            data['date_to'] = searchDateTo

            if searchWithoutOpening:
                day_difference = (date_to - datetime(date_to.year, 4, 1).date()).days
                if day_difference >= 0:
                    data['date_from'] = datetime(date_to.year, 4, 1).date().strftime('%Y-%m-%d')
                else:
                    data['date_from'] = datetime(date_to.year - 1, 4, 1).date().strftime('%Y-%m-%d')
            else:
                data['date_from'] = searchDateFrom
                if DateTo and DateFrom:
                    if data['date_from'] > data['date_to']:
                        raise UserError("From date can't be greater than To date")

                start_yr = date_from.year
                end_yr = date_to.year
                if start_yr == end_yr: end_yr += 1
                if date_from >= datetime(start_yr, 4, 1).date():
                    if date_to <= datetime(end_yr, 3, 31).date():
                        pass
                    else:
                        raise UserError(_("Select Date Between 01/04/%s to 31/03/%s") % (start_yr, end_yr))
                else:
                    if date_to <= datetime(start_yr, 3, 31).date():
                        pass
                    else:

                        raise UserError(_("Select Date Between 01/04/%s to 31/03/%s") % (start_yr, end_yr))
        if self._context.get('allowed_company_ids'):
            data['allowed_company_ids'] = self._context.get('allowed_company_ids')
        if self._context.get('allowed_company_ids'):
            data['allowed_company_ids'] = self._context.get('allowed_company_ids')
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
