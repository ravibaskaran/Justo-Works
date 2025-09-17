import traceback
import werkzeug
from odoo import models, exceptions
from odoo.addons.base.models.qweb import QWebException
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = ['ir.http']

    @classmethod
    def _get_exception_code_values(cls, exception):
        """ Return a tuple with the error code following by the values matching the exception"""
        code = 500  # default code
        if request.env.user.has_group('base.group_system'):
            error_msg = traceback.format_exc()
        else:
            error_msg = 'An error occurred \nPlease contact your support service'
        values = dict(
            exception=exception,
            traceback=error_msg,
        )
        if isinstance(exception, exceptions.UserError):
            values['error_message'] = exception.args[0]
            code = 400
            if isinstance(exception, exceptions.AccessError):
                code = 403
        elif isinstance(exception, QWebException):
            values.update(qweb_exception=exception)
            if type(exception.error) == exceptions.AccessError:
                code = 403
        elif isinstance(exception, werkzeug.exceptions.HTTPException):
            code = exception.code
        values.update(
            status_message=werkzeug.http.HTTP_STATUS_CODES.get(code, ''),
            status_code=code,
        )
        return (code, values)
