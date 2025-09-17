# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from dateutil.rrule import rrule, MONTHLY
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_round

expected_timeline_years = [(str(key), str(key)) for key in range(1, 11)]
retainer_months_domain = [(str(key), str(key)) for key in range(1, 51)]
no_of_months_domain = [(str(key), str(key)) for key in range(1, 51)]


class EvaluationSheet(models.Model):
    _name = 'evaluation.sheet'
    _inherit = ['mail.thread']
    _description = 'Project Evaluation Sheet'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')
    form_editable = fields.Boolean(compute='compute_form_editable')

    @api.depends('state')
    def compute_form_editable(self):
        for rec in self:
            rec.form_editable = True
            if rec.state == 'confirmed' and not self.env.user.has_group(
                    'real_estate_sheets.group_evaluation_budgeting_confirm'):
                rec.form_editable = False

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    activate = fields.Boolean('Active', default=True)
    deactivating_reason = fields.Text()

    def action_export_form(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/evaluation/excel_export/%s' % self.env.context.get('active_id'),
            'target': 'self',
        }

    name = fields.Char('Name', default='New')

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('project.evaluation.sheet')
        return super(EvaluationSheet, self).create(values)

    developer_id = fields.Many2one('res.partner', 'Developer Name', domain=[('is_owner', '=', True)])
    developer_credentials = fields.Char('Credentials of Developer')
    project_location = fields.Char('Location of Project')
    location_grade = fields.Char()
    developer_source = fields.Many2one('developer.source', 'Source of Identifying Developer')
    rera_number = fields.Char('RERA No.')
    remarks = fields.Char()
    cc_status = fields.Char('Commencement Certificate (CC) Status')
    analysis_competition_source = fields.Char('Source of Analysis of Competition')
    project_name = fields.Char('Name of Project')
    no_of_wings = fields.Integer('No. of Wings/Tower')
    each_tower_storey = fields.Integer('Storey in Each Tower')
    apartment_type_ids = fields.Many2many('building.unit')
    apartments_no_best = fields.Integer('No. of Apartments (Best scenario)')
    apartments_no_worst = fields.Integer('No. of Apartments (Worst scenario)')
    saleable_area = fields.Float('Saleable Area in Sq. Ft')
    tentative_unit_sales_price = fields.Float('Tentative Unit Sales Price (Lakhs)')
    total_value = fields.Float('Total Value (Lakhs) - Best')
    total_value_worst = fields.Float('Total Value (Lakhs) - Worst')
    expected_timeline = fields.Selection(expected_timeline_years, 'Expected Timeline of Project')
    mandate_nature = fields.Char('Nature of Mandate')
    possession_date = fields.Date()
    construction_stage = fields.Many2one('construction.stage', 'Stage of Construction')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Cost Center')

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
    monthly_retainer_fee = fields.One2many('evaluation.sheet.line', 'evaluation_id')

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
            if self.forecast_date:
                date_from = self.forecast_date.strftime('%Y-%m-01')
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                if date_from:
                    loop_number = 1
                    for dt in rrule(freq=MONTHLY, count=(retainer_month + forecast_month), dtstart=date_from):
                        if loop_number <= retainer_month:
                            data.append((0, 0, {
                                'month_year': dt.strftime('%B %Y'),
                                'amount': self.retainer_fee,
                                'line_identifier': loop_number
                            }))
                        forecast_data.append((
                            (0, 0, {
                                'month_year': dt.strftime('%B %Y'),
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
                        'line_identifier': line.line_identifier
                    }))
                for line in self.sales_forecast_lines:
                    data_tuple = (0, 0, {
                        'month_year': line.month_year,
                        'line_identifier': line.line_identifier
                    })
                    others_data.append(data_tuple)
                    walk_in_data.append(data_tuple)
                    if line.line_identifier > int(self.retainer_month):
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
    sales_forecast_lines = fields.One2many('evaluation.sheet.line', 'sales_forecast_evaluation_id')

    @api.onchange('sales_forecast_lines')
    def change_profit_loss_booking_registration(self):
        conf = self.env['evaluation.configuration'].sudo().search([('activate', '=', True)], limit=1)
        reg_1 = conf.reg_month_1
        reg_2 = conf.reg_month_2
        reg_3 = conf.reg_month_3
        reg_4 = conf.reg_month_4
        for line in self.sales_forecast_lines:
            line_1 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 3).booking
            line_2 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 2).booking
            line_3 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier - 1).booking
            line_4 = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == line.line_identifier).booking
            registration = (line_1 * reg_4 + line_2 * reg_3 + line_3 * reg_2 + line_4 * reg_1) / 100
            line.registration = float_round(registration, precision_digits=0)
            profit_loss_line = self.profit_loss_lines.filtered(lambda l: l.line_identifier == line.line_identifier)
            profit_loss_line.booking = line.booking
            profit_loss_line.registration = line.registration
            walk_in_line = self.walk_in_lines.filtered(lambda l: l.line_identifier == line.line_identifier)
            walk_in_line.booking = line.booking
        if sum(self.sales_forecast_lines.mapped('booking')) != sum(self.sales_forecast_lines.mapped('registration')):  # Rounding value difference adjusting
            diff = sum(self.sales_forecast_lines.mapped('booking')) - sum(self.sales_forecast_lines.mapped('registration'))
            last_line = self.sales_forecast_lines.filtered(lambda l: l.line_identifier == len(self.sales_forecast_lines))
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
    man_power_lines = fields.One2many('evaluation.sheet.line', 'man_power_evaluation_id')
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
    man_power_cost_lines = fields.One2many('evaluation.sheet.line', 'man_power_cost_evaluation_id',
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
    profit_loss_lines = fields.One2many('evaluation.sheet.line', 'profit_loss_evaluation_id')
    total_revenue = fields.Float(compute='compute_total_revenue')

    @api.depends('signing_amount', 'profit_loss_lines')
    def compute_total_revenue(self):
        for rec in self:
            rec.total_revenue = sum(rec.profit_loss_lines.mapped('total_revenue')) + rec.signing_amount

    @api.onchange('profit_loss_lines', 'net_justo_commission', 'signing_amount', 'monthly_retainer_fee')
    def compute_profit_loss_billing_revenue(self):
        for res in self:
            adjustment = self.signing_amount
            for rec in res.profit_loss_lines:
                rec.billing = 0
                billing_value = rec.sales_value * res.net_justo_commission / 100
                billing = billing_value - (adjustment + rec.retainer_fee)
                adjustment = -billing if -billing > 0 else 0
                rec.billing = billing if billing > 0 else 0
                rec.total_revenue = rec.billing + rec.retainer_fee

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

    # Profit & loss Expenses
    profit_loss_expense_lines = fields.One2many('evaluation.sheet.line', 'profit_loss_expense_evaluation_id')

    # Cash Flow Statement
    cash_flow_lines = fields.One2many('evaluation.sheet.line', 'cash_flow_evaluation_id')
    signing_gst_inflow = fields.Float(compute='compute_cash_flow_totals_signings')
    signing_gross_inflow = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_retainer_fee_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_collection_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_gst_inflow_total = fields.Float(compute='compute_cash_flow_totals_signings')
    cf_gross_inflow_total = fields.Float(compute='compute_cash_flow_totals_signings')

    @api.depends('cash_flow_lines', 'signing_amount')
    def compute_cash_flow_totals_signings(self):
        for rec in self:
            rec.signing_gst_inflow = rec.signing_amount * self.env.company.account_sale_tax_id.amount / 100
            rec.signing_gross_inflow = rec.signing_gst_inflow + rec.signing_amount
            rec.cf_retainer_fee_total = sum(rec.cash_flow_lines.mapped('retainer_fee')) + rec.signing_amount
            rec.cf_collection_total = sum(rec.cash_flow_lines.mapped('collection'))
            rec.cf_gst_inflow_total = sum(rec.cash_flow_lines.mapped('gst_inflow')) + rec.signing_gst_inflow
            rec.cf_gross_inflow_total = sum(rec.cash_flow_lines.mapped('gross_inflow')) + rec.signing_gross_inflow

    # Cash Flow Expenses
    cash_flow_expense_lines = fields.One2many('evaluation.sheet.line', 'cash_flow_expense_evaluation_id',
                                              compute='compute_cash_flow_expense_lines', store=True)

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
                'line_identifier': line.line_identifier
            }))
            man_power_cost = manpower_cost_line.man_power_total
        if self.cash_flow_lines:
            extra_date = self.forecast_date + relativedelta(
                months=(int(self.retainer_month) + int(self.forecast_month)))
            data.append((0, 0, {
                'month_year': extra_date.strftime('%B %Y'),
                'admin_exp': 0,
                'manpower_cost': man_power_cost,
                'sales_incentive': 0,
                'other_expenses': 0,
                'gst_outflow': 0,
                'gross_outflow': 0,
                'in_outflow_diff': 0,
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

    # Walk In Projections
    walk_in_lines = fields.One2many('evaluation.sheet.line', 'walk_in_evaluation_id')

    # Productivity Ratio
    productivity_ratio_lines = fields.One2many('evaluation.sheet.line', 'productivity_ratio_evaluation_id',
                                               compute='compute_productivity_ratio_lines', store=True)

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
                'line_identifier': line.line_identifier
            }))
        self.productivity_ratio_lines = False
        self.productivity_ratio_lines = data

    # Cost sheet options
    cost_sheet_lines = fields.One2many('evaluation.sheet.line', 'cost_sheet_evaluation_id')
    cost_sheet_header = fields.Char(compute='compute_apartment_type_header_count')
    apartment_type_count = fields.Integer(compute='compute_apartment_type_header_count')

    @api.depends('apartment_type_ids')
    def compute_apartment_type_header_count(self):
        for rec in self:
            rec.apartment_type_count = len(rec.apartment_type_ids)
            rec.cost_sheet_header = '~'.join(self.apartment_type_ids.mapped('name'))

    @api.onchange('apartment_type_ids')
    def develop_cost_sheet_lines(self):
        if not self.cost_sheet_lines:
            labels = ['Saleable Area', 'Usable Carpet', 'Basic Amount', 'Dev Charge', 'AV', 'SC 7%', 'Registration',
                      'GST', 'Legal Charges', 'Total Cost', 'All in on Carpet', 'All in on Saleable', 'With Dev Charge']
            data = []
            i = 0
            for label in labels:
                i += 1
                data.append((0, 0, {
                    'labels': label,
                    'line_identifier': i  # be careful with this all calculations and fields attrs are based on this
                }))
            self.cost_sheet_lines = False
            self.cost_sheet_lines = data

    @api.onchange('cost_sheet_lines')
    def onchange_cost_sheet_lines(self):
        line_5 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 5)
        line_3_4 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier in (3, 4))
        line_5.cost_col_1 = sum(line_3_4.mapped('cost_col_1'))
        line_5.cost_col_2 = sum(line_3_4.mapped('cost_col_2'))
        line_5.cost_col_3 = sum(line_3_4.mapped('cost_col_3'))
        line_5.cost_col_4 = sum(line_3_4.mapped('cost_col_4'))
        line_5.cost_col_5 = sum(line_3_4.mapped('cost_col_5'))
        line_10 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 10)
        line_5_to_9 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier in (5, 6, 7, 8, 9))
        line_10.cost_col_1 = sum(line_5_to_9.mapped('cost_col_1'))
        line_10.cost_col_2 = sum(line_5_to_9.mapped('cost_col_2'))
        line_10.cost_col_3 = sum(line_5_to_9.mapped('cost_col_3'))
        line_10.cost_col_4 = sum(line_5_to_9.mapped('cost_col_4'))
        line_10.cost_col_5 = sum(line_5_to_9.mapped('cost_col_5'))
        line_11 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 11)
        line_2 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 2)
        line_11.cost_col_1 = line_10.cost_col_1 / line_2.cost_col_1 if line_2.cost_col_1 != 0 else 0
        line_11.cost_col_2 = line_10.cost_col_2 / line_2.cost_col_2 if line_2.cost_col_2 != 0 else 0
        line_11.cost_col_3 = line_10.cost_col_3 / line_2.cost_col_3 if line_2.cost_col_3 != 0 else 0
        line_11.cost_col_4 = line_10.cost_col_4 / line_2.cost_col_4 if line_2.cost_col_4 != 0 else 0
        line_11.cost_col_5 = line_10.cost_col_5 / line_2.cost_col_5 if line_2.cost_col_5 != 0 else 0
        line_12 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 12)
        line_1 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 1)
        line_12.cost_col_1 = line_10.cost_col_1 / line_1.cost_col_1 if line_1.cost_col_1 != 0 else 0
        line_12.cost_col_2 = line_10.cost_col_2 / line_1.cost_col_2 if line_1.cost_col_2 != 0 else 0
        line_12.cost_col_3 = line_10.cost_col_3 / line_1.cost_col_3 if line_1.cost_col_3 != 0 else 0
        line_12.cost_col_4 = line_10.cost_col_4 / line_1.cost_col_4 if line_1.cost_col_4 != 0 else 0
        line_12.cost_col_5 = line_10.cost_col_5 / line_1.cost_col_5 if line_1.cost_col_5 != 0 else 0
        line_13 = self.cost_sheet_lines.filtered(lambda l: l.line_identifier == 13)
        line_13.cost_col_1 = line_5.cost_col_1 / line_1.cost_col_1 if line_1.cost_col_1 != 0 else 0
        line_13.cost_col_2 = line_5.cost_col_2 / line_1.cost_col_2 if line_1.cost_col_2 != 0 else 0
        line_13.cost_col_3 = line_5.cost_col_3 / line_1.cost_col_3 if line_1.cost_col_3 != 0 else 0
        line_13.cost_col_4 = line_5.cost_col_4 / line_1.cost_col_4 if line_1.cost_col_4 != 0 else 0
        line_13.cost_col_5 = line_5.cost_col_5 / line_1.cost_col_5 if line_1.cost_col_5 != 0 else 0

