from odoo.exceptions import ValidationError
from odoo import models, fields, api


class BuildingWing(models.Model):
    _name = 'building.wing'
    _description = 'Wing'
    _inherit = ['mail.thread']

    name = fields.Char()
    code = fields.Char()


class BuildingUnit(models.Model):
    _name = 'building.unit'
    _description = 'Type'
    _inherit = ['mail.thread']

    name = fields.Char()
    wing_id = fields.Many2one('building.wing')
    project_id = fields.Many2one('building')

    @api.constrains('name')
    def validate_unique_name(self):
        confs = self.env['building.unit'].search(
            [('name', '=', self.name), ('id', '!=', self.id)])
        if confs:
            raise ValidationError('Configuration with same name already exists!')
