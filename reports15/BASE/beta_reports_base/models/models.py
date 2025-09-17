# -*- coding: utf-8 -*-

from odoo import models, fields


class BetaReports(models.TransientModel):
    _name = 'beta.reports'

    template_area = fields.Text()
    layout=fields.Boolean()
    report_id = fields.Many2one('ir.actions.report')
    form_edit = fields.Boolean()

    def beta_pdf_print(self):
        data = {
            'doc_ids': self.id,
            'doc_model': self.report_id.model,
            'docs': self.id,
            'template_area': self.template_area
        }
        return self.report_id.report_action(self.id, data=data)

