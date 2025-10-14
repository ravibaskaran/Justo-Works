# -*- coding: utf-8 -*-
from odoo import http


class JustoWebsite(http.Controller):
    @http.route('/privacy-policy', auth='public')
    def index(self, **kw):
        return http.request.render('justo_website.privacy_policy_template')

#     @http.route('/justo_website/justo_website/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('justo_website.listing', {
#             'root': '/justo_website/justo_website',
#             'objects': http.request.env['justo_website.justo_website'].search([]),
#         })

#     @http.route('/justo_website/justo_website/objects/<model("justo_website.justo_website"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('justo_website.object', {
#             'object': obj
#         })
