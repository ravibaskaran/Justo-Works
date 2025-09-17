# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from pytz import timezone
from odoo.exceptions import Warning


class BetaProductLedger(models.TransientModel):  # change this
    _name = 'beta.payroll.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Payroll Report')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    product_ids = fields.Many2many('product.product', string='Products', domain=[('sale_ok', '=', True), ('type', '=', 'product')])
    horizontal_view = fields.Boolean()
    branch_id = fields.Reference([('res.branch', 'Branch')])
    employee_id = fields.Many2many('hr.employee', string='Employee', domain=[])
    department_id = fields.Many2many('hr.department', string='Department', domain=[])
    order_by = fields.Selection([('employee_wise', 'Employee'), ('department_wise','Department'), ('date_wise', 'Date')], default='employee_wise')
    type = fields.Selection([('employee', 'Employee'), ('department', 'Department')], default='employee')
    selection = fields.Selection([('all', 'All'),('selection', 'Selection')], default='all')
    branch_exist = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaProductLedger, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = today.replace(day=1)
        res['date_to'] = today
        if 'branch_id' in self.env.user._fields:
            res['branch_id'] = 'res.branch,' + str(self.env.user.branch_id.id)
            res['branch_exist'] = True
        else:
            res['branch_exist'] = False
        return res

    @api.model
    def get_report_values(self, data=None):
        date_from = date_to = False
        loc_obj = self.env['stock.location']
        location = ''
        if data['date_from']:
            try:
                date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except TypeError:
                raise Warning("Invalid Date Format")
        if data['date_to']:
            try:
                date_to = datetime.strptime(data['date_to'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except TypeError:
                raise Warning("Invalid Date Format")
        if data['location_ids']:
            for loc in data['location_ids']:
                location += loc_obj.browse(loc).complete_name + ","
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'location': location,
            'type': data['type'],
            'order_by': data['order_by'],
            'branch_name': data['branch_name'],
            'lines': self.get_payroll_report(data),
        }

    def get_payroll_report(self, data):
        domain = [('slip_id.state','=','done')]
        final_data = {
            'records': {},
            'final_value': {},
        }



        request = """
            SELECT DISTINCT hpl.name, hpl.salary_rule_id
            FROM hr_payslip_line AS hpl
            LEFT JOIN hr_payslip AS hp ON (hp.id = hpl.slip_id)
            WHERE hp.created_date >= %s AND hp.created_date <= %s AND hp.state = 'done'
            ORDER BY hpl.salary_rule_id
        """
        self.env.cr.execute(request, (self.date_from, self.date_to))

        header = self.env.cr.dictfetchall()

        if data['employee_id']:
            if data['selection'] == 'selection' and data['type'] == 'employee':
                domain.append(('slip_id.employee_id','in',data['employee_id']))
            else:
                self.employee_id = False
        if data['department_id']:
            if data['selection'] == 'selection'and data['type'] == 'department':
                domain.append(('slip_id.employee_id.department_id', 'in', data['department_id']))
            else:
                self.department_id = False
        if data['date_from']:
            domain.append(('slip_id.created_date','>=', data['date_from']))
        if data['date_to']:
            domain.append(('slip_id.created_date','<=',data['date_to']))
        if 'branch_id' in self.env.user._fields:
            domain.append(('slip_id.branch_id', '=', self.branch_id.id))
        payslip = self.env['hr.payslip.line'].search(domain, order='slip_id, salary_rule_id')
        if data['order_by'] != 'department_wise':
            payslip = payslip.sorted(lambda x: x.slip_id.employee_id.name)
        for pay in payslip:
            if pay.salary_rule_id.id in final_data['final_value']:
                final_data['final_value'][pay.salary_rule_id.id]['total'] += pay.total
            else:
                final_data['final_value'][pay.salary_rule_id.id] = {
                    'total': pay.total
                }
            if data['order_by'] == 'employee_wise':
                heading = pay.slip_id.employee_id.id
            elif data['order_by'] == 'department_wise':
                heading = pay.slip_id.employee_id.department_id.id
            elif data['order_by'] == 'date_wise':
                heading = pay.slip_id.created_date.strftime('%d-%m-%Y')

            if heading in final_data['records']:
                if pay.salary_rule_id.id in final_data['records'][heading]['grand_total']:
                    final_data['records'][heading]['grand_total'][pay.salary_rule_id.id]['total'] += pay.total
                else:
                    final_data['records'][heading]['grand_total'][pay.salary_rule_id.id] = {
                        'total': pay.total,
                    }
                if pay.slip_id.id in final_data['records'][heading]['row']:
                    if pay.salary_rule_id.id in final_data['records'][heading]['row'][pay.slip_id.id]:
                        final_data['records'][heading]['row'][pay.slip_id.id][pay.salary_rule_id.id]['total'] += pay.total
                    else:
                        final_data['records'][heading]['row'][pay.slip_id.id][pay.salary_rule_id.id] = {
                            'name': pay.name,
                            'total': pay.total,
                        }
                else:
                    final_data['records'][heading]['row'][pay.slip_id.id] = {
                            'date': pay.slip_id.created_date.strftime('%d-%m-%Y'),
                            'employee_name': pay.slip_id.employee_id.name,
                            'net_salary': pay.slip_id.payable_amount,
                            'slip_number': pay.slip_id.number,
                            'model': pay.slip_id._name,
                            pay.salary_rule_id.id:
                            {
                                'name': pay.name,
                                'total': pay.total,
                            }
                        }
            else:
                final_data['records'][heading] = {
                    'employee_name': pay.slip_id.employee_id.name,
                    'department_name': pay.slip_id.employee_id.department_id.name,
                    'date': pay.slip_id.created_date.strftime('%d-%m-%Y'),
                    'grand_total': {
                        pay.salary_rule_id.id:
                            {
                                'total': pay.total,
                            }
                    },
                    'row': {
                        pay.slip_id.id: {
                            'date': pay.slip_id.created_date.strftime('%d-%m-%Y'),
                            'employee_name': pay.slip_id.employee_id.name,
                            'net_salary': pay.slip_id.payable_amount,
                            'slip_number': pay.slip_id.number,
                            'model': pay.slip_id._name,
                            pay.salary_rule_id.id:
                                {
                                    'name': pay.name,
                                    'total': pay.total,
                                }
                        }
                    }

                }
        return {
            'header': header,
            'body': final_data,
        }

    def get_html(self):  # Just changed this function ******
        if self.date_from > self.date_to:
            raise Warning('From date should be less than to date')
        res = self._get_report_data(search_date_from=self.date_from.strftime('%Y-%m-%d'),
                                    search_date_to=self.date_to.strftime('%Y-%m-%d'),
                                    report_location=self.branch_id,
                                    type=self.type,
                                    order_by=self.order_by,
                                    employee_id= self.employee_id.ids,
                                    department_id=self.department_id.ids,
                                    selection=self.selection)
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines'] = self.env.ref('beta_payroll_report.report_payroll')._render(
            {'lines': res['lines']['lines'],
             'date_from': res['lines']['date_from'],
             'date_to': res['lines']['date_to'],
             'data': res['lines']['data'],
             'type': res['lines']['type'],
             'order_by': res['lines']['order_by'],
             'location': res['lines']['location'],
             'branch_name': res['lines']['branch_name'],
             })
        self.template_area = res['lines']

    @api.model
    def _get_report_data(self,
                         search_date_from=False,
                         search_date_to=False,
                         report_location=False,
                         type=False,
                         order_by=False,
                         employee_id=False,
                         department_id=False,
                         selection=False
                         ):
        branch_name = ''
        if 'branch_id' in self.env.user._fields:
            loc_default = self.env['stock.warehouse'].search(
                [('branch_id', '=', self.env.user.branch_id.id)])
            if report_location:
                branch_name = report_location.name
        else:
            loc_default = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        rep_location = False
        if report_location:
            rep_location = self.env['stock.warehouse'].search([('branch_id', '=', report_location.id)])
        data = {
            'date_from': search_date_from,
            'date_to': search_date_to,
            'branch_name': branch_name,
            'location_ids': [int(rep_location.lot_stock_id.id)] if rep_location else [loc_default.lot_stock_id.id],
            'type': type if type else False,
            'order_by': order_by if order_by else False,
            'employee_id': employee_id if employee_id else False,
            'department_id': department_id if department_id else False,
            'selection': selection if selection else False
        }
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
