from odoo import models, api
from lxml import etree


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Base, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        remove_delete_button = True
        if not self.env.user.has_group('base.group_system') and view_type in ['form', 'tree']:
            if self._name in ['unit.reservation', 'product.template'] and self.env.user.has_group(
                    'real_estate_extension.group_user_delete_button'):
                remove_delete_button = False;
            view_xml = res.get('arch')
            if view_xml:
                doc = etree.XML(res['arch'])
                if remove_delete_button:
                    doc.set('delete', '0')
                res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
