# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import base64

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def get_max_upload_fsize(self,key):
        max_upload_fsize = False
        max_upload_fsize_conf = self.env['ir.config_parameter'].sudo().get_param('security_update.max_upload_fsize')
        if max_upload_fsize_conf:
            try:
                # max_upload_fsize = int(max_upload_fsize_conf) * 10 ** 6
                max_upload_fsize = float(max_upload_fsize_conf)  * 1024 * 1024
            except:
                max_upload_fsize = False
        return max_upload_fsize

    @api.model
    def create(self, values):
        if isinstance(values,dict):
            data = values.get('datas', False)
            bin_data = base64.b64decode(data) if data else b''
            max_upload_fsize = 1e+6
            max_upload_fsize_conf = self.env['ir.config_parameter'].sudo().get_param('security_update.max_upload_fsize')
            if max_upload_fsize_conf:
                try:
                    max_upload_fsize = int(max_upload_fsize_conf) * 10 ** 6
                except:
                    max_upload_fsize = 1e+6
            file_size = len(bin_data)
            # if file_size > max_upload_fsize:
            #     raise ValidationError("The selected file exceed the maximum file size of %s MB"%(max_upload_fsize/1e+6))
            name = values.get('name', False)
            mimetype = values.get('mimetype', False)
            if name and "script>" in name:
                raise ValidationError("Invalid Name")
            if mimetype and "svg" in mimetype:
                raise ValidationError("Invalid Format")

        elif isinstance(values,list):
            for val in values:
                name = val.get('name', False)
                mimetype = val.get('mimetype', False)
                if name and "script>" in name:
                    raise ValidationError("Invalid Name")
                if mimetype and "svg" in mimetype:
                    raise ValidationError("Invalid Format")
        return super(IrAttachment, self).create(values)


    def write(self, values):
        if isinstance(values,dict):
            name = values.get('name', False)
            mimetype = values.get('mimetype', False)
            if name and "script>" in name:
                raise ValidationError("Invalid Name")
            if mimetype and "svg" in mimetype:
                raise ValidationError("Invalid Format")
        elif isinstance(values,list):
            for val in values:
                name = val.get('name', False)
                mimetype = values.get('mimetype', False)
                if name and "script>" in name:
                    raise ValidationError("Invalid Name")
                if mimetype and "svg" in mimetype:
                    raise ValidationError("Invalid Format")
        return super(IrAttachment, self).write(values)
