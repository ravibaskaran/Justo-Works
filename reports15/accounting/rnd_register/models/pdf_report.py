from odoo import models, fields, api,_


class DaybookCoOpPdf(models.TransientModel):
    _name = 'rnd_register.pdf'
    report = fields.Html()

    @api.model
    def get_pdf_report(self,report):
        res = self.sudo().create({})
        res.sudo().write({'report': report})
        return res.id


class DaybookPdfReport(models.AbstractModel):
    _name = 'report.rnd_register.rnd_register_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['rnd_register.pdf'].sudo().search([('id','=',docids)]).report
        return {'report':report}