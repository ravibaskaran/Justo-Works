from odoo import models, fields


class TermSheetTemplate(models.Model):
    _name = 'term.sheet.template'
    _description = 'Term Sheet Template'

    name = fields.Char(required=True)
    code = fields.Char()
    template = fields.Html()
