# -*- coding: utf-8 -*-
from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def button_cancel_inx(self):
        self.button_draft()
        self.button_cancel()
        if self.direct_move_type and self.direct_move_picking_id:
            self.direct_move_picking_id.action_cancel()

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        if self.direct_move_picking_id:
            self.direct_move_picking_id.action_cancel()
            self.direct_move_picking_id.action_cancel_draft()
            self.direct_move_picking_id.action_cancel()
            if self.direct_move_picking_id.state == 'cancel':
                self.direct_move_picking_id.sudo().unlink()
        return res