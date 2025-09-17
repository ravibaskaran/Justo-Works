from odoo import models, fields, api,_


class TradingPdf(models.TransientModel):
    _name = 'trading.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self,report):
        res = self.sudo().create({})
        res.sudo().write({'report': report})
        return res.id


class TradingPdfReport(models.AbstractModel):
    _name = 'report.manufacturing_trading.trading_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['trading.pdf'].sudo().search([('id','=',docids)]).report
        return {'report':report}