# import base64
# import pdfkit
# from odoo import http
# from odoo.http import request
#
#
# class HtmlToPdfController(http.Controller):
#     @http.route('/convert_html_to_pdf', type='json', auth='public')
#     def convert_html_to_pdf(self, html_content):
#         pdf_file = pdfkit.from_string(html_content, False)
#         pdf_base64 = base64.b64encode(pdf_file)
#
#         return pdf_base64