from odoo import models, fields


class DeveloperSource(models.Model):
    _name = 'developer.source'

    name = fields.Char('Source', required=True)


class ConstructionStage(models.Model):
    _name = 'construction.stage'

    name = fields.Char('Stage of Construction', required=True)

