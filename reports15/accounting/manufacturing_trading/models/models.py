# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import pytz


class BetaManufacturingTrading(models.TransientModel):  # change this
    _name = 'beta.manufacturing.trading'  # change this
    _inherit = 'beta.reports'

    name = fields.Char()  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    without_opening = fields.Boolean()
    summary = fields.Boolean()
    last_purchase_cost = fields.Boolean()
    report_type = fields.Selection([('manufacturing', 'Manufacturing'), ('trading', 'Trading')])

    @api.model
    def default_get(self, fields_list):
        res = super(BetaManufacturingTrading, self).default_get(fields_list)
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
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d")
        linedata = self.get_trading_accounts_data(data)
        debit_data = linedata[0]
        credit_data = linedata[1]
        table = []
        table2 = []
        i = 100
        id1 = ''
        j = 100
        id2 = ''
        direction = ''
        if data['summary']:
            direction = 'right'
        else:
            direction = 'down'
        if 'branch' in data:
            branch_ids = data['branch']
        else:
            branch_ids = 'false'
        credit_total = []
        debit_total = []
        for credit_key in list(credit_data.keys()):
            c_total = 0
            if credit_data[credit_key].get('child'):
                for child in credit_data[credit_key]['child']:
                    c_total += credit_data[credit_key]['child'][child]['balance'] * -1
                credit_total.append({'type': credit_data[credit_key]['name'], 'total': c_total})
        for credit_key in list(credit_data.keys()):
            if credit_data[credit_key].get('child'):
                i = i + 1
                id1 = "credit" + str(i)
                balance = 0
                for cr in credit_total:
                    if cr['type'] == credit_data[credit_key]['name']:
                        balance = cr['total']
                table.append(
                    [
                        '<td class="parent" id="' + id1 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 10px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                        credit_data[credit_key]['name'] + '</td>',
                        '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right: 1px solid;">' + str(
                            "{:.2f}".format(balance)) + '</td>'])
                for child in credit_data[credit_key]['child']:

                    res_id = str(credit_data[credit_key]['child'][child]['account_id'])
                    if data['summary']:
                        table.append(
                            [
                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                    data['date_from']) + '" data-date-to="' + str(
                                    data['date_to']) + '" data-branch-ids="' + str(
                                    branch_ids) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                '<td class="text-right child-' + id1 + '"style="padding-right: 10px;display:none;border-right: 1px solid;">' +
                                str("{:.2f}".format(credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                        )
                    else:
                        table.append(
                            [
                                '<td class="child-' + id1 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                    data['date_from']) + '" data-date-to="' + str(
                                    data['date_to']) + '" data-branch-ids="' + str(
                                    branch_ids) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                credit_data[credit_key]['child'][child]['name'] + '</a></td>',
                                '<td class="text-right child-' + id1 + '"style="padding-right: 10px;border-right: 1px solid;">' +
                                str("{:.2f}".format(
                                    credit_data[credit_key]['child'][child]['balance'] * -1)) + '</td>']
                        )
            else:
                table.append([
                    '<td style="font-weight:bold;padding-left: 10px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;">' +
                    credit_data[credit_key]['name'],
                    '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right: 1px solid;">' +
                    str("{:.2f}".format(credit_data[credit_key]['balance'] * -1)) if credit_data[
                        credit_key].get(
                        'balance') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right: 1px solid;">0.00</td>'
                ])

        for debit_key in list(debit_data.keys()):
            d_total = 0
            if debit_data[debit_key].get('child'):
                for child2 in debit_data[debit_key]['child']:
                    d_total += debit_data[debit_key]['child'][child2]['balance']
                debit_total.append({'type': debit_data[debit_key]['name'], 'total': d_total})
        for debit_key in list(debit_data.keys()):
            if debit_data[debit_key].get('child'):
                j = j + 1
                id2 = "debit" + str(j)
                balance = 0
                for dr in debit_total:
                    if dr['type'] == debit_data[debit_key]['name']:
                        balance = dr['total']
                table2.append(
                    [
                        '<td class="parent" id="' + id2 + '" title="Click to expand/collapse" style="font-weight:bold;padding-left: 10px;cursor: pointer;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><span class="o_trial_reports_foldable 1 o_trial_reports_caret_icon"><i class="fa fa-fw fa-caret-' + direction + '" role="img" aria-label="Fold" title="Fold" style="width: 30px;"></i></span>' +
                        debit_data[debit_key]['name'] + '</td>',
                        '<td class="text-right" style="font-weight:bold;padding-right: 10px;cursor: pointer;border-right: 1px solid;">' + str(
                            "{:.2f}".format(balance)) + '</td>'])
                for child2 in debit_data[debit_key]['child']:
                    res_id = str(debit_data[debit_key]['child'][child2]['account_id'])
                    if data['summary']:
                        table2.append(
                            [
                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;display:none;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                    data['date_from']) + '" data-date-to="' + str(
                                    data['date_to']) + '" data-branch-ids="' + str(
                                    branch_ids) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                '<td class="text-right child-' + id2 + '"style="padding-right: 10px;display:none;border-right: 1px solid;" >' +
                                str("{:.2f}".format(debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])
                    else:
                        table2.append(
                            [
                                '<td  class="child-' + id2 + '" style="padding-left: 20px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;"><a href="#" class="o_general_ledger_action" data-res-id="' + res_id + '" data-date-from="' + str(
                                    data['date_from']) + '" data-date-to="' + str(
                                    data['date_to']) + '" data-branch-ids="' + str(
                                    branch_ids) + '" style="text-decoration: none !important;color: inherit !important;">' +
                                debit_data[debit_key]['child'][child2]['name'] + '</a></td>',
                                '<td class="text-right child-' + id2 + '"style="padding-right: 10px;border-right: 1px solid;" >' +
                                str("{:.2f}".format(debit_data[debit_key]['child'][child2]['balance'])) + '</td>'])

            else:
                table2.append([
                    '<td style="font-weight:bold;padding-left: 10px;border-right:1px solid;text-overflow: ellipsis;white-space: nowrap;overflow: hidden;max-width: 10px;">' +
                    debit_data[debit_key]['name'],
                    '<td class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right: 1px solid;">' +
                    str("{:.2f}".format(debit_data[debit_key]['balance']))
                    if debit_data[debit_key].get(
                        'balance') else '<td  class="text-right" style="font-weight:bold;padding-left: 5px;padding-right: 10px;border-right: 1px solid;">0.00</td>'
                ])
        final_list = []
        maxlen = len(table) if len(table) > len(table2) else len(table2)
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

        if data['date_from'] and data['date_to']:
            date_from = date_from.strftime('%d/%m/%Y')
            date_to = date_to.strftime('%d/%m/%Y')

        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'debit_data': linedata[0],
            'credit_data': linedata[1],
            'tot': round(linedata[2] + linedata[3], 2),
            'rows': linedata[4],
            'g_tot': linedata[2] if linedata[2] >= (linedata[3] * -1) else linedata[3] * -1,
            'final_list': final_list,
            'branch_name': branch_name,
            'table': table,
            'table2': table2,
            'summary': data['summary'],

        }

    def get_trading_accounts_data(self, data):
        account = False
        if data['type'] == 'trading':
            account = self.env.ref("manufacturing_trading.data_trading_account")
        elif data['type'] == 'manufacturing':
            account = self.env.ref("manufacturing_trading.data_manuf_account")
        account_types = self.get_child(account, account.account_type_ids)
        dom = [('move_id.state', '=', 'posted')]
        if 'branch' in data:
            dom.append(('move_id.branch_id', 'in', data['branch']))
            branch = data['branch']
        else:
            branch = False
        res = self.get_report_template_data(data, set(account_types), account, dom, data['date_from'], data['without_opening'], branch)
        return res

    def get_report_template_data(self, data, account_types, account, dom, date_from, wopening, branch):
        movelines_all = self.env['account.move.line']
        credit_data = {}
        debit_data = {}
        deb_row, cre_row = 0, 0
        debit_tot = 0
        credit_tot = 0
        if data['date_from']:
            dom.append(('move_id.date', '>=', data['date_from']))
            opening_date = datetime.strptime(data['date_from'], '%Y-%m-%d') - timedelta(days=1)
            opening = self.get_opening_closing(movelines_all, opening_date.strftime("%Y-%m-%d"), data)
            debit_data['op_stk'] = {
                'name': 'Opening Stock A/C',
                'balance': opening,
            }
            print(opening)
            debit_tot += opening
        if data['date_to']:
            dom.append(('move_id.date', '<=', data['date_to']))

        if data.get('allowed_company_ids'):
            dom.append(('company_id', 'in', data.get('allowed_company_ids')))

        for account_type in account_types:
            movelines = movelines_all.search([('account_id.user_type_id', '=', account_type.id)] + dom)
            if account_type.id == 3:
                account_type
            childs = {}
            for moveline in movelines:
                if moveline.account_id.id in childs:
                    childs[moveline.account_id.id]['balance'] += moveline.debit - moveline.credit
                else:
                    tot_open = 0
                    if not wopening:
                        opening = self.get_trading_credit_and_debit(moveline.account_id.id, date_from,
                                                                    branch)
                        if opening[0] or opening[1]:
                            debit = opening[1]
                            credit = opening[0]
                            tot_open = debit - credit

                    childs[moveline.account_id.id] = {
                        'name': str(moveline.account_id.code) + '-' + moveline.account_id.name,
                        'balance': (moveline.debit - moveline.credit) + tot_open,
                        'account_id': moveline.account_id.id,
                    }

            if childs:
                for child_id in childs:
                    if childs[child_id]['balance'] >= 0:
                        if account_type.id in debit_data:
                            debit_data[account_type.id]['child'][child_id] = childs[child_id]
                            debit_tot += childs[child_id]['balance']
                        else:
                            debit_data[account_type.id] = {
                                'name': account_type.name,
                                'child': {child_id: childs[child_id]}
                            }
                            debit_tot += childs[child_id]['balance']
                    else:
                        if account_type.id in credit_data:
                            credit_data[account_type.id]['child'][child_id] = childs[child_id]
                            credit_tot += childs[child_id]['balance']
                        else:
                            credit_data[account_type.id] = {
                                'name': account_type.name,
                                'child': {child_id: childs[child_id]}
                            }
                            credit_tot += childs[child_id]['balance']
        closing = self.get_opening_closing(movelines_all, data['date_to'], data) * -1  # -ve values in credit
        credit_data['cl_stk'] = {
            'name': 'Closing Stock A/C',
            'balance': closing,
        }
        credit_tot += closing
        return [debit_data, credit_data, debit_tot, credit_tot, deb_row - cre_row, account]

    def get_opening_closing(self, movelines_all, date, data):
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



    # def get_opening_closing(self, movelines_all, date, data):
    #     if self.env['ir.model'].sudo().search([('model', '=', 'stock.move.line')]):
    #         final_data = []
    #         amount_sum = 0
    #         if date:
    #             closing_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
    #             products = self.env['product.product'].search([('type', 'in', ['product', 'consu'])], order='name')
    #             stock_line = self.env['stock.move.line']
    #             company = self.env.user.company_id
    #             if 'branch' in data:
    #                 wh = self.env['stock.warehouse'].search([('branch_id', 'in', data['branch'])])
    #                 loc = wh.mapped('lot_stock_id').ids
    #             else:
    #                 wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)])
    #                 loc = [wh.lot_stock_id.id]
    #             for product in products:
    #                 in_moves = stock_line.search(
    #                     [('location_dest_id', 'in', loc), ('product_id', '=', product.id), ('date', '<', closing_date),
    #                      ('state', '=', 'done')])
    #                 out_moves = stock_line.search(
    #                     [('location_id', 'in', loc), ('product_id', '=', product.id), ('date', '<', closing_date),
    #                      ('state', '=', 'done')])
    #                 qty_in = 0
    #                 qty_out = 0
    #                 lot_list = {}
    #                 for in_move in in_moves:
    #                     in_q = in_move.product_uom_id._compute_quantity(in_move.qty_done, in_move.product_id.uom_id)
    #                     qty_in += in_q
    #                     if in_move.lot_id:
    #                         if in_move.lot_id.id not in lot_list:
    #                             lot_list[in_move.lot_id.id] = {
    #                                 'quantity_in': in_q,
    #                                 'quantity_out': 0,
    #                                 'balance': in_q,
    #                             }
    #                         else:
    #                             lot_list[in_move.lot_id.id]['quantity_in'] += in_q
    #                             lot_list[in_move.lot_id.id]['balance'] += in_q
    #                 for out_move in out_moves:
    #                     out_q = out_move.product_uom_id._compute_quantity(out_move.qty_done, out_move.product_id.uom_id)
    #                     qty_out += out_q
    #                     if out_move.lot_id:
    #                         if out_move.lot_id.id not in lot_list:
    #                             lot_list[out_move.lot_id.id] = {
    #                                 'quantity_out': out_q,
    #                                 'quantity_in': 0,
    #                                 'balance': out_q,
    #                             }
    #                         else:
    #                             lot_list[out_move.lot_id.id]['quantity_out'] += out_q
    #                             lot_list[out_move.lot_id.id]['balance'] -= out_q
    #                 qty = qty_in - qty_out
    #                 lot = [key for key, values in lot_list.items() if values['balance'] > 0]
    #                 if qty != 0:
    #                     cost_value = self.get_product_cost_value(movelines_all, product, qty, closing_date, [], data,lot)
    #                     final_data.append(cost_value)
    #             amount_sum = sum(final_data)
    #         return amount_sum
    #     return 0

    # def get_product_cost_value(self, movelines_all, product, qty, date, moveid_list, data,lot, moveid=None):
    #     value = 0
    #     stock_production_lot_obj = self.env['stock.production.lot'].sudo().search([('id', 'in', lot)])
    #     domain = [('product_id', '=', product.id), ('move_id.move_type', '=', 'in_invoice'),
    #               ('move_id.state', '=', 'posted'),
    #               ('exclude_from_invoice_tab', '=', False)]
    #     if 'direct_move_type' in self.env['account.move']._fields:
    #         domain.append(('move_id.direct_move_type', '=', 'incoming'))
    #     if 'branch' in data:
    #         domain.append(('move_id.branch_id', 'in', data['branch']))
    #     if date:
    #         # domain.append(('date', '<=', date))
    #         domain.append(('date', '<', date))
    #     if moveid:
    #         moveid_list.append(moveid)
    #         domain.append(('id', 'not in', moveid_list))
    #         # domain.append(('id','!=', moveid))
    #     moveline = self.env['account.move.line'].search(domain, order='date desc,id desc', limit=1)
    #     if moveline:
    #         if data['last_purchase_cost']:
    #             return qty * moveline.price_unit
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
    #                 value += self.get_product_cost_value(movelines_all, product, qty - moveline.quantity, moveline.date,
    #                                                  moveid_list, data,lot, moveid=moveline.id)
    #     else:
    #         if data['last_purchase_cost']:
    #             return qty * product.standard_price
    #         value += qty * product.standard_price
    #     return value

    def get_child(self, account, acc_type):
        if not account.children_ids:
            if account.account_type_ids not in acc_type:
                return account.account_type_ids
        else:
            for child in account.children_ids:
                acc_type += self.get_child(child, acc_type)
        return acc_type

    def get_trading_credit_and_debit(self, account, date_from, branch):
        credit = debit = 0
        if date_from:
            domain = [('move_id.state', '=', 'posted'), ('date', '<', date_from), ('account_id', '=', account)]
            account_id = self.env['account.account'].search([('id','=',account)])
            selected_year = datetime.strptime(str(date_from), '%Y-%m-%d')
            date_f = datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            date_fr = datetime.strptime(str(date_f), '%d-%m-%Y').date()
            if not account_id.user_type_id.include_initial_balance:
                # today = date.today()
                if date_fr < datetime.strptime('01-04-' + str(selected_year.year), '%d-%m-%Y').date():
                    fin_date = str(selected_year.year-1) + '-04-01'
                else:
                    fin_date = str(selected_year.year) + '-04-01'
                domain.append(('date','>=',fin_date))
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
            for move in moves:
                credit += move.credit
                debit += move.debit
        return (credit, debit)

    def get_html(self):
        if self.date_from > self.date_to:
            raise UserError('From date should be less than to date')
        res = self._get_report_data(searchDateFrom=self.date_from.strftime('%Y-%m-%d'),
                                    searchDateTo=self.date_to.strftime('%Y-%m-%d'),
                                    report_type=self.report_type,
                                    searchWithoutOpening=self.without_opening, summary=self.summary,
                                    last_purchase_cost=self.last_purchase_cost)
        res['lines'] = self.env.ref('manufacturing_trading.report_manufacturing_trading')._render(
            {
                'data': res['lines']['data'],
                'date_from': res['lines']['date_from'],
                'date_to': res['lines']['date_to'],
                'debit_data': res['lines']['debit_data'],
                'credit_data': res['lines']['credit_data'],
                'tot': res['lines']['tot'],
                'rows': res['lines']['rows'],
                'g_tot': res['lines']['g_tot'],
                'final_list': res['lines']['final_list'],
                'branch_name': res['lines']['branch_name'],
                'summary': res['lines']['summary'],
                'table': res['lines']['table'],
                'table2': res['lines']['table2'],
            })
        self.template_area = res['lines']

    def _get_report_data(self, searchDateFrom=False, searchDateTo=False, report_type=False,
                         searchWithoutOpening=False, summary=False, last_purchase_cost=False):
        data = {
            'date_from': searchDateFrom,
            'date_to': searchDateTo,
            'type': report_type,
            'without_opening': searchWithoutOpening,
            'summary': summary,
            'last_purchase_cost': last_purchase_cost,
        }
        if searchDateTo and searchDateFrom:
            DateFrom = datetime.strptime(searchDateFrom, '%Y-%m-%d').date()
            DateTo = datetime.strptime(searchDateTo, '%Y-%m-%d').date()
            date_from = DateFrom
            date_to = DateTo
            data['date_to'] = searchDateTo
            if not searchWithoutOpening:
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
            'lines': dat
        }
