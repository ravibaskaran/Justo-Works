from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    type = fields.Selection(selection_add=[('cp_brokerage', 'CP Brokerage'), ('spot_booking', 'Spot Booking')],
                            ondelete={'cp_brokerage': 'cascade', 'spot_booking': 'cascade'})
