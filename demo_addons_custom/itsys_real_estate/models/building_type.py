# -*- coding: utf-8 -*-
from odoo import fields, models


class BuildingType(models.Model):
    _name = "building.type"
    _description = "Building Type"

    name = fields.Char('Type')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    type = fields.Selection([('residential', 'Residential'), ('commercial', 'Commercial')])
