from odoo import models, fields, api,_


# ♦ ▼  Daybook co op 2 PDF Report ▼ ♦
class DaybookCoOpPdf(models.TransientModel):
    _name = 'daybook_co_op.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self,report):
        res = self.sudo().create({})
        res.sudo().write({'report': report})
        return res.id


class DaybookPdfReport(models.AbstractModel):
    _name = 'report.daybook_co_op.daybook_co_op_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['daybook_co_op.pdf'].sudo().search([('id','=',docids)]).report
        return {'report':report}