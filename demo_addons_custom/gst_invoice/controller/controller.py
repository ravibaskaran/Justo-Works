from odoo import http
from odoo.http import request

class GstInvoice(http.Controller):

    @http.route('/invoice_correct_partner_type', auth='public', type='http')
    def invoice_correct_partner_type(self):
        if request.env.user.has_group('base.group_system'):
            data = request.env['account.move'].search([('move_type', '!=', 'entry')])
            for move in data:
                if move.partner_id:
                    if move.partner_id.partner_type:
                        if move.partner_id.partner_type == 'B2B':
                            request.env.cr.execute("update account_move set invoice_type='b2b' where id=" + str(move.id))
                        else:
                            request.env.cr.execute(
                                "update account_move set invoice_type=False where id=" + str(move.id))
                    else:
                        request.env.cr.execute(
                            "update account_move set invoice_type=False where id=" + str(move.id))
            return 'success'
        else:
            return 'Access Denied'