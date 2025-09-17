# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class JupiterAccounts(http.Controller):

    @http.route('/check_booking_registration', auth='public')
    def check_booking_registration(self, **kw):
        if request.env.user.has_group('base.group_system'):
            data = ''
            booking = request.env['unit.reservation'].search([('state', 'in', ('draft', 'cancel', 'canceled', 'cancelled'))])
            for b in booking:
                reg = request.env['project.registration'].search([('flat_id', '=', b.building_unit.id), ('state', 'not in', ('draft', 'canceled'))])
                if reg:
                    data += reg.name + b.name + ','
            return data
        else:
            return 'failed'

    @http.route('/correct_employee_partner', auth='public')
    def correct_employee_partner(self, **kw):
        if request.env.user.has_group('base.group_system'):
            employees = request.env['hr.employee'].search([])
            for emp in employees:
                if not emp.partner_id:
                    partner = request.env['res.partner'].search([('name', '=', emp.name)], limit=1)
                    if partner:
                        emp.partner_id = partner.id
                        partner.is_employee = True
                    else:
                        partner = request.env['res.partner'].sudo().create({
                            'name': emp.name,
                            'company_id': request.env.company.id,
                        })
                        emp.partner_id = partner.id
                        partner.is_employee = True
                else:
                    emp.partner_id.is_employee = True
            return 'success'
        else:
            return 'failed'


    @http.route('/update_cp_accounts', auth='public')
    def update_cp_accounts(self, **kw):
        if request.env.user.has_group('base.group_system'):
            # devs = request.env['res.partner'].search([('is_owner', '=', True)])
            # for dev in devs:
            #     dev.

            # cp_cpe_vendors = request.env['res.partner'].search([]).filtered(lambda l: l.is_channel or l.is_channel_employee)
            # for partner in cp_cpe_vendors:
            #     # partner.property_account_receivable_id.user_type_id = 2
            #     # partner.property_account_payable_id = partner.property_account_receivable_id
            #     account = request.env['account.account'].search([('name', '=', partner.name)], limit=1)
            #     account.reconcile = True
            #     account.user_type_id = 2
            #     prop = request.env['ir.property'].search(
            #         [('name', '=', 'property_account_payable_id'), ('fields_id', '=', 3600),
            #          ('res_id', '=', 'res.partner,' + str(partner.id))])
            #     if prop:
            #         prop.value_reference = 'account.account,' + str(account.id)
            #     else:
            #         request.env['ir.property'].create({
            #             'name': 'property_account_payable_id',
            #             'fields_id': 3600,
            #             'res_id': 'res.partner,' + str(partner.id),
            #             'value_reference': 'account.account,' + str(account.id)
            #         })
            #     # partner.property_account_receivable_id = 7
            #     prop = request.env['ir.property'].search(
            #         [('name', '=', 'property_account_receivable_id'), ('fields_id', '=', 3601),
            #          ('res_id', '=', 'res.partner,' + str(partner.id))])
            #     if prop:
            #         prop.value_reference = 'account.account,' + str(7)
            employee = request.env['res.partner'].search([('is_employee', '=', True)])
            for emp in employee:
                account = request.env['account.account'].search([('name', '=', emp.name)], limit=1)
                if not account:
                    ir_config = request.env['ir.config_parameter'].sudo()
                    account_obj = request.env['account.account']
                    sequence_obj = request.env['ir.sequence']
                    account_type_obj = request.env['account.account.type']
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
                    account = account_obj.create({
                        'code': code,
                        'name': emp.name,
                        'user_type_id': user_type_id.id,
                        'company_id': request.env.company.id,
                        'reconcile': True,
                        'partner_account_inx': True
                    })
                account.reconcile = True
                account.user_type_id = 2
                prop = request.env['ir.property'].search(
                    [('name', '=', 'property_account_payable_id'), ('fields_id', '=', 3600),
                     ('res_id', '=', 'res.partner,' + str(emp.id))])
                if prop:
                    prop.value_reference = 'account.account,' + str(account.id)
                else:
                    request.env['ir.property'].create({
                        'name': 'property_account_payable_id',
                        'fields_id': 3600,
                        'res_id': 'res.partner,' + str(emp.id),
                        'value_reference': 'account.account,' + str(account.id)
                    })
                # partner.property_account_receivable_id = 7
                prop = request.env['ir.property'].search(
                    [('name', '=', 'property_account_receivable_id'), ('fields_id', '=', 3601),
                     ('res_id', '=', 'res.partner,' + str(emp.id))])
                if prop:
                    prop.value_reference = 'account.account,' + str(7)
            return 'Success'
        else:
            return 'Access Denied'

    @http.route('/update_invoice_accounts', auth='public')
    def update_invoice_accounts(self, **kw):
        if request.env.user.has_group('base.group_system'):
            lines = request.env['account.move.line'].search([('account_id', 'in', (26, 7))])
            for line in lines:
                partner = line.move_id.partner_id
                if partner.is_owner:
                    # line.account_id = line.move_id.partner_id.property_account_receivable_id.id
                    request.env.cr.execute("update account_move_line set account_id = %s where id = %s" % (str(line.move_id.partner_id.property_account_receivable_id.id), str(line.id)))
                elif partner.is_vendor or partner.is_channel or partner.is_channel_employee or partner.is_employee:
                    # line.account_id = line.move_id.partner_id.property_account_payable_id.id
                    request.env.cr.execute("update account_move_line set account_id = %s where id = %s" % (
                    str(line.move_id.partner_id.property_account_payable_id.id), str(line.id)))
            return 'Success'
        else:
            return 'Access Denied'

    @http.route('/correct_invoice_project_id', auth='public')
    def correct_invoice_project_id(self, **kw):
        if request.env.user.has_group('base.group_system'):
            bookings = request.env['unit.reservation'].search([])
            for booking in bookings:
                booking.spot_booking_invoice_id.project_id = booking.building.id
                booking.cp_brokerage_invoice_id.project_id = booking.building.id
            registrations = request.env['project.registration'].search([])
            for registration in registrations:
                registration.developer_invoice_id.project_id = registration.project_id.id
                for invoice in registration.employee_invoice_ids:
                    invoice.project_id = registration.project_id.id
            return 'Success'
        else:
            return 'Access Denied'

    @http.route('/update_partner_accounts', auth='public')
    def update_partner_accounts(self, **kw):
        if request.env.user.has_group('base.group_system'):
            partners = request.env['res.partner'].search([])
            for partner in partners:
                if partner.is_vendor or partner.is_owner or partner.is_channel or partner.is_channel_employee:
                    if not partner.company_id:
                        request.env.cr.execute('update res_partner set company_id=' + str(request.env.company.id) + ' where id=' + str(partner.id))
                        # partner.company_id = request.env.company.id
                    ir_config = request.env['ir.config_parameter'].sudo()
                    account_obj = request.env['account.account']
                    sequence_obj = request.env['ir.sequence']
                    account_type_obj = request.env['account.account.type']
                    if ir_config.get_param('partner_account_creation.create_payable_account') and partner.is_vendor:
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
                        property_account_payable_id = account_obj.create({
                            'code': code,
                            'name': partner.name,
                            'user_type_id': user_type_id.id,
                            'company_id': request.env.company.id,
                            'reconcile': True,
                            'partner_account_inx': True
                        }).id
                        prop = request.env['ir.property'].search([('name', '=', 'property_account_payable_id'), ('fields_id', '=', 3600), ('res_id', '=', 'res.partner,' + str(partner.id))])
                        if prop:
                            prop.value_reference = 'account.account,' + str(property_account_payable_id)
                        else:
                            request.env['ir.property'].create({
                                'name': 'property_account_payable_id',
                                'fields_id': 3600,
                                'res_id': 'res.partner,' + str(partner.id),
                                'value_reference': 'account.account,' + str(property_account_payable_id)
                            })

                        # request.env.cr.execute('update res_partner set property_account_payable_id=' + str(property_account_payable_id) + ' where id = ' + str(partner.id))
                    elif ir_config.get_param('partner_account_creation.create_receivable_account') and (
                            partner.is_owner or partner.is_channel or partner.is_channel_employee):
                        user_type_id = account_type_obj.search([('type', '=', 'receivable')], limit=1)
                        code = False
                        try:
                            if user_type_id.prefix:
                                prefix = user_type_id.prefix + '-'
                                code = prefix + f'{user_type_id.next_number:05d}'
                        except:
                            pass
                        if not code:
                            code = sequence_obj.next_by_code('partner.account.receivable.seq')
                        property_account_receivable_id = account_obj.create({
                            'code': code,
                            'name': partner.name,
                            'user_type_id': user_type_id.id,
                            'company_id': request.env.company.id,
                            'reconcile': True,
                            'partner_account_inx': True
                        }).id
                        prop = request.env['ir.property'].search(
                            [('name', '=', 'property_account_receivable_id'), ('fields_id', '=', 3601),
                             ('res_id', '=', 'res.partner,' + str(partner.id))])
                        if prop:
                            prop.value_reference = 'account.account,' + str(property_account_receivable_id)
                        else:
                            request.env['ir.property'].create({
                                'name': 'property_account_receivable_id',
                                'fields_id': 3601,
                                'res_id': 'res.partner,' + str(partner.id),
                                'value_reference': 'account.account,' + str(property_account_receivable_id)
                            })
                        # request.env.cr.execute('update res_partner set property_account_receivable_id=' + str(
                        #     property_account_receivable_id) + ' where id = ' + str(partner.id))
            return 'SUCCESS'
        return "Access Denied"

    @http.route('/update_head_type_prefix', auth='public')
    def update_head_type_prefix(self, **kw):
        if request.env.user.has_group('base.group_system'):
            acc_types = request.env['account.account.type'].search([])
            for acc_type in acc_types:
                if not acc_type.prefix:
                    if acc_type.name == 'Non-current Assets':
                        acc_type.prefix = 'NCA'
                        continue
                    if acc_type.name == 'Non-current Liabilities':
                        acc_type.prefix = 'NCL'
                        continue
                    acc_type.prefix = acc_type.name[:3].upper()
            return 'SUCCESS'
        return "Access Denied"

    @http.route('/update_booking_registration_invoice_type', auth='public')
    def update_booking_registration_invoice_type(self, **kw):
        if request.env.user.has_group('base.group_system'):
            bookings = request.env['unit.reservation'].search([])
            for booking in bookings:
                for inv in booking.spot_booking_invoice_id:
                    inv.project_invoice_type = 'spot_booking'
                for inv in booking.cp_brokerage_invoice_id:
                    inv.project_invoice_type = 'cp_brokerage'
            registrations = request.env['project.registration'].search([])
            for reg in registrations:
                for inv in reg.employee_invoice_ids:
                    inv.project_invoice_type = 'employee_invoice'
                for inv in reg.developer_invoice_id:
                    inv.project_invoice_type = 'developer_invoice'
            return 'SUCCESS'
        return "Access Denied"
