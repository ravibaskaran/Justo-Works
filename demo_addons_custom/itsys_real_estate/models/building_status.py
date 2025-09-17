# -*- coding: utf-8 -*-
from odoo import fields, models


class BuildingStatus(models.Model):
    _name = "building.status"
    _description = "building state"

    name = fields.Char('State')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
