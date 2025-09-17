# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.fields import datetime

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    partner_journal_balance = fields.Char(compute="_compute_partner_journal_balance", store=False)
    journal_balance = fields.Char(compute="_compute_journal_balance", store=False)

    @api.depends('partner_id')
    def _compute_partner_journal_balance(self):
        self.partner_journal_balance = 0.0
        if self.partner_id:
            move_line_obj = self.env['account.move.line']
            domain = [('move_id.state', '=', 'posted'), ('move_id.date', '<=', self.date)]
            if self.partner_type == 'customer':
                account_id = self.partner_id.property_account_receivable_id
                if 'create_receivable_account' in self.env['res.config.settings']._fields:
                    create_receivable_account = self.env['ir.config_parameter'].sudo().get_param(
                        'partner_account_creation.create_receivable_account')
                    if not create_receivable_account:
                        domain.append(('partner_id', '=', self.partner_id.id))
                else:
                    domain.append(('partner_id', '=', self.partner_id.id))
            else:
                account_id = self.partner_id.property_account_payable_id
                if 'create_payable_account' in self.env['res.config.settings']._fields:
                    create_payable_account = self.env['ir.config_parameter'].sudo().get_param(
                        'partner_account_creation.create_payable_account')
                    if not create_payable_account:
                        domain.append(('partner_id', '=', self.partner_id.id))
                else:
                    domain.append(('partner_id', '=', self.partner_id.id))
            domain.append(('account_id', '=', account_id.id))
            if 'branch_id' in self._fields:
                domain.append(('branch_id', '=', self.branch_id.id))
            move_lines = move_line_obj.search(domain)
            # print(domain,'domian')
            debit = sum(move_lines.mapped('debit'))
            credit = sum(move_lines.mapped('credit'))
            if debit > credit:
                coeff = '(Dr)'
            elif debit < credit:
                coeff = '(Cr)'
            else:
                coeff = ''
            self.partner_journal_balance = str('{:.2f}'.format(abs(debit - credit))) + coeff


    @api.depends('journal_id')
    def _compute_journal_balance(self):
        self.journal_balance = ''
        if self.journal_id:
            move_line_obj = self.env['account.move.line']
            domain = [('move_id.state', '=', 'posted'), ('move_id.date', '<=', self.date),
                      ('account_id', '=', self.journal_id.default_account_id.id)]
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

