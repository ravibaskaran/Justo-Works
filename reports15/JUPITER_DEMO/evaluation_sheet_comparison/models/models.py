# -*- coding: utf-8 -*-
from odoo import models, fields


class BetaEvaluationSheetComparison(models.TransientModel):  # change this
    _name = 'beta.evaluation.sheet.comparison'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Evaluation Sheet Comparison')  # change this
    evaluation_sheet_ids = fields.Many2many('evaluation.sheet')

    def get_html(self):
        table = ""
        for sheet in self.evaluation_sheet_ids:
            form = self.env.ref('real_estate_sheets.evaluation_sheet_view_form', False)
            sheet_head = """
                <a href="#" class="o_beta_report_action"
                   data-res-id="%s"
                   data-model="evaluation.sheet"
                   data-form="%s">%s
                </a>
            """ % (sheet.id, form.id, sheet.name)
            data = {
                'header': "<div class='table-responsive mb-4'><table border='1' class='table-scroll table table-sm table-bordered'><tbody><tr><td class='stick-td' width='280px'/><td class='stick-evaluation-td evaluation-head'>" + sheet_head + "</td>",
                'project': "<tr><td class='stick-td'>Project Name</td><th class='stick-evaluation-td'>" + str(sheet.project_name or '') + "</th>",
                'developer': "<tr><td class='stick-td'>Developer</td><td class='stick-evaluation-td'>" + str(sheet.developer_id.name or '') + "</td>",
                'configuration': "<tr><td class='stick-td'>Configuration</td><td class='stick-evaluation-td'>" + str(', '.join(sheet.apartment_type_ids.mapped('name')) or '') + "</td>",
                'carpet': "<tr><td class='stick-td'>Carpet Area</td><td class='stick-evaluation-td'></td>",
                'saleable': "<tr><td class='stick-td'>Saleable Area</td><td class='stick-evaluation-td'>" + str('{:.2f}'.format(sheet.saleable_area)) + "</td>",
                'agreement': "<tr><td class='stick-td'>Quoted Agreement Value</td><td class='stick-evaluation-td'></td>",
                'discount': "<tr><td class='stick-td'>Discount</td><td class='stick-evaluation-td'></td>",
                'package': "<tr><td class='stick-td'>All in Package</td><td class='stick-evaluation-td'></td>",
                'location': "<tr><td class='stick-td'>Location</td><td class='stick-evaluation-td'>" + str(sheet.project_location or '') + "</td>",
                'transacted_av': "<tr><td class='stick-td'>Transacted AV</td><td class='stick-evaluation-td'></td>",
                'transacted_saleable': "<tr><td class='stick-td'>Transacted rate Per Sq. Ft Including infrastructure On saleable area</td><td class='stick-evaluation-td'></td>",
                'transacted_carpet': "<tr><td class='stick-td'>Transacted rate per Sq. Ft Including infrastructure On carpet area</td><td class='stick-evaluation-td'></td>",
                'package_after_discount': "<tr><td class='stick-td'>Approx. all-inclusive Package after discount</td><td class='stick-evaluation-td'></td>",
                'possession': "<tr><td class='stick-td'>Possession Date</td><td class='stick-evaluation-td'>" + str(sheet.possession_date.strftime('%d/%m/%Y') if sheet.possession_date else '') + "</td>",
            }
            competitions = self.env['competition.sheet'].search([('evaluation_sheet_id', '=', sheet.id)])
            for competition in competitions:
                data['header'] += "<td class='competition-td'/>"
                data['project'] += "<th class='competition-td'>"+ str(competition.name) + "</th>"
                data['developer'] += "<td class='competition-td'>"+ str(competition.developer_id.name) + "</td>"
                data['configuration'] += "<td class='competition-td'>"+ str(competition.configuration.name or '') + "</td>"
                data['carpet'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.carpet_area)) + "</td>"
                data['saleable'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.saleable_area)) + "</td>"
                data['agreement'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.quoted_agreement_value)) + "</td>"
                data['discount'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.discount)) + "</td>"
                data['package'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.all_in_package)) + "</td>"
                data['location'] += "<td class='competition-td'>"+ str(competition.location) + "</td>"
                data['transacted_av'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.transacted_av)) + "</td>"
                data['transacted_saleable'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.transacted_rate_sale_area)) + "</td>"
                data['transacted_carpet'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.transacted_rate_carpet_area)) + "</td>"
                data['package_after_discount'] += "<td class='competition-td'>"+ str('{:.2f}'.format(competition.approx_after_discount)) + "</td>"
                data['possession'] += "<td class='competition-td'>"+ str(competition.possession_date.strftime('%d/%m/%Y')) + "</td>"
            for key in data:
                table += data[key] + "</tr>"
            table += "</tbody></table></div>"
        self.template_area = self.env.ref('evaluation_sheet_comparison.report_evaluation_sheet_comparison')._render({
            'table': table,
        })
