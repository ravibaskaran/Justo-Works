# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def default_get(self, fields):
        res = super(AccountMove, self).default_get(fields)
        if 'default_direct_journal_type_inx' in self._context and self._context['default_direct_journal_type_inx'] in ['receipt','payment']:
            res['direct_journal_id_inx'] = self.env['account.journal'].search([('type','=','cash')], limit=1).id
        return res

    direct_journal_entry_inx = fields.Boolean(default=False)
    direct_journal_id_inx = fields.Many2one('account.journal', string='Journal',
                                 domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]", track_visibility='onchange')
    direct_journal_item_ids = fields.One2many('direct.journal.entry.items', 'move_id', readonly=True, states={'draft': [('readonly', False)]})
    direct_journal_type_inx = fields.Selection([('receipt','Receipt'),('payment','Payment'),('receipt_reverse','Receipt Reverse'),
                                                ('payment_reverse','Payment Reverse')], string="Direct Journal Type")

    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'direct_journal_item_ids.payment_amount',
        'direct_journal_item_ids.receipt_amount')
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for move in self:
            if move.direct_journal_entry_inx and move.state != 'posted':
                amount = 0
                if move.direct_journal_type_inx == 'receipt':
                    for item in move.direct_journal_item_ids:
                        amount += item.receipt_amount
                elif move.direct_journal_type_inx == 'payment':
                    for item in move.direct_journal_item_ids:
                        amount += item.payment_amount
                move.amount_total_signed = amount
        return res

    def _reverse_moves(self, default_values_list=None, cancel=False):
        res = super(AccountMove, self)._reverse_moves(default_values_list=default_values_list, cancel=cancel)
        if self.direct_journal_entry_inx and self.direct_journal_type_inx:
            if self.direct_journal_type_inx == 'receipt':
                res.direct_journal_type_inx = 'receipt_reverse'
            elif self.direct_journal_type_inx == 'payment':
                res.direct_journal_type_inx = 'payment_reverse'
            elif self.direct_journal_type_inx == 'payment_reverse':
                res.direct_journal_type_inx = 'payment'
            elif self.direct_journal_type_inx == 'receipt_reverse':
                res.direct_journal_type_inx = 'receipt'
            data = []
            for line in self.direct_journal_item_ids:
                data.append((0, 0, {
                    'name': line.name,
                    'account_id': line.account_id.id,
                    'partner_id': line.partner_id.id if line.partner_id else False,
                    'receipt_amount': line.payment_amount,
                    'payment_amount' : line.receipt_amount,
                    'move_id': self.id,
                }))
            res.write({
                'direct_journal_item_ids' : data,
            })
        return res

    @api.onchange('direct_journal_id_inx')
    def check_entry_accounts_inx(self):
        if self.direct_journal_id_inx:
            for line in self.direct_journal_item_ids:
                if line.account_id and line.account_id.id == self.direct_journal_id_inx.default_debit_account_id.id:
                    self.direct_journal_id_inx = False
                    return {
                        'warning': {'title': _('Invalid entry'),
                                    'message': _("You can't make transactions between same accounts."), },
                    }

    @api.model
    def create(self, vals):
        res =  super(AccountMove, self).create(vals)
        res.remove_zero_journals_inx()
        return res

    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        self.remove_zero_journals_inx()
        return res

    def remove_zero_journals_inx(self):
        for line in self.direct_journal_item_ids:
            if line.receipt_amount == 0 and line.payment_amount == 0:
                line.unlink()

    def action_post(self):
        if self.type == 'entry':
            if self.direct_journal_entry_inx:
                direct_journal_type = self.direct_journal_type_inx
                self.line_ids.unlink()
                for item in self.direct_journal_item_ids:
                    if direct_journal_type == 'receipt':
                        self.write({'line_ids': [(0, 0, {
                            'account_id': item.account_id.id,
                            'partner_id': item.partner_id.id if item.partner_id else False,
                            'name': item.name,
                            'credit': item.receipt_amount,
                            'debit': 0,
                            'move_id': self.id,
                        }), (0, 0, {
                            'account_id': self.direct_journal_id_inx.default_credit_account_id.id,
                            'partner_id': item.partner_id.id if item.partner_id else False,
                            'name': item.name,
                            'debit': item.receipt_amount,
                            'credit': 0,
                            'move_id': self.id,
                        })]})
                    elif direct_journal_type == 'payment':
                        self.write({'line_ids': [(0, 0, {
                            'account_id': item.account_id.id,
                            'partner_id': item.partner_id.id if item.partner_id else False,
                            'name': item.name,
                            'credit': 0,
                            'debit': item.payment_amount,
                            'move_id': self.id,
                        }), (0, 0, {
                            'account_id': self.direct_journal_id_inx.default_credit_account_id.id,
                            'partner_id': item.partner_id.id if item.partner_id else False,
                            'name': item.name,
                            'debit': 0,
                            'credit': item.payment_amount,
                            'move_id': self.id,
                        })]})

        return super(AccountMove, self).action_post()

class DirectJournalEntryItems(models.Model):
    _name = "direct.journal.entry.items"
    _description = "Items"

    name = fields.Char("Remarks")
    account_id = fields.Many2one('account.account', string='Account', required=True,
                                 index=True, ondelete="restrict", check_company=True,
                                 domain=[('deprecated', '=', False)])
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict')
    payment_amount = fields.Float(string='Payment')
    receipt_amount = fields.Float(string='Receipt')
    move_id = fields.Many2one('account.move')

    @api.onchange('account_id')
    def check_entry_accounts_inx(self):
        if self.account_id and self.move_id.direct_journal_id_inx and self.account_id.id == self.move_id.direct_journal_id_inx.default_debit_account_id.id:
            self.account_id = False
            return {
                'warning': {'title': _('Invalid entry'), 'message': _("You can't make transactions between same accounts."), },
            }