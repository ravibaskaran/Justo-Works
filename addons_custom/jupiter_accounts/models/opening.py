from odoo import models, api
from odoo.exceptions import UserError


class MultipleAccountOpening(models.Model):
    _inherit = 'multiple.account.opening'

    def validate_opening(self):
        if self.env['multiple.account.opening'].search([('state', '=', 'posted'), ('date', '=', self.date)]):
            raise UserError('Only one opening allowed per financial year!')
        res = super(MultipleAccountOpening, self).validate_opening()
        account_list = []
        for line in self.opening_ids:
            if line.account_id.id in account_list:
                raise UserError('%s exists in multiple lines!' % line.account_id.name)
            account_list.append(line.account_id.id)
            partner = self.env['res.partner'].search([('property_account_payable_id', '=', line.account_id.id)])
            if partner and not partner.is_vendor:
                partner = False
            if not partner:
                partner = self.env['res.partner'].search([('property_account_receivable_id', '=', line.account_id.id)])
                if partner and not (partner.is_owner or partner.is_channel or partner.is_channel_employee):
                    partner = False
            line.account_id.opening_balance = 0
            partner.opening_balance = 0
            if line.debit > 0:
                line.account_id.opening_balance += line.debit
                line.account_id.opening_type = 'debit'
                partner.opening_balance += line.debit
                partner.opening_type = 'debit'
            else:
                line.account_id.opening_balance += line.credit
                line.account_id.opening_type = 'credit'
                partner.opening_balance += line.credit
                partner.opening_type = 'credit'
        return res

    def set_to_draft_opening(self):
        res = super(MultipleAccountOpening, self).set_to_draft_opening()
        for line in self.opening_ids:
            partner = self.env['res.partner'].search([('property_account_payable_id', '=', line.account_id.id)])
            if partner and not partner.is_vendor:
                partner = False
            if not partner:
                partner = self.env['res.partner'].search([('property_account_receivable_id', '=', line.account_id.id)])
                if partner and not (partner.is_owner or partner.is_channel or partner.is_channel_employee):
                    partner = False
            if line.debit > 0:
                line.account_id.opening_balance -= line.debit
                line.account_id.opening_type = 'debit'
                partner.opening_balance -= line.debit
                partner.opening_type = 'debit'
            else:
                line.account_id.opening_balance -= line.credit
                line.account_id.opening_type = 'credit'
                partner.opening_balance -= line.credit
                partner.opening_type = 'credit'
        return res
