from lxml import etree
from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_types = ['bank', 'cash']
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountPayment, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if self.env.context.get('default_partner') == 'is_owner':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_owner', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
            if self.env.context.get('default_partner') == 'is_channel_employee':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_channel_employee', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
            if self.env.context.get('default_partner') == 'is_channel':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_channel', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
            if self.env.context.get('default_partner') == 'is_employee':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_employee', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
            if self.env.context.get('res_partner_search_mode') == 'supplier':
                for field in doc.xpath("//field[@name='partner_id']"):
                    field.set('domain', "[('is_vendor', '=', True)]")
                    field.set('options',
                              "{'no_create': True, 'no_quick_create':True,'no_create_edit':True}")
            res['arch'] = etree.tostring(doc)
        return res