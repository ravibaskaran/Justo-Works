# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.rrule import rrule, MONTHLY
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools.float_utils import float_round

expected_timeline_years = [(str(key), str(key)) for key in range(1, 11)]
retainer_months_domain = [(str(key), str(key)) for key in range(1, 51)]
no_of_months_domain = [(str(key), str(key)) for key in range(1, 51)]


class BudgetSheet(models.Model):
    _name = 'budget.sheet'
    _inherit = ['mail.thread']
    _description = 'Budgeting'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')
    form_editable = fields.Boolean(compute='compute_form_editable', default=True)

    @api.depends('state')
    def compute_form_editable(self):
        for rec in self:
            rec.form_editable = True
            if rec.state == 'confirmed' and not self.env.user.has_group('real_estate_sheets.group_evaluation_budgeting_confirm'):
                rec.form_editable = False

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_export_form(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/budgeting/excel_export/%s' % self.env.context.get('active_id'),
            'target': 'self',
        }

    name = fields.Char('Number', default='/')

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('project.budget.sheet')
        return super(BudgetSheet, self).create(values)

    budget_starting_date = fields.Date()

    # INFORMATION ABOUT PROJECT
    project_id = fields.Many2one('building', 'Name of Project')
    apartment_type_ids = fields.Many2many('building.unit', string='Project Details')
    apartments_no_best = fields.Integer('No. of Apartments (Best scenario)')
    apartments_no_worst = fields.Integer('No. of Apartments (Worst scenario)')
    saleable_area = fields.Float('Saleable Area in Sq. Ft')
    tentative_unit_sales_price = fields.Float('Tentative Unit Sales Price (Lakhs)')
    total_value = fields.Float('Total Value (Lakhs) - Best')
    total_value_worst = fields.Float('Total Value (Lakhs) - Worst')
    developer_id = fields.Many2one('res.partner', 'Name of Developer', domain=[('is_owner', '=', True)])
    project_location = fields.Char('Location')
    rera_number = fields.Char('RERA No.')
    project_status = fields.Char('Status of Project')
    mandate_nature = fields.Char('Nature of Mandate')
    expected_timeline = fields.Selection(expected_timeline_years, 'Expected Timeline of Project')
    possession_date = fields.Date()
    construction_stage = fields.Many2one('construction.stage', 'Stage of Construction')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Cost Center')

    @api.onchange('budget_starting_date', 'project_id')
    def check_financial_year_project_uniqueness(self):
        if self.project_id and self.budget_starting_date:
            budget_start = self.budget_starting_date.strftime('%Y-%m-01')
            budget_start = datetime.strptime(budget_start, '%Y-%m-%d')
            if budget_start.month < 4:
                financial_end = str(budget_start.year) + '-03-31'
                financial_start = str(budget_start.year - 1) + '-04-01'
            else:
                financial_end = str(budget_start.year + 1) + '-03-31'
                financial_start = str(budget_start.year) + '-04-01'
            data = self.env['budget.sheet'].search(
                [('id', '!=', self._origin.id), ('project_id', '=', self.project_id.id)]).filtered(
                lambda l: datetime.strptime(financial_start, '%Y-%m-%d').date() < l.budget_starting_date < datetime.strptime(
                    financial_end, '%Y-%m-%d').date())
            if data:
                raise UserError('Budget already exists in the selected financial year for this project')
            previous_budgets = self.env['budget.sheet'].search(
                [('budget_starting_date', '<', self.budget_starting_date), ('project_id', '=', self.project_id.id)])
            if previous_budgets:
                sales_forecast_lines = previous_budgets.mapped('sales_forecast_lines')
                self.booking_ptd = sum(sales_forecast_lines.mapped('booking'))
                self.registration_ptd = sum(sales_forecast_lines.mapped('registration'))
                profit_loss_lines = previous_budgets.mapped('profit_loss_lines')
                self.sales_value_ptd = sum(profit_loss_lines.mapped('sales_value'))
                self.retainer_fee_ptd = sum(profit_loss_lines.mapped('retainer_fee'))
                self.billing_ptd = sum(profit_loss_lines.mapped('billing'))
                self.total_revenue_ptd = sum(profit_loss_lines.mapped('total_revenue'))
                profit_loss_expense_lines = previous_budgets.mapped('profit_loss_expense_lines')
                self.admin_exp_ptd = sum(profit_loss_expense_lines.mapped('admin_exp'))
                self.manpower_cost_ptd = sum(profit_loss_expense_lines.mapped('manpower_cost'))
                self.sales_incentive_ptd = sum(profit_loss_expense_lines.mapped('sales_incentive'))
                self.other_expenses_ptd = sum(profit_loss_expense_lines.mapped('other_expenses'))
                self.total_expense_ptd = sum(profit_loss_expense_lines.mapped('total_expense'))
                self.revenue_expense_diff_ptd = sum(profit_loss_expense_lines.mapped('revenue_expense_diff'))
                cash_flow_lines = previous_budgets.mapped('cash_flow_lines')
                self.collection_ptd = sum(cash_flow_lines.mapped('collection'))
                self.gst_inflow_ptd = sum(cash_flow_lines.mapped('gst_inflow'))
                self.gross_inflow_ptd = sum(cash_flow_lines.mapped('gross_inflow'))
                cash_flow_expense_lines = previous_budgets.mapped('cash_flow_expense_lines')
                self.cf_admin_exp_ptd = sum(cash_flow_expense_lines.mapped('admin_exp'))
                self.cf_manpower_cost_ptd = sum(cash_flow_expense_lines.mapped('manpower_cost'))
                self.cf_sales_incentive_ptd = sum(cash_flow_expense_lines.mapped('sales_incentive'))
                self.cf_other_expenses_ptd = sum(cash_flow_expense_lines.mapped('other_expenses'))
                self.gst_outflow_ptd = sum(cash_flow_expense_lines.mapped('gst_outflow'))
                self.gross_outflow_ptd = sum(cash_flow_expense_lines.mapped('gross_outflow'))
                self.in_outflow_diff_ptd = sum(cash_flow_expense_lines.mapped('in_outflow_diff'))
                productivity_ratio_lines = previous_budgets.mapped('productivity_ratio_lines')
                self.total_expenses_pr_ptd = sum(productivity_ratio_lines.mapped('total_expenses'))
                self.revenue_ptd = sum(productivity_ratio_lines.mapped('revenue'))
                self.manpower_cost_pr_ptd = sum(productivity_ratio_lines.mapped('manpower_cost'))
                self.inflow_outflow_ptd = sum(productivity_ratio_lines.mapped('inflow_outflow'))

    @api.model
    def default_get(self, fields_list):
        res = super(BudgetSheet, self).default_get(fields_list)
        res['budget_starting_date'] = datetime.today().strftime('%Y-%m-01')
        return res

    @api.onchange('apartments_no_best', 'tentative_unit_sales_price')
    def calculate_total_value(self):
        self.total_value = self.apartments_no_best * self.tentative_unit_sales_price

    @api.onchange('apartments_no_worst', 'tentative_unit_sales_price')
    def calculate_total_value_worst(self):
        self.total_value_worst = self.apartments_no_worst * self.tentative_unit_sales_price

    # Financial Status
    loan_details = fields.Char('Loans, If Any')
    mortgage_partners = fields.Char()
    finance_partners = fields.Char()

    # Activities to be performed by Justo for Developer
    hiring = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    marketing_atl = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Marketing - ATL')
    marketing_btl = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Marketing - BTL')

    # Key Assumptions
    gross_justo_commission = fields.Float("Gross JUSTO's Commission %")
    net_justo_commission = fields.Float("Net JUSTO's Commission %")
    avg_sales_team_incentive = fields.Float('Avg. Sales Team Incentive per Unit %')
    commission_retention = fields.Float('Commission Retention %')

    # JUSTO's Commission Billing
    signing_amount = fields.Float()
    retainer_fee = fields.Float()
    retainer_month = fields.Selection(retainer_months_domain)
    monthly_retainer_fee = fields.One2many('budget.sheet.line', 'budget_id')
    is_not_first_budget = fields.Boolean()

    @api.onchange('signing_amount')
    def check_signing_with_previous_budget(self):
        previous_budgets = self.env['budget.sheet'].search(
            [('budget_starting_date', '<', self.budget_starting_date),
             ('project_id', '=', self.project_id.id)])
        if previous_budgets:
            for budget in previous_budgets:
                if self.signing_amount != budget.signing_amount:
                    raise UserError('Signing amount of previous budget is ' + str(budget.signing_amount))

    @api.onchange('retainer_fee')
    def onchange_signing_amount(self):
        for line in self.monthly_retainer_fee:
            line.amount = self.retainer_fee

    commission_generate_button = fields.Boolean()

    @api.onchange('commission_generate_button')
    def commission_generate_month(self):
        if self.retainer_month and self.forecast_month:
            self.monthly_retainer_fee = False
            self.sales_forecast_lines = False
            self.man_power_lines = False
            self.profit_loss_lines = False
            self.profit_loss_expense_lines = False
            self.cash_flow_lines = False
            self.walk_in_lines = False
            data = []
            forecast_data = []
            retainer_month = int(self.retainer_month)
            forecast_month = int(self.forecast_month)
            previous_budgets = self.env['budget.sheet'].search(
                [('budget_starting_date', '<', self.budget_starting_date),
                 ('project_id', '=', self.project_id.id)])
            monthly_retainer_total_len = len(previous_budgets.mapped('monthly_retainer_fee'))
            if self.forecast_date and self.budget_starting_date:
                date_from = self.forecast_date.strftime('%Y-%m-01')
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                budget_start = self.budget_starting_date.strftime('%Y-%m-01')
                budget_start = datetime.strptime(budget_start, '%Y-%m-%d')
                if budget_start.month < 4:
                    financial_end = str(budget_start.year) + '-03-31'
                else:
                    financial_end = str(budget_start.year + 1) + '-03-31'
                financial_end = datetime.strptime(financial_end, '%Y-%m-%d')
                if date_from:
                    loop_number = 1
                    for dt in rrule(freq=MONTHLY, count=(retainer_month + forecast_month), dtstart=date_from):
                        if budget_start <= dt <= financial_end:
                            if loop_number <= retainer_month and not self.is_not_first_budget:
                                if retainer_month > monthly_retainer_total_len:
                                    monthly_retainer_total_len += 1
                                    data.append((0, 0, {
                                        'month_year': dt.strftime('%B %Y'),
                                        'month': int(dt.month),
                                        'amount': self.retainer_fee,
                                        'line_identifier': loop_number
                                    }))
                            forecast_data.append((
                                (0, 0, {
                                    'month_year': dt.strftime('%B %Y'),
                                    'month': int(dt.month),
                                    'amount': 0,
                                    'line_identifier': loop_number
                                })
                            ))
                            loop_number += 1

                self.monthly_retainer_fee = data
                self.sales_forecast_lines = forecast_data
                others_data = []
                profit_loss_data = []
                walk_in_data = []
                for line in self.monthly_retainer_fee:
                    profit_loss_data.append((0, 0, {
                        'month_year': line.month_year,
                        'retainer_fee': line.amount,
                        'line_identifier': line.line_identifier,
                        'month': line.month
                    }))
                for line in self.sales_forecast_lines:
                    data_tuple = (0, 0, {
                        'month_year': line.month_year,
                        'line_identifier': line.line_identifier,
                        'month': line.month
                    })
                    others_data.append(data_tuple)
                    walk_in_data.append(data_tuple)
                    if line.line_identifier > len(self.monthly_retainer_fee):
                        profit_loss_data.append(data_tuple)

                self.man_power_lines = others_data
                self.profit_loss_lines = profit_loss_data
                self.profit_loss_expense_lines = others_data
                self.cash_flow_lines = others_data
                self.walk_in_lines = walk_in_data

    @api.onchange('monthly_retainer_fee')
    def change_profit_loss_retainer_fee(self):
        for line in self.monthly_retainer_fee:
            profit_loss_line = self.profit_loss_lines.filtered(lambda l: l.line_identifier == line.line_identifier)
            profit_loss_line.retainer_fee = line.amount
        self.compute_cash_flow_expense_lines()
        self.compute_productivity_ratio_lines()

    # Sales Forecast
    forecast_month = fields.Selection(no_of_months_domain, 'No. of Months (Forecast)')
    forecast_date = fields.Date('Starting Date')
    sales_forecast_lines = fields.One2many('budget.sheet.line', 'sales_forecast_budget_id')
    booking_h1 = fields.Float(compute="compute_forecast_totals")
    booking_h2 = fields.Float(compute="compute_forecast_totals")
    booking_fy = fields.Float(compute="compute_forecast_totals")
    registration_h1 = fields.Float(compute="compute_forecast_totals")
    registration_h2 = fields.Float(compute="compute_forecast_totals")
    registration_fy = fields.Float(compute="compute_forecast_totals")
    booking_ptd = fields.Float()
    registration_ptd = fields.Float()

    @api.depends('sales_forecast_lines')
    def compute_forecast_totals(self):
        h1_data = self.sales_forecast_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.sales_forecast_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.booking_h1 = sum(h1_data.mapped('booking'))
        self.booking_h2 = sum(h2_data.mapped('booking'))
        self.registration_h1 = sum(h1_data.mapped('registration'))
        self.registration_h2 = sum(h2_data.mapped('registration'))
        self.booking_fy = sum(h1_data.mapped('booking')) + sum(h2_data.mapped('booking'))
        self.registration_fy = sum(h1_data.mapped('registration')) + sum(h2_data.mapped('registration'))

    @api.onchange('sales_forecast_lines')
    def change_profit_loss_booking_registration(self):
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        reg_1 = conf.reg_month_1
        reg_2 = conf.reg_month_2
        reg_3 = conf.reg_month_3
        reg_4 = conf.reg_month_4
        previous_budgets = self.env['budget.sheet'].search(
            [('budget_starting_date', '<', self.budget_starting_date),
             ('project_id', '=', self.project_id.id)])
        full_sales_forecast_lines = self.sales_forecast_lines + previous_budgets.mapped('sales_forecast_lines')
        for line in self.sales_forecast_lines:
            # line_1 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 3).booking
            # line_2 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 2).booking
            # line_3 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 1).booking
            # line_4 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier).booking
            # if previous_budgets:
            line_date_4 = datetime.strptime('1 ' + line.month_year, '%d %B %Y')
            line_date_3 = (line_date_4 - timedelta(days=line_date_4.day)).replace(day=1)
            line_date_2 = (line_date_3 - timedelta(days=line_date_3.day)).replace(day=1)
            line_date_1 = (line_date_2 - timedelta(days=line_date_2.day)).replace(day=1)
            line_1 = full_sales_forecast_lines.filtered(
                lambda l: l.month_year == line_date_1.strftime('%B %Y')).booking
            line_2 = full_sales_forecast_lines.filtered(
                lambda l: l.month_year == line_date_2.strftime('%B %Y')).booking
            line_3 = full_sales_forecast_lines.filtered(
                lambda l: l.month_year == line_date_3.strftime('%B %Y')).booking
            line_4 = full_sales_forecast_lines.filtered(
                lambda l: l.month_year == line_date_4.strftime('%B %Y')).booking
            registration = (line_1 * reg_4 + line_2 * reg_3 + line_3 * reg_2 + line_4 * reg_1) / 100
            line.registration = float_round(registration, precision_digits=0)
            profit_loss_line = self.profit_loss_lines.filtered(lambda l: l.line_identifier == line.line_identifier)
            profit_loss_line.booking = line.booking
            profit_loss_line.registration = line.registration
            walk_in_line = self.walk_in_lines.filtered(lambda l: l.line_identifier == line.line_identifier)
            walk_in_line.booking = line.booking
        if sum(full_sales_forecast_lines.mapped('booking')) != sum(
                full_sales_forecast_lines.mapped('registration')) and len(
                full_sales_forecast_lines) == self.project_id.term_sheet_id.evaluation_sheet_id.sales_forecast_lines:  # Rounding value difference adjusting
            diff = sum(full_sales_forecast_lines.mapped('booking')) - sum(
                full_sales_forecast_lines.mapped('registration'))
            last_line = self.sales_forecast_lines.filtered(
                lambda l: l.line_identifier == len(self.sales_forecast_lines))
            last_profit_loss_line = self.profit_loss_lines.filtered(
                lambda l: l.line_identifier == len(self.sales_forecast_lines))
            adjusted_value = last_line.registration + diff
            if adjusted_value >= 0:
                last_line.registration = adjusted_value
                last_profit_loss_line.registration = adjusted_value
            else:
                last_line.registration = 0
                last_profit_loss_line.registration = 0
        self.compute_cash_flow_expense_lines()
        self.compute_productivity_ratio_lines()

    # Man Power Forecast
    man_power_lines = fields.One2many('budget.sheet.line', 'man_power_budget_id')
    tab_identifier = fields.Char(store=False)

    @api.onchange('tab_identifier')
    def copy_manpower_line(self):
        for line in self.man_power_lines:
            if str(line.line_identifier) == self.tab_identifier:
                next_line = self.man_power_lines.filtered(
                    lambda l: l.line_identifier == line.line_identifier + 1)
                next_line.update({
                    'site_head': line.site_head,
                    'cluster_head': line.cluster_head,
                    'sourcing': line.sourcing,
                    'closing': line.closing,
                    'crm': line.crm,
                    'others': line.others,
                })
                self.tab_identifier = 'copied'

    # Man Power Cost Per Individual
    site_head = fields.Float()
    cluster_head = fields.Float()
    sourcing = fields.Float()
    closing = fields.Float()
    crm = fields.Float('CRM')
    others = fields.Float('Others(MIS)')

    # Total Man Power Cost
    man_power_cost_lines = fields.One2many('budget.sheet.line', 'man_power_cost_budget_id',
                                           compute='compute_total_man_power_cost', store=True)

    @api.depends('man_power_lines', 'site_head', 'cluster_head', 'sourcing', 'closing', 'crm', 'others')
    def compute_total_man_power_cost(self):
        data = []
        self.man_power_cost_lines = False
        if self.man_power_lines:
            for line in self.man_power_lines:
                data.append((0, 0, {
                    'month_year': line.month_year,
                    'site_head': line.site_head * self.site_head,
                    'cluster_head': line.cluster_head * self.cluster_head,
                    'sourcing': line.sourcing * self.sourcing,
                    'closing': line.closing * self.closing,
                    'crm': line.crm * self.crm,
                    'others': line.others * self.others,
                    'line_identifier': line.line_identifier
                }))
        self.man_power_cost_lines = data
        self.compute_cash_flow_expense_lines()
        self.compute_productivity_ratio_lines()

    @api.onchange('man_power_cost_lines', 'man_power_lines', 'site_head', 'cluster_head', 'sourcing', 'closing', 'crm',
                  'others')
    def change_profit_loss_expense_man_power_cost(self):
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        for line in self.man_power_cost_lines:
            profit_loss_line = self.profit_loss_expense_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            profit_loss_line.manpower_cost = line.man_power_total
            man_power_line = self.man_power_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            profit_loss_line.admin_exp = man_power_line.man_power_total * conf.admin_expense

    # Profit & loss Statement
    profit_loss_lines = fields.One2many('budget.sheet.line', 'profit_loss_budget_id')
    sales_value_h1 = fields.Float(compute="compute_profit_loss_totals")
    sales_value_h2 = fields.Float(compute="compute_profit_loss_totals")
    sales_value_fy = fields.Float(compute="compute_profit_loss_totals")
    retainer_fee_h1 = fields.Float(compute="compute_profit_loss_totals")
    retainer_fee_h2 = fields.Float(compute="compute_profit_loss_totals")
    retainer_fee_fy = fields.Float(compute="compute_profit_loss_totals")
    billing_h1 = fields.Float(compute="compute_profit_loss_totals")
    billing_h2 = fields.Float(compute="compute_profit_loss_totals")
    billing_fy = fields.Float(compute="compute_profit_loss_totals")
    total_revenue_h1 = fields.Float(compute="compute_profit_loss_totals")
    total_revenue_h2 = fields.Float(compute="compute_profit_loss_totals")
    total_revenue_fy = fields.Float(compute="compute_profit_loss_totals")
    sales_value_ptd = fields.Float()
    retainer_fee_ptd = fields.Float()
    billing_ptd = fields.Float()
    total_revenue_ptd = fields.Float()

    balance = fields.Float()
    total_revenue = fields.Float(compute='compute_profit_loss_billing_revenue')

    @api.onchange('profit_loss_lines', 'net_justo_commission', 'signing_amount', 'monthly_retainer_fee')
    def compute_profit_loss_billing_revenue(self):
        previous_budgets = self.env['budget.sheet'].search(
            [('budget_starting_date', '<', self.budget_starting_date),
             ('project_id', '=', self.project_id.id)])
        for res in self:
            adjustment = res.signing_amount
            for budget in previous_budgets:
                for line in budget.profit_loss_lines:
                    billing_value = line.sales_value * budget.net_justo_commission / 100
                    billing = billing_value - (adjustment + line.retainer_fee)
                    adjustment = -billing if -billing > 0 else 0
            if self.is_not_first_budget:
                adjustment = 0
            self.balance = adjustment
            for rec in res.profit_loss_lines:
                rec.billing = 0
                billing_value = rec.sales_value * res.net_justo_commission / 100
                billing = billing_value - (adjustment + rec.retainer_fee)
                adjustment = -billing if -billing > 0 else 0
                rec.billing = billing if billing > 0 else 0
                rec.total_revenue = rec.billing + rec.retainer_fee
            if previous_budgets or self.is_not_first_budget:
                res.total_revenue = sum(res.profit_loss_lines.mapped('total_revenue'))
            else:
                res.total_revenue = sum(res.profit_loss_lines.mapped('total_revenue')) + res.signing_amount
            res.compute_profit_loss_totals()

    @api.depends('profit_loss_lines')
    def compute_profit_loss_totals(self):
        h1_data = self.profit_loss_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.profit_loss_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.sales_value_h1 = sum(h1_data.mapped('sales_value'))
        self.sales_value_h2 = sum(h2_data.mapped('sales_value'))
        self.sales_value_fy = sum(h1_data.mapped('sales_value')) + sum(h2_data.mapped('sales_value'))
        self.retainer_fee_h1 = sum(h1_data.mapped('retainer_fee'))
        self.retainer_fee_h2 = sum(h2_data.mapped('retainer_fee'))
        self.retainer_fee_fy = sum(h1_data.mapped('retainer_fee')) + sum(h2_data.mapped('retainer_fee'))
        self.billing_h1 = sum(h1_data.mapped('billing'))
        self.billing_h2 = sum(h2_data.mapped('billing'))
        self.billing_fy = sum(h1_data.mapped('billing')) + sum(h2_data.mapped('billing'))
        self.total_revenue_h1 = sum(h1_data.mapped('total_revenue'))
        self.total_revenue_h2 = sum(h2_data.mapped('total_revenue'))
        self.total_revenue_fy = sum(h1_data.mapped('total_revenue')) + sum(h2_data.mapped('total_revenue'))

    @api.onchange('profit_loss_lines', 'avg_sales_team_incentive', 'tentative_unit_sales_price',
                  'profit_loss_expense_lines')
    def change_profit_loss_expense_sales_incentive(self):
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        incentive_group = conf.sales_incentive_group_count + 1
        incentive = 0
        profit_loss_line = False
        self.profit_loss_expense_lines.update({'sales_incentive': 0})
        for line in self.profit_loss_lines:
            profit_loss_line = self.profit_loss_expense_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            incentive += line.sales_value * self.avg_sales_team_incentive / 100
            # profit_loss_line.sales_incentive = 0
            if incentive_group == 0:
                profit_loss_line.sales_incentive = incentive
            elif line.line_identifier == incentive_group:
                profit_loss_line.sales_incentive = incentive
                incentive = 0
                incentive_group += conf.sales_incentive_group_count + 1
            # if line.line_identifier == incentive_group:
            #     next_profit_loss_line = self.profit_loss_expense_lines.filtered(
            #         lambda l: l.line_identifier == line.line_identifier + 1)
            #     if next_profit_loss_line:
            #         next_profit_loss_line.sales_incentive = incentive
            #         incentive = 0
            #     incentive_group += conf.sales_incentive_group_count
            profit_loss_line.other_expenses = line.sales_value * (conf.other_exp_percentage / 100)
            profit_loss_line.revenue_expense_diff = line.total_revenue - profit_loss_line.total_expense
        if profit_loss_line and incentive > 0:
            profit_loss_line.sales_incentive = incentive
        self.compute_cash_flow_expense_lines()
        self.compute_productivity_ratio_lines()
        self.compute_profit_loss_expense_totals()

    @api.onchange('profit_loss_lines', 'commission_retention')
    def change_cash_flow_collection(self):
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        count = conf.collection_billing_count if conf.collection_billing_count > 0 else 1
        for line in self.profit_loss_lines:
            identifier_list = []
            cash_flow_line = self.cash_flow_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            for i in range(1, count + 1):
                identifier_list.append(line.line_identifier - i)
            # profit_loss_lines = self.profit_loss_lines.filtered(
            #     lambda l: l.line_identifier in (
            #         line.line_identifier - 1, line.line_identifier - 2, line.line_identifier - 3))
            profit_loss_lines = self.profit_loss_lines.filtered(lambda l: l.line_identifier in identifier_list)
            billing_sum = sum(profit_loss_lines.mapped('billing'))
            # cash_flow_line.collection = (1 / 3) * (1 - self.commission_retention) * billing_sum
            cash_flow_line.collection = (1 / count) * (1 - self.commission_retention) * billing_sum
            cash_flow_line.retainer_fee = line.retainer_fee
        self.compute_cash_flow_expense_lines()
        self.compute_productivity_ratio_lines()
        self.compute_cash_flow_totals()

    # Profit & loss Expenses
    profit_loss_expense_lines = fields.One2many('budget.sheet.line', 'profit_loss_expense_budget_id')
    admin_exp_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    admin_exp_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    admin_exp_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    manpower_cost_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    manpower_cost_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    manpower_cost_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    sales_incentive_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    sales_incentive_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    sales_incentive_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    other_expenses_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    other_expenses_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    other_expenses_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    total_expense_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    total_expense_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    total_expense_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    revenue_expense_diff_h1 = fields.Float(compute="compute_profit_loss_expense_totals")
    revenue_expense_diff_h2 = fields.Float(compute="compute_profit_loss_expense_totals")
    revenue_expense_diff_fy = fields.Float(compute="compute_profit_loss_expense_totals")
    admin_exp_ptd = fields.Float()
    manpower_cost_ptd = fields.Float()
    sales_incentive_ptd = fields.Float()
    other_expenses_ptd = fields.Float()
    total_expense_ptd = fields.Float()
    revenue_expense_diff_ptd = fields.Float()

    @api.depends('profit_loss_expense_lines')
    def compute_profit_loss_expense_totals(self):
        h1_data = self.profit_loss_expense_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.profit_loss_expense_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.admin_exp_h1 = sum(h1_data.mapped('admin_exp'))
        self.admin_exp_h2 = sum(h2_data.mapped('admin_exp'))
        self.admin_exp_fy = sum(h1_data.mapped('admin_exp')) + sum(h2_data.mapped('admin_exp'))
        self.manpower_cost_h1 = sum(h1_data.mapped('manpower_cost'))
        self.manpower_cost_h2 = sum(h2_data.mapped('manpower_cost'))
        self.manpower_cost_fy = sum(h1_data.mapped('manpower_cost')) + sum(h2_data.mapped('manpower_cost'))
        self.sales_incentive_h1 = sum(h1_data.mapped('sales_incentive'))
        self.sales_incentive_h2 = sum(h2_data.mapped('sales_incentive'))
        self.sales_incentive_fy = sum(h1_data.mapped('sales_incentive')) + sum(h2_data.mapped('sales_incentive'))
        self.other_expenses_h1 = sum(h1_data.mapped('other_expenses'))
        self.other_expenses_h2 = sum(h2_data.mapped('other_expenses'))
        self.other_expenses_fy = sum(h1_data.mapped('other_expenses')) + sum(h2_data.mapped('other_expenses'))
        self.total_expense_h1 = sum(h1_data.mapped('total_expense'))
        self.total_expense_h2 = sum(h2_data.mapped('total_expense'))
        self.total_expense_fy = sum(h1_data.mapped('total_expense')) + sum(h2_data.mapped('total_expense'))
        self.revenue_expense_diff_h1 = sum(h1_data.mapped('revenue_expense_diff'))
        self.revenue_expense_diff_h2 = sum(h2_data.mapped('revenue_expense_diff'))
        self.revenue_expense_diff_fy = sum(h1_data.mapped('revenue_expense_diff')) + sum(
            h2_data.mapped('revenue_expense_diff'))

    # Cash Flow Statement
    cash_flow_lines = fields.One2many('budget.sheet.line', 'cash_flow_budget_id')
    collection_h1 = fields.Float(compute="compute_cash_flow_totals")
    collection_h2 = fields.Float(compute="compute_cash_flow_totals")
    collection_fy = fields.Float(compute="compute_cash_flow_totals")
    gst_inflow_h1 = fields.Float(compute="compute_cash_flow_totals")
    gst_inflow_h2 = fields.Float(compute="compute_cash_flow_totals")
    gst_inflow_fy = fields.Float(compute="compute_cash_flow_totals")
    gross_inflow_h1 = fields.Float(compute="compute_cash_flow_totals")
    gross_inflow_h2 = fields.Float(compute="compute_cash_flow_totals")
    gross_inflow_fy = fields.Float(compute="compute_cash_flow_totals")
    collection_ptd = fields.Float()
    gst_inflow_ptd = fields.Float()
    gross_inflow_ptd = fields.Float()
    signing_gst_inflow = fields.Float(compute='compute_cash_flow_totals_signings')
    signing_gross_inflow = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_retainer_fee_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_collection_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_gst_inflow_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_gross_inflow_total = fields.Float(compute='compute_cash_flow_totals_signings')

    @api.depends('cash_flow_lines', 'signing_amount')
    def compute_cash_flow_totals_signings(self):
        for rec in self:
            previous_budgets = self.env['budget.sheet'].search(
                [('budget_starting_date', '<', self.budget_starting_date),
                 ('project_id', '=', self.project_id.id)])
            signing_amount = rec.signing_amount
            if previous_budgets or self.is_not_first_budget:
                signing_amount = 0
            rec.signing_gst_inflow = signing_amount * self.env.company.account_sale_tax_id.amount / 100
            rec.signing_gross_inflow = rec.signing_gst_inflow + signing_amount
            rec.cf_retainer_fee_total = sum(rec.cash_flow_lines.mapped('retainer_fee')) + signing_amount
            rec.cf_collection_total = sum(rec.cash_flow_lines.mapped('collection'))
            rec.cf_gst_inflow_total = sum(rec.cash_flow_lines.mapped('gst_inflow')) + rec.signing_gst_inflow
            rec.cf_gross_inflow_total = sum(rec.cash_flow_lines.mapped('gross_inflow')) + rec.signing_gross_inflow

    @api.depends('cash_flow_lines')
    def compute_cash_flow_totals(self):
        h1_data = self.cash_flow_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.cash_flow_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.collection_h1 = sum(h1_data.mapped('collection'))
        self.collection_h2 = sum(h2_data.mapped('collection'))
        self.collection_fy = sum(h1_data.mapped('collection')) + sum(h2_data.mapped('collection'))
        self.gst_inflow_h1 = sum(h1_data.mapped('gst_inflow'))
        self.gst_inflow_h2 = sum(h2_data.mapped('gst_inflow'))
        self.gst_inflow_fy = sum(h1_data.mapped('gst_inflow')) + sum(h2_data.mapped('gst_inflow'))
        self.gross_inflow_h1 = sum(h1_data.mapped('gross_inflow'))
        self.gross_inflow_h2 = sum(h2_data.mapped('gross_inflow'))
        self.gross_inflow_fy = sum(h1_data.mapped('gross_inflow')) + sum(h2_data.mapped('gross_inflow'))

    # Cash Flow Expenses
    cash_flow_expense_lines = fields.One2many('budget.sheet.line', 'cash_flow_expense_budget_id',
                                              compute='compute_cash_flow_expense_lines', store=True, compute_sudo=True)
    cf_admin_exp_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_admin_exp_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_admin_exp_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_manpower_cost_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_manpower_cost_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_manpower_cost_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_sales_incentive_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_sales_incentive_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_sales_incentive_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_other_expenses_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_other_expenses_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_other_expenses_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    gst_outflow_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    gst_outflow_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    gst_outflow_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    gross_outflow_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    gross_outflow_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    gross_outflow_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    in_outflow_diff_h1 = fields.Float(compute="compute_cash_flow_expense_totals")
    in_outflow_diff_h2 = fields.Float(compute="compute_cash_flow_expense_totals")
    in_outflow_diff_fy = fields.Float(compute="compute_cash_flow_expense_totals")
    cf_admin_exp_ptd = fields.Float()
    cf_manpower_cost_ptd = fields.Float()
    cf_sales_incentive_ptd = fields.Float()
    cf_other_expenses_ptd = fields.Float()
    gst_outflow_ptd = fields.Float()
    gross_outflow_ptd = fields.Float()
    in_outflow_diff_ptd = fields.Float()

    @api.depends('profit_loss_expense_lines', 'man_power_cost_lines', 'cash_flow_lines', 'monthly_retainer_fee')
    def compute_cash_flow_expense_lines(self):
        data = []
        man_power_cost = 0
        for line in self.cash_flow_lines:
            profit_loss_expense_line = self.profit_loss_expense_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            manpower_cost_line = self.man_power_cost_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            gross_outflow = profit_loss_expense_line.admin_exp + man_power_cost \
                            + profit_loss_expense_line.sales_incentive + profit_loss_expense_line.other_expenses \
                            + line.gst_inflow
            data.append((0, 0, {
                'month_year': line.month_year,
                'admin_exp': profit_loss_expense_line.admin_exp,
                'manpower_cost': man_power_cost,
                'sales_incentive': 0,
                'other_expenses': profit_loss_expense_line.other_expenses,
                'gst_outflow': line.gst_inflow,
                'gross_outflow': gross_outflow,
                'in_outflow_diff': line.gross_inflow - gross_outflow,
                'line_identifier': line.line_identifier,
                'month': line.month
            }))
            man_power_cost = manpower_cost_line.man_power_total
        if self.cash_flow_lines:
            budget_start = self.budget_starting_date.strftime('%Y-%m-01')
            budget_start = datetime.strptime(budget_start, '%Y-%m-%d').date()
            if budget_start.month < 4:
                financial_end = str(budget_start.year) + '-03-31'
            else:
                financial_end = str(budget_start.year + 1) + '-03-31'
            financial_end = datetime.strptime(financial_end, '%Y-%m-%d').date()
            extra_date = self.forecast_date + relativedelta(
                months=(int(self.retainer_month) + int(self.forecast_month)))
            # print(budget_start, extra_date, financial_end,budget_start <= extra_date <= financial_end,'fjfjfjfj')
            if budget_start <= extra_date <= financial_end:
                data.append((0, 0, {
                    'month_year': extra_date.strftime('%B %Y'),
                    'admin_exp': 0,
                    'manpower_cost': man_power_cost,
                    'sales_incentive': 0,
                    'other_expenses': 0,
                    'gst_outflow': 0,
                    'gross_outflow': 0,
                    'in_outflow_diff': 0,
                    'month': extra_date.month
                }))
        self.cash_flow_expense_lines = False
        self.cash_flow_expense_lines = data
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        incentive_group = conf.cf_sales_incentive_group_count
        incentive = 0
        line = False
        self.cash_flow_expense_lines.update({'sales_incentive': 0})
        for line in self.cash_flow_expense_lines:
            profit_loss_line = self.profit_loss_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            incentive += profit_loss_line.sales_value * self.avg_sales_team_incentive / 100
            if line.line_identifier == incentive_group:
                next_profit_loss_line = self.cash_flow_expense_lines.filtered(
                    lambda l: l.line_identifier == line.line_identifier + 1)
                if next_profit_loss_line:
                    next_profit_loss_line.sales_incentive = incentive
                    incentive = 0
                incentive_group += conf.cf_sales_incentive_group_count
        if line and incentive > 0:
            line.sales_incentive = incentive
        self.compute_productivity_ratio_lines()
        self.compute_cash_flow_expense_totals()

    @api.depends('cash_flow_expense_lines')
    def compute_cash_flow_expense_totals(self):
        h1_data = self.cash_flow_expense_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.cash_flow_expense_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.cf_admin_exp_h1 = sum(h1_data.mapped('admin_exp'))
        self.cf_admin_exp_h2 = sum(h2_data.mapped('admin_exp'))
        self.cf_admin_exp_fy = sum(h1_data.mapped('admin_exp')) + sum(h2_data.mapped('admin_exp'))
        self.cf_manpower_cost_h1 = sum(h1_data.mapped('manpower_cost'))
        self.cf_manpower_cost_h2 = sum(h2_data.mapped('manpower_cost'))
        self.cf_manpower_cost_fy = sum(h1_data.mapped('manpower_cost')) + sum(h2_data.mapped('manpower_cost'))
        self.cf_sales_incentive_h1 = sum(h1_data.mapped('sales_incentive'))
        self.cf_sales_incentive_h2 = sum(h2_data.mapped('sales_incentive'))
        self.cf_sales_incentive_fy = sum(h1_data.mapped('sales_incentive')) + sum(h2_data.mapped('sales_incentive'))
        self.cf_other_expenses_h1 = sum(h1_data.mapped('other_expenses'))
        self.cf_other_expenses_h2 = sum(h2_data.mapped('other_expenses'))
        self.cf_other_expenses_fy = sum(h1_data.mapped('other_expenses')) + sum(h2_data.mapped('other_expenses'))
        self.gst_outflow_h1 = sum(h1_data.mapped('gst_outflow'))
        self.gst_outflow_h2 = sum(h2_data.mapped('gst_outflow'))
        self.gst_outflow_fy = sum(h1_data.mapped('gst_outflow')) + sum(h2_data.mapped('gst_outflow'))
        self.gross_outflow_h1 = sum(h1_data.mapped('gross_outflow'))
        self.gross_outflow_h2 = sum(h2_data.mapped('gross_outflow'))
        self.gross_outflow_fy = sum(h1_data.mapped('gross_outflow')) + sum(h2_data.mapped('gross_outflow'))
        self.in_outflow_diff_h1 = sum(h1_data.mapped('in_outflow_diff'))
        self.in_outflow_diff_h2 = sum(h2_data.mapped('in_outflow_diff'))
        self.in_outflow_diff_fy = sum(h1_data.mapped('in_outflow_diff')) + sum(h2_data.mapped('in_outflow_diff'))

    # Walk In Projections
    walk_in_lines = fields.One2many('budget.sheet.line', 'walk_in_budget_id')

    # Productivity Ratio
    productivity_ratio_lines = fields.One2many('budget.sheet.line', 'productivity_ratio_budget_id',
                                               compute='compute_productivity_ratio_lines', store=True)
    total_expenses_pr_h1 = fields.Float(compute="compute_productivity_ratio_totals")
    total_expenses_pr_h2 = fields.Float(compute="compute_productivity_ratio_totals")
    total_expenses_pr_fy = fields.Float(compute="compute_productivity_ratio_totals")
    revenue_h1 = fields.Float(compute="compute_productivity_ratio_totals")
    revenue_h2 = fields.Float(compute="compute_productivity_ratio_totals")
    revenue_fy = fields.Float(compute="compute_productivity_ratio_totals")
    manpower_cost_pr_h1 = fields.Float(compute="compute_productivity_ratio_totals")
    manpower_cost_pr_h2 = fields.Float(compute="compute_productivity_ratio_totals")
    manpower_cost_pr_fy = fields.Float(compute="compute_productivity_ratio_totals")
    inflow_outflow_h1 = fields.Float(compute="compute_productivity_ratio_totals")
    inflow_outflow_h2 = fields.Float(compute="compute_productivity_ratio_totals")
    inflow_outflow_fy = fields.Float(compute="compute_productivity_ratio_totals")
    total_expenses_pr_ptd = fields.Float()
    revenue_ptd = fields.Float()
    manpower_cost_pr_ptd = fields.Float()
    inflow_outflow_ptd = fields.Float()

    @api.depends('profit_loss_lines', 'profit_loss_expense_lines', 'man_power_cost_lines', 'cash_flow_lines',
                 'cash_flow_expense_lines')
    def compute_productivity_ratio_lines(self):
        data = []
        self.productivity_ratio_lines = False
        for line in self.profit_loss_lines:
            profit_loss_expense_lines = self.profit_loss_expense_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            man_power_cost_lines = self.man_power_cost_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            cash_flow_lines = self.cash_flow_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            cash_flow_expense_lines = self.cash_flow_expense_lines.filtered(
                lambda l: l.line_identifier == line.line_identifier)
            revenue = line.total_revenue
            expense = profit_loss_expense_lines.total_expense
            manpower_cost = man_power_cost_lines.man_power_total
            gross_inflow = cash_flow_lines.gross_inflow
            gross_outflow = cash_flow_expense_lines.gross_outflow
            data.append((0, 0, {
                'month_year': line.month_year,
                'operating_margin_ratio': (revenue - expense) / revenue * 100 if revenue != 0 else 0,
                'total_expenses': (revenue - expense) / expense * 100 if expense != 0 else 0,
                'revenue': revenue / expense * 100 if expense != 0 else 0,
                'manpower_cost': revenue / manpower_cost * 100 if manpower_cost != 0 else 0,
                'inflow_outflow': gross_inflow / gross_outflow * 100 if gross_outflow != 0 else 0,
                'line_identifier': line.line_identifier,
                'month': line.month
            }))
        self.productivity_ratio_lines = False
        self.productivity_ratio_lines = data
        self.compute_productivity_ratio_totals()

    @api.depends('productivity_ratio_lines')
    def compute_productivity_ratio_totals(self):
        h1_data = self.productivity_ratio_lines.filtered(lambda l: 4 <= l.month <= 9)
        h2_data = self.productivity_ratio_lines.filtered(lambda l: l.month < 4 or l.month > 9)
        self.total_expenses_pr_h1 = sum(h1_data.mapped('total_expenses'))
        self.total_expenses_pr_h2 = sum(h2_data.mapped('total_expenses'))
        self.total_expenses_pr_fy = sum(h1_data.mapped('total_expenses')) + sum(h2_data.mapped('total_expenses'))
        self.revenue_h1 = sum(h1_data.mapped('revenue'))
        self.revenue_h2 = sum(h2_data.mapped('revenue'))
        self.revenue_fy = sum(h1_data.mapped('revenue')) + sum(h2_data.mapped('revenue'))
        self.manpower_cost_pr_h1 = sum(h1_data.mapped('manpower_cost'))
        self.manpower_cost_pr_h2 = sum(h2_data.mapped('manpower_cost'))
        self.manpower_cost_pr_fy = sum(h1_data.mapped('manpower_cost')) + sum(h2_data.mapped('manpower_cost'))
        self.inflow_outflow_h1 = sum(h1_data.mapped('inflow_outflow'))
        self.inflow_outflow_h2 = sum(h2_data.mapped('inflow_outflow'))
        self.inflow_outflow_fy = sum(h1_data.mapped('inflow_outflow')) + sum(h2_data.mapped('inflow_outflow'))

    # @api.depends('project_id')
    # def compute_ptd(self):
    #     self.booking_ptd = self.registration_ptd = 0
    #     self.sales_value_ptd = self.retainer_fee_ptd = self.billing_ptd = self.total_revenue_ptd = 0
    #     self.admin_exp_ptd = self.manpower_cost_ptd = self.sales_incentive_ptd = 0
    #     self.other_expenses_ptd = self.total_expense_ptd = self.revenue_expense_diff_ptd = 0
    #     self.collection_ptd = self.gst_inflow_ptd = self.gross_inflow_ptd = 0
    #     self.cf_admin_exp_ptd = self.cf_manpower_cost_ptd = self.cf_sales_incentive_ptd = self.cf_other_expenses_ptd = 0
    #     self.gst_outflow_ptd = self.gross_outflow_ptd = self.in_outflow_diff_ptd = 0
    #     self.total_expenses_pr_ptd = self.revenue_ptd = self.manpower_cost_pr_ptd = self.inflow_outflow_ptd = 0
    #     previous_budgets = self.env['budget.sheet'].search(
    #         [('budget_starting_date', '<', self.budget_starting_date), ('project_id', '=', self.project_id.id)])
    #     if previous_budgets:
    #         sales_forecast_lines = previous_budgets.mapped('sales_forecast_lines')
    #         self.booking_ptd = sum(sales_forecast_lines.mapped('booking'))
    #         self.registration_ptd = sum(sales_forecast_lines.mapped('registration'))
    #         profit_loss_lines = previous_budgets.mapped('profit_loss_lines')
    #         self.sales_value_ptd = sum(profit_loss_lines.mapped('sales_value'))
    #         self.retainer_fee_ptd = sum(profit_loss_lines.mapped('retainer_fee'))
    #         self.billing_ptd = sum(profit_loss_lines.mapped('billing'))
    #         self.total_revenue_ptd = sum(profit_loss_lines.mapped('total_revenue'))
    #         profit_loss_expense_lines = previous_budgets.mapped('profit_loss_expense_lines')
    #         self.admin_exp_ptd = sum(profit_loss_expense_lines.mapped('admin_exp'))
    #         self.manpower_cost_ptd = sum(profit_loss_expense_lines.mapped('manpower_cost'))
    #         self.sales_incentive_ptd = sum(profit_loss_expense_lines.mapped('sales_incentive'))
    #         self.other_expenses_ptd = sum(profit_loss_expense_lines.mapped('other_expenses'))
    #         self.total_expense_ptd = sum(profit_loss_expense_lines.mapped('total_expense'))
    #         self.revenue_expense_diff_ptd = sum(profit_loss_expense_lines.mapped('revenue_expense_diff'))
    #         cash_flow_lines = previous_budgets.mapped('cash_flow_lines')
    #         self.collection_ptd = sum(cash_flow_lines.mapped('collection'))
    #         self.gst_inflow_ptd = sum(cash_flow_lines.mapped('gst_inflow'))
    #         self.gross_inflow_ptd = sum(cash_flow_lines.mapped('gross_inflow'))
    #         cash_flow_expense_lines = previous_budgets.mapped('cash_flow_expense_lines')
    #         self.cf_admin_exp_ptd = sum(cash_flow_expense_lines.mapped('admin_exp'))
    #         self.cf_manpower_cost_ptd = sum(cash_flow_expense_lines.mapped('manpower_cost'))
    #         self.cf_sales_incentive_ptd = sum(cash_flow_expense_lines.mapped('sales_incentive'))
    #         self.cf_other_expenses_ptd = sum(cash_flow_expense_lines.mapped('other_expenses'))
    #         self.gst_outflow_ptd = sum(cash_flow_expense_lines.mapped('gst_outflow'))
    #         self.gross_outflow_ptd = sum(cash_flow_expense_lines.mapped('gross_outflow'))
    #         self.in_outflow_diff_ptd = sum(cash_flow_expense_lines.mapped('in_outflow_diff'))
    #         productivity_ratio_lines = previous_budgets.mapped('productivity_ratio_lines')
    #         self.total_expenses_pr_ptd = sum(productivity_ratio_lines.mapped('total_expenses'))
    #         self.revenue_ptd = sum(productivity_ratio_lines.mapped('revenue'))
    #         self.manpower_cost_pr_ptd = sum(productivity_ratio_lines.mapped('manpower_cost'))
    #         self.inflow_outflow_ptd = sum(productivity_ratio_lines.mapped('inflow_outflow'))


