# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from odoo.exceptions import UserError


class MultipleAccountOpening(models.Model):
    _inherit = 'multiple.account.opening'

    financial_range = fields.Many2one('ir.sequence.date_range')

    def validate_opening(self):
        if self.account_opening_move_id:
            if self.date != self.account_opening_move_id.date:
                raise UserError('Date mismatch with journal entry and opening!')
        return super(MultipleAccountOpening, self).validate_opening()

    @api.onchange('financial_range')
    def set_financial_date(self):
        if self.financial_range:
            self.date = self.financial_range.date_from


class IrSequenceDaterange(models.Model):
    _inherit = 'ir.sequence.date_range'
    _rec_name = "name"

    name = fields.Char(compute="compute_name")

    def compute_name(self):
        for data in self:
            data.name = data.date_from.strftime('%y') + '-' + data.date_to.strftime('%y')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        sequence = journal.sequence_id
        if not sequence:
            sequence = self.env['ir.sequence'].search([('use_date_range', '=', True),('date_range_ids','!=',False)], limit=1)
        if self._context.get('financial_year'):
            domain = [('sequence_id', '=', sequence.id)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        # rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        # return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))
