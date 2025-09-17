# -*- coding: utf-8 -*-
import re
from datetime import datetime
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


def is_valid_date_format(date_string):
    formats_to_check = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
    for date_format in formats_to_check:
        try:
            datetime.strptime(date_string, date_format)
            return datetime.strptime(date_string, date_format).strftime('%Y-%m-%d')
        except ValueError:
            pass
    return False


class RealEstateExtension(http.Controller):

    def add_api_log(self, record, code, response, api_type, status, name, direction, args):
        try:
            request.env['api.log'].sudo().create({
                'record': str(record),
                'code': code,
                'response': response,
                'date': datetime.now(),
                'type': api_type,
                'status': status,
                'name': name,
                'direction': direction,
                'args': str(args)
            })
        except Exception as e:
            _logger.warning(str(e))

    # Api for sending employee_details
    # create api key with scope employee_out
    # 71119f18dd995f6746e4e8d97f3b304e7c525c9e
    @http.route(['/employee/get_details'], type='json', auth='public', methods=['POST'])
    def employee_get_details(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='employee_details', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'employee_details',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'employee_details',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            employees = request.env['hr.employee'].sudo().search([])
            final_data = []
            for employee_id in employees:
                final_data.append({
                    "name": employee_id.name,
                    "employee_id": employee_id.id,
                    "pan": employee_id.pan_number or '',
                    "work_mobile": employee_id.mobile_phone or '',
                    "work_phone": employee_id.work_phone or '',
                    "date_of_birth": employee_id.birthday.strftime('%d/%m/%Y') if employee_id.birthday else '',
                    "gender": 1 if employee_id.gender == 'male' else 2 if employee_id.gender == 'female' else 1 if employee_id.gender == 'other' else 1,
                    "city": employee_id.city or "",
                    "location": employee_id.location or "",
                    "email": employee_id.private_email or "",
                    "corporate_email": employee_id.corporate_email or "",
                    "personal_mobile": employee_id.mobile or "",
                    "active_status": True if employee_id.active_status else False,
                    "relieving_date": employee_id.departure_date.strftime('%d/%m/%Y') if employee_id.departure_date else "",
                    "role": employee_id.role or ''
                })
            response = {
                'data': final_data,
                'status': 'Success',
                'code': 200
            }
            self.add_api_log('', 200, str(response), 'employee_details', 'success', '', 'in',
                             kwargs)
            return response

    # Api for creating booking
    # create api key with scope booking
    # 71119f18dd995f6746e4e8d97f3b304e7c525c9e
    @http.route(['/project/flat_booking_create'], type='json', auth='public', methods=['POST'])
    def flat_booking_create(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='booking', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'booking',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'booking',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            vals_list = kwargs.get('record')
            if not vals_list.get('project'):
                self.add_api_log('', 201, str('project is required!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'project is required!',
                    'status': 'Failed',
                    'code': 201
                }
            if not vals_list.get('flat'):
                self.add_api_log('', 201, str('flat is required!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'flat is required!',
                    'status': 'Failed',
                    'code': 201
                }
            if not vals_list.get('customer'):
                self.add_api_log('', 201, str('customer is required!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'customer is required!',
                    'status': 'Failed',
                    'code': 201
                }
            project = request.env['building'].sudo().search([('code', '=', vals_list.get('project'))], limit=1)
            if not project:
                self.add_api_log('', 201, str('project not found!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'project not found!',
                    'status': 'Failed',
                    'code': 201
                }
            flat = request.env['product.template'].sudo().search([('name', '=', vals_list.get('flat')), ('is_property', '=', True), ('building_id', '=', project.id)], limit=1)
            if not flat:
                self.add_api_log('', 201, str('flat not found!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'flat not found!',
                    'status': 'Failed',
                    'code': 201
                }
            if flat.state != 'free':  # todo:add condition for checking if flat have booking in draft state
                self.add_api_log('', 201, str('flat is not in available state!'), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'flat is not in available state!',
                    'status': 'Failed',
                    'code': 201
                }

            customer_id = False
            if vals_list.get('customer'):
                customer = request.env['res.partner'].sudo().search([('jv_cid', '=', vals_list.get('customer')), ('is_tenant','=',True)], limit=1)
                if not customer:
                    self.add_api_log('', 201, str('customer not found!'), 'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': 'customer not found!',
                        'status': 'Failed',
                        'code': 201
                    }
                customer_id = customer.id
            if vals_list.get('date'):
                booking_date = is_valid_date_format(vals_list.get('date'))
                if not booking_date:
                    self.add_api_log('', 201,
                                     str('Invalid input for Date (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': 'Invalid input for Date'
                                '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                        'status': 'Failed',
                        'code': 201
                    }
                date = datetime.strptime(booking_date, '%Y-%m-%d')
                now = datetime.now().time()
                booking_date = datetime.combine(date, now)
            else:
                booking_date = datetime.now()
            cp_employee_id = False
            cp_id = False
            sub_source_id = False
            referred_person_id = False
            referral_partner_name = False  # Initialize the name field
            referral_partner_mobile = False  # Initialize the phone field
            referral_partner_email = False  # Initialize the email field
            if vals_list.get('source_of_booking'):
                source = vals_list.get('source_of_booking')
                # 1) Extract the field (mobile side might call it cp_lead_type)
                source_booking_type = vals_list.get('cp_lead_type') or ''

                if source not in ('cp', 'direct', 'referral_partner'):
                    self.add_api_log('', 201,
                                     str('source_of_booking allowed inputs: cp, direct, referral_partner'),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': 'source_of_booking allowed inputs: "cp", "direct", "referral_partner"',
                        'status': 'Failed',
                        'code': 201
                    }
                # Extract the referral partner details if the source is referral_partner (referred_person, referred_no, referred_email)
                if source == 'referral_partner':
                    referral_partner_name = vals_list.get('referred_person')
                    referral_partner_mobile = vals_list.get('referred_no')
                    referral_partner_email = vals_list.get('referred_email')

                if source == 'cp':
                    if source_booking_type not in ('tele_call', 'walk_in'):
                        self.add_api_log('', 201,
                                         f'Invalid source_of_booking_type: {source_booking_type}',
                                         'booking', 'failed', '', 'in', kwargs)


                    if vals_list.get('cp_main'):
                        cp_main = request.env['res.partner'].sudo().search(
                            [('jv_cp_id', '=', vals_list.get('cp_main')), ('is_channel', '=', True)], limit=1)
                        if not cp_main:
                            self.add_api_log('', 201, str('cp not found!'), 'booking',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'cp not found!',
                                'status': 'Failed',
                                'code': 201
                            }
                        cp_id = cp_main.id
                    else:
                        self.add_api_log('', 201,
                                         str('cp is required since source_of_booking is cp'),
                                         'booking',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'cp is required since source_of_booking is cp',
                            'status': 'Failed',
                            'code': 201
                        }
                    if vals_list.get('cp_employee'):
                        cp_employee = request.env['res.partner'].sudo().search(
                            [('jv_cpe_id', '=', vals_list.get('cp_employee')), ('is_channel_employee', '=', True)], limit=1)
                        # if not cp_employee:
                        #     self.add_api_log('', 201, str('cp_employee not found!'), 'booking',
                        #                      'failed', '', 'in', kwargs)
                        #     return {
                        #         'data': 'cp_employee not found!',
                        #         'status': 'Failed',
                        #         'code': 201
                        #     }
                        if cp_employee:
                            cp_employee_id = cp_employee.id
                    # else:
                    #     self.add_api_log('', 201,
                    #                      str('cp_employee is required since source_of_booking is cp'),
                    #                      'booking',
                    #                      'failed', '', 'in', kwargs)
                    #     return {
                    #         'data': 'cp_employee is required since source_of_booking is cp',
                    #         'status': 'Failed',
                    #         'code': 201
                    #     }
                elif source == 'direct':
                    if vals_list.get('sub_source'):
                        sub_source = request.env['booking.direct.type'].sudo().search([('name', '=', vals_list.get('sub_source'))], limit=1)
                        if sub_source:
                            sub_source_id = sub_source.id
                            if vals_list.get('referred_no'):
                                referred_no = vals_list.get('referred_no')
                                if referred_no and not re.match(r'^\d{10}$', referred_no):
                                    self.add_api_log('', 201,
                                                     str('referred_no must be of 10 digits'),
                                                     'booking',
                                                     'failed', '', 'in', kwargs)
                                    return {
                                        'data': 'referred_no must be of 10 digits',
                                        'status': 'Failed',
                                        'code': 201
                                    }
                            # take referred_person only if sub_source given
                            if vals_list.get('referred_person') and vals_list.get('referred_no'):
                                referred_person = request.env['res.partner'].sudo().search([('name', '=', vals_list.get('referred_person')), ('mobile', '=', vals_list.get('referred_no')), ('is_referrer', '=', True)], limit=1)
                                if not referred_person:
                                    referred_person = request.env['res.partner'].sudo().create({
                                        'name': vals_list.get('referred_person'),
                                        'is_referrer': True,
                                        'country_id': request.env.user.company_id.country_id.id,
                                        'state_id': request.env.user.company_id.state_id.id,
                                        'customer_rank': 0,
                                        'supplier_rank': 0,
                                        'mobile': vals_list.get('referred_no')
                                    })
                                referred_person_id = referred_person.id
            else:
                self.add_api_log('', 201,
                                 str('source_of_booking is required'),
                                 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': 'source_of_booking is required',
                    'status': 'Failed',
                    'code': 201
                }
            prev_booking = request.env['unit.reservation'].sudo().search(
                [('building_unit', '=', flat.id), ('state', '=', 'draft')],
                order='date desc', limit=1)
            if prev_booking:
                booking_draft_checking_hours = request.env['ir.config_parameter'].sudo().get_param(
                    'itsys_real_estate.booking_draft_checking_hours')
                if booking_draft_checking_hours:
                    booking_draft_checking_hours = int(booking_draft_checking_hours)
                    difference = booking_date - prev_booking.date
                    hours_difference = difference.total_seconds() / 3600
                    if booking_draft_checking_hours > hours_difference:
                        msg = f'The flat has already been selected for another draft booking within {booking_draft_checking_hours} hours of the booking date.'
                        self.add_api_log('', 201,
                                         str(msg),
                                         'booking',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': msg,
                            'status': 'Failed',
                            'code': 201
                        }
            advance_amount = 0
            if vals_list.get('advance_amount'):
                try:
                    advance_amount = float(vals_list.get('advance_amount'))
                except:
                    msg = f'advance_amount is not valid.'
                    self.add_api_log('', 201,
                                     str(msg),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': msg,
                        'status': 'Failed',
                        'code': 201
                    }
            closing_manager_id = False
            closing_tl_id = False
            sourcing_manager_id = False
            sourcing_tl_id = False
            if vals_list.get('closed_by'):
                closed_by = False
                try:
                    closed_by = int(vals_list.get('closed_by'))
                except:
                    pass
                if not closed_by:
                    msg = f'closing manager or closing tl not found.'
                    self.add_api_log('', 201,
                                     str(msg),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': msg,
                        'status': 'Failed',
                        'code': 201
                    }
                closed_by = request.env['hr.employee'].sudo().search([('id', '=', closed_by), ('role', 'in', ('closing_manager', 'closing_tl'))], limit=1)
                if not closed_by:
                    msg = f'closing manager or closing tl not found.'
                    self.add_api_log('', 201,
                                     str(msg),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': msg,
                        'status': 'Failed',
                        'code': 201
                    }
                else:
                    if closed_by.id in project.closing_manager_ids.ids:
                        closing_manager_id = closed_by.id
                    elif closed_by.id in project.closing_tl_ids.ids:
                        closing_tl_id = closed_by.id
                    else:
                        msg = f'closing manager or closing tl not found in project.'
                        self.add_api_log('', 201,
                                         str(msg),
                                         'booking',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': msg,
                            'status': 'Failed',
                            'code': 201
                        }
            if vals_list.get('sourced_by'):
                sourced_by = False
                try:
                    sourced_by = int(vals_list.get('sourced_by'))
                except:
                    pass
                if not sourced_by:
                    msg = f'sourcing manager or sourcing tl not found.'
                    self.add_api_log('', 201,
                                     str(msg),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': msg,
                        'status': 'Failed',
                        'code': 201
                    }
                sourced_by = request.env['hr.employee'].sudo().search([('id', '=', sourced_by), ('role', 'in', ('sourcing_manager', 'sourcing_tl'))], limit=1)
                if not sourced_by:
                    msg = f'sourcing manager or sourcing tl not found.'
                    self.add_api_log('', 201,
                                     str(msg),
                                     'booking',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': msg,
                        'status': 'Failed',
                        'code': 201
                    }
                else:
                    if sourced_by.id in project.sourcing_manager_ids.ids:
                        sourcing_manager_id = sourced_by.id
                    elif sourced_by.id in project.sourcing_tl_ids.ids:
                        sourcing_tl_id = sourced_by.id
                    else:
                        msg = f'sourcing manager or sourcing tl not found in project.'
                        self.add_api_log('', 201,
                                         str(msg),
                                         'booking',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': msg,
                            'status': 'Failed',
                            'code': 201
                        }

            try:
                booking = request.env['unit.reservation'].sudo().create({
                    'building': project.id,
                    'building_unit': flat.id,
                    'partner_id': customer_id,
                    'rera_no': project.license_code,
                    'developer_id': project.partner_id.id,
                    'cp_employee_id': cp_employee_id,
                    # 'cp_id': cp_id,
                    'date': booking_date,
                    'source_of_booking': source,
                    'source_of_booking_type': source_booking_type,  # <= here
                    'direct_type_id': sub_source_id,
                    'referred_person': referred_person_id,
                    'advance_amount': advance_amount,
                    'closing_manager_id': closing_manager_id,
                    'closing_tl_id': closing_tl_id,
                    'sourcing_manager_id': sourcing_manager_id,
                    'sourcing_tl_id': sourcing_tl_id,
                    'referral_partner_name': referral_partner_name,  # Pass the referral partner name
                    'referral_partner_mobile': referral_partner_mobile,  # Pass the referral partner phone
                    'referral_partner_email': referral_partner_email,  # Pass the referral partner email
                })
                booking.onchange_flat()
                booking.onchange_sq_ft_rate()
                booking.onchange_flat_cost_real()
                booking.fill_applicant_address()
                booking.fill_co_applicant_address()
                booking.cp_id = cp_id
                # booking.onchange_cp_employee()
                booking.compute_agreement_value()
                booking.fill_developer_commission_percentage()
                booking.fill_cp_brokerage()
                booking.onchange_project()
                # booking.onchange_flat_cost_fill_advance_amount()

            except Exception as e:
                self.add_api_log('', 201, str(e), 'booking',
                                 'failed', '', 'in', kwargs)
                return {
                    'data': e,
                    'status': 'Failed',
                    'code': 201
                }
            try:
                booking.jv_id = vals_list.get('jv_id') or ''
            except:
                pass
            success_response = {
                'data': {
                    'booking_no': booking.name,
                },
                'status': 'Success',
                'code': 200
            }
            self.add_api_log(booking.id, 200, str(success_response), 'booking', 'success', booking.name, 'in', kwargs)
            return success_response

    # Api for creating cp employee and returning customer code
    # create api key with scope cp_emp
    @http.route(['/project/cp_employee_create'], type='json', auth='public', methods=['POST'])
    def cp_employee_create(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='cp_emp', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'cp_emp',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'cp_emp',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            vals_list = kwargs.get('record')
            cp_returns = []
            for vals in vals_list:
                if vals:
                    # if vals.get('name'):
                    # country_id = request.env['res.country'].search([('code', '=', vals.get('country_code'))])
                    # if vals.get('country_code') and country_id:
                    #     state_id = request.env['res.country.state'].search(
                    #         [('code', '=', vals.get('state_code')), ('country_id', '=', country_id.id)])
                    #     if vals.get('state_code') and state_id:
                    gender = vals.get('gender')
                    if gender:
                        if gender.upper() == 'M':
                            gender = 'male'
                        elif gender.upper() == 'F':
                            gender = 'female'
                        elif gender.upper() == 'O':
                            gender = 'other'
                        else:
                            self.add_api_log('', 201, str('Invalid input for gender'), 'cp_emp',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'Invalid input for gender '
                                        '(Valid inputs: F or f for Female, M or m for Male, O or o for Other)',
                                'status': 'Failed',
                                'code': 201
                            }
                    dob = vals.get('date_of_birth')
                    if dob:
                        dob = is_valid_date_format(dob)
                        if not dob:
                            self.add_api_log('', 201, str('Invalid input for Date of Birth (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'), 'cp_emp',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'Invalid input for Date of Birth'
                                        '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                                'status': 'Failed',
                                'code': 201
                            }
                    else:
                        dob = False
                    cp_parent = False
                    if vals.get('cp_id'):
                        cp_parent_id = request.env['res.partner'].sudo().search([('jv_cp_id', '=', vals.get('cp_id')), ('is_channel', '=', True)], limit=1)
                        if cp_parent_id:
                            cp_parent = cp_parent_id
                        else:
                            self.add_api_log('', 201, str('Channel Partner with the provided id is not found!'+ vals.get('cp_id')), 'cp_emp',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'Channel Partner with the provided id is not found!'+ vals.get('cp_id'),
                                'status': 'Failed',
                                'code': 201
                            }
                    try:
                        if vals.get('cp_employee_id'):
                            cp = request.env['res.partner'].sudo().search([('jv_cpe_id', '=', vals.get('cp_employee_id')), ('is_channel_employee', '=', True)], limit=1)
                            if cp:
                                cp.write({
                                    'name': vals.get('name') if vals.get('name') else cp.name,
                                    'street': vals.get('street') if vals.get('street') else cp.street,
                                    'street2': vals.get('street2') if vals.get('street2') else cp.street2,
                                    'city': vals.get('city') if vals.get('city') else cp.city,
                                    # 'state_id': state_id.id if state_id else cp.state_id,
                                    # 'country_id': country_id.id if country_id else cp.country_id,
                                    'zip': vals.get('zip') if vals.get('zip') else cp.zip,
                                    'vat': vals.get('gstin') if vals.get('gstin') else cp.vat,
                                    'pan_number': vals.get('pan') if vals.get('pan') else cp.pan_number,
                                    'aadhar_number': vals.get('aadhar') if vals.get('aadhar') else cp.aadhar_number,
                                    'function': vals.get('occupation') if vals.get('occupation') else cp.function,
                                    'phone': vals.get('phone') if vals.get('phone') else cp.phone,
                                    'mobile': vals.get('mobile') if vals.get('mobile') else cp.mobile,
                                    'email': vals.get('email') if vals.get('email') else cp.email,
                                    'website': vals.get('website') if vals.get('website') else cp.website,
                                    'bank_name': vals.get('bank') if vals.get('bank') else cp.bank_name,
                                    'ifsc_code': vals.get('ifsc') if vals.get('ifsc') else cp.ifsc_code,
                                    'account_number': vals.get('account_number') if vals.get('account_number') else cp.account_number,
                                    'gender': gender if gender else cp.gender,
                                    'dob': dob if dob else cp.dob,
                                    'parent_id': cp_parent.id if cp_parent else cp.parent_id.id,
                                    'parent_channel_id': cp_parent.channel_id if cp_parent else cp.parent_id.channel_id
                                })
                                cp_returns.append(cp)
                            else:
                                if not vals.get('name'):
                                    self.add_api_log('', 201, str('Name not provided'), 'cp_emp',
                                                     'failed', '', 'in', kwargs)
                                    return {
                                        'data': 'Name not provided',
                                        'status': 'Failed',
                                        'code': 201
                                    }
                                cp = request.env['res.partner'].sudo().create({
                                    'is_channel_employee': True,
                                    'company_id': request.env.user.company_id.id,
                                    'name': vals.get('name'),
                                    # 'cp_employee_id': vals.get('cp_employee_id'),
                                    'street': vals.get('street'),
                                    'street2': vals.get('street2'),
                                    'city': vals.get('city'),
                                    'state_id': request.env.company.state_id.id,
                                    'country_id': request.env.company.country_id.id,
                                    'zip': vals.get('zip'),
                                    'vat': vals.get('gstin'),
                                    'pan_number': vals.get('pan'),
                                    'aadhar_number': vals.get('aadhar'),
                                    'function': vals.get('occupation'),
                                    'phone': vals.get('phone'),
                                    'mobile': vals.get('mobile'),
                                    'email': vals.get('email'),
                                    'website': vals.get('website'),
                                    'bank_name': vals.get('bank'),
                                    'ifsc_code': vals.get('ifsc'),
                                    'account_number': vals.get('account_number'),
                                    'gender': gender,
                                    'dob': dob,
                                    'parent_id': cp_parent.id if cp_parent else None,
                                    'parent_channel_id': cp_parent.channel_id,
                                    'jv_cpe_id': vals.get('cp_employee_id')
                                })
                                cp_returns.append(cp)
                        else:
                            self.add_api_log('', 201, str('cp_employee_id is required'), 'cp_emp',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'cp_employee_id is required!',
                                'status': 'Failed',
                                'code': 201
                            }
                    except Exception as e:
                        self.add_api_log('', 201, str(e), 'cp_emp',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': e,
                            'status': 'Failed',
                            'code': 201
                        }
            if cp_returns:
                success_response = {
                    'data': {
                        'cp_employee_id': ', '.join([str(i.jv_cpe_id) for i in cp_returns]),
                    },
                    'status': 'Success',
                    'code': 200
                }
                self.add_api_log(str(', '.join([str(i.id) for i in cp_returns])), 200,
                                 str(success_response), 'cp_emp',
                                 'success', ', '.join([str(i.name) for i in cp_returns]), 'in', kwargs)
                return success_response
                    #     else:
                    #         self.add_api_log('', 201, str('State Code not provided or Invalid State Code'), 'cp_emp',
                    #                          'failed', '', 'in', kwargs)
                    #         return {
                    #             'data': 'State Code not provided or Invalid State Code',
                    #             'status': 'Failed',
                    #             'code': 201
                    #         }
                    # else:
                    #     self.add_api_log('', 201, str('Country Code not provided or Invalid Country Code'), 'cp_emp',
                    #                      'failed', '', 'in', kwargs)
                    #     return {
                    #         'data': 'Country Code not provided or Invalid Country Code',
                    #         'status': 'Failed',
                    #         'code': 201
                    #     }
                # else:
                #     return {
                #         'data': 'Name not provided',
                #         'status': 'Failed',
                #         'code': 201
                #     }
            else:
                self.add_api_log('', 201, str(failed_response), 'cp_emp',
                                 'failed', '', 'in', kwargs)
                return failed_response

    # Api for creating customer and returning customer code
    # create api key with scope customer
    @http.route(['/project/customer_master_create'], type='json', auth='public', methods=['POST'])
    def customer_master_create(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='customer', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'customer',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'customer',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            vals = kwargs.get('record')
            if vals:
                # if vals.get('name'):
                # country_id = request.env['res.country'].search([('code', '=', vals.get('country_code'))])
                # if vals.get('country_code') and country_id:
                #     state_id = request.env['res.country.state'].search(
                #         [('code', '=', vals.get('state_code')), ('country_id', '=', country_id.id)])
                #     if vals.get('state_code') and state_id:
                gender = vals.get('gender')
                if gender:
                    if gender.upper() == 'M':
                        gender = 'male'
                    elif gender.upper() == 'F':
                        gender = 'female'
                    elif gender.upper() == 'O':
                        gender = 'other'
                    else:
                        self.add_api_log('', 201, str('Invalid input for gender'), 'customer',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for gender '
                                    '(Valid inputs: F or f for Female, M or m for Male, O or o for Other)',
                            'status': 'Failed',
                            'code': 201
                        }
                dob = vals.get('date_of_birth')
                if dob:
                    dob = is_valid_date_format(dob)
                    if not dob:
                        self.add_api_log('', 201, str('Invalid input for Date of Birth (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'), 'customer',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for Date of Birth'
                                    '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                            'status': 'Failed',
                            'code': 201
                        }
                else:
                    dob = False
                credit_days = vals.get('credit_days')
                if credit_days:
                    try:
                        credit_days = int(credit_days)
                    except:
                        self.add_api_log('', 201, str('Invalid input for credit_days'), 'customer',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for credit_days',
                            'status': 'Failed',
                            'code': 201
                        }
                income = vals.get('income')
                if income:
                    try:
                        income = float(income)
                    except:
                        self.add_api_log('', 201, str('Invalid input for income'), 'customer',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for income',
                            'status': 'Failed',
                            'code': 201
                        }
                try:
                    if vals.get('customer_id'):
                        cp = request.env['res.partner'].sudo().search([('jv_cid', '=', vals.get('customer_id'))], limit=1)

                        if cp:
                            cp.write({
                                'name': vals.get('name') if vals.get('name') else cp.name,
                                'street': vals.get('street') if vals.get('street') else cp.street,
                                'street2': vals.get('street2') if vals.get('street2') else cp.street2,
                                'city': vals.get('city') if vals.get('city') else cp.city,
                                # 'state_id': state_id.id if state_id else cp.state_id,
                                # 'country_id': country_id.id if country_id else cp.country_id,
                                'zip': vals.get('zip') if vals.get('zip') else cp.zip,
                                'vat': vals.get('gstin') if vals.get('gstin') else cp.vat,
                                'pan_number': vals.get('pan') if vals.get('pan') else cp.pan_number,
                                'aadhar_number': vals.get('aadhar') if vals.get('aadhar') else cp.aadhar_number,
                                'function': vals.get('occupation') if vals.get('occupation') else cp.function,
                                'phone': vals.get('phone') if vals.get('phone') else cp.phone,
                                'mobile': vals.get('mobile') if vals.get('mobile') else cp.mobile,
                                'email': vals.get('email') if vals.get('email') else cp.email,
                                'website': vals.get('website') if vals.get('website') else cp.website,
                                'bank_name': vals.get('bank') if vals.get('bank') else cp.bank_name,
                                'ifsc_code': vals.get('ifsc') if vals.get('ifsc') else cp.ifsc_code,
                                'account_number': vals.get('account_number') if vals.get('account_number') else cp.account_number,
                                'gender': gender if gender else cp.gender,
                                'dob': dob if dob else cp.dob,
                                'credit_days': credit_days if credit_days else cp.credit_days,
                                'income': income if income else cp.income,
                            })

                        else:
                            if not vals.get('name'):
                                self.add_api_log('', 201, str('Name not provided'), 'customer', 'failed', '', 'in', kwargs)
                                return {
                                    'data': 'Name not provided',
                                    'status': 'Failed',
                                    'code': 201
                                }
                            state_id = request.env.company.state_id
                            country_id = request.env.company.country_id
                            cp = request.env['res.partner'].sudo().create({
                                'is_tenant': True,
                                'customer_rank': 1,
                                'company_id': request.env.user.company_id.id,
                                'name': vals.get('name'),
                                'street': vals.get('street'),
                                'street2': vals.get('street2'),
                                'city': vals.get('city'),
                                'state_id': state_id.id,
                                'country_id': country_id.id,
                                'zip': vals.get('zip'),
                                'vat': vals.get('gstin'),
                                'pan_number': vals.get('pan'),
                                'aadhar_number': vals.get('aadhar'),
                                'function': vals.get('occupation'),
                                'phone': vals.get('phone'),
                                'mobile': vals.get('mobile'),
                                'email': vals.get('email'),
                                'website': vals.get('website'),
                                'bank_name': vals.get('bank'),
                                'ifsc_code': vals.get('ifsc'),
                                'account_number': vals.get('account_number'),
                                'gender': gender,
                                'dob': dob,
                                'credit_days': credit_days,
                                'income': income,
                                'jv_cid': vals.get('customer_id')
                            })
                        success_response = {
                            'data': {
                                'customer_id': cp.jv_cid,
                            },
                            'status': 'Success',
                            'code': 200
                        }
                        self.add_api_log(cp.id, 200, str(success_response), 'customer', 'success', cp.name, 'in', kwargs)
                    else:
                        self.add_api_log('', 201, str('customer_id is required!'), 'customer',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'customer_id is required!',
                            'status': 'Failed',
                            'code': 201
                        }
                except Exception as e:
                    self.add_api_log('', 201, str(e), 'customer', 'failed', '', 'in', kwargs)
                    return {
                        'data': e,
                        'status': 'Failed',
                        'code': 201
                    }
                return success_response
                    # else:
                    #     return {
                    #         'data': 'State Code not provided or Invalid State Code',
                    #         'status': 'Failed',
                    #         'code': 201
                    #     }
                # else:
                #     return {
                #         'data': 'Country Code not provided or Invalid Country Code',
                #         'status': 'Failed',
                #         'code': 201
                #     }
                # else:
                #     return {
                #         'data': 'Name not provided',
                #         'status': 'Failed',
                #         'code': 201
                #     }
            else:
                self.add_api_log('', 201, str(failed_response), 'customer', 'failed', '', 'in', kwargs)
                return failed_response

    # Api for creating employee and returning employee code
    # create api key with scope emp
    @http.route(['/employee/fetch_employee_code123'], type='json', auth='public', methods=['POST'])
    def fetch_employee_details(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='emp', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201, str(failed_response), 'employee',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201, str(failed_response), 'employee',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            vals = kwargs.get('record')
            if vals:
                # if vals.get('name'):
                gender = vals.get('gender')
                if gender:
                    if gender.upper() == 'M':
                        gender = 'male'
                    elif gender.upper() == 'F':
                        gender = 'female'
                    elif gender.upper() == 'O':
                        gender = 'other'
                    else:
                        self.add_api_log('', 201, str('Invalid input for gender'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for gender '
                                    '(Valid inputs: F or f for Female, M or m for Male, O or o for Other)',
                            'status': 'Failed',
                            'code': 201
                        }
                department = vals.get('department')
                department_id = False
                if department:
                    department_id = request.env['hr.department'].sudo().search([('name', '=', department)],
                                                                               limit=1)
                    if not department_id:
                        department_id = request.env['hr.department'].sudo().create({
                            'name': department
                        })
                manager_id = False
                manager = vals.get('manager')
                if manager:
                    manager_id = request.env['hr.employee'].sudo().search([('barcode', '=', manager)], limit=1)
                    # if not manager_id:
                    #     return {
                    #         'data': 'Manager does not exists !',
                    #         'status': 'Failed',
                    #         'code': 201
                    #     }
                marital_status = vals.get('marital_status')
                if marital_status:
                    if marital_status not in ('single', 'married', 'cohabitant', 'widower', 'divorced'):
                        self.add_api_log('', 201, str('Invalid input for marital status'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for marital status '
                                    '(Valid inputs: single, married, cohabitant, widower, divorced)',
                            'status': 'Failed',
                            'code': 201
                        }
                active_status = vals.get('active_status')
                if active_status:
                    if active_status.upper() == 'T':
                        active_status = True
                    elif active_status.upper() == 'F':
                        active_status = False
                    else:
                        self.add_api_log('', 201, str('Invalid input for Active Status'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for Active Status'
                                    '(Valid inputs: T or t for True, F or f for False)',
                            'status': 'Failed',
                            'code': 201
                        }
                dob = vals.get('date_of_birth')
                if dob:
                    dob = is_valid_date_format(dob)
                    if not dob:
                        self.add_api_log('', 201, str('Invalid input for Date of Birth (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for Date of Birth'
                                    '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                            'status': 'Failed',
                            'code': 201
                        }
                else:
                    dob = False
                joining_date = vals.get('joining_date')
                if joining_date:
                    joining_date = is_valid_date_format(joining_date)
                    if not joining_date:
                        self.add_api_log('', 201, str('Invalid input for Joining Date (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for Joining Date'
                                    '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                            'status': 'Failed',
                            'code': 201
                        }
                else:
                    joining_date = False
                relieving_date = vals.get('relieving_date')
                if relieving_date:
                    relieving_date = is_valid_date_format(relieving_date)
                    if not relieving_date:
                        self.add_api_log('', 201, str('Invalid input for Relieving Date (Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'Invalid input for Relieving Date'
                                    '(Valid input formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)',
                            'status': 'Failed',
                            'code': 201
                        }
                else:
                    relieving_date = False
                try:
                    # if vals.get('corporate_email'):
                    #     employee_id = request.env['hr.employee'].sudo().search([('corporate_email', '=', vals.get('corporate_email'))], limit=1)
                    # else:
                    #     return {
                    #         'data': "The corporate_email is required",
                    #         'status': 'Failed',
                    #         'code': 201
                    #     }
                    if vals.get('employee_id'):
                        employee_id = request.env['hr.employee'].sudo().search([('barcode', '=', vals.get('employee_id'))], limit=1)
                        # if request.env['hr.employee'].sudo().search([('barcode', '=', vals.get('employee_id')), ('id', '!=', employee_id.id)]):
                            # return {
                            #     'data': "The Employee ID must be unique, this one is already assigned to another employee.",
                            #     'status': 'Failed',
                            #     'code': 201
                            # }
                    else:
                        self.add_api_log('', 201, str('Employee ID is required.'), 'employee',
                                         'failed', '', 'in', kwargs)
                        return{
                            'data': "Employee ID is required.",
                            'status': 'Failed',
                            'code': 201
                        }
                    if employee_id:
                        employee_id.write({
                            'name': vals.get('name') if vals.get('name') else employee_id.name,
                            'pan_number': vals.get('pan') if vals.get('pan') else employee_id.pan_number,
                            'job_title': vals.get('job_position') if vals.get(
                                'job_position') else employee_id.job_title,
                            'mobile_phone': vals.get('work_mobile') if vals.get(
                                'work_mobile') else employee_id.mobile_phone,
                            'work_phone': vals.get('work_phone') if vals.get(
                                'work_phone') else employee_id.work_phone,
                            'birthday': dob if dob else employee_id.birthday,
                            'department_id': department_id.id if department_id else employee_id.department_id.id,
                            'parent_id': manager_id.id if manager_id else employee_id.parent_id.id,
                            'gender': gender if gender else employee_id.gender,
                            'joining_date': joining_date if joining_date else employee_id.joining_date,
                            'departure_date': relieving_date if relieving_date else employee_id.departure_date,
                            'city': vals.get('city') if vals.get('city') else employee_id.city,
                            'zip': vals.get('zip') if vals.get('zip') else employee_id.zip,
                            'private_email': vals.get('email') if vals.get(
                                'email') else employee_id.private_email,
                            'corporate_email': vals.get('corporate_email') if vals.get(
                                'corporate_email') else employee_id.corporate_email,
                            'work_email': vals.get('corporate_email') if vals.get(
                                'corporate_email') else employee_id.work_email,
                            'mobile': vals.get('personal_mobile') if vals.get(
                                'personal_mobile') else employee_id.mobile,
                            'marital': marital_status if marital_status else employee_id.marital,
                            'emergency_contact': vals.get('emergency_contact_number') if vals.get(
                                'emergency_contact_number') else employee_id.emergency_contact,
                            'active_status': active_status if active_status else employee_id.active_status,
                            'ctc': vals.get('ctc') if vals.get('ctc') else employee_id.ctc,
                            'location': vals.get('location') if vals.get('location') else employee_id.location,
                            'barcode': vals.get('employee_id') if vals.get('employee_id') else employee_id.barcode,
                        })
                    else:
                        if not vals.get('name'):
                            self.add_api_log('', 201, str('Name not provided'), 'employee',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'Name not provided',
                                'status': 'Failed',
                                'code': 201
                            }
                        # if not vals.get('corporate_email'):
                        #     return {
                        #         'data': "The corporate_email is required",
                        #         'status': 'Failed',
                        #         'code': 201
                        #     }
                        if vals.get('email'):
                            private_email_emp = request.env['hr.employee'].sudo().search(
                                [('private_email', '=', vals.get('email'))], limit=1)
                            if private_email_emp:
                                self.add_api_log('', 201, str('Employee with Email already exists'), 'employee',
                                                 'failed', '', 'in', kwargs)
                                return {
                                    'data': 'Employee with Email already exists !',
                                    'status': 'Failed',
                                    'code': 201
                                }
                        employee_id = request.env['hr.employee'].sudo().create({
                            'employee_type': 'employee',
                            'name': vals.get('name'),
                            'state_id': request.env.company.state_id.id,
                            'country_id': request.env.company.country_id.id,
                            'pan_number': vals.get('pan'),
                            'job_title': vals.get('job_position'),
                            'mobile_phone': vals.get('work_mobile'),
                            'work_phone': vals.get('work_phone'),
                            'birthday': dob,
                            'department_id': department_id.id if department_id else False,
                            'parent_id': manager_id.id if manager_id else False,
                            'gender': gender,
                            'joining_date': joining_date,
                            'departure_date': relieving_date,
                            'city': vals.get('city'),
                            'zip': vals.get('zip'),
                            'private_email': vals.get('email'),
                            'corporate_email': vals.get('corporate_email'),
                            'work_email': vals.get('corporate_email'),
                            'mobile': vals.get('personal_mobile'),
                            'marital': marital_status,
                            'emergency_contact': vals.get('emergency_contact_number'),
                            'active_status': active_status,
                            'ctc': vals.get('ctc'),
                            'location': vals.get('location'),
                            'barcode': vals.get('employee_id'),
                        })
                    success_response = {
                        'status': 'Success',
                        'code': 200
                    }
                    self.add_api_log(employee_id.id, 200, str(success_response), 'employee',
                                     'success', str(employee_id.name), 'in', kwargs)
                except Exception as e:
                    if 'hr_employee_unique_name_per_employee' in str(e):
                        e = 'Employee with name already exists !'
                    if 'unique_corporate_email_per_employee' in str(e):
                        e = 'Employee with Corporate Email already exists !'
                    self.add_api_log('', 201, str(e), 'employee',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': e,
                        'status': 'Failed',
                        'code': 201
                    }
                # out_api = request.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_employee_out_api')
                # if out_api:
                #     # commented fields - because not in mobile app
                #     params = {
                #         "name": employee_id.name,
                #         "employee_id": employee_id.barcode,
                #         "pan": employee_id.pan_number or "",
                #         # "job_position": employee_id.job_title or "",
                #         "work_mobile": employee_id.mobile_phone or "",
                #         "work_phone": employee_id.work_phone or "",
                #         "date_of_birth": employee_id.birthday.strftime('%d/%m/%Y') if employee_id.birthday else "",
                #         # "department": employee_id.department_id.name or "",
                #         # "manager": employee_id.parent_id.barcode or "",
                #         "gender": 1 if employee_id.gender == 'male' else 2 if employee_id.gender == 'female' else 1 if employee_id.gender == 'other' else 1,
                #         # "joining_date": employee_id.joining_date.strftime('%d/%m/%Y') if employee_id.joining_date else "",
                #         "city": employee_id.city or "",
                #         "location": employee_id.location or "",
                #         # "zip": employee_id.zip or "",
                #         "email": employee_id.private_email or "",
                #         "corporate_email": employee_id.corporate_email or "",
                #         "personal_mobile": employee_id.mobile or "",
                #         # "marital_status": employee_id.marital or "",
                #         # "emergency_contact_number": employee_id.emergency_contact or "",
                #         "active_status": True if employee_id.active_status else False,
                #         # "relieving_date": employee_id.departure_date.strftime('%d/%m/%Y') if employee_id.departure_date else "",
                #         # "ctc": employee_id.ctc,
                #     }
                #     url = request.env['ir.config_parameter'].sudo().get_param('real_estate_extension.employee_api_url')
                #     username = request.env['ir.config_parameter'].sudo().get_param(
                #         'real_estate_extension.employee_api_username')
                #     password = request.env['ir.config_parameter'].sudo().get_param('real_estate_extension.employee_api_key')
                #
                #     data = {
                #         'params': {
                #             'login': username,
                #             'password': password,
                #             'record': params
                #         }
                #     }
                #     code = ''
                #     try:
                #         headers = {"Content-Type": "application/json; charset=utf-8"}
                #         response = requests.post(url, headers=headers, json=data)
                #         if response.ok:
                #             res = json.loads(response.text)
                #             if res.get('status') == 201:
                #                 code = res.get('status')
                #                 response = response.content
                #                 status = 'success'
                #                 pass
                #             else:
                #                 raise ValidationError(str(res))
                #         else:
                #             raise ValidationError(str(response.text))
                #     except Exception as e:
                #         response = e
                #         status = 'failed'
                #         pass
                #     request.env['api.log'].sudo().create({
                #         'record': str(employee_id.id),
                #         'code': code,
                #         'response': response,
                #         'date': datetime.now(),
                #         'type': 'employee',
                #         'status': status,
                #         'name': employee_id.barcode
                #     })

                return success_response
            else:
                self.add_api_log('', 201, str(failed_response), 'employee',
                                 'failed', '', 'in', kwargs)
                return failed_response

    # Api for creating channel partner and returning cp_id
    # create api key with scope cp
    @http.route(['/cp/fetch_channel_partner_id'], type='json', auth='public', methods=['POST'])
    def fetch_channel_partner_details(self, **kwargs):
        failed_response = {
            'data': 'Access Denied',
            'status': 'Failed',
            'code': 201
        }
        user_id = request.env["res.users.apikeys"]._check_credentials(scope='cp', key=kwargs.get('password'))
        if not user_id:
            self.add_api_log('', 201,
                             str(failed_response), 'cp',
                             'failed', '', 'in', kwargs)
            return failed_response
        if request.env['res.users'].sudo().browse(user_id).login != kwargs.get('login'):
            self.add_api_log('', 201,
                             str(failed_response), 'cp',
                             'failed', '', 'in', kwargs)
            return failed_response
        else:
            vals = kwargs.get('record')
            if vals:
                # if vals.get('name'):
                # country_id = request.env['res.country'].search([('code', '=', vals.get('country_code'))])
                # country_id = request.env.user.company_id.country_id
                # if country_id:
                #     state_id = request.env['res.country.state'].search([('code', '=', vals.get('state_code')), ('country_id', '=', country_id.id)])
                #     if state_id:
                # if vals.get('mobile'):
                try:
                    if not vals.get('cp_id') or (vals.get('cp_id') and vals['cp_id'] == ''):
                        self.add_api_log('', 201,
                                         str('cp_id is required!'), 'cp',
                                         'failed', '', 'in', kwargs)
                        return {
                            'data': 'cp_id is required!',
                            'status': 'Failed',
                            'code': 201
                        }
                    cp = request.env['res.partner'].sudo().search(
                        [('jv_cp_id', '=', vals.get('cp_id')),
                         ('is_channel', '=', True)], limit=1)
                    if cp:
                        # cp = request.env['res.partner'].sudo().search(
                        #     [('channel_id', '=', vals.get('cp_id')),
                        #      ('is_channel', '=', True)])
                        # if not cp:
                        #     self.add_api_log('', 201,
                        #                      str('Channel Partner with the provided id is not found!'), 'cp',
                        #                      'failed', '', 'in', kwargs)
                        #     return {
                        #         'data': 'Channel Partner with the provided id is not found!',
                        #         'status': 'Failed',
                        #         'code': 201
                        #     }
                        cp.write({
                            'name': vals.get('name') if vals.get('name') else cp.name,
                            'owner_name': vals.get('owner_name') if vals.get('owner_name') else cp.owner_name,
                            'street': vals.get('street') if vals.get('street') else cp.street,
                            'street2': vals.get('street2') if vals.get('street2') else cp.street2,
                            'city': vals.get('city') if vals.get('city') else cp.city,
                            # 'state_id': state_id.id if state_id else cp.state_id,
                            # 'country_id': country_id.id if country_id else cp.country_id,
                            'zip': vals.get('zip') if vals.get('zip') else cp.zip,
                            'vat': vals.get('gstin') if vals.get('gstin') else cp.vat,
                            'rera_number': vals.get('rera_number') if vals.get('rera_number') else cp.rera_number,
                            'pan_number': vals.get('pan') if vals.get('pan') else cp.pan_number,
                            'aadhar_number': vals.get('aadhar') if vals.get(
                                'aadhar') else cp.aadhar_number,
                            'phone': vals.get('phone') if vals.get('phone') else cp.phone,
                            'mobile': vals.get('mobile') if vals.get('mobile') else cp.mobile,
                            'email': vals.get('email') if vals.get('email') else cp.email,
                            'website': vals.get('website') if vals.get('website') else cp.website,
                            'bank_name': vals.get('bank') if vals.get('bank') else cp.bank_name,
                            'ifsc_code': vals.get('ifsc') if vals.get('ifsc') else cp.ifsc_code,
                            'account_number': vals.get('account_number') if vals.get(
                                'account_number') else cp.account_number,
                        })

                    else:
                        if not vals.get('name'):
                            self.add_api_log('', 201,
                                             str('Name not provided'), 'cp',
                                             'failed', '', 'in', kwargs)
                            return {
                                'data': 'Name not provided',
                                'status': 'Failed',
                                'code': 201
                            }
                        cp = request.env['res.partner'].sudo().create({
                            'is_channel': True,
                            'is_company': True,
                            'company_id': request.env.user.company_id.id,
                            'name': vals.get('name'),
                            'owner_name': vals.get('owner_name'),
                            'street': vals.get('street'),
                            'street2': vals.get('street2'),
                            'city': vals.get('city'),
                            'state_id': request.env.company.state_id.id,
                            'country_id': request.env.company.country_id.id,
                            'zip': vals.get('zip'),
                            'vat': vals.get('gstin'),
                            'rera_number': vals.get('rera_number'),
                            'pan_number': vals.get('pan'),
                            'aadhar_number': vals.get('aadhar'),
                            'phone': vals.get('phone'),
                            'mobile': vals.get('mobile'),
                            'email': vals.get('email'),
                            'website': vals.get('website'),
                            'bank_name': vals.get('bank'),
                            'ifsc_code': vals.get('ifsc'),
                            'account_number': vals.get('account_number'),
                            'jv_cp_id': vals.get('cp_id')
                        })
                    success_response = {
                        'data': {
                            'cp_id': cp.jv_cp_id,
                        },
                        'status': 'Success',
                        'code': 200
                    }
                    self.add_api_log(cp.id, 201,
                                     str(success_response), 'cp',
                                     'success', str(cp.name), 'in', kwargs)
                except Exception as e:
                    self.add_api_log('', 201,
                                     str(e), 'cp',
                                     'failed', '', 'in', kwargs)
                    return {
                        'data': e,
                        'status': 'Failed',
                        'code': 201
                    }
                return success_response
                # else:
                #     self.add_api_log('', 201,
                #                      str('Mobile not provided'), 'cp',
                #                      'failed', '', 'in', kwargs)
                #     return {
                #         'data': 'Mobile not provided',
                #         'status': 'Failed',
                #         'code': 201
                #     }
                #     else:
                #         self.add_api_log('', 201,
                #                          str('State Code not provided or Invalid State Code'), 'cp',
                #                          'failed', '', 'in', kwargs)
                #         return {
                #             'data': 'State Code not provided or Invalid State Code',
                #             'status': 'Failed',
                #             'code': 201
                #         }
                # else:
                #     self.add_api_log('', 201,
                #                      str('Country Code not provided or Invalid Country Code'), 'cp',
                #                      'failed', '', 'in', kwargs)
                #     return {
                #         'data': 'Country Code not provided or Invalid Country Code',
                #         'status': 'Failed',
                #         'code': 201
                #     }
                # else:
                #     return {
                #         'data': 'Name not provided',
                #         'status': 'Failed',
                #         'code': 201
                #     }
            else:
                self.add_api_log('', 201,
                                 str(failed_response), 'cp',
                                 'failed', '', 'in', kwargs)
                return failed_response

    @http.route('/correct_booking_employee_fields', auth='public')
    def correct_booking_employee_fields(self, **kw):
        if request.env.user.has_group('base.group_system'):
            employees = request.env['hr.employee'].search([])
            data = {}
            for employee in employees:
                if employee.name in data:
                    data[employee.name].append(employee.id)
                else:
                    data[employee.name] = [employee.id]
            for line in data:
                if len(data[line]) > 1:
                    booking_obj = request.env['unit.reservation']
                    for emp in data[line]:
                        closing_booking = booking_obj.search([('closing_manager_id', '=', emp)])
                        sourcing_booking = booking_obj.search([('sourcing_manager_id', '=', emp)])
                        closing_tl_booking = booking_obj.search([('closing_tl_id', '=', emp)])
                        sourcing_tl_booking = booking_obj.search([('sourcing_tl_id', '=', emp)])
                        crm_booking = booking_obj.search([('crm_id', '=', emp)])
                        marketing_booking = booking_obj.search([('marketing_id', '=', emp)])
                        for closing in closing_booking:
                            closing.closing_manager_id = data[line][0]
                        for sourcing in sourcing_booking:
                            sourcing.sourcing_manager_id = data[line][0]
                        for closing_tl in closing_tl_booking:
                            closing_tl.closing_tl_id = data[line][0]
                        for sourcing_tl in sourcing_tl_booking:
                            sourcing_tl.sourcing_tl_id = data[line][0]
                        for crm in crm_booking:
                            crm.crm_id = data[line][0]
                        for marketing in marketing_booking:
                            marketing.marketing_id = data[line][0]
                    request.env['hr.employee'].search([('id', 'in', data[line]), ('id', '!=', data[line][0])]).unlink()
            messages = request.env['mail.message'].search([('model', '=', 'hr.employee')])
            messages.filtered(lambda l: "May I recommend you to setup an" in l.body).unlink()
            return 'Success'
        return "You have no access to this url"
