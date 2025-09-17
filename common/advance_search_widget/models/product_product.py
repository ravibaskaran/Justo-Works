# -*- coding: utf-8 -*-

from odoo import models


class AdvanceSearch(models.AbstractModel):
    _inherit = "advance.search"

    def _adv_search_rec_get(self, model, domain, search_on, search_keyword, search_result_fields, limit):
        if model == 'product.product' and 'tally' not in search_on and len(search_on) == 1 and search_on[0] == 'name':
            search_on = ['name%', 'barcode']
        res = super(AdvanceSearch, self)._adv_search_rec_get(
            model, domain, search_on, search_keyword, search_result_fields, limit)
        return res
