from odoo import models, fields, api
import datetime


class OpeningUpdater(models.TransientModel):
    _name = 'opening.updater'

    amount = fields.Float()
    account_id = fields.Many2one('account.account')
    type = fields.Selection([('debit', 'Debit'), ('credit', 'Credit')])

    def update_opening(self):
        today = datetime.date.today()
        if today.month >= 4:
            financial_year_start = datetime.date(today.year, 4, 1)
        else:
            financial_year_start = datetime.date(today.year - 1, 4, 1)
        opening_lines = self.env['multiple.account.opening.line'].search(
            [('account_id', '=', self.account_id.id), ('multiple_id.state', '=', 'posted'), ('multiple_id.date', '=', financial_year_start)])
        partner = self.env['res.partner'].search([('property_account_payable_id', '=', self.account_id.id)])
        if partner and not partner.is_vendor:
            partner = False
        if not partner:
            partner = self.env['res.partner'].search([('property_account_receivable_id', '=', self.account_id.id)])
            if partner and not (partner.is_owner or partner.is_channel or partner.is_channel_employee):
                partner = False
        partner.opening_balance = self.amount
        partner.opening_type = self.type
        self.account_id.opening_balance = self.amount
        self.account_id.opening_type = self.type
        if opening_lines:
            for line in opening_lines:
                if line.multiple_id.state == 'posted':
                    line.multiple_id.set_to_draft_opening()
                line.debit = 0
                line.credit = 0
                if self.amount > 0:
                    if self.type == 'debit':
                        line.debit = self.amount
                        self.amount = 0
                    else:
                        line.credit = self.amount
                        self.amount = 0
            for opening in opening_lines.mapped('multiple_id'):
                opening.validate_opening()
        else:
            opening = self.env['multiple.account.opening'].search([('state', '=', 'posted'), ('date', '=', financial_year_start)], limit=1)
            opening_ids = [(0, 0, {
                    'account_id': self.account_id.id,
                    'debit': self.amount if self.type == 'debit' else 0,
                    'credit': self.amount if self.type == 'credit' else 0
                })]
            if opening:
                opening.set_to_draft_opening()
                opening.opening_ids = opening_ids
            else:
                date_range = self.env['ir.sequence.date_range'].search([('date_from', '=', financial_year_start)], limit=1)
                opening = self.env['multiple.account.opening'].sudo().create({
                    'name': str(financial_year_start.year)[-2:] + '-' + str(financial_year_start.year + 1)[-2:],
                    'date': financial_year_start,
                    'financial_range': date_range.id,
                    'account_opening_move_id': self.env.company.account_opening_move_id.id,
                    'opening_ids': opening_ids
                })
            opening.validate_opening()
