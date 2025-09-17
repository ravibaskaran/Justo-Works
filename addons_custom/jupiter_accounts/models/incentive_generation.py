from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class IncentiveGeneration(models.Model):
    _name = 'incentive.generation'
    _description = 'Incentive Generation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(default='Draft', copy=False, tracking=True)
    date = fields.Date(copy=False, tracking=True)
    financial_range = fields.Many2one('ir.sequence.date_range')
    period_from = fields.Date(copy=False)
    period_to = fields.Date(copy=False)
    line_ids = fields.One2many('incentive.generation.line', 'generation_id', copy=False)
    interval = fields.Integer(copy=False)
    period_id = fields.Many2one('incentive.period', copy=False)
    state = fields.Selection([('draft', 'Draft'), ('generated', 'Generated')], default='draft', copy=False, tracking=True)
    invoice_ids = fields.Many2many('account.move', copy=False)

    def view_invoices(self):
        form_view_id = self.env.ref("account.view_move_form").id
        tree_view_id = self.env.ref("account.view_invoice_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incentives',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }

    @api.model
    def create(self, vals_list):
        res = super(IncentiveGeneration, self).create(vals_list)
        if not res.line_ids:
            raise UserError('No lines found!')
        res.name = self.env['ir.sequence'].next_by_code('incentive.generation.sequence')
        return res

    @api.model
    def default_get(self, fields_list):
        res = super(IncentiveGeneration, self).default_get(fields_list)
        res['date'] = fields.Date.today()
        config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
        if config:
            res['interval'] = config.incentive_interval
        return res

    @api.onchange('period_id', 'financial_range')
    def onchange_period_id(self):
        if self.financial_range:
            if not self.financial_range.date_from <= fields.Date.today() <= self.financial_range.date_to:
                raise UserError('Only this financial year can be selected!')
        self.period_from = self.period_to = False
        if self.period_id and self.financial_range:
            date_intervals = []
            initial_date = self.financial_range.date_from
            while initial_date <= self.financial_range.date_to:
                date_list = [initial_date]
                initial_date += relativedelta(months=self.interval)
                initial_date -= relativedelta(days=1)
                date_list.append(initial_date)
                initial_date += relativedelta(days=1)
                date_intervals.append(date_list)
            self.period_from = date_intervals[self.period_id.count - 1][0]
            self.period_to = date_intervals[self.period_id.count - 1][1]

            # take configuration for monthly minimum booking count and incentive interval
            config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
            if not config:
                raise UserError('Configuration not found!')
            if config.monthly_minimum_booking <= 0:
                raise UserError('Monthly minimum booking is not configured!')
            if config.incentive_interval <= 0:
                raise UserError('Incentive Interval is not configured!')

            def check_eligibility(date_from, date_to, employee_id):
                # get month count between two dates
                month_count = relativedelta(date_to, date_from).years * 12 + relativedelta(date_to, date_from).months + 1

                # take all the booking of the employee at the period and check if the employee is eligible
                # if the booking count is greater than or equal to month count * monthly min count then the employee is eligible
                bookings = """
                    SELECT COALESCE(count(ur.id), 0)
                    FROM unit_reservation ur 
                    LEFT JOIN building b ON b.id = ur.building
                    WHERE ur.date <= '%s' and ur.date >= '%s' and
                    %s IN (ur.closing_manager_id, ur.sourcing_manager_id,
                    ur.closing_tl_id, ur.sourcing_tl_id, ur.crm_id, ur.marketing_id) and
                    b.incentive_type = '2' and ur.state not in ('draft', 'canceled')
                """
                self.env.cr.execute(
                    bookings % (date_to.strftime('%Y-%m-%d'), date_from.strftime('%Y-%m-%d'), employee_id))
                booking_count = self.env.cr.fetchone()[0]
                if booking_count >= month_count * config.monthly_minimum_booking:
                    return True
                return False

            # Take all the registrations in the period and group all of its employees
            qry = """
                SELECT COALESCE(CONCAT(
                    STRING_AGG(DISTINCT ur.closing_manager_id::text, ','), ',',
                    STRING_AGG(DISTINCT ur.sourcing_manager_id::text, ','), ',',
                    STRING_AGG(DISTINCT ur.closing_tl_id::text, ','), ',',
                    STRING_AGG(DISTINCT ur.sourcing_tl_id::text, ','), ',',
                    STRING_AGG(DISTINCT ur.crm_id::text, ','), ',',
                    STRING_AGG(DISTINCT ur.marketing_id::text, ',')
                ), '') as all_ids
                FROM project_registration pr
                LEFT JOIN unit_reservation ur ON ur.id = pr.booking_id
                LEFT JOIN building b ON b.id = pr.project_id 
                WHERE pr.registration_date <= '%s' and pr.registration_date >= '%s'
                    and pr.state != 'draft' and b.incentive_type = '2'
            """
            self.env.cr.execute(qry % (self.period_to.strftime('%Y-%m-%d'), self.financial_range.date_from.strftime('%Y-%m-%d')))
            employees = self.env.cr.fetchone()
            line_data = []
            if employees:
                employees = employees[0]
                employees = employees.split(',')

                # Now loop through the employees and take each employee's registrations
                for employee in employees:
                    if employee:
                        registration_qry = """
                            SELECT pr.id as registration_id, pr.booking_id, 
                            b.id as project_id, pr.flat_id,ur.date as booking_date,
                            STRING_AGG(am.partner_id::text, ',') as incentive_employees, rp.id as employee_partner
                            FROM project_registration pr
                            LEFT JOIN unit_reservation ur ON ur.id = pr.booking_id
                            LEFT JOIN building b ON b.id = ur.building
                            LEFT JOIN account_move_project_registration_rel apr ON apr.project_registration_id = pr.id
                            LEFT JOIN account_move am ON am.id = apr.account_move_id
                            LEFT JOIN hr_employee emp ON emp.id = %s
                            LEFT JOIN res_partner rp ON rp.id = emp.partner_id
                            WHERE %s IN (ur.closing_manager_id, ur.sourcing_manager_id, 
                                ur.closing_tl_id, ur.sourcing_tl_id, ur.crm_id, ur.marketing_id) and
                                pr.registration_date <= '%s' and pr.registration_date >= '%s'
                                and pr.state != 'draft' and b.incentive_type = '2'
                            GROUP BY pr.id, b.id, ur.id, rp.id
                        """
                        self.env.cr.execute(registration_qry % (
                            employee, employee, self.period_to.strftime('%Y-%m-%d'), self.financial_range.date_from.strftime('%Y-%m-%d')))
                        registrations = self.env.cr.dictfetchall()

                        # Now loop through the registrations and check if the employee is eligible for incentive for the registration
                        for registration in registrations:

                            # check if employee already get incentive for the registration
                            if registration.get('incentive_employees') and registration.get(
                                    'employee_partner') and registration.get('employee_partner') in [int(i) for i in registration.get(
                                    'incentive_employees').split(',')]:
                                continue

                            booking_date = registration.get('booking_date')

                            # get financial range of the booking date
                            # if the employee has the min booking for the financial year then he is eligible
                            if booking_date.month >= 4:
                                start_year = booking_date.year
                                end_year = booking_date.year + 1
                            else:
                                start_year = booking_date.year - 1
                                end_year = booking_date.year
                            financial_year_start = datetime(start_year, 4, 1).date()
                            financial_year_end = datetime(end_year, 3, 31).date()
                            period_start = financial_year_start
                            period_end = financial_year_end

                            # if the booking is in this financial year we should take the forms period to as end date else financial year end as end date
                            if self.period_to < financial_year_end:
                                period_end = self.period_to
                            eligible = check_eligibility(period_start, period_end, employee)

                            # if the employee is still not eligible then look at the range fin start and booking date's incentive interval end
                            if not eligible:
                                date_intervals = []
                                initial_date = financial_year_start
                                while initial_date <= financial_year_end:
                                    date_list = [initial_date]
                                    initial_date += relativedelta(months=config.incentive_interval)
                                    initial_date -= relativedelta(days=1)
                                    date_list.append(initial_date)
                                    initial_date += relativedelta(days=1)
                                    date_intervals.append(date_list)
                                for interval in date_intervals:
                                    if interval[0] <= booking_date.date() <= interval[1]:
                                        period_end = interval[1]
                                        break
                                eligible = check_eligibility(period_start, period_end, employee)

                            # if the employee is still not eligible then loot at the month of the booking to check eligibility
                            # if not eligible:
                            #     period_start = datetime(booking_date.year, booking_date.month, 1)
                            #     period_end = period_start + relativedelta(months=1) - relativedelta(days=1)
                            #     eligible = check_eligibility(period_start, period_end, employee)

                            # if the employee is eligible we will add the registrations to the table
                            # and generate their incentive invoices by the generate button
                            if eligible:
                                line_data.append((0, 0, {
                                    'employee_id': int(employee),
                                    'registration_id': registration.get('registration_id'),
                                    'project_id': registration.get('project_id'),
                                    'flat_id': registration.get('flat_id')
                                }))
            self.line_ids = False
            self.line_ids = line_data

    def action_generate(self):
        config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
        if not config:
            raise UserError('Configuration not found!')
        if not config.incentive_product:
            raise UserError('Incentive service product not found in configurations!')
        if not self.line_ids:
            raise UserError('No lines found!')
        for line in self.line_ids:
            if line.project_id.incentive_type == '2':
                booking = line.registration_id.booking_id
                if booking:
                    incentive_voucher = self.env['employee.incentive.move'].search([('date', '<', booking.date), ('project_id', '=', line.project_id.id)],
                                                                                   order='date desc', limit=1)
                    if incentive_voucher:
                        if line.employee_id == booking.closing_manager_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.closing_manager_id, incentive_voucher.closing_manager_amount, config, 'Closing Manager')
                        elif line.employee_id == booking.sourcing_manager_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.sourcing_manager_id, incentive_voucher.sourcing_manager_amount, config, 'Sourcing Manager')
                        elif line.employee_id == booking.closing_tl_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.closing_tl_id, incentive_voucher.closing_tl_amount, config, 'Closing TL')
                        elif line.employee_id == booking.sourcing_tl_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.sourcing_tl_id, incentive_voucher.sourcing_tl_amount, config, 'Sourcing TL')
                        elif line.employee_id == booking.crm_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.crm_id, incentive_voucher.crm_amount, config, 'CRM')
                        elif line.employee_id == booking.marketing_id:
                            self.invoice_ids += line.registration_id.employee_invoice_creation(booking.marketing_id, incentive_voucher.marketing_amount, config, 'Marketing')
                    else:
                        raise UserError('No Employee Incentive Voucher Found!')
                else:
                    raise UserError('No Booking Found!')
        self.state = 'generated'


class IncentiveGenerationLine(models.Model):
    _name = 'incentive.generation.line'

    generation_id = fields.Many2one('incentive.generation')
    employee_id = fields.Many2one('hr.employee')
    project_id = fields.Many2one('building')
    flat_id = fields.Many2one('product.template')
    registration_id = fields.Many2one('project.registration')


class IncentivePeriod(models.Model):
    _name = 'incentive.period'

    name = fields.Char()
    count = fields.Integer()


class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    name = fields.Char(compute="compute_name")

    def compute_name(self):
        for data in self:
            data.name = data.date_from.strftime('%y') + '-' + data.date_to.strftime('%y')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        sequence = journal.sequence_id
        if not sequence:
            sequence = self.env['ir.sequence'].search([('use_date_range', '=', True),('date_range_ids','!=',False)], limit=1)
        if self._context.get('financial_year'):
            domain = [('sequence_id', '=', sequence.id)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
