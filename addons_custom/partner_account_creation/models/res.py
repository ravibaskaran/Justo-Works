# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        if self.env['ir.config_parameter'].sudo().get_param('partner_account_creation.create_partner_account'):
            res['company_id'] = self.env.company.id
        return res

    @api.model
    def create(self, vals):
        ir_config = self.env['ir.config_parameter'].sudo()
        create_account = ir_config.get_param('partner_account_creation.create_partner_account')
        if create_account and not vals.get('company_id') and (
                vals.get('customer_rank') > 0 or vals.get('supplier_rank') > 0):
            raise UserError('Please select a company!')
        res = super(ResPartner, self).create(vals)
        if create_account:
            res.create_partner_accounts_inx()
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if vals.get('name'):
            if self.property_account_payable_id.partner_account_inx:
                self.property_account_payable_id.name = self.name
            if self.property_account_receivable_id.partner_account_inx:
                self.property_account_receivable_id.name = self.name
        return res

    def create_partner_accounts_inx(self):  # modified for justo
        ir_config = self.env['ir.config_parameter'].sudo()
        account_obj = self.env['account.account']
        sequence_obj = self.env['ir.sequence']
        account_type_obj = self.env['account.account.type']
        if ir_config.get_param('partner_account_creation.create_payable_account') and (self.is_vendor or self.is_channel or self.is_channel_employee or self.is_employee):
            user_type_id = account_type_obj.search([('type', '=', 'payable')], limit=1)
            code = False
            try:
                if user_type_id.prefix:
                    prefix = user_type_id.prefix + '-'
                    code = prefix + f'{user_type_id.next_number:05d}'
            except:
                pass
            if not code:
                code = sequence_obj.next_by_code('partner.account.payable.seq')
            self.property_account_payable_id = account_obj.create({
                'code': code,
                'name': self.name,
                'user_type_id': user_type_id.id,
                'company_id': self.company_id.id,
                'reconcile': True,
                'partner_account_inx': True
            }).id
        elif ir_config.get_param('partner_account_creation.create_receivable_account') and self.is_owner:
            user_type_id =account_type_obj.search([('type', '=', 'receivable')], limit=1)
            code = False
            try:
                if user_type_id.prefix:
                    prefix = user_type_id.prefix + '-'
                    code = prefix + f'{user_type_id.next_number:05d}'
            except:
                pass
            if not code:
                code = sequence_obj.next_by_code('partner.account.receivable.seq')
            self.property_account_receivable_id = account_obj.create({
                'code': code,
                'name': self.name,
                'user_type_id': user_type_id.id,
                'company_id': self.company_id.id,
                'reconcile': True,
                'partner_account_inx': True
            }).id
        return True
