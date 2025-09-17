# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions


class ProductTemplate(models.Model):
    _inherit = "product.template"

    on_hold = fields.Boolean(string="On Hold", readonly=True)

    def unlink(self): # delete
        for record in self:
            if not self.env.user.has_group('base.group_system'):  # Non-system users
                if record.state != 'free':
                    raise exceptions.UserError("You can only delete this flat if it is in 'Available' state.")

        return super(ProductTemplate, self).unlink()