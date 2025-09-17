from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    developer_invoice_creation_state = fields.Selection(
        selection=[('draft', 'Draft'), ('posted', 'Posted')],
        config_parameter='jupiter_accounts.developer_invoice_creation_state',
        string="Developer Invoice Creation State")
