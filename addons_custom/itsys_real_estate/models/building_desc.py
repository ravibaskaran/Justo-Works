# -*- coding: utf-8 -*-

from odoo import fields, models


class BuildingDesc(models.Model):
    _name = "building.desc"
    _description = "building Description"
    name = fields.Char('State')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
