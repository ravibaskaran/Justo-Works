# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('cash_book.cash_book_account_id', self.cash_book_account_id.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        with_user = self.env['ir.config_parameter'].sudo()
        cash_book_account_id = with_user.get_param('cash_book.cash_book_account_id')
        res.update(
            cash_book_account_id=[(6, 0, literal_eval(cash_book_account_id))] if cash_book_account_id else False, )
        return res

    cash_book_account_id = fields.Many2many('account.account','cash_book_filter')
