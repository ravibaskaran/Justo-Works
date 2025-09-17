from odoo import models, fields
from odoo.tools.float_utils import float_round


# ♦ ▼ Inherited 'Product Product'. ▼ ♦
class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        result = []
        if self._context.get('show_qty'):
            for product in self:
                name = product.name + "/" + "{0:,.2f}".format(product.sudo().virtual_available) + " " + product.uom_id.name
                result.append((product.id, name))
        else:
            result = super(ProductProduct, self).name_get()
        return result

