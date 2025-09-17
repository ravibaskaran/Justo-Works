from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    address_home_id = fields.Many2one('res.partner', 'Partner')

    @api.model
    def create(self, vals_list):
        res = super(HrEmployee, self).create(vals_list)
        address_home_id = self.env['res.partner'].create({
            'name': res.name,
            'mobile': res.mobile_phone,
            'phone': res.work_phone,
            'email': res.work_email,
        })
        res.address_home_id = address_home_id.id
        return res
