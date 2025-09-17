from odoo import models, fields, api,_


class CashBookPdf(models.TransientModel):
    _name = 'cash.book.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self,report):
        res = self.sudo().create({})
        res.sudo().write({'report': report})
        return res.id


class CashBookPdfReport(models.AbstractModel):
    _name = 'report.cash_book.cash_book_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['cash.book.pdf'].sudo().search([('id','=',docids)]).report
        return {'report':report}