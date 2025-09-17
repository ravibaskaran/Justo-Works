# -*- coding: utf-8 -*-

from odoo import models, fields, api


class inexoft_account_voucher_access(models.Model):
    _inherit='account.move'
    
    def button_draft_voucher(self):
        self.button_draft()
    
    def button_cancel_voucher(self):
        self.button_cancel()