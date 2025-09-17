from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = 'account.account'

    comment = fields.Html(string='Notes')

    @api.onchange('user_type_id')
    def fill_code_from_account_type(self):
        self.code = False
        if self.user_type_id.prefix:
            self.code = self.user_type_id.prefix + '-' + f'{self.user_type_id.next_number:05d}'
        elif self.user_type_id:
            raise UserError('No prefix in account type!')

    @api.model
    def create(self, values):
        res = super(AccountAccount, self).create(values)
        if res.user_type_id.prefix:
            res.user_type_id.next_number += 1
        return res

    @api.onchange('user_type_id')  # Replaced to block default taxes autocompletion
    def _onchange_user_type_id(self):
        self.reconcile = self.internal_type in ('receivable', 'payable')
        if self.internal_type == 'liquidity':
            self.reconcile = False
        elif self.internal_group == 'off_balance':
            self.reconcile = False


class AccountAccountType(models.Model):
    _inherit = 'account.account.type'

    next_number = fields.Integer(default=1)
    prefix = fields.Char()
    sequence = fields.Integer()