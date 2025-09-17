from odoo import models, fields, api


class BudgetSheet(models.Model):
    _inherit = 'budget.sheet'

    evaluation_sheet = fields.Char()

    @api.onchange('evaluation_sheet')
    def apply_evaluation_data(self):
        # INFORMATION ABOUT PROJECT
        evaluation_id = self.project_id.term_sheet_id.evaluation_sheet_id
        self.apartment_type_ids = evaluation_id.apartment_type_ids
        self.apartments_no_best = evaluation_id.apartments_no_best
        self.apartments_no_worst = evaluation_id.apartments_no_worst
        self.saleable_area = evaluation_id.saleable_area
        self.tentative_unit_sales_price = evaluation_id.tentative_unit_sales_price
        self.total_value = evaluation_id.total_value
        self.developer_id = evaluation_id.developer_id
        self.project_location = evaluation_id.project_location
        self.rera_number = evaluation_id.rera_number
        self.mandate_nature = evaluation_id.mandate_nature
        self.expected_timeline = evaluation_id.expected_timeline
        self.possession_date = evaluation_id.possession_date
        self.construction_stage = evaluation_id.construction_stage
        self.analytic_account_id = evaluation_id.analytic_account_id
        # Financial Status
        self.loan_details = evaluation_id.loan_details
        self.mortgage_partners = evaluation_id.mortgage_partners
        self.finance_partners = evaluation_id.finance_partners
        # Activities to be performed by Justo for Developer
        self.hiring = evaluation_id.hiring
        self.marketing_atl = evaluation_id.marketing_atl
        self.marketing_btl = evaluation_id.marketing_btl
        # Key Assumptions
        self.gross_justo_commission = evaluation_id.gross_justo_commission
        self.net_justo_commission = evaluation_id.net_justo_commission
        self.avg_sales_team_incentive = evaluation_id.avg_sales_team_incentive
        self.commission_retention = evaluation_id.commission_retention
        if self.evaluation_sheet == 'update_all_from_evaluation':
            # JUSTO's Commission Billing
            self.signing_amount = evaluation_id.signing_amount
            self.retainer_fee = evaluation_id.retainer_fee
            self.retainer_month = evaluation_id.retainer_month
            # Sales Forecast
            self.forecast_month = evaluation_id.forecast_month
            self.forecast_date = evaluation_id.forecast_date
            self.commission_generate_month()
            previous_budgets = self.env['budget.sheet'].search(
                [('budget_starting_date', '<', self.budget_starting_date),
                 ('project_id', '=', self.project_id.id)])
            for line in self.monthly_retainer_fee:
                line_identifier = line.line_identifier + len(previous_budgets.mapped('monthly_retainer_fee'))
                ev_line = evaluation_id.monthly_retainer_fee.filtered(lambda l: l.line_identifier == line_identifier)
                line.amount = ev_line.amount
            for line in self.sales_forecast_lines:
                line_identifier = line.line_identifier + len(previous_budgets.mapped('sales_forecast_lines'))
                ev_line = evaluation_id.sales_forecast_lines.filtered(lambda l: l.line_identifier == line_identifier)
                line.booking = ev_line.booking
            for line in self.man_power_lines:
                line_identifier = line.line_identifier + len(previous_budgets.mapped('man_power_lines'))
                ev_line = evaluation_id.man_power_lines.filtered(lambda l: l.line_identifier == line_identifier)
                line.site_head = ev_line.site_head
                line.cluster_head = ev_line.cluster_head
                line.sourcing = ev_line.sourcing
                line.closing = ev_line.closing
                line.crm = ev_line.crm
                line.others = ev_line.others
            self.site_head = evaluation_id.site_head
            self.cluster_head = evaluation_id.cluster_head
            self.sourcing = evaluation_id.sourcing
            self.closing = evaluation_id.closing
            self.crm = evaluation_id.crm
            self.others = evaluation_id.others
            for line in self.profit_loss_expense_lines:
                line_identifier = line.line_identifier + len(previous_budgets.mapped('profit_loss_expense_lines'))
                ev_line = evaluation_id.profit_loss_expense_lines.filtered(lambda l: l.line_identifier == line_identifier)
                line.admin_exp = ev_line.admin_exp
                line.marketing_expenses = ev_line.marketing_expenses

    @api.model
    def get_evaluation_id(self, project_id):
        project = self.env['building'].search([('id', '=', int(project_id))])
        return project.term_sheet_id.evaluation_sheet_id.id if project.term_sheet_id.evaluation_sheet_id else False
