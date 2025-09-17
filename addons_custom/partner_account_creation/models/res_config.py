from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    create_partner_account = fields.Boolean(config_parameter='partner_account_creation.create_partner_account',
                                            string="Create Partner Account")
    create_payable_account = fields.Boolean(config_parameter='partner_account_creation.create_payable_account',
                                            string="Create Payable Account")
    create_receivable_account = fields.Boolean(config_parameter='partner_account_creation.create_receivable_account',
                                               string="Create Receivable Account")
