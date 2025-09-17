# -*- coding: utf-8 -*-
from odoo.tools.misc import formatLang
from odoo import models, fields, api
import json

class AccountMove(models.Model):
    _inherit = "account.move"

    freight_charge_ids = fields.One2many('account.freight.charges', 'move_id', readonly=True,
                                              states={'draft': [('readonly', False)]})
    other_charge_total = fields.Monetary(string='Additional Charges', store=True, readonly=True, compute='_compute_amount')

    @api.model
    def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
        res = super(AccountMove, self)._get_tax_totals(partner, tax_lines_data, amount_total, amount_untaxed, currency)
        res['other_charge_total'] = self.other_charge_total
        res['formatted_other_charge_total'] = formatLang(self.env, self.other_charge_total, currency_obj=currency)
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        res = super(AccountMove, self).copy(default=default)
        print(res,"resssssssssssssssssssssssss")
        remove_freight = []
        copy_freight = []
        if self.freight_charge_ids:
            freight_credit = 0
            freight_debit = 0
            account_id = self.partner_id.property_account_payable_id.id
            account_line_id = False
            for freight in self.freight_charge_ids:
                copy_freight.append((0, 0, {'name' :freight.name, 'account_id': freight.account_id.id, 'amount' : freight.amount}))
            for line in res.line_ids:
                if line.is_freight:
                    remove_freight.append((2, line.id))
                    freight_credit += line.credit
                    freight_debit += line.debit
                if line.account_id.id == account_id:
                    account_line_id = line
            remove_freight.append((1, account_line_id.id, {
                'credit': account_line_id.credit - freight_debit,
                'debit': account_line_id.debit - freight_credit,
            }))
            res.write({'line_ids':remove_freight,'freight_charge_ids':copy_freight})
        return res

    def _reverse_move_vals(self, default_values, cancel=True):
        move_vals = super(AccountMove, self)._reverse_move_vals(default_values, cancel=cancel)
        if self.freight_charge_ids:
            new_line_ids = []
            freight_credit = 0
            freight_debit = 0
            account_id = self.partner_id.property_account_payable_id.id
            for item in move_vals['line_ids']:
                if not item[2].get('is_freight'):
                    new_line_ids.append(item)
                else:
                    freight_credit += item[2].get('credit')
                    freight_debit += item[2].get('debit')
            for item in move_vals['line_ids']:
                if item[2].get('account_id') == account_id:
                    item[2]['credit'] = item[2]['credit'] - freight_debit
                    item[2]['debit'] = item[2]['debit'] - freight_credit
            move_vals['line_ids'] = new_line_ids
        return move_vals

    def _reverse_moves(self, default_values_list=None, cancel=False):
        res = super(AccountMove, self)._reverse_moves(default_values_list=default_values_list, cancel=cancel)
        data = []
        for freight in self.freight_charge_ids:
            data.append((0,0,
                         {
                             'name' : freight.name,
                             'account_id' : freight.account_id.id,
                             'amount' : freight.amount,
                         }))
        res.write({
            'freight_charge_ids' : data,
        })
        return res

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'freight_charge_ids.amount')
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for move in self:
            total = 0
            for freight in move.freight_charge_ids:
                total += freight.amount
            move.other_charge_total = total
            move.amount_total += total

    def action_post(self):
        if self.move_type in ['in_invoice', 'in_refund']:
            data = []
            credit_reduce = 0
            debit_reduce = 0
            move_line_obj = self.env["account.move.line"]
            account_id = self.partner_id.property_account_payable_id.id
            move_line_id = self.env["account.move.line"].search([('move_id','=',self.id),('account_id','=', account_id), ('exclude_from_invoice_tab','=',True),('is_freight', '=', False)],limit=1)
            freight_ids = move_line_obj.search([('move_id', '=', self.id), ('is_freight', '=', True), ('exclude_from_invoice_tab', '=', True)])
            if freight_ids:
                for item in freight_ids:
                    data.append((2, item.id))
                credit_reduce = sum(freight_ids.mapped('debit'))
                debit_reduce = sum(freight_ids.mapped('credit'))
            line_credit = move_line_id.credit
            line_debit = move_line_id.debit
            line_credit -= credit_reduce
            line_debit -= debit_reduce
            for item in self.freight_charge_ids:
                if item.account_id and item.amount != 0:
                    credit = debit = 0
                    if self.move_type == 'in_invoice':
                        if item.amount > 0:
                            debit = item.amount
                            line_credit += item.amount
                        else:
                            credit = abs(item.amount)
                            line_debit += abs(item.amount)
                    elif self.move_type == 'in_refund':
                        if item.amount > 0:
                            credit = item.amount
                            line_debit += item.amount
                        else:
                            debit = abs(item.amount)
                            line_credit += abs(item.amount)
                    data.append((0,0,{
                            'account_id': item.account_id.id,
                            'debit': debit,
                            'credit': credit,
                            'is_freight': True,
                            'exclude_from_invoice_tab': True
                        }))
            if self.move_type == 'in_invoice':
                if line_debit != 0:
                    line_credit -= line_debit
                    line_debit = 0
            elif self.move_type == 'in_refund':
                if line_credit != 0:
                    line_debit -= line_credit
                    line_credit = 0
            data.append((1,move_line_id.id,{
                'credit': line_credit,
                'debit': line_debit,
            }))
            if data:
                self.write({
                    'line_ids': data,
                })

        return super(AccountMove, self).action_post()


    def _compute_tax_totals_json(self):
        super(AccountMove, self)._compute_tax_totals_json()
        for rec in self:
            try:
                tax_totals_json_dict = json.loads(rec.tax_totals_json)
                tax_totals_json_dict.update(
                    {'other_charge_total': rec.other_charge_total})
                rec.tax_totals_json = json.dumps(tax_totals_json_dict)
            except:
                pass

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_freight = fields.Boolean()

class FreightCharges(models.Model):
    _name = 'account.freight.charges'

    name = fields.Char("Remarks")
    account_id = fields.Many2one('account.account', string='Account', required=True,
                                 index=True, ondelete="restrict", check_company=True,
                                 domain=[('deprecated', '=', False)])
    amount = fields.Float(string='Amount')
    move_id = fields.Many2one('account.move')
