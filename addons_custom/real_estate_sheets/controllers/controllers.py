import base64
import xlsxwriter
import io
from odoo import http
from odoo.http import content_disposition, request


class RealEstateSheetsController(http.Controller):

    @http.route(['/evaluation/excel_export/<model("evaluation.sheet"):evaluation>'], type='http', auth="user",
                csrf=False)
    def evaluation_export_excel(self, evaluation=None, **args):
        file_name = str(evaluation.name or 'Project Evaluation Sheet')
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition(file_name + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("evaluation")

        number_format = workbook.add_format({'num_format': '###0.00'})
        int_format = workbook.add_format({'num_format': '###0'})
        seperator_format = workbook.add_format({
            'bold': 1,
            'font_size': 12,
            'font_color': '#435ef0'
        })
        page_header_format = workbook.add_format({
            'bold': 1,
            'font_size': 13,
            'font_color': '#ffffff',
            'bg_color': '#004589',
            'align': 'center'
        })
        label_format = workbook.add_format({'bold': 1})
        name_format = workbook.add_format({
            'bold': 1,
            'font_size': 13,
            'valign': 'vcenter',
            'align': 'center'
        })
        table_label = workbook.add_format({
            'underline': 1,
            'bold': 1
        })
        table_header_left = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
        })
        table_header_right = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'align': 'right',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
        })
        table_footer_right = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'align': 'right',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
            'num_format': '###0.00',
        })
        table_border = workbook.add_format({
            'border': 1,
            'border_color': '#9f9f9f',
        })
        number_table_border = workbook.add_format({
            'border': 1,
            'num_format': '###0.00',
            'border_color': '#9f9f9f',
        })
        company = request.env.company
        image_data = io.BytesIO(base64.b64decode(company.logo))
        sheet.insert_image("B3", 'logo.png', {"image_data": image_data, 'x_scale': .15, 'y_scale': .15})

        header_data = [
            company.street, company.street2, company.city, company.state_id.name, company.country_id.name,
        ]
        header_data = [str(item) for item in header_data if item]

        sheet.merge_range('F2:P3', company.name, workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 15,
            'bold': 1,
            'font_color': '#2179d0',
        }))
        header_line1 = ', '.join(header_data) + ((' - ' + company.zip) if company.zip else '')

        sheet.merge_range('F4:P4', str(header_line1), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        header_line2 = (('Phone: ' + str(company.phone)) if company.phone else '') + ((
                    ' Email: ' + str(company.email)) if company.email else '')
        sheet.merge_range('F5:P5', str(header_line2), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        header_line3 = ('GSTIN: ' + str(company.vat)) if company.vat else ''
        sheet.merge_range('F6:P6', str(header_line3), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        sheet.merge_range('F8:P8', 'Project Evaluation Sheet', name_format)

        project_details = {
            'Number': evaluation.name or '',
            'Developer Name': evaluation.developer_id.name or '',
            'Credentials of Developer': evaluation.developer_credentials or '',
            'Location of Project': evaluation.project_location or '',
            'Location Grade': evaluation.location_grade or '',
            'Source of Identifying Developer': evaluation.developer_source.name or '',
            'Commencement Certificate (CC) Status': evaluation.cc_status or '',
            'RERA No.': evaluation.rera_number or '',
            'Remarks': evaluation.remarks or '',
            'Source of Analysis of Competition': evaluation.analysis_competition_source or '',
            'Name of Project': evaluation.project_name or '',
            'No. of Wings/Tower': evaluation.no_of_wings,
            'Storey in Each Tower': evaluation.each_tower_storey,
            'Apartment Type': str(evaluation.apartment_type_ids.mapped('name')).replace("'", '').replace('[', '').replace(']', ''),
            'No. of Apartments(Best scenario)': evaluation.apartments_no_best,
            'No. of Apartments(Worst scenario)': evaluation.apartments_no_worst,
            'Saleable Area in Sq. Ft': evaluation.saleable_area,
            'Tentative Unit Sales Price (Lakhs)': evaluation.tentative_unit_sales_price,
            'Total Value (Lakhs)': evaluation.total_value,
            'Expected Timeline of Project': (evaluation.expected_timeline + " Years") if evaluation.expected_timeline else '',
            'Possession': evaluation.possession_date.strftime('%d/%m/%Y') if evaluation.possession_date else '',
            'Nature of Mandate': evaluation.mandate_nature or '',
            'Stage of Construction': evaluation.construction_stage.name or '',
            'Cost Center': evaluation.analytic_account_id.name or '',
            ' ': '',
            'FINANCIAL STATUS': '~',
            'Loans, If Any': evaluation.loan_details or '',
            'Mortgage Partners': evaluation.mortgage_partners or '',
            'Finance Partners': evaluation.finance_partners or '',
            '  ': '',
            'ACTIVITIES TO BE PERFORMED BY JUSTO FOR DEVELOPER': '~',
            'Hiring': evaluation.hiring or '',
            'Marketing - ATL': evaluation.marketing_atl or '',
            'Marketing - BTL': evaluation.marketing_btl or '',
            '   ': '',
            'KEY ASSUMPTIONS': '~',
            "Gross JUSTO's Commission %": evaluation.gross_justo_commission,
            "Net JUSTO's Commission %" : evaluation.net_justo_commission,
            'Avg. Sales Team Incentive per Unit %': evaluation.avg_sales_team_incentive,
            'Commission Retention %': evaluation.commission_retention,
            '    ': '',
            "JUSTO'S COMMISSION BILLING": '~~~',
            'Signing Amount': evaluation.signing_amount,
            'Retainer Fee': evaluation.retainer_fee,
            'Retainer Month': int(evaluation.retainer_month) or '',
            'No. of Months (Forecast)': int(evaluation.forecast_month) or '',
            'Starting Date': evaluation.forecast_date.strftime('%d/%m/%Y') if evaluation.forecast_date else '',
        }
        # sheet.merge_range('A1:' + 'G2', evaluation.name or '', name_format)
        row = 10
        for item in project_details:
            if project_details[item] == '~':
                sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), item, seperator_format)
            elif project_details[item] == '~~~':
                sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), item, page_header_format)
            else:
                sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), item,label_format)
                if isinstance(project_details[item], float):
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), project_details[item], number_format)
                elif isinstance(project_details[item], int):
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), project_details[item], int_format)
                else:
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), str(project_details[item]))
            row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), str('Monthly Retainer Fee:'), table_label)
        row += 1

        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Month', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Amount', table_header_right)
        for line in evaluation.monthly_retainer_fee:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.amount, number_table_border)

        # SALES FORECAST PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'J' + str(row), 'SALES FORECAST', page_header_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Registration', table_header_right)
        for line in evaluation.sales_forecast_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.registration, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(evaluation.sales_forecast_lines.mapped('booking')),
                          table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(evaluation.sales_forecast_lines.mapped('registration')), table_footer_right)

        # MAN POWER PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Y' + str(row), 'MAN POWER', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'MAN POWER FORECAST', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Site Head', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Cluster Head', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sourcing', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Closing', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'CRM', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Others(MIS)', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Total', table_header_right)
        for line in evaluation.man_power_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.site_head, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.cluster_head, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sourcing, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.closing, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.crm, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.others, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.man_power_total, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(evaluation.man_power_lines.mapped('site_head')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(evaluation.man_power_lines.mapped('cluster_head')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(evaluation.man_power_lines.mapped('sourcing')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(evaluation.man_power_lines.mapped('closing')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(evaluation.man_power_lines.mapped('crm')), table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(evaluation.man_power_lines.mapped('others')), table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), sum(evaluation.man_power_lines.mapped('man_power_total')), table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'MAN POWER COST PER INDIVIDUAL', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Man Power Cost', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Unit Cost in Rs. Lakhs Per Month', table_header_right)
        man_power_data = {
            'Site Head': evaluation.site_head,
            'Cluster Head': evaluation.cluster_head,
            'Sourcing': evaluation.sourcing,
            'Closing': evaluation.closing,
            'CRM': evaluation.crm,
            'Others': evaluation.others
        }
        for line in man_power_data:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line, table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), man_power_data[line], number_table_border)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'TOTAL MAN POWER COST', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Site Head', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Cluster Head', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sourcing', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Closing', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'CRM', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Others(MIS)', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Total', table_header_right)
        for line in evaluation.man_power_cost_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.site_head, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.cluster_head, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sourcing, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.closing, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.crm, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.others, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.man_power_total, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(evaluation.man_power_cost_lines.mapped('site_head')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(evaluation.man_power_cost_lines.mapped('cluster_head')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(evaluation.man_power_cost_lines.mapped('sourcing')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(evaluation.man_power_cost_lines.mapped('closing')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(evaluation.man_power_cost_lines.mapped('crm')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(evaluation.man_power_cost_lines.mapped('others')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(evaluation.man_power_cost_lines.mapped('man_power_total')), table_footer_right)

        # PROFIT & LOSS STATEMENT PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Z' + str(row), 'PROFIT & LOSS STATEMENT', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'INCOME', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Signing Amount', label_format)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), evaluation.signing_amount, number_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Registration', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Average Ticket Size', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Sales Value', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Retainer Fee', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), 'Billing (After 1st Disbursement)', table_header_right)
        sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row), 'Total Revenue', table_header_right)
        for line in evaluation.profit_loss_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.registration, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.avg_ticket_size, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.sales_value, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.retainer_fee, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), line.billing, number_table_border)
            sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row), line.total_revenue , number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(evaluation.profit_loss_lines.mapped('booking')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(evaluation.profit_loss_lines.mapped('registration')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(evaluation.profit_loss_lines.mapped('avg_ticket_size')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(evaluation.profit_loss_lines.mapped('sales_value')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(evaluation.profit_loss_lines.mapped('retainer_fee')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), sum(evaluation.profit_loss_lines.mapped('billing')),
                          table_footer_right)
        sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row),
                          sum(evaluation.profit_loss_lines.mapped('total_revenue')), table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'EXPENSES', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Admin Exp.', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Manpower Cost', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sales Incentive', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Other Expenses', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Marketing Expenses', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Total Expenses', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Net Profit/Loss', table_header_right)
        for line in evaluation.profit_loss_expense_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.admin_exp, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sales_incentive, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.other_expenses, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.marketing_expenses, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.total_expense, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.revenue_expense_diff, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('admin_exp')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('manpower_cost')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('sales_incentive')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('other_expenses')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('marketing_expenses')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(evaluation.profit_loss_expense_lines.mapped('total_expense')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(evaluation.profit_loss_expense_lines.mapped('revenue_expense_diff')), table_footer_right)

        # CASH FLOW STATEMENT PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Y' + str(row), 'CASH FLOW STATEMENT', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'INFLOW', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Signing Amount', label_format)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), evaluation.signing_amount, number_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Retainer Fee', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), 'Collection (After 1st Disbursement)', table_header_right)
        sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), 'GST Inflow', table_header_right)
        sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), 'Gross Inflow', table_header_right)
        for line in evaluation.cash_flow_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.retainer_fee, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), line.collection, number_table_border)
            sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), line.gst_inflow, number_table_border)
            sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), line.gross_inflow, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(evaluation.cash_flow_lines.mapped('retainer_fee')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), sum(evaluation.cash_flow_lines.mapped('collection')),
                          table_footer_right)
        sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), sum(evaluation.cash_flow_lines.mapped('gst_inflow')),
                          table_footer_right)
        sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), sum(evaluation.cash_flow_lines.mapped('gross_inflow')),
                          table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'OUTFLOW', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Admin Exp.', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Manpower Cost', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sales Incentive', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Other Expenses', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'GST Outflow', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Gross Outflow', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Net Gross Inflow', table_header_right)
        for line in evaluation.cash_flow_expense_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.admin_exp, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sales_incentive, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.other_expenses, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.gst_outflow, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.gross_outflow, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.in_outflow_diff, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('admin_exp')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('manpower_cost')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('sales_incentive')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('other_expenses')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('gst_outflow')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(evaluation.cash_flow_expense_lines.mapped('gross_outflow')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(evaluation.cash_flow_expense_lines.mapped('in_outflow_diff')), table_footer_right)

        # WALK IN PROJECTIONS PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'V' + str(row), 'WALK IN PROJECTIONS', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'LEAD DETAILS', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Walk Ins', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'CP Walk Ins', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Direct Walk Ins', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Digital Walk Ins', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'No. of Digital Leads', table_header_right)
        for line in evaluation.walk_in_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.walk_ins, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.cp_walk_ins, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.direct_walk_ins, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.digital_walk_ins, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.no_of_digital_leads, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(evaluation.walk_in_lines.mapped('booking')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(evaluation.walk_in_lines.mapped('walk_ins')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(evaluation.walk_in_lines.mapped('cp_walk_ins')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(evaluation.walk_in_lines.mapped('direct_walk_ins')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(evaluation.walk_in_lines.mapped('digital_walk_ins')), table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(evaluation.walk_in_lines.mapped('no_of_digital_leads')), table_footer_right)

        # PRODUCTIVITY RATIO PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'S' + str(row), 'PRODUCTIVITY RATIO', page_header_format)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Operating Margin Ratio', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Net Profit/Total Expenses', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Revenue Total Expenses', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Revenue Manpower Cost', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Inflow/Outflow', table_header_right)
        for line in evaluation.productivity_ratio_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.operating_margin_ratio, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.total_expenses, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.revenue, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.inflow_outflow, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(evaluation.productivity_ratio_lines.mapped('operating_margin_ratio')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(evaluation.productivity_ratio_lines.mapped('total_expenses')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(evaluation.productivity_ratio_lines.mapped('revenue')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(evaluation.productivity_ratio_lines.mapped('manpower_cost')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(evaluation.productivity_ratio_lines.mapped('inflow_outflow')), table_footer_right)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response

    @http.route(['/budgeting/excel_export/<model("budget.sheet"):budget>'], type='http', auth="user",
                csrf=False)
    def budget_export_excel(self, budget=None, **args):
        file_name = str(budget.name or 'Budgeting')
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition(file_name + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("budget")

        number_format = workbook.add_format({'num_format': '###0.00'})
        int_format = workbook.add_format({'num_format': '###0'})
        seperator_format = workbook.add_format({
            'bold': 1,
            'font_size': 12,
            'font_color': '#435ef0'
        })
        page_header_format = workbook.add_format({
            'bold': 1,
            'font_size': 13,
            'font_color': '#ffffff',
            'bg_color': '#004589',
            'align': 'center'
        })
        label_format = workbook.add_format({'bold': 1})
        name_format = workbook.add_format({
            'bold': 1,
            'font_size': 13,
            'valign': 'vcenter',
            'align': 'center'
        })
        table_label = workbook.add_format({
            'underline': 1,
            'bold': 1
        })
        table_header_left = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
        })
        table_header_right = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'align': 'right',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
        })
        table_footer_right = workbook.add_format({
            'bold': 1,
            'bg_color': '#eeeeee',
            'align': 'right',
            'border': 1,
            'border_color': '#9f9f9f',
            'font_size': 12,
            'num_format': '###0.00',
        })
        table_border = workbook.add_format({
            'border': 1,
            'border_color': '#9f9f9f',
        })
        number_table_border = workbook.add_format({
            'border': 1,
            'num_format': '###0.00',
            'border_color': '#9f9f9f',
        })
        company = request.env.company
        image_data = io.BytesIO(base64.b64decode(company.logo))
        sheet.insert_image("B3", 'logo.png', {"image_data": image_data, 'x_scale': .15, 'y_scale': .15})

        header_data = [
            company.street, company.street2, company.city, company.state_id.name, company.country_id.name,
        ]
        header_data = [str(item) for item in header_data if item]

        sheet.merge_range('F2:P3', company.name, workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 15,
            'bold': 1,
            'font_color': '#2179d0',
        }))
        header_line1 = ', '.join(header_data) + ((' - ' + company.zip) if company.zip else '')

        sheet.merge_range('F4:P4', str(header_line1), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        header_line2 = (('Phone: ' + str(company.phone)) if company.phone else '') + ((
                    ' Email: ' + str(company.email)) if company.email else '')
        sheet.merge_range('F5:P5', str(header_line2), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        header_line3 = ('GSTIN: ' + str(company.vat)) if company.vat else ''
        sheet.merge_range('F6:P6', str(header_line3), workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 12,
            'bold': 1,
        }))

        sheet.merge_range('F8:P8', 'Budgeting', name_format)

        project_details = {
            'Number': budget.name or '',
            'Budget Starting Date': budget.budget_starting_date.strftime('%d/%m/%Y') if budget.budget_starting_date else '',
            ' ': '',
            'INFORMATION ABOUT PROJECT': '~',
            'Name of Project': budget.project_id.name or '',
            'Project Details': str(budget.apartment_type_ids.mapped('name')).replace("'", '').replace('[', '').replace(
                ']', ''),
            'No. of Apartments(Best scenario)': budget.apartments_no_best,
            'No. of Apartments(Worst scenario)': budget.apartments_no_worst,
            'Saleable Area in Sq. Ft': budget.saleable_area,
            'Tentative Unit Sales Price (Lakhs)': budget.tentative_unit_sales_price,
            'Total Value (Lakhs)': budget.total_value,
            'Developer Name': budget.developer_id.name or '',
            'Location': budget.project_location or '',
            'RERA No.': budget.rera_number or '',
            'Status of Project': budget.project_status or '',
            'Nature of Mandate': budget.mandate_nature or '',
            'Expected Timeline of Project': (budget.expected_timeline + " Years") if budget.expected_timeline else '',
            'Possession Date': budget.possession_date.strftime('%d/%m/%Y') if budget.possession_date else '',
            'Stage of Construction': budget.construction_stage.name or '',
            'Cost Center': budget.analytic_account_id.name or '',
            '  ': '',
            'FINANCIAL STATUS': '~',
            'Loans, If Any': budget.loan_details or '',
            'Mortgage Partners': budget.mortgage_partners or '',
            'Finance Partners': budget.finance_partners or '',
            '   ': '',
            'ACTIVITIES TO BE PERFORMED BY JUSTO FOR DEVELOPER': '~',
            'Hiring': budget.hiring or '',
            'Marketing - ATL': budget.marketing_atl or '',
            'Marketing - BTL': budget.marketing_btl or '',
            '    ': '',
            'KEY ASSUMPTIONS': '~',
            "Gross JUSTO's Commission %": budget.gross_justo_commission,
            "Net JUSTO's Commission %" : budget.net_justo_commission,
            'Avg. Sales Team Incentive per Unit %': budget.avg_sales_team_incentive,
            'Commission Retention %': budget.commission_retention,
            '     ': '',
            "JUSTO'S COMMISSION BILLING": '~~~',
            'Signing Amount': budget.signing_amount,
            'Retainer Fee': budget.retainer_fee,
            'Retainer Month': int(budget.retainer_month) or '',
            'No. of Months (Forecast)': int(budget.forecast_month) or '',
            'Starting Date': budget.forecast_date.strftime('%d/%m/%Y') if budget.forecast_date else '',
        }

        row = 10
        for item in project_details:
            if project_details[item] == '~':
                sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), item, seperator_format)
            elif project_details[item] == '~~~':
                sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), item, page_header_format)
            else:
                sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), item,label_format)
                if isinstance(project_details[item], float):
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), project_details[item], number_format)
                elif isinstance(project_details[item], int):
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), project_details[item], int_format)
                else:
                    sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), str(project_details[item]))
            row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), str('Monthly Retainer Fee:'), table_label)
        row += 1

        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Month', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Amount', table_header_right)
        for line in budget.monthly_retainer_fee:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.amount, number_table_border)

        # SALES FORECAST PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'J' + str(row), 'SALES FORECAST', page_header_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Registration', table_header_right)
        for line in budget.sales_forecast_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.registration, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(budget.sales_forecast_lines.mapped('booking')),
                          table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(budget.sales_forecast_lines.mapped('registration')), table_footer_right)

        forecast_totals = [
            ['H1', budget.booking_h1, budget.registration_h1],
            ['H2', budget.booking_h2, budget.registration_h2],
            ['FY', budget.booking_fy, budget.registration_fy],
            ['PTD', budget.booking_ptd, budget.registration_ptd]
        ]
        for line in forecast_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line[2], table_footer_right)

        # MAN POWER PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Y' + str(row), 'MAN POWER', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'MAN POWER FORECAST', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Site Head', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Cluster Head', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sourcing', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Closing', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'CRM', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Others(MIS)', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Total', table_header_right)
        for line in budget.man_power_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.site_head, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.cluster_head, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sourcing, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.closing, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.crm, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.others, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.man_power_total, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(budget.man_power_lines.mapped('site_head')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(budget.man_power_lines.mapped('cluster_head')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(budget.man_power_lines.mapped('sourcing')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(budget.man_power_lines.mapped('closing')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(budget.man_power_lines.mapped('crm')), table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(budget.man_power_lines.mapped('others')), table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), sum(budget.man_power_lines.mapped('man_power_total')), table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'MAN POWER COST PER INDIVIDUAL', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Man Power Cost', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Unit Cost in Rs. Lakhs Per Month', table_header_right)
        man_power_data = {
            'Site Head': budget.site_head,
            'Cluster Head': budget.cluster_head,
            'Sourcing': budget.sourcing,
            'Closing': budget.closing,
            'CRM': budget.crm,
            'Others': budget.others
        }
        for line in man_power_data:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line, table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), man_power_data[line], number_table_border)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'TOTAL MAN POWER COST', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Site Head', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Cluster Head', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sourcing', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Closing', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'CRM', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Others(MIS)', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Total', table_header_right)
        for line in budget.man_power_cost_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.site_head, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.cluster_head, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sourcing, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.closing, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.crm, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.others, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.man_power_total, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(budget.man_power_cost_lines.mapped('site_head')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(budget.man_power_cost_lines.mapped('cluster_head')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(budget.man_power_cost_lines.mapped('sourcing')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(budget.man_power_cost_lines.mapped('closing')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(budget.man_power_cost_lines.mapped('crm')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(budget.man_power_cost_lines.mapped('others')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(budget.man_power_cost_lines.mapped('man_power_total')), table_footer_right)

        # PROFIT & LOSS STATEMENT PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Z' + str(row), 'PROFIT & LOSS STATEMENT', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'INCOME', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Signing Amount', label_format)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), budget.signing_amount, number_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Registration', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Average Ticket Size', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Sales Value', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Retainer Fee', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), 'Billing (After 1st Disbursement)', table_header_right)
        sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row), 'Total Revenue', table_header_right)
        for line in budget.profit_loss_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.registration, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.avg_ticket_size, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.sales_value, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.retainer_fee, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), line.billing, number_table_border)
            sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row), line.total_revenue , number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(budget.profit_loss_lines.mapped('booking')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(budget.profit_loss_lines.mapped('registration')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(budget.profit_loss_lines.mapped('avg_ticket_size')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(budget.profit_loss_lines.mapped('sales_value')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(budget.profit_loss_lines.mapped('retainer_fee')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), sum(budget.profit_loss_lines.mapped('billing')),
                          table_footer_right)
        sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row),
                          sum(budget.profit_loss_lines.mapped('total_revenue')), table_footer_right)

        profit_loss_totals = [
            ['H1', budget.booking_h1, budget.registration_h1, '', budget.sales_value_h1, budget.retainer_fee_h1,
             budget.billing_h1, budget.total_revenue_h1],
            ['H2', budget.booking_h2, budget.registration_h2, '', budget.sales_value_h2, budget.retainer_fee_h2,
             budget.billing_h2, budget.total_revenue_h2],
            ['FY', budget.booking_fy, budget.registration_fy, '', budget.sales_value_fy, budget.retainer_fee_fy,
             budget.billing_fy, budget.total_revenue_fy],
            ['PTD', budget.booking_ptd, budget.registration_ptd, '', budget.sales_value_ptd,
             budget.retainer_fee_ptd, budget.billing_ptd, budget.total_revenue_ptd],
        ]
        for line in profit_loss_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line[2], table_footer_right)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line[3], table_footer_right)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line[4], table_footer_right)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line[5], table_footer_right)
            sheet.merge_range('T' + str(row) + ':' + 'W' + str(row), line[6], table_footer_right)
            sheet.merge_range('X' + str(row) + ':' + 'Z' + str(row), line[7], table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'EXPENSES', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Admin Exp.', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Manpower Cost', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sales Incentive', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Other Expenses', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Marketing Expenses', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Total Expenses', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Net Profit/Loss', table_header_right)
        for line in budget.profit_loss_expense_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.admin_exp, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sales_incentive, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.other_expenses, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.marketing_expenses, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.total_expense, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.revenue_expense_diff, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('admin_exp')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('manpower_cost')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('sales_incentive')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('other_expenses')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('marketing_expenses')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(budget.profit_loss_expense_lines.mapped('total_expense')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(budget.profit_loss_expense_lines.mapped('revenue_expense_diff')), table_footer_right)

        profit_loss_expense_totals = [
            ['H1', budget.admin_exp_h1, budget.manpower_cost_h1, budget.sales_incentive_h1,
             budget.other_expenses_h1, '', budget.total_expense_h1, budget.revenue_expense_diff_h1],
            ['H2', budget.admin_exp_h2, budget.manpower_cost_h2, budget.sales_incentive_h2,
             budget.other_expenses_h2, '', budget.total_expense_h2, budget.revenue_expense_diff_h2],
            ['FY', budget.admin_exp_fy, budget.manpower_cost_fy, budget.sales_incentive_fy,
             budget.other_expenses_fy, '', budget.total_expense_fy, budget.revenue_expense_diff_fy],
            ['PTD', budget.admin_exp_ptd, budget.manpower_cost_ptd, budget.sales_incentive_ptd,
             budget.other_expenses_ptd, '', budget.total_expense_ptd, budget.revenue_expense_diff_ptd],
        ]
        for line in profit_loss_expense_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line[2], table_footer_right)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line[3], table_footer_right)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line[4], table_footer_right)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line[5], table_footer_right)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line[6], table_footer_right)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line[7], table_footer_right)

        # CASH FLOW STATEMENT PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'Y' + str(row), 'CASH FLOW STATEMENT', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'INFLOW', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Signing Amount', label_format)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), budget.signing_amount, number_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Retainer Fee', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), 'Collection (After 1st Disbursement)', table_header_right)
        sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), 'GST Inflow', table_header_right)
        sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), 'Gross Inflow', table_header_right)
        for line in budget.cash_flow_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.retainer_fee, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), line.collection, number_table_border)
            sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), line.gst_inflow, number_table_border)
            sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), line.gross_inflow, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(budget.cash_flow_lines.mapped('retainer_fee')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), sum(budget.cash_flow_lines.mapped('collection')),
                          table_footer_right)
        sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), sum(budget.cash_flow_lines.mapped('gst_inflow')),
                          table_footer_right)
        sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), sum(budget.cash_flow_lines.mapped('gross_inflow')),
                          table_footer_right)

        cash_flow_totals = [
            ['H1', budget.retainer_fee_h1, budget.collection_h1, budget.gst_inflow_h1, budget.gross_inflow_h1],
            ['H2', budget.retainer_fee_h2, budget.collection_h2, budget.gst_inflow_h2, budget.gross_inflow_h2],
            ['FY', budget.retainer_fee_fy, budget.collection_fy, budget.gst_inflow_fy, budget.gross_inflow_fy],
            ['PTD', budget.retainer_fee_ptd, budget.collection_ptd, budget.gst_inflow_ptd, budget.gross_inflow_ptd],
        ]
        for line in cash_flow_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'K' + str(row), line[2], table_footer_right)
            sheet.merge_range('L' + str(row) + ':' + 'N' + str(row), line[3], table_footer_right)
            sheet.merge_range('O' + str(row) + ':' + 'Q' + str(row), line[4], table_footer_right)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'OUTFLOW', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Admin Exp.', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Manpower Cost', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Sales Incentive', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Other Expenses', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'GST Outflow', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'Gross Outflow', table_header_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), 'Net Gross Inflow', table_header_right)
        for line in budget.cash_flow_expense_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.admin_exp, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.sales_incentive, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.other_expenses, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.gst_outflow, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.gross_outflow, number_table_border)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line.in_outflow_diff, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('admin_exp')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('manpower_cost')),
                          table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('sales_incentive')),
                          table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('other_expenses')),
                          table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('gst_outflow')),
                          table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(budget.cash_flow_expense_lines.mapped('gross_outflow')),
                          table_footer_right)
        sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row),
                          sum(budget.cash_flow_expense_lines.mapped('in_outflow_diff')), table_footer_right)

        cash_flow_expense_totals = [
            ['H1', budget.cf_admin_exp_h1, budget.cf_manpower_cost_h1, budget.cf_sales_incentive_h1,
             budget.cf_other_expenses_h1, budget.gst_outflow_h1, budget.gross_outflow_h1, budget.in_outflow_diff_h1],
            ['H2', budget.cf_admin_exp_h2, budget.cf_manpower_cost_h2, budget.cf_sales_incentive_h2,
             budget.cf_other_expenses_h2, budget.gst_outflow_h2, budget.gross_outflow_h2, budget.in_outflow_diff_h2],
            ['FY', budget.cf_admin_exp_fy, budget.cf_manpower_cost_fy, budget.cf_sales_incentive_fy,
             budget.cf_other_expenses_fy, budget.gst_outflow_fy, budget.gross_outflow_fy, budget.in_outflow_diff_fy],
            ['PTD', budget.cf_admin_exp_ptd, budget.cf_manpower_cost_ptd, budget.cf_sales_incentive_ptd,
             budget.cf_other_expenses_ptd, budget.gst_outflow_ptd, budget.gross_outflow_ptd, budget.in_outflow_diff_ptd]
        ]
        for line in cash_flow_expense_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line[2], table_footer_right)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line[3], table_footer_right)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line[4], table_footer_right)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line[5], table_footer_right)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line[6], table_footer_right)
            sheet.merge_range('W' + str(row) + ':' + 'Y' + str(row), line[7], table_footer_right)

        # WALK IN PROJECTIONS PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'V' + str(row), 'WALK IN PROJECTIONS', page_header_format)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'G' + str(row), 'LEAD DETAILS', seperator_format)

        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Booking', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Walk Ins', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'CP Walk Ins', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Direct Walk Ins', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Digital Walk Ins', table_header_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), 'No. of Digital Leads', table_header_right)
        for line in budget.walk_in_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.booking, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.walk_ins, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.cp_walk_ins, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.direct_walk_ins, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.digital_walk_ins, number_table_border)
            sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), line.no_of_digital_leads, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(budget.walk_in_lines.mapped('booking')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(budget.walk_in_lines.mapped('walk_ins')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(budget.walk_in_lines.mapped('cp_walk_ins')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(budget.walk_in_lines.mapped('direct_walk_ins')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(budget.walk_in_lines.mapped('digital_walk_ins')), table_footer_right)
        sheet.merge_range('T' + str(row) + ':' + 'V' + str(row), sum(budget.walk_in_lines.mapped('no_of_digital_leads')), table_footer_right)

        # PRODUCTIVITY RATIO PAGE
        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'S' + str(row), 'PRODUCTIVITY RATIO', page_header_format)

        row += 2
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), '', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), 'Operating Margin Ratio', table_header_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), 'Net Profit/Total Expenses', table_header_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), 'Revenue Total Expenses', table_header_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), 'Revenue Manpower Cost', table_header_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), 'Inflow/Outflow', table_header_right)
        for line in budget.productivity_ratio_lines:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), str(line.month_year), table_border)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line.operating_margin_ratio, number_table_border)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line.total_expenses, number_table_border)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line.revenue, number_table_border)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line.manpower_cost, number_table_border)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line.inflow_outflow, number_table_border)
        row += 1
        sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), 'Total', table_header_left)
        sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), sum(budget.productivity_ratio_lines.mapped('operating_margin_ratio')), table_footer_right)
        sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), sum(budget.productivity_ratio_lines.mapped('total_expenses')), table_footer_right)
        sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), sum(budget.productivity_ratio_lines.mapped('revenue')), table_footer_right)
        sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), sum(budget.productivity_ratio_lines.mapped('manpower_cost')), table_footer_right)
        sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), sum(budget.productivity_ratio_lines.mapped('inflow_outflow')), table_footer_right)

        productivity_ratio_totals = [
            ['H1', '', budget.total_expenses_pr_h1, budget.revenue_h1,
             budget.manpower_cost_pr_h1, budget.inflow_outflow_h1],
            ['H2', '', budget.total_expenses_pr_h2, budget.revenue_h2,
             budget.manpower_cost_pr_h2, budget.inflow_outflow_h2],
            ['FY', '', budget.total_expenses_pr_fy, budget.revenue_fy,
             budget.manpower_cost_pr_fy, budget.inflow_outflow_fy],
            ['PTD', '', budget.total_expenses_pr_ptd, budget.revenue_ptd,
             budget.manpower_cost_pr_ptd, budget.inflow_outflow_ptd]
        ]
        for line in productivity_ratio_totals:
            row += 1
            sheet.merge_range('A' + str(row) + ':' + 'D' + str(row), line[0], table_header_left)
            sheet.merge_range('E' + str(row) + ':' + 'G' + str(row), line[1], table_footer_right)
            sheet.merge_range('H' + str(row) + ':' + 'J' + str(row), line[2], table_footer_right)
            sheet.merge_range('K' + str(row) + ':' + 'M' + str(row), line[3], table_footer_right)
            sheet.merge_range('N' + str(row) + ':' + 'P' + str(row), line[4], table_footer_right)
            sheet.merge_range('Q' + str(row) + ':' + 'S' + str(row), line[5], table_footer_right)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response
