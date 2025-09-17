from datetime import datetime, timedelta
import logging
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

_logger = logging.getLogger(__name__)


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    def _get_prefix_suffix(self, date=None, date_range=None):
        print("_get_prefix_suffix:- date-", date, "date_range-", date_range)

        def _interpolate(s, d):
            return (s % d) if s else ''

        def _interpolation_dict():
            now = range_date = effective_date = datetime.now(
                pytz.timezone(self._context.get('tz') or 'UTC'))
            if date or self._context.get('ir_sequence_date'):
                effective_date = fields.Datetime.from_string(
                    date or self._context.get('ir_sequence_date'))
            if date_range or self._context.get('ir_sequence_date_range'):
                range_date = fields.Datetime.from_string(
                    date_range or self._context.get('ir_sequence_date_range'))

            sequences = {
                'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
                'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
            }
            res = {}
            for key, format in sequences.items():
                res[key] = effective_date.strftime(format)
                res['range_' + key] = range_date.strftime(format)
                res['current_' + key] = now.strftime(format)
            if effective_date:
                current_date_range = self.date_range_ids.filtered(
                    lambda x: x.date_from <= effective_date.date() and x.date_to >= effective_date.date())
            else:
                current_date_range = self.date_range_ids.filtered(
                    lambda x: x.date_from <= now.date() and x.date_to >= now.date())
            if self.date_range_ids and current_date_range and len(current_date_range) == 1:
                yr_1 = str(current_date_range.date_from.year)[2:]
                yr_2 = str(current_date_range.date_to.year)[2:]
                if yr_1 == yr_2:
                    year_range = str(current_date_range.date_to.year)
                else:
                    year_range = yr_1 + '-' + yr_2
            else:
                year_range = '%Y'
            res.update({'fyear_range': year_range})
            return res

        self.ensure_one()
        d = _interpolation_dict()
        try:
            interpolated_prefix = _interpolate(self.prefix, d)
            interpolated_suffix = _interpolate(self.suffix, d)
        except ValueError:
            raise UserError(
                _('Invalid prefix or suffix for sequence \'%s\'') % self.name)
        return interpolated_prefix, interpolated_suffix

    # def _create_date_range_seq(self, date):
    #     # Fix issue creating new date range for future dates
    #     # It assigns more than one month
    #     # TODO: Remove if odoo merge the following PR:
    #     # https://github.com/odoo/odoo/pull/91019
    #     date_obj = fields.Date.from_string(date)
    #     sequence_range = self.env["ir.sequence.date_range"]
    #     prefix_suffix = "%s %s" % (self.prefix, self.suffix)
    #     if "%(range_day)s" in prefix_suffix:
    #         date_from = date_obj
    #         date_to = date_obj
    #     elif "%(range_month)s" in prefix_suffix:
    #         date_from = fields.Date.start_of(date_obj, "month")
    #         date_to = fields.Date.end_of(date_obj, "month")
    #     else:
    #         date_from = fields.Date.start_of(date_obj, "year")
    #         date_to = fields.Date.end_of(date_obj, "year")
    #     date_range = sequence_range.search(
    #         [
    #             ("sequence_id", "=", self.id),
    #             ("date_from", ">=", date),
    #             ("date_from", "<=", date_to),
    #         ],
    #         order="date_from desc",
    #         limit=1,
    #     )
    #     if date_range:
    #         date_to = fields.Date.subtract(date_range.date_from, days=1)
    #     date_range = sequence_range.search(
    #         [
    #             ("sequence_id", "=", self.id),
    #             ("date_to", ">=", date_from),
    #             ("date_to", "<=", date),
    #         ],
    #         order="date_to desc",
    #         limit=1,
    #     )
    #     if date_range:
    #         date_to = fields.Date.add(date_range.date_to, days=1)
    #     sequence_range_vals = {
    #         "date_from": date_from,
    #         "date_to": date_to,
    #         "sequence_id": self.id,
    #     }
    #     seq_date_range = sequence_range.sudo().create(sequence_range_vals)
    #     return seq_date_range

    def _create_date_range_seq(self, date):
        year = fields.Date.from_string(date).strftime('%Y')
        current_month = fields.Date.from_string(date).strftime('%m')
        year_int = int(year)
        month_int = int(current_month)
        date_from = '{}-04-01'.format(year)
        date_to = '{}-03-31'.format(year)
        if 1 <= month_int <= 3:
            date_from = '{}-04-01'.format(str(year_int - 1))
            date_to = '{}-03-31'.format(year)

        else:
            date_from = '{}-04-01'.format(year)
            date_to = '{}-03-31'.format(str(year_int + 1))

        date_range = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), (
            'date_from', '>=', date), ('date_from', '<=', date_to)], order='date_from desc', limit=1)
        if date_range:
            date_to = date_range.date_from + timedelta(days=-1)
        date_range = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), (
            'date_to', '>=', date_from), ('date_to', '<=', date)], order='date_to desc', limit=1)
        if date_range:
            date_from = date_range.date_to + timedelta(days=1)
        seq_date_range = self.env['ir.sequence.date_range'].sudo().create({
            'date_from': date_from,
            'date_to': date_to,
            'sequence_id': self.id,
        })
        return seq_date_range