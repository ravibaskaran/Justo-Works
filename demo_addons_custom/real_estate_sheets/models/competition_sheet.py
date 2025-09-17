from odoo import models, fields


class CompetitionSheet(models.Model):
    _name = 'competition.sheet'
    _inherit = ['mail.thread']
    _description = 'Competition Sheet'

    name = fields.Char('Name of Project')
    developer_id = fields.Many2one('res.partner', 'Name of Developer', domain=[('is_owner', '=', True)])
    configuration = fields.Many2one('building.unit')
    carpet_area = fields.Float()
    saleable_area = fields.Float()
    quoted_agreement_value = fields.Float()
    discount = fields.Float()
    transacted_av = fields.Float('Transacted AV')
    transacted_rate_sale_area = fields.Float('Transacted rate Per Sq. Ft Including infrastructure On saleable area')
    transacted_rate_carpet_area = fields.Float('Transacted rate per Sq. Ft Including infrastructure On carpet area')
    approx_after_discount = fields.Float('Approx. all-inclusive Package after discount')
    possession_date = fields.Date()
    all_in_package = fields.Float('All in Package')
    location = fields.Char()
    evaluation_sheet_id = fields.Many2one('evaluation.sheet')
