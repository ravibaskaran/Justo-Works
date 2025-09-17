# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import Warning


class BetaRegisterMarking(models.TransientModel):  # change this
    _name = 'beta.register.making'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Register Marking')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    report_type = fields.Selection([('all', 'All Employee'), ('selected_employee', 'Selected Employee')], 'Type',
                                   default='all')
    # employee_ids = fields.Many2one('hr.employee', string='Employee', domain=[('active', '=', True)])
    employee_ids = fields.Many2many('hr.employee', string='Employee', domain=[('active', '=', True)])
    register_id = fields.Many2one('hr.contribution.register', string='Register', required=True)
    branch_id = fields.Reference([('res.branch', 'Branch')])
    branch_exist = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaRegisterMarking, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = today
        res['date_to'] = today
        if 'branch_id' in self.env.user._fields:
            res['branch_id'] = 'res.branch,' + str(self.env.user.branch_id.id)
            res['branch_exist'] = True
        else:
            res['branch_exist'] = False
        return res

    # ▼ Generate Report value ▼
    @api.model
    def get_report_values(self, data=None):
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","
        # ▼ Returns to view ▼
        return {
            'data': data,
            'date_start': data['date_start'],
            'date_end': data['date_end'],
            'emp_type': data['employee_type'],
            'register': data['register'].name,
            'employee': data['employee'],
            'branch_ids': branch,
            'isbranch': data['isbranch'],
            'branch_name': data['branch_name'],
            'lines': self.get_register_marking(data),
        }

    # ♦ ▼ Call is received from get_report_values with parameter to fetch lines ▼ ♦
    def get_register_marking(self, data):
        if 'branch_id' in self.env.user._fields:
            date_start = data['date_start']
            date_end = data['date_end']
            register = data['register']
            emp_type = data['employee_type']
            employee = data['employee']
            branch_ids = data['branch_ids']
            filters = ''
            if date_start:
                filters = "where hp.created_date>='" + str(date_start) + "' "
            if date_end:
                filters = str(filters) + " and  hp.created_date<='" + str(date_end) + "' " if filters\
                    else "  hp.created_date<='" + str(date_end) + "' "
            if emp_type == 'selected_employee':
                if employee:
                    filters = str(filters) + "and hp.employee_id in" + str(tuple(employee)).replace(',)', ')')
            if register:
                filters = str(filters) + " and (hs.register_id ='" + str(register.id) + "' or hs2.register_id='" + str(register.id) + "')"
            if branch_ids:
                filters = str(filters) + "and hp.branch_id in" + str(tuple(branch_ids)).replace(',)', ')')
            if filters:
                filters = (str(filters))
            else:
                filters = ""
            docs = []
            temp = {}
            table = ''
            if date_start:
                request = """select hp.created_date as date,hp.number as voucher,hp.date_from,hp.date_to,
                            hpl.id as plid, hp.employee_id as eid,he.name as employee,hpl.category_id,hpl.amount,
                            hc.name as category,hpl.code as code, hpl.name as name,hpl.parent_rule_id,hs.name as child,hp.no_of_days,
                            hp.no_of_leaves,hp.salary_per_day,hp.leave_deduction_amount,hs.id rule_id1,hs.register_id rule_reg,
                            hs2.id parent_rule_id,hs2.register_id parent_rule_reg from hr_payslip_line as hpl
                            left join hr_salary_rule as hs on hs.id=hpl.salary_rule_id left join hr_salary_rule as hs2 on hs2.id=hs.parent_rule_id
                            left join hr_salary_rule_category as hc on hc.id=hpl.category_id
                            left join hr_payslip as hp on hp.id=hpl.slip_id
                            left join hr_employee as he on hp.employee_id = he.id """ + str(filters) +\
                            """ and hp.state = 'done' order by hp.employee_id """
                print('request', request)
                self.env.cr.execute(request)
                i = 0
                name = ''
                uid = ''
                temp_data = {}
                reg = []
                for row in self.env.cr.dictfetchall():
                    docs.append({
                        'voucher': str(row['voucher']),
                        'date': row['date'].strftime("%d/%m/%Y"),
                        'plid': row['plid'],
                        'eid': row['eid'],
                        'employee': row['employee'],
                        'category': str(row['category']),
                        'code': row['code'],
                        'date_from': row['date_from'].strftime("%d/%m/%Y"),
                        'name': row['name'],
                        'child': row['child'],
                        'date_to': row['date_to'].strftime("%d/%m/%Y"),
                        'reg_total': (row['no_of_days'] * row['salary_per_day']) - row['leave_deduction_amount'],
                        'amount': row['amount'],
                    })
                print('docs', docs)
                for row in docs:
                    if row['name'] not in reg:
                        reg += [row['name']]
                    x = row['name']
                    if temp.get(row['eid']):
                        if temp[row['eid']]['data'].get(row['voucher']):
                            if temp[row['eid']]['data'][row['voucher']].get(x):
                                # temp[row['eid']]['data'][row['voucher']][x] += row['amount']
                                temp[row['eid']]['data'][row['voucher']]['Total'] += row['amount']
                            else:
                                temp[row['eid']]['data'][row['voucher']][x] = row['amount']
                                temp[row['eid']]['data'][row['voucher']]['Total'] += row['amount']
                        else:
                            temp[row['eid']]['data'][row['voucher']] = {'Date':row['date'], 'Vr. No':row['voucher'],
                                                      'Description': row['date_from'] + '-' + row['date_to'], x: row['amount'],
                                                       'Total': row['amount']}
                    else:
                        temp[row['eid']] = {
                            'name': row['employee'],
                            'data': {row['voucher']: {'Date':row['date'], 'Vr. No':row['voucher'],
                                                      'Description': row['date_from'] + '-' + row['date_to'], x: row['amount'],
                                                       'Total': row['amount']}}
                        }
                colspan = 4 + len(reg)
                table += """
                    <table id="tableId" rules="groups" frame="hsides" border="1"
                           class="table table-bordered table-striped table-font-size"
                           style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px;">
                        <style>.table td{ padding: .8px !important;}
                                .td-hide{display:none !important;}
                        </style>
                            <thead>
                            <th class="text-center style="width: 15%">Date</th>
                            <th class="text-center style="width: 15%">Voucher No.</th>
                            <th class="text-center style="width: 15%">Description</th>
                """
                if reg:
                    for x in reg:
                        table += """
                        <th class="text-center">%s</th>
                        """ % (x)
                table += """
                    <th class="text-center">Total</th></thead><tbody>
                """
                grand_total = 0.0
                if temp:
                    for x in temp:
                        table += """
                                <tr>
                                   <td class="table-font-size" colspan="%s" style="text-align:left;padding-left:15px !important;font-weight:bold;font-size:14px">%s</td></tr>
                                """ % (colspan, str(temp[x]['name']))
                        for y in temp[x]['data']:
                            table += """
                                <tr>
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                """ % (temp[x]['data'][y]['Date'], temp[x]['data'][y]['Vr. No'], temp[x]['data'][y]['Description'])
                            for z in reg:
                                if temp[x]['data'][y].get(z):
                                    table += """
                                                <td style="text-align:right;padding-right:5px !important;">%s</td> 
                                             """ % ("%.2f" % temp[x]['data'][y][z])
                                else:
                                    table += """
                                                <td style="text-align:right;padding-right:5px !important;">0.00</td> 
                                             """
                            table += """
                            <td style="text-align:right;padding-right:5px !important;">%s</td> 
                            </tr>""" % ("%.2f" % temp[x]['data'][y]['Total'])
                            grand_total += temp[x]['data'][y]['Total']
                    table += """
                            <td class="table-font-size" colspan="%s" style="text-align:right;padding-right:5px !important;font-weight:bold;font-size:14px"">%s</td> 
                            </tr>""" % (colspan, "%.2f" % grand_total)
        else:
            date_start = data['date_start']
            date_end = data['date_end']
            register = data['register']
            emp_type = data['employee_type']
            employee = data['employee']
            filters = ''
            if date_start:
                filters = "where hp.created_date>='" + str(date_start) + "' "
            if date_end:
                filters = str(filters) + " and  hp.created_date<='" + str(date_end) + "' " if filters\
                    else "  hp.created_date<='" + str(date_end) + "' "
            if emp_type == 'selected_employee':
                if employee:
                    filters = str(filters) + "and hp.employee_id in" + str(tuple(employee)).replace(',)', ')')
            if register:
                # filters = str(filters) + " and hs.register_id='" + str(register.id) + "'"
                filters = str(filters) + " and (hs.register_id ='" + str(register.id) + "' or hs2.register_id='" + str(register.id) + "')"
            if filters:
                filters = (str(filters))
            else:
                filters = ""
            docs = []
            temp = {}
            table = ''
            if date_start:
                request = """select hp.created_date as date,hp.number as voucher,hp.date_from,hp.date_to,
                            hpl.id as plid, hp.employee_id as eid,he.name as employee,hpl.category_id,hpl.amount,
                            hc.name as category,hpl.code as code, hpl.name as name,hpl.parent_rule_id,hs.name as child,hp.no_of_days,
                            hp.no_of_leaves,hp.salary_per_day,hp.leave_deduction_amount,hs.id rule_id1,hs.register_id rule_reg,
                            hs2.id parent_rule_id,hs2.register_id parent_rule_reg from hr_payslip_line as hpl
                            left join hr_salary_rule as hs on hs.id=hpl.salary_rule_id left join hr_salary_rule as hs2 on hs2.id=hs.parent_rule_id
                            left join hr_salary_rule_category as hc on hc.id=hpl.category_id
                            left join hr_payslip as hp on hp.id=hpl.slip_id
                            left join hr_employee as he on hp.employee_id = he.id """ + str(filters) +\
                            """ and state = 'done' order by hp.employee_id """
                print('request', request)
                self.env.cr.execute(request)
                i = 0
                name = ''
                uid = ''
                temp_data = {}
                reg = []
                for row in self.env.cr.dictfetchall():
                    docs.append({
                        'voucher': str(row['voucher']),
                        'date': row['date'].strftime("%d/%m/%Y"),
                        'plid': row['plid'],
                        'eid': row['eid'],
                        'employee': row['employee'],
                        'category': str(row['category']),
                        'code': row['code'],
                        'date_from': row['date_from'].strftime("%d/%m/%Y"),
                        'name': row['name'],
                        'child': row['child'],
                        'date_to': row['date_to'].strftime("%d/%m/%Y"),
                        'reg_total': (row['no_of_days'] * row['salary_per_day']) - row['leave_deduction_amount'],
                        'amount': row['amount'],
                    })
                print('docs', docs)
                for row in docs:
                    if row['name'] not in reg:
                        reg += [row['name']]
                    x = row['name']
                    if temp.get(row['eid']):
                        if temp[row['eid']]['data'].get(row['voucher']):
                            if temp[row['eid']]['data'][row['voucher']].get(x):
                                # temp[row['eid']]['data'][row['voucher']][x] += row['amount']
                                temp[row['eid']]['data'][row['voucher']]['Total'] += row['amount']
                            else:
                                temp[row['eid']]['data'][row['voucher']][x] = row['amount']
                                temp[row['eid']]['data'][row['voucher']]['Total'] += row['amount']
                        else:
                            temp[row['eid']]['data'][row['voucher']] = {'Date':row['date'], 'Vr. No':row['voucher'],
                                                      'Description': row['date_from'] + '-' + row['date_to'], x: row['amount'],
                                                       'Total': row['amount']}
                    else:
                        temp[row['eid']] = {
                            'name': row['employee'],
                            'data': {row['voucher']: {'Date':row['date'], 'Vr. No':row['voucher'],
                                                      'Description': row['date_from'] + '-' + row['date_to'], x: row['amount'],
                                                       'Total': row['amount']}}
                        }
                colspan = 4 + len(reg)
                table += """
                    <table id="tableId" rules="groups" frame="hsides" border="1"
                           class="table table-bordered table-striped table-font-size"
                           style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px;">
                        <style>.table td{ padding: .8px !important;}
                                .td-hide{display:none !important;}
                        </style>
                            <thead>
                            <th class="text-center style="width: 15%">Date</th>
                            <th class="text-center style="width: 15%">Voucher No.</th>
                            <th class="text-center style="width: 15%">Description</th>
                """
                if reg:
                    for x in reg:
                        table += """
                        <th class="text-center">%s</th>
                        """ % (x)
                table += """
                    <th class="text-center">Total</th></thead><tbody>
                """
                grand_total = 0.0
                if temp:
                    for x in temp:
                        table += """
                                <tr>
                                   <td class="table-font-size" colspan="%s" style="text-align:left;padding-left:15px !important;font-weight:bold;font-size:14px">%s</td></tr>
                                """ % (colspan, str(temp[x]['name']))
                        for y in temp[x]['data']:
                            table += """
                                <tr>
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                    <td style="text-align:center;padding-left:5px !important;">%s</td> 
                                """ % (temp[x]['data'][y]['Date'], temp[x]['data'][y]['Vr. No'], temp[x]['data'][y]['Description'])
                            for z in reg:
                                if temp[x]['data'][y].get(z):
                                    table += """
                                                <td style="text-align:right;padding-right:5px !important;">%s</td> 
                                             """ % ("%.2f" % temp[x]['data'][y][z])
                                else:
                                    table += """
                                                <td style="text-align:right;padding-right:5px !important;">0.00</td> 
                                             """
                            table += """
                            <td style="text-align:right;padding-right:5px !important;">%s</td> 
                            </tr>""" % ("%.2f" % temp[x]['data'][y]['Total'])
                            grand_total += temp[x]['data'][y]['Total']
                    table += """
                            <td class="table-font-size" colspan="%s" style="text-align:right;padding-right:5px !important;font-weight:bold;font-size:14px"">%s</td> 
                            </tr>""" % (colspan, "%.2f" % grand_total)

        return {
            # 'doc_ids': data['ids'],
            # 'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            # 'p_type': p_types,
            'docs': table,
        }

    def get_html(self):  # Just changed this function ******
        if self.date_from > self.date_to:
            raise Warning('From date should be less than to date')
        res = self._get_report_data(date_start=self.date_from.strftime('%Y-%m-%d'),
                                    date_end=self.date_to.strftime('%Y-%m-%d'),
                                    register=self.register_id, sp_type=self.report_type, report_location=self.branch_id,
                                    employee=self.employee_ids.ids if self.employee_ids else False)
        res['lines'] = self.env.ref('beta_register_marking.report_register_marking')._render({
            'lines': res['lines']['lines'],
            'date_start': res['lines']['date_start'],
            'date_end': res['lines']['date_end'],
            'register': res['lines']['register'],
            # 'sp_type': res['lines']['sp_type'],
            'branch_ids': res['lines']['branch_ids'],
            'isbranch': res['lines']['isbranch'],
            'branch_name': res['lines']['branch_name'],
            'employee': res['lines']['employee'],
            'data': res['lines']['data'],
        })
        self.template_area = res['lines']

    # ▼ Get Report Data ▼
    @api.model
    def _get_report_data(self, date_start=False, date_end=False, register=False, sp_type=False, report_location=False, employee=False):
        branch_name = ''
        is_branch = False
        if 'branch_id' in self.env.user._fields:
            branch_list = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            branch_default = self.env['res.branch'].search(
                [('id', '=', self.env.user.branch_id.id)])
            is_branch = True
        else:
            branch_default = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])

            is_branch = False
        rl = ''
        emp = {}
        if employee:
            emp = [int(i) for i in employee]
        if report_location:
            rl = [int(i) for i in report_location]
        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))
        data = {
            'date_start': date_start if date_start else False,
            'date_end': date_end if date_end else False,
            'register': register if register else False,
            'employee_type': sp_type if sp_type else False,
            'branch_ids': rl if rl else (branch_default.id,),
            'isbranch': is_branch,
            'branch_name': branch_name,
            'employee': emp if emp else False,
        }
        dat = self.get_report_values(data=data)
        return {
            'lines': dat,
        }
