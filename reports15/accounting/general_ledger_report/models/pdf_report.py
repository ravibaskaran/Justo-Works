from odoo import models, fields, api


class GeneralLedgerPdf(models.TransientModel):
    _name = 'general.ledger.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self, report):
        res = self.sudo().create({})
        res.write({'report': report})
        return res.id


class GeneralLedgerPdfReport(models.AbstractModel):
    _name = 'report.general_ledger_report.general_ledger_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['general.ledger.pdf'].sudo().search([('id', '=', docids)]).report
        return {'report': report}
