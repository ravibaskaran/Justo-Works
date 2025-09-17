from lxml import etree

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_date = fields.Date(default=fields.Date.context_today)
    bill_date = fields.Date()
    is_project_invoice = fields.Boolean(default=False)
    partner_details = fields.Char(compute='compute_partner_details', string=' ')
    project_invoice_type = fields.Char()
    project_id = fields.Many2one('building')
    registration_id = fields.Many2one('project.registration')
    booking_id = fields.Many2one('unit.reservation')
    narration = fields.Char()
    multiple_cost_center = fields.Boolean(default=True)

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        res = super(AccountMove, self)._compute_suitable_journal_ids()
        for m in self:
            if m.direct_journal_entry_inx and m.direct_journal_type_inx not in ['payment','receipt','receipt_reverse','payment_reverse']:
                journal_types = ['journal_voucher',]
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)
        return res

    @api.depends('move_type')
    def _compute_invoice_filter_type_domain(self):
        for move in self:
            if move.is_sale_document(include_receipts=True):
                move.invoice_filter_type_domain = 'sale'
            elif move.is_purchase_document(include_receipts=True):
                move.invoice_filter_type_domain = 'purchase'
            else:
                if move.direct_journal_entry_inx and move.direct_journal_type_inx in ['receipt','payment_reverse']:
                    move.invoice_filter_type_domain = 'receipt_voucher'
                elif move.direct_journal_entry_inx and move.direct_journal_type_inx in ['payment','receipt_reverse']:
                    move.invoice_filter_type_domain = 'payment_voucher'
                elif move.direct_journal_entry_inx and move.direct_journal_type_inx not in ['payment','receipt','receipt_reverse','payment_reverse']:
                    move.invoice_filter_type_domain = 'journal_voucher'
                else:
                    move.invoice_filter_type_domain = False

    @api.depends('partner_id')
    def compute_partner_details(self):
        for rec in self:
            rec.partner_details = rec.partner_id.mobile

    def print(self):
        result = self.env.ref('real_estate_extension.account_invoice_print_action').report_action(self)
        result['default_print_option'] = 'print'
        return result

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                     submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if self.env.context.get('default_project_invoice_type') == 'spot_booking':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_channel_employee', '=', True)]")
                    field.set('options', "{'no_create': True, 'no_open': True,'no_quick_create':True,'no_create_edit':True}")
            if self.env.context.get('default_project_invoice_type') == 'cp_brokerage':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_channel', '=', True)]")
                    field.set('options', "{'no_create': True, 'no_open': True,'no_quick_create':True,'no_create_edit':True}")
            if self.env.context.get('default_project_invoice_type') == 'employee_invoice':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_employee', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_open': True,'no_quick_create':True,'no_create_edit':True}")
            if self.env.context.get('default_project_invoice_type') == 'developer_invoice':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_owner', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_open': True,'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
        return res


class DirectJournalEntryItems(models.Model):
    _inherit = 'direct.journal.entry.items'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Cost Center')
