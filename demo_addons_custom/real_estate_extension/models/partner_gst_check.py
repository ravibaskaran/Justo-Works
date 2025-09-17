# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import ValidationError
import re


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res_partner = self.sudo()
        vat_domain = [('vat', '=', vals_list.get('vat'))]
        pan_domain = [('pan_number', '=', vals_list.get('pan_number'))]
        aadhar_domain = [('aadhar_number', '=', vals_list.get('aadhar_number'))]
        name_domain = [('name', '=', vals_list.get('name'))]
        partner_type = 'Partner'
        type_domain = False
        if vals_list.get('is_owner') if vals_list.get('is_owner') else self.is_owner:
            vals_list['developer_code'] = self.env['ir.sequence'].next_by_code(
                'developer.master.sequence')  # Dev Code generation
            type_domain = ('is_owner', '=', True)
            partner_type = 'Developer'
        elif vals_list.get('is_channel') if vals_list.get('is_channel') else self.is_channel:
            vals_list['channel_id'] = self.env['ir.sequence'].next_by_code(
                'channel.partner.sequence')  # CP Code generation
            type_domain = ('is_channel', '=', True)
            partner_type = 'Channel Partner'
        elif vals_list.get('is_channel_employee') if vals_list.get('is_channel_employee') else self.is_channel_employee:
            type_domain = ('is_channel_employee', '=', True)
            partner_type = 'Channel Partner Employee'
        elif vals_list.get('is_tenant') if vals_list.get('is_tenant') else self.is_tenant:
            vals_list['customer_code'] = self.env['ir.sequence'].next_by_code(
                'customer.master.sequence')  # Customer Code generation
            type_domain = ('is_tenant', '=', True)
            partner_type = 'Customer'
        elif vals_list.get('is_vendor') if vals_list.get('is_vendor') else self.is_vendor:
            type_domain = ('is_vendor', '=', True)
            partner_type = 'Vendor'
        if type_domain:
            vat_domain.append(type_domain)
            pan_domain.append(type_domain)
            aadhar_domain.append(type_domain)
            name_domain.append(type_domain)
        partner = self.env['res.partner'].sudo().search(vat_domain)
        if vals_list.get('vat') and partner:
            if res_partner.parent_id.vat != vals_list.get('vat'):
                raise ValidationError(_(partner_type + ' with GST Number already exists!'))
        if vals_list.get('pan_number') and res_partner.search(pan_domain):
            raise ValidationError(_(partner_type + ' with PAN Number already exists!'))
        if vals_list.get('aadhar_number') and res_partner.search(aadhar_domain):
            raise ValidationError(_(partner_type + ' with Aadhar Number already exists!'))
        if vals_list.get('name') and res_partner.search(name_domain) and not vals_list.get('is_referrer'):
            raise ValidationError(_(partner_type + ' with Name already exists!'))
        vat = self.vat or vals_list.get('vat')
        if not vat:
            return super(Partner, self).create(vals_list)
        if len(vat) != 15:
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN. GSTIN number must be 15 digits.
            # Please check.',}, }
            raise ValidationError(_("Invalid GSTIN. GSTIN number must be 15 digits. Please check."))
        if not (re.match("\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}", vat.upper())):
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN format.\r\n.GSTIN must be in the
            # format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either.',}, }
            raise ValidationError(
                _("Invalid GSTIN.\r\n.GSTIN must be in the format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either."))
        if not (Partner.check_gstin_chksum(vat)):
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN. Checksum validation failed. It
            # means one or more characters are probably wrong.',}, }
            raise ValidationError(
                _("Invalid GSTIN. Checksum validation failed. It means one or more characters are probably wrong."))
        return super(Partner, self).create(vals_list)

    #
    def write(self, vals_list):
        vat = vals_list.get('vat') if vals_list.get('vat') else self.vat
        if not vat:
            self.check_unique_partner_fields(vals_list)
            return super(Partner, self).write(vals_list)

        if len(vat) != 15:
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN. GSTIN number must be 15 digits.
            # Please check.',}, }
            raise ValidationError(_("Invalid GSTIN. GSTIN number must be 15 digits. Please check."))
        if not (re.match("\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d][Z]{1}[A-Z\d]{1}", vat.upper())):
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN format.\r\n.GSTIN must be in the
            # format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either.',}, }
            raise ValidationError(
                _("Invalid GSTIN.\r\n.GSTIN must be in the format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either."))
        if not (Partner.check_gstin_chksum(vat)):
            # return { 'warning': {'title': 'Warning', 'message': 'Invalid GSTIN. Checksum validation failed. It
            # means one or more characters are probably wrong.',}, }
            raise ValidationError(
                _("Invalid GSTIN. Checksum validation failed. It means one or more characters are probably wrong."))
        res = super(Partner, self).write(vals_list)
        self.check_unique_partner_fields(vals_list)
        return res

    def check_unique_partner_fields(self, vals_list):
        res_partner = self.sudo()
        vat_domain = [('vat', '=', vals_list.get('vat')), ('id', '!=', self._origin.id), ('commercial_partner_id', '!=', self.id)]
        pan_domain = [('pan_number', '=', vals_list.get('pan_number')), ('id', '!=', self._origin.id)]
        aadhar_domain = [('aadhar_number', '=', vals_list.get('aadhar_number')), ('id', '!=', self._origin.id)]
        name_domain = [('name', '=', vals_list.get('name')), ('id', '!=', self._origin.id)]
        partner_type = 'Partner'
        type_domain = False
        if vals_list.get('is_owner') if vals_list.get('is_owner') else self.is_owner:
            type_domain = ('is_owner', '=', True)
            partner_type = 'Developer'
        elif vals_list.get('is_channel') if vals_list.get('is_channel') else self.is_channel:
            type_domain = ('is_channel', '=', True)
            partner_type = 'Channel Partner'
        elif vals_list.get('is_channel_employee') if vals_list.get('is_channel_employee') else self.is_channel_employee:
            type_domain = ('is_channel_employee', '=', True)
            partner_type = 'Channel Partner Employee'
        elif vals_list.get('is_tenant') if vals_list.get('is_tenant') else self.is_tenant:
            type_domain = ('is_tenant', '=', True)
            partner_type = 'Customer'
        elif vals_list.get('is_vendor') if vals_list.get('is_vendor') else self.is_vendor:
            type_domain = ('is_vendor', '=', True)
            partner_type = 'Vendor'
        if type_domain:
            vat_domain.append(type_domain)
            pan_domain.append(type_domain)
            aadhar_domain.append(type_domain)
            name_domain.append(type_domain)
        partner = self.env['res.partner'].sudo().search(vat_domain)
        if vals_list.get('vat') and partner and res_partner:
            if res_partner.parent_id.vat != vals_list.get('vat'):
                raise ValidationError(_(partner_type + ' with GST Number already exists!'))
        if vals_list.get('pan_number') and res_partner.search(pan_domain):
            raise ValidationError(_(partner_type + ' with PAN Number already exists!'))
        if vals_list.get('aadhar_number') and res_partner.search(aadhar_domain):
            raise ValidationError(_(partner_type + ' with Aadhar Number already exists!'))
        if vals_list.get('name') and res_partner.search(name_domain) and not vals_list.get('is_referrer'):
            raise ValidationError(_(partner_type + ' with Name already exists!'))

    @staticmethod
    def check_gstin_chksum(gstin_num):
        gstin_num = gstin_num.upper()
        keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        values = range(36)
        hash = {k: v for k, v in zip(keys, values)}
        index = 0
        sum = 0
        while index < len(gstin_num) - 1:
            lettr = gstin_num[index]
            tmp = (hash[lettr]) * ((index % 2) + 1)  # Factor =1 fr index odd
            sum += tmp // 36 + tmp % 36
            index = index + 1
        Z = sum % 36
        Z = (36 - Z) % 36
        if ((hash[(gstin_num[-1:])]) == Z):
            return True
        return False

    @api.onchange('vat')
    def do_stuff(self):
        if self.vat:
            self.vat = self.vat.upper()
