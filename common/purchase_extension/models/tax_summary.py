from odoo import fields, models


class AccountMoveTax(models.Model):
    _name = "account.move.tax.summary"

    move_id = fields.Many2one("account.move")
    tax_id = fields.Many2one("account.tax")
    cgst = fields.Float("CGST")
    sgst = fields.Float("SGST")
    igst = fields.Float("IGST")
    cess = fields.Float("CESS")
    total_excluded = fields.Float("Taxable")
    total_included = fields.Float("Total")
