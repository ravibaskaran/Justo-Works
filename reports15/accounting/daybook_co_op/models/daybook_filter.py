
from odoo import models, fields, api
from ast import literal_eval


#  ♦ ▼ Configuration Setting Inherited ▼ ♦
class ConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    dayabook_entries_filter = fields.Boolean(string='Daybook filter',config_parameter='daybook_co_op.dayabook_entries_filter', required=False)
