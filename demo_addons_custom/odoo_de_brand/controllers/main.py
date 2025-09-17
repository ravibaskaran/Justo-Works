from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class InexoftDebrandBackendController(http.Controller):

    @http.route(['/UpdateOdooBotMessage'], type='http', auth="user", website=True)
    def UpdateOdooBotMessageMethod(self):
        try:
            if request.env.user.has_group('base.group_system'):
                messages = request.env['mail.message'].sudo().search(
                    [('model', '=', 'mail.channel'), ('message_type', '=', 'comment')])
                for message in messages:
                    message.body = "<p>Hello,<br>This chat helps employees collaborate efficiently. I'm here to help you discover its features.<br><b>Try to send me an emoji :)</b></p>"
                return "Success"
            else:
                return "Not Authorize to do this"
        except Exception as e:
            return "{0}".format(e)
