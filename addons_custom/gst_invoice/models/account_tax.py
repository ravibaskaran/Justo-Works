from odoo import api, fields, models, _

class AccountTax(models.Model):
    _inherit = 'account.tax'

    included_in_price = fields.Boolean()

    @api.onchange('included_in_price')
    def set_include_in_price(self):
        if self.included_in_price:
            for line in self.children_tax_ids:
                self.env.cr.execute("""update account_tax set price_include='True' where id = %s""" %line._origin.id)
        else:
            for line in self.children_tax_ids:
                self.env.cr.execute("""update account_tax set price_include='False' where id = %s""" %line._origin.id)
