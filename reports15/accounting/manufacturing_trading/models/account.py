# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    internal_group = fields.Selection(
        selection_add=[('trading_account', 'Trading A/C'), ('manuf_account', 'Manufacturing A/C'),
                       ('bs_other', 'B.S Other')],
        ondelete={'trading_account': 'cascade', 'manuf_account': 'cascade', 'bs_other': 'cascade', })

    def remove_account_type_ids(self, res, account):
        if account.children_ids:
            account.children_ids[0].account_type_ids -= res

    def add_account_type_ids(self, res, account):
        if account.children_ids:
            account.children_ids[0].account_type_ids += res
        else:
            account.children_ids.create({'name': account.name.split(' ')[0],
                                         'parent_id': account.id,
                                         'type': 'account_type',
                                         })
            account.children_ids[0].account_type_ids += res

    @api.model
    def create(self, vals):
        res = super(AccountAccountType, self).create(vals)
        account = False
        if res.internal_group == 'trading_account':
            account = self.env.ref("manufacturing_trading.data_trading_account")
        elif res.internal_group == 'manuf_account':
            account = self.env.ref("manufacturing_trading.data_manuf_account")
        if account:
            self.add_account_type_ids(res, account)
        return res

    def write(self, vals):
        to_remove = False
        to_add = False
        if vals.get('internal_group'):
            if self.internal_group == 'trading_account':
                to_remove = self.env.ref("manufacturing_trading.data_trading_account")
            elif self.internal_group == 'manuf_account':
                to_remove = self.env.ref("manufacturing_trading.data_manuf_account")
            if vals.get('internal_group') == 'trading_account':
                to_add = self.env.ref("manufacturing_trading.data_trading_account")
            elif vals.get('internal_group') == 'manuf_account':
                to_add = self.env.ref("manufacturing_trading.data_manuf_account")
        res = super(AccountAccountType, self).write(vals)
        if to_remove:
            self.remove_account_type_ids(self, to_remove)
        if to_add:
            self.add_account_type_ids(self, to_add)
        return res