class EvaluationSheetLine(models.Model):
    _name = 'evaluation.sheet.line'
    _description = 'Evaluation Sheet Lines'

    evaluation_id = fields.Many2one('evaluation.sheet')
    month = fields.Integer()
    amount = fields.Float()
    percentage = fields.Float()
    month_year = fields.Char("Month")
    registration = fields.Integer()
    line_identifier = fields.Integer()

    # Sales Forecast
    sales_forecast_evaluation_id = fields.Many2one('evaluation.sheet')
    booking = fields.Integer()
    booking_enable = fields.Boolean(compute="set_booking_enable")

    @api.depends('sales_forecast_evaluation_id.retainer_month', 'sales_forecast_evaluation_id.forecast_month')
    def set_booking_enable(self):
        for rec in self:
            rec.booking_enable = True
            retainer_month = rec.sales_forecast_evaluation_id.retainer_month
            forecast_month = rec.sales_forecast_evaluation_id.forecast_month
            if retainer_month and forecast_month and rec.line_identifier > int(retainer_month) + int(
                    forecast_month) - 3:
                rec.booking_enable = False

    # Man Power Forecast
    man_power_evaluation_id = fields.Many2one('evaluation.sheet')
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

    man_power_cost_evaluation_id = fields.Many2one('evaluation.sheet')

    # Profit & Loss Statement
    profit_loss_evaluation_id = fields.Many2one('evaluation.sheet')
    avg_ticket_size = fields.Float('Average Ticket Size', compute='compute_sales_value_avg_ticket_size')
    sales_value = fields.Float(compute='compute_sales_value_avg_ticket_size')
    retainer_fee = fields.Float()
    billing = fields.Float('Billing (After 1st Disbursement)')
    total_revenue = fields.Float()
    monthly_retainer_line_id = fields.Many2one('evaluation.sheet.line')

    @api.depends('profit_loss_evaluation_id.tentative_unit_sales_price', 'registration')
    def compute_sales_value_avg_ticket_size(self):
        for rec in self:
            rec.avg_ticket_size = rec.profit_loss_evaluation_id.tentative_unit_sales_price
            rec.sales_value = rec.avg_ticket_size * rec.registration

    # @api.depends('sales_value', 'profit_loss_evaluation_id.net_justo_commission', 'retainer_fee',
    #              'profit_loss_evaluation_id.signing_amount', 'profit_loss_evaluation_id.monthly_retainer_fee')
    # def compute_profit_loss_billing_revenue(self):
    #     adjustment = self.profit_loss_evaluation_id.signing_amount
    #     for rec in self:
    #         rec.billing = 0
    #         billing_value = rec.sales_value * rec.profit_loss_evaluation_id.net_justo_commission / 100
    #         billing = billing_value - (adjustment + rec.retainer_fee)
    #         adjustment = -billing if -billing > 0 else 0
    #         rec.billing = billing if billing > 0 else 0
    #         rec.total_revenue = rec.billing + rec.retainer_fee

    # Profit & Loss Expenses
    profit_loss_expense_evaluation_id = fields.Many2one('evaluation.sheet')
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

    # Cash Flow Statement
    cash_flow_evaluation_id = fields.Many2one('evaluation.sheet')
    collection = fields.Float('Collection (After 1st Disbursement)')
    gst_inflow = fields.Float('GST Inflow', compute='compute_gst_gross_inflow')
    gross_inflow = fields.Float(compute='compute_gst_gross_inflow')

    @api.depends('retainer_fee', 'collection')
    def compute_gst_gross_inflow(self):
        for rec in self:
            rec.gst_inflow = (rec.retainer_fee + rec.collection) * self.env.company.account_sale_tax_id.amount / 100
            rec.gross_inflow = rec.gst_inflow + rec.collection + rec.retainer_fee

    # Cash Flow Expenses
    cash_flow_expense_evaluation_id = fields.Many2one('evaluation.sheet')
    gst_outflow = fields.Float('GST Outflow')
    gross_outflow = fields.Float()
    in_outflow_diff = fields.Float('Net Gross Inflow')

    # Walk in Projections
    walk_in_evaluation_id = fields.Many2one('evaluation.sheet')
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
    productivity_ratio_evaluation_id = fields.Many2one('evaluation.sheet')
    operating_margin_ratio = fields.Float('Operating Margin Ratio(%)')
    total_expenses = fields.Float('Net Profit/Total Expenses(%)')
    revenue = fields.Float('Revenue/Total Expenses(%)')
    manpower_cost = fields.Float('Revenue/Manpower Cost(%)')
    inflow_outflow = fields.Float('Inflow/Outflow(%)')

    # Cost Sheet Options
    cost_sheet_evaluation_id = fields.Many2one('evaluation.sheet')
    labels = fields.Char('Type')
    cost_col_1 = fields.Float(' ')
    cost_col_2 = fields.Float(' ')
    cost_col_3 = fields.Float(' ')
    cost_col_4 = fields.Float(' ')
    cost_col_5 = fields.Float(' ')