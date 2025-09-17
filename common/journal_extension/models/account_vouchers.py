from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_default_journal(self):
        if self.direct_journal_entry_inx is True or self.env.context.get('default_direct_journal_entry_inx'):
            journal = False
            voucher_type = ''
            if self.direct_journal_type_inx in ('receipt', 'payment_reverse') or self.env.context.get(
                    'default_direct_journal_type_inx') in ('receipt', 'payment_reverse'):
                journal = self.env['account.journal'].search(
                    [('type', '=', 'receipt_voucher')], limit=1)
                voucher_type = 'Receipt'
            elif self.direct_journal_type_inx in ('payment', 'receipt_reverse') or self.env.context.get(
                    'default_direct_journal_type_inx') in ('payment', 'receipt_reverse'):
                journal = self.env['account.journal'].search(
                    [('type', '=', 'payment_voucher')], limit=1)
                voucher_type = 'Payment'
            elif self.direct_journal_type_inx not in (
            'payment', 'receipt', 'receipt_reverse', 'payment_reverse') or self.env.context.get(
                    'default_direct_journal_type_inx') not in (
            'payment', 'receipt', 'receipt_reverse', 'payment_reverse'):
                journal = self.env['account.journal'].search(
                    [('type', '=', 'journal_voucher')], limit=1)
                voucher_type = 'Journal'
            if not journal:
                raise UserError(_('Please define a journal with sequence for %s Voucher') % voucher_type)
            return journal
        else:
            return super(AccountMove, self)._get_default_journal()

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        check_company=True, domain="[('id', 'in', suitable_journal_ids)]",
        default=_get_default_journal)

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            if m.direct_journal_entry_inx is True or self.env.context.get('default_direct_journal_entry_inx'):
                journal_types = ['receipt_voucher', 'payment_voucher', 'journal_voucher',]
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)
            elif (self.env.context.get('params') and self.env.context.get('params').get('model') == 'account.payment') or self.env.context.get('default_partner'):
                journal_types = ['bank', 'cash']
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)
            else:
                journal_type = m.invoice_filter_type_domain or 'general'
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)