class BudgetSheetLine(models.Model):
    _name = 'budget.sheet.line'
    _description = 'Budgeting Lines'

    budget_id = fields.Many2one('budget.sheet')
    month = fields.Integer()
    amount = fields.Float()
    percentage = fields.Float()
    month_year = fields.Char("Month")
    registration = fields.Integer()
    line_identifier = fields.Integer()

    # Sales Forecast
    sales_forecast_budget_id = fields.Many2one('budget.sheet')
    booking = fields.Integer()
    booking_enable = fields.Boolean(compute="set_booking_enable")

    @api.depends('sales_forecast_budget_id.retainer_month', 'sales_forecast_budget_id.forecast_month')
    def set_booking_enable(self):
        for rec in self:
            rec.booking_enable = True
            retainer_month = rec.sales_forecast_budget_id.retainer_month
            forecast_month = rec.sales_forecast_budget_id.forecast_month
            evaluation_sheet = rec.sales_forecast_budget_id.project_id.term_sheet_id.evaluation_sheet_id
            if evaluation_sheet:
                booking_enabled_months_len = len(evaluation_sheet.sales_forecast_lines) - 3
                previous_budgets = self.env['budget.sheet'].search(
                    [('budget_starting_date', '<', rec.sales_forecast_budget_id.budget_starting_date),
                     ('project_id', '=', rec.sales_forecast_budget_id.project_id.id)])
                previous_budget_forecast_lines_len = len(previous_budgets.mapped('sales_forecast_lines'))
                line_identifier = rec.line_identifier + previous_budget_forecast_lines_len
                if retainer_month and forecast_month and line_identifier > booking_enabled_months_len:
                    rec.booking_enable = False
            else:
                if retainer_month and forecast_month and rec.line_identifier > int(retainer_month) + int(
                        forecast_month) - 3:
                    rec.booking_enable = False

    # Man Power Forecast
    man_power_budget_id = fields.Many2one('budget.sheet')
    site_head = fields.Float()
    cluster_head = fields.Float()
    sourcing = fields.Float()
    closing = fields.Float()
    crm = fields.Float('CRM')
    others = fields.Float('Others(MIS)')
    man_power_total = fields.Float('Total', compute='compute_man_power_line_total')

    @api.depends('site_head', 'cluster_head', 'sourcing', 'closing', 'crm', 'others')
    def compute_man_power_line_total(self):
        for rec in self:
            rec.man_power_total = rec.site_head + rec.cluster_head + rec.sourcing + rec.closing + rec.crm + rec.others

    man_power_cost_budget_id = fields.Many2one('budget.sheet')

    # Profit & Loss Statement
    profit_loss_budget_id = fields.Many2one('budget.sheet')
    avg_ticket_size = fields.Float('Average Ticket Size', compute='compute_sales_value_avg_ticket_size')
    sales_value = fields.Float(compute='compute_sales_value_avg_ticket_size')
    retainer_fee = fields.Float()
    billing = fields.Float('Billing (After 1st Disbursement)')
    total_revenue = fields.Float()
    monthly_retainer_line_id = fields.Many2one('budget.sheet.line')

    @api.depends('profit_loss_budget_id.tentative_unit_sales_price', 'registration')
    def compute_sales_value_avg_ticket_size(self):
        for rec in self:
            rec.avg_ticket_size = rec.profit_loss_budget_id.tentative_unit_sales_price
            rec.sales_value = rec.avg_ticket_size * rec.registration
        self.profit_loss_budget_id.compute_profit_loss_totals()

    # @api.depends('sales_value', 'profit_loss_budget_id.net_justo_commission', 'retainer_fee',
    #              'profit_loss_budget_id.signing_amount', 'profit_loss_budget_id.monthly_retainer_fee')
    # def compute_profit_loss_billing_revenue(self):
    #     for res in self:
    #         adjustment = res.profit_loss_budget_id.signing_amount
    #         for rec in res:
    #             rec.billing = 0
    #             billing_value = rec.sales_value * rec.profit_loss_budget_id.net_justo_commission / 100
    #             billing = billing_value - (adjustment + rec.retainer_fee)
    #             adjustment = -billing if -billing > 0 else 0
    #             rec.billing = billing if billing > 0 else 0
    #             rec.total_revenue = rec.billing + rec.retainer_fee
    #         res.profit_loss_budget_id.compute_profit_loss_totals()

    # Profit & Loss Expenses
    profit_loss_expense_budget_id = fields.Many2one('budget.sheet')
    admin_exp = fields.Float('Admin Exp.')
    sales_incentive = fields.Float()
    other_expenses = fields.Float()
    marketing_expenses = fields.Float()
    total_expense = fields.Float(compute='compute_total_expense')
    revenue_expense_diff = fields.Float('Net Profit/Loss')

    @api.depends('admin_exp', 'manpower_cost', 'sales_incentive', 'other_expenses', 'marketing_expenses')
    def compute_total_expense(self):
        for rec in self:
            rec.total_expense = rec.admin_exp + rec.manpower_cost + rec.sales_incentive + rec.other_expenses \
                                + rec.marketing_expenses
        self.profit_loss_expense_budget_id.compute_profit_loss_expense_totals()

    # Cash Flow Statement
    cash_flow_budget_id = fields.Many2one('budget.sheet')
    collection = fields.Float('Collection (After 1st Disbursement)')
    gst_inflow = fields.Float('GST Inflow', compute='compute_gst_gross_inflow')
    gross_inflow = fields.Float(compute='compute_gst_gross_inflow')

    @api.depends('retainer_fee', 'collection')
    def compute_gst_gross_inflow(self):
        for rec in self:
            rec.gst_inflow = (rec.retainer_fee + rec.collection) * self.env.company.account_sale_tax_id.amount / 100
            rec.gross_inflow = rec.gst_inflow + rec.collection + rec.retainer_fee
        self.cash_flow_budget_id.compute_cash_flow_totals()

    # Cash Flow Expenses
    cash_flow_expense_budget_id = fields.Many2one('budget.sheet')
    gst_outflow = fields.Float('GST Outflow')
    gross_outflow = fields.Float()
    in_outflow_diff = fields.Float('Net Gross Inflow')

    # Walk in Projections
    walk_in_budget_id = fields.Many2one('budget.sheet')
    walk_ins = fields.Float(compute='compute_walk_in_fields')
    cp_walk_ins = fields.Float(compute='compute_walk_in_fields')
    direct_walk_ins = fields.Float(compute='compute_walk_in_fields')
    digital_walk_ins = fields.Float(compute='compute_walk_in_fields')
    no_of_digital_leads = fields.Float('No. of Digital Leads', compute='compute_walk_in_fields')

    @api.depends('booking')
    def compute_walk_in_fields(self):
        for rec in self:
            rec.walk_ins = 0
            rec.cp_walk_ins = 0
            rec.direct_walk_ins = 0
            rec.digital_walk_ins = 0
            rec.no_of_digital_leads = 0
            conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
            if not conf:
                raise UserError('Walk in configurations not found')
            rec.walk_ins = rec.booking * 100 / conf.walk_ins
            rec.cp_walk_ins = rec.walk_ins * conf.cp_walk_ins / 100
            rec.direct_walk_ins = rec.walk_ins * conf.direct_walk_ins / 100
            rec.digital_walk_ins = rec.walk_ins * conf.digital_walk_ins / 100
            rec.no_of_digital_leads = conf.no_of_digital_leads * rec.walk_ins

    # Productivity Ratio
    productivity_ratio_budget_id = fields.Many2one('budget.sheet')
    operating_margin_ratio = fields.Float('Operating Margin Ratio(%)')
    total_expenses = fields.Float('Net Profit/Total Expenses(%)')
    revenue = fields.Float('Revenue/Total Expenses(%)')
    manpower_cost = fields.Float('Revenue/Manpower Cost(%)')
    inflow_outflow = fields.Float('Inflow/Outflow(%)')
