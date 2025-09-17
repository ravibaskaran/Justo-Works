from lxml import etree
from odoo import models, api, exceptions


class UnitReservation(models.Model):
    _inherit = 'unit.reservation'

    def unlink(self):
        for record in self:
            if not self.env.user.has_group('base.group_system'):  # Non-system users
                if record.state != 'draft':
                    raise exceptions.UserError("You cannot delete this record unless it is in the 'draft' state.")

        return super(UnitReservation, self).unlink()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if not self.env.user.has_group('project_transactions.view_all_projects'):
                employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
                rec_ids = []
                if employee:
                    records = self.env['building'].search([])
                    for project in records:
                        allowed_employees = project.closing_manager_ids + project.sourcing_manager_ids + project.closing_tl_ids \
                                            + project.sourcing_tl_ids + project.crm_ids + project.marketing_ids \
                                            + project.business_head_id + project.site_head_id + project.cluster_head_id
                        if employee.id in allowed_employees.ids:
                            rec_ids.append(project.id)

                domain = [('id', 'in', rec_ids)]
                for field in doc.xpath("//field[@name='building']"):
                    field.set('domain', str(domain))
            res['arch'] = etree.tostring(doc)
        return res
