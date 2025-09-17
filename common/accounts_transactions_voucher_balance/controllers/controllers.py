# -*- coding: utf-8 -*-
# from odoo import http


# class ReceiptPaymentVoucherBalance(http.Controller):
#     @http.route('/receipt_payment_voucher_balance/receipt_payment_voucher_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/receipt_payment_voucher_balance/receipt_payment_voucher_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('receipt_payment_voucher_balance.listing', {
#             'root': '/receipt_payment_voucher_balance/receipt_payment_voucher_balance',
#             'objects': http.request.env['receipt_payment_voucher_balance.receipt_payment_voucher_balance'].search([]),
#         })

#     @http.route('/receipt_payment_voucher_balance/receipt_payment_voucher_balance/objects/<model("receipt_payment_voucher_balance.receipt_payment_voucher_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('receipt_payment_voucher_balance.object', {
#             'object': obj
#         })
