from odoo import models, fields, api,_


class FinancialReportsPdf(models.TransientModel):
    _name = 'profit.reports.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self,report):
        res = self.sudo().create({})
        res.sudo().write({'report': report})
        return res.id


class FinancialPdfReport(models.AbstractModel):
    _name = 'report.profit_loss_balance_sheet.profit_reports_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['profit.reports.pdf'].sudo().search([('id','=',docids)]).report
        return {'report':report}