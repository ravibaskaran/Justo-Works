from odoo import models, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type in ['form', 'tree']:
            if res.get('toolbar') and self._context.get('default_type') not in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund']:
                if res['toolbar'].get('action'):
                    actions = tuple(res['toolbar']['action'])
                    for action in actions:
                        if action.get('xml_id'):
                            if action['xml_id'] in ['account.action_validate_account_move']:
                                res['toolbar']['action'].remove(action)
        return res


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    def validate_move(self):
        account_moves = False
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get(
                'active_ids', [])), ('state', '=', 'draft')]
            cust_domain = [
                ('move_type', 'in', ['in_invoice', 'in_refund', 'out_invoice', 'out_refund'])]
            account_moves = self.env['account.move'].search(domain+cust_domain)
        elif self._context.get('active_model') == 'account.journal':
            domain = [('journal_id', '=', self._context.get(
                'active_id')), ('state', '=', 'draft')]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        if account_moves:
            for account_move in account_moves:
                account_move.action_post_custom()
        else:
            moves = self.env['account.move'].search(
                domain).filtered('line_ids')
            if not moves:
                raise UserError(_('There are no journal items in the draft state to post.'))
            moves.post()
        return {'type': 'ir.actions.act_window_close'}
