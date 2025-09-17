from odoo import models, fields, api
from odoo.exceptions import UserError


class Project(models.Model):
    _inherit = 'building'

    term_sheet_id = fields.Many2one('term.sheet')

    @api.onchange('term_sheet_id')
    def onchange_term_sheet(self):
        if self.term_sheet_id:
            if self.env['building'].search([('term_sheet_id', '=', self.term_sheet_id.id)]):
                self.term_sheet_id = False
                raise UserError('Project with term sheet already exists!')
        self.name = self.term_sheet_id.name
