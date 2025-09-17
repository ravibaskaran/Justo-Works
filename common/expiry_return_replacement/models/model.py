from odoo import fields, models, api


class inherit(models.Model):
    _inherit = 'account.move'

    expiry_type = fields.Selection(selection=[('expiry_rpl', 'Expiry Replacement'), ('expiry_rtn', 'Expiry Return')])


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    default_account_id = fields.Many2one(
        comodel_name='account.account', check_company=True, copy=False, ondelete='restrict',
        string='Default Account',
        domain="[('deprecated', '=', False), ('company_id', '=', company_id),'|', ('user_type_id', 'in', type_control_ids),('user_type_id.type', 'not in', ('receivable', 'payable'))]")