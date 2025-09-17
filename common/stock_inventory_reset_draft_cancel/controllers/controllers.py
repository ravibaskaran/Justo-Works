# -*- coding: utf-8 -*-
# from odoo import http


# class StockInventoryResetDraftCancel(http.Controller):
#     @http.route('/stock_inventory_reset_draft_cancel/stock_inventory_reset_draft_cancel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_inventory_reset_draft_cancel/stock_inventory_reset_draft_cancel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_inventory_reset_draft_cancel.listing', {
#             'root': '/stock_inventory_reset_draft_cancel/stock_inventory_reset_draft_cancel',
#             'objects': http.request.env['stock_inventory_reset_draft_cancel.stock_inventory_reset_draft_cancel'].search([]),
#         })

#     @http.route('/stock_inventory_reset_draft_cancel/stock_inventory_reset_draft_cancel/objects/<model("stock_inventory_reset_draft_cancel.stock_inventory_reset_draft_cancel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_inventory_reset_draft_cancel.object', {
#             'object': obj
#         })
