# -*- coding: utf-8 -*-
# from odoo import http


# class InvoicePrintCustom(http.Controller):
#     @http.route('/invoice_print_custom/invoice_print_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_print_custom/invoice_print_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_print_custom.listing', {
#             'root': '/invoice_print_custom/invoice_print_custom',
#             'objects': http.request.env['invoice_print_custom.invoice_print_custom'].search([]),
#         })

#     @http.route('/invoice_print_custom/invoice_print_custom/objects/<model("invoice_print_custom.invoice_print_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_print_custom.object', {
#             'object': obj
#         })
