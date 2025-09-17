# -*- coding: utf-8 -*-
from odoo import models, fields,api, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    journal_type = fields.Selection([
            ('sale', 'Sales'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('bank', 'Bank'),
            ('general', 'Miscellaneous'),
        ], related='journal_id.type')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True,
                                          states={'draft': [('readonly', False)]})
    
    @api.model
    def default_get(self, fields):
        res = super(AccountPayment, self).default_get(fields)
        j_id=self.env['account.journal'].search([('type','=','cash')], limit=1).id
        if j_id:
            res['journal_id'] =j_id
        return res
