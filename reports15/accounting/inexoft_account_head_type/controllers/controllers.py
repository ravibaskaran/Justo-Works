# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class AccountTypeCustom(http.Controller):
    @http.route('/account_type/correction', auth='public')
    def index(self, **kw):
        move = request.env['account.account.type'].search([])
        if move:
            for j in move:
                to_remove = False
                to_add = False
                type = 0
                type1 = 0
                if j.internal_group:
                    if j.internal_group == 'trading_account':
                        to_remove = request.env.ref("manufacturing_trading.data_trading_account")
                    elif j.internal_group == 'manuf_account':
                        to_remove = request.env.ref("manufacturing_trading.data_manuf_account")
                    elif j.internal_group == 'asset':
                        to_remove = request.env['account.financial.report'].search(
                            [('name', '=', 'Balance Sheet'), ('type', '=', 'sum')])
                    elif j.internal_group == 'liability':
                        to_remove = request.env['account.financial.report'].search(
                            [('name', '=', 'Liability'), ('type', '=', 'sum')])
                    elif j.internal_group == 'income':
                        to_remove = request.env['account.financial.report'].search(
                            [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])

                    elif j.internal_group == 'expense':
                        to_remove = request.env['account.financial.report'].search(
                            [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
                        type = 1
                    if j.internal_group == 'trading_account':
                        to_add = request.env.ref("manufacturing_trading.data_trading_account")
                    elif j.internal_group == 'manuf_account':
                        to_add = request.env.ref("manufacturing_trading.data_manuf_account")
                    elif j.internal_group == 'asset':
                        to_add = request.env['account.financial.report'].search(
                            [('name', '=', 'Balance Sheet'), ('type', '=', 'sum')])
                    elif j.internal_group == 'liability':
                        to_add = request.env['account.financial.report'].search(
                            [('name', '=', 'Liability'), ('type', '=', 'sum')])
                    elif j.internal_group == 'income':
                        to_add = request.env['account.financial.report'].search(
                            [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
                    elif j.internal_group == 'expense':
                        to_add = request.env['account.financial.report'].search(
                            [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
                        type1 = 1

                if to_remove:
                    if to_remove.children_ids:
                        to_remove.children_ids[type].account_type_ids -= j
                if to_add:
                    if to_add.children_ids:
                        to_add.children_ids[type1].account_type_ids += j
                    else:
                        to_add.children_ids.create({'name': to_add.name.split(' ')[type1],
                                                     'parent_id': to_add.id,
                                                     'type': 'account_type',
                                                     })
                        to_add.children_ids[type1].account_type_ids += j
        return "Success"

