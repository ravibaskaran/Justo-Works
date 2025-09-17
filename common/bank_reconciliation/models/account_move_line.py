# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    bank_statement_id = fields.Many2one('bank.statement', 'Bank Statement', copy=False)
    statement_date = fields.Date('Bank.St Date', copy=False)
    reconciled = fields.Boolean('reconciled', default=False)

    def write(self, vals):
        if not vals.get("statement_date"):
            vals.update({"reconciled": False})
            # for record in self:
            #     if record.payment_id and record.payment_id.state == 'reconciled':
            #         record.payment_id.state = 'posted'
            #         print(record.payment_id.state, "record.payment_id.state")
        elif vals.get("statement_date"):
            vals.update({"reconciled": True})
            # for record in self:
            #     if record.payment_id:
            #         record.payment_id.state = 'reconciled'
            #         print(record.payment_id.state,"record.payment_id.state")
        res = super(AccountMoveLine, self).write(vals)
        return res

#
