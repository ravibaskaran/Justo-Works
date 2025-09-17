from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    project_id = fields.Many2one('building', 'Project Name')
    is_retention = fields.Boolean(default=False)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        search_mode = self.env.context.get('res_partner_search_mode')
        if search_mode == 'developer':
            args = [('is_owner', '=', True)]
        return super(ResPartner, self)._name_search(name, args, operator=operator, limit=limit,
                                                    name_get_uid=name_get_uid)
