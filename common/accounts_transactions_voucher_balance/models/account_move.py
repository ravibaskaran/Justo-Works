# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.fields import datetime


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    journal_balance = fields.Char(compute="_compute_journal_balance", store=False)

    @api.depends('direct_journal_id_inx')
    def _compute_journal_balance(self):
        self.journal_balance = ''
        if self.direct_journal_id_inx:
            move_line_obj = self.env['account.move.line']
            domain = [('move_id.state', '=', 'posted'), ('move_id.date', '<=', datetime.now()),
                      ('account_id', '=', self.direct_journal_id_inx.default_account_id.id)]
            if 'branch_id' in self._fields:
                domain.append(('move_id.branch_id', '=', self.branch_id.id))
            move_lines = move_line_obj.search(domain)
            debit = sum(move_lines.mapped('debit'))
            credit = sum(move_lines.mapped('credit'))
            if debit > credit:
                coeff = '(Dr)'
            elif debit < credit:
                coeff = '(Cr)'
            else:
                coeff = ''
            self.journal_balance = str('{:.2f}'.format(abs(debit - credit))) + coeff
