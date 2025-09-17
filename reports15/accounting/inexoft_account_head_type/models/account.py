# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    internal_group = fields.Selection(
        selection_add=[('trading_account', 'Trading A/C'), ('manuf_account', 'Manufacturing A/C'),
                       ('bs_other', 'B.S Other')],
        ondelete={'trading_account': 'cascade', 'manuf_account': 'cascade', 'bs_other': 'cascade', })

    def remove_account_type_ids(self, res, account,type):
        if account.children_ids:
            account.children_ids[type].account_type_ids -= res
    
    def add_account_type_ids(self, res, account,type):
        if account.children_ids:
            account.children_ids[type].account_type_ids += res
        else:
            account.children_ids.create({'name': account.name.split(' ')[type],
                                         'parent_id': account.id,
                                         'type': 'account_type',
                                         })
            account.children_ids[type].account_type_ids += res
    
    
    @api.model
    def create(self,vals):
        res=super(AccountAccountType,self).create(vals)
        account = False
        type = 0
        if res.internal_group=='trading_account':
            account = self.env.ref("manufacturing_trading.data_trading_account")
        elif res.internal_group == 'manuf_account':
            account=self.env.ref("manufacturing_trading.data_manuf_account")
        elif res.internal_group == 'asset':
            account = self.env['account.financial.report'].search([('name','=','Balance Sheet'),('type','=','sum')])
        elif res.internal_group == 'liability':
            account = self.env['account.financial.report'].search([('name','=','Liability'),('type','=','sum')])
        elif res.internal_group == 'income':
            account = self.env['account.financial.report'].search([('name','=','Profit and Loss'),('type','=','sum')])
        elif res.internal_group == 'expense':
            account = self.env['account.financial.report'].search(
                [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
            type = 1

        if account:
            self.add_account_type_ids(res,account,type)
        return res

    def write(self, vals):
        to_remove = False
        to_add = False
        type = 0
        type1=0
        if vals.get('internal_group'):
            if self.internal_group == 'trading_account':
                to_remove = self.env.ref("manufacturing_trading.data_trading_account")
            elif self.internal_group == 'manuf_account':
                to_remove = self.env.ref("manufacturing_trading.data_manuf_account")
            elif self.internal_group == 'asset':
                to_remove = self.env['account.financial.report'].search(
                    [('name', '=', 'Balance Sheet'), ('type', '=', 'sum')])
            elif self.internal_group == 'liability':
                to_remove = self.env['account.financial.report'].search(
                    [('name', '=', 'Liability'), ('type', '=', 'sum')])
            elif self.internal_group == 'income':
                to_remove = self.env['account.financial.report'].search(
                    [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])

            elif self.internal_group == 'expense':
                to_remove = self.env['account.financial.report'].search(
                    [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
                type = 1
            if vals.get('internal_group') == 'trading_account':
                to_add = self.env.ref("manufacturing_trading.data_trading_account")
            elif vals.get('internal_group') == 'manuf_account':
                to_add = self.env.ref("manufacturing_trading.data_manuf_account")
            elif vals.get('internal_group') == 'asset':
                to_add = self.env['account.financial.report'].search(
                    [('name', '=', 'Balance Sheet'), ('type', '=', 'sum')])
            elif vals.get('internal_group') == 'liability':
                to_add = self.env['account.financial.report'].search(
                    [('name', '=', 'Liability'), ('type', '=', 'sum')])
            elif vals.get('internal_group') == 'income':
                to_add = self.env['account.financial.report'].search(
                    [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])

            elif vals.get('internal_group') == 'expense':
                to_add = self.env['account.financial.report'].search(
                    [('name', '=', 'Profit and Loss'), ('type', '=', 'sum')])
                type1 = 1
        res = super(AccountAccountType, self).write(vals)
        if to_remove:
            self.remove_account_type_ids(self, to_remove,type)
        if to_add:
            self.add_account_type_ids(self, to_add,type1)
        return res