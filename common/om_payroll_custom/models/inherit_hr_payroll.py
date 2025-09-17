from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import date, datetime
from calendar import monthrange


class HrPayroll(models.Model):
    _inherit = 'hr.payslip'

    no_of_leaves = fields.Float('No of Leaves',digits=(16,1), track_visibility='onchange')
    salary_per_day = fields.Float('Per Day', track_visibility='onchange')
    no_of_days = fields.Integer('No of Days')
    payable_amount = fields.Float('Payable Amount')
    leave_deduction_amount = fields.Float('Leave Deduction Amount')
    created_date = fields.Date("Create Date", default=date.today())
    pay_type = fields.Selection(related='contract_id.schedule_pay', store=False)



    @api.onchange('employee_id', 'date_from', 'date_to')
    def check_employee_payslip(self):
        if self.employee_id and self.date_from and self.date_to:
            domains = [
                [
                    ('employee_id', '=', self.employee_id.id),
                    ('date_from', '<=', self.date_to),
                    ('date_to', '>=', self.date_to),
                    ('state', '=', 'done')
                ],
                [
                    ('employee_id', '=', self.employee_id.id),
                    ('date_from', '<=', self.date_from),
                    ('date_to', '>=', self.date_from),
                    ('state', '=', 'done')
                ],
                [
                    ('employee_id', '=', self.employee_id.id),
                    ('date_from', '>=', self.date_from),
                    ('date_from', '<=', self.date_to),
                    ('state', '=', 'done')],
                [
                    ('employee_id', '=', self.employee_id.id),
                    ('date_to', '>=', self.date_from),
                    ('date_to', '<=', self.date_to),
                    ('state', '=', 'done')
                ]
            ]
            for domain in domains:
                data = self.env['hr.payslip'].search(domain)
                if data:
                    raise UserError('Payslip already exists for the employee at the selected time period')
            data = self.env['hr.payslip'].search(
                [('employee_id', '=', self.employee_id.id), ('date_from', '>=', self.date_to), ('state', '=', 'done')])
            if data:
                raise UserError('Previous date entry not allowed!')

    def payslip_print(self):
        result = self.env.ref('om_hr_payroll.action_report_payslip').report_action(self)
        result['default_print_option'] = 'print'
        return result

    def cancel_sheet(self):
        self.write({'state':'cancel'})
        for move in self.move_ids:
            move.state = 'cancel'

    def compute_sheet(self):
        res = super(HrPayroll, self).compute_sheet()
        self.number = ''
        amount = 0.00
        for payslip in self:
            if payslip.credit_note != True:
                payslip_lines = self.env['hr.payslip'].search([
                    ('employee_id', '=', payslip.employee_id.id),
                    ('date_from', '=', payslip.date_from),
                    ('date_to', '=', payslip.date_to),
                    ('state', '=', 'done')
                ])

                if payslip_lines:
                    raise UserError('Payslip already exist')
        for lines in self.details_by_salary_rule_category:
            if lines.category_id.type == 'addition':
                amount += lines.total
            elif lines.category_id.type == 'deduction':
                amount -= lines.total
        round_off = 0
        if amount % 1 != 0:
            round_off = round(amount) - amount
            round_off_rule = self.env.ref('om_payroll_custom.round_off_payroll')
            line = self.env['hr.payslip.line'].create({
                'contract_id': self.contract_id.id,
                'slip_id': self.id,
                'salary_rule_id': round_off_rule.id,
                'code': 'ROUND',
                'category_id': round_off_rule.category_id.id,
                'name': 'Round Off',
                'amount': round_off
            })
            self.details_by_salary_rule_category += line
        self.payable_amount = amount + round_off
        print(amount)
        return res

    @api.onchange('no_of_leaves', 'salary_per_day')
    def onchange_leave_deduction_amount(self):
        if self.no_of_leaves != 0:
            if self.salary_per_day:
                self.leave_deduction_amount = self.no_of_leaves * self.salary_per_day
        else:
            self.leave_deduction_amount = 0.00

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        res = super(HrPayroll, self).onchange_employee()
        if self.employee_id and self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise UserError('From date should be less than to date')

            # Purpose : Calculating the days from given period
            self.no_of_days = (self.date_to - self.date_from).days + 1
            # Notes: day salary is calculated based on the contract schedule_pay
            if self.pay_type == 'weekly':
                self.salary_per_day = self.contract_id.wage / 7
            elif self.pay_type == 'daily':
                self.salary_per_day = self.contract_id.wage
            elif self.pay_type == 'biweekly':
                self.salary_per_day = self.contract_id.wage/ 14
            elif self.pay_type == 'monthly':
                check_days = self.check_month(self.date_from,self.date_to)
                self.salary_per_day = self.contract_id.wage / check_days['days']
                if check_days['message']:
                    return {'warning': {
                        'title': "Warning",
                        'message': check_days['message']}
                    }
            else:
                self.salary_per_day = self.contract_id.wage / self.no_of_days
            # Reference : f'q{(int(from_month)-1)//3+1}' to find the which quarter information from the given month
        return res

    def check_month(self, datefrom,dateto):
        """
            To Get Days in Month this function will check whether the month and year
            of the from and to date is same else make those field none.
            :param datefrom:  From date
            :param dateto:  To date
            :return: Total days in given month
        """

        # ♦ Date From ♦
        month = datetime.strftime(datetime.strptime(str(datefrom), "%Y-%m-%d"), "%m")
        year = datetime.strftime(datetime.strptime(str(datefrom), "%Y-%m-%d"), "%Y")

        # ♦ Date To ♦
        month2 = datetime.strftime(datetime.strptime(str(dateto), "%Y-%m-%d"), "%m")
        year2 = datetime.strftime(datetime.strptime(str(dateto), "%Y-%m-%d"), "%Y")

        # Notes: Function to get days from month and year
        last_day = monthrange(int(year), int(month))
        days = str(last_day).replace('(', '').replace(')', '').split(',')
        if year == year2:
            if month == month2:
                msg = None
            else:
                self.date_to = None
                msg ='From and To period should be in same month'
        else:
            self.date_to = None
            msg = 'From and To period should be in same year'

        return {
            'days': int(days[1]) if days else 30,
            'message': msg
        }

    # Reference : update hr_salary_rule set amount_python_compute=REPLACE(amount_python_compute, 'contract.wage', '(payslip.no_of_days * payslip.salary_per_day) - payslip.leave_deduction_amount')


class HrPaySlipLine(models.Model):
    _inherit = 'hr.payslip.line'

    category_type = fields.Selection([('addition', 'Addition'), ('deduction', 'Deduction'), ('z_adjustment', 'Adjustment')], related='category_id.type')
