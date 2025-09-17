import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_is_zero


class AccountAssetCategory(models.Model):
    _inherit = 'account.asset.category'

    method = fields.Selection(
        [('linear', 'Straight Line Method'), ('degressive', 'Written Down Value Method')])


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    method = fields.Selection([('linear', 'Straight Line Method'), ('degressive', 'Written Down Value Method')])

    def compute_depreciation_board(self):
        self.ensure_one()
        posted_depreciation_line_ids = self.depreciation_line_ids.filtered(
            lambda x: x.move_check).sorted(key=lambda l: l.depreciation_date)
        unposted_depreciation_line_ids = self.depreciation_line_ids.filtered(
            lambda x: not x.move_check)

        # Remove old unposted depreciation lines. We cannot use unlink() with One2many field
        commands = [(2, line_id.id, False) for line_id in
                    unposted_depreciation_line_ids]

        if self.value_residual != 0.0:
            amount_to_depr = residual_amount = self.value_residual
            if self.prorata:
                # if we already have some previous validated entries, starting date is last entry + method perio
                if posted_depreciation_line_ids and \
                        posted_depreciation_line_ids[-1].depreciation_date:
                    last_depreciation_date = datetime.strptime(
                        posted_depreciation_line_ids[-1].depreciation_date,
                        DF).date()
                    depreciation_date = last_depreciation_date + relativedelta(
                        months=+self.method_period)
                else:
                    depreciation_date = datetime.strptime(
                        str(self._get_last_depreciation_date()[self.id]),
                        DF).date()
            else:
                # depreciation_date = 1st of January of purchase year if annual valuation, 1st of
                # purchase month in other cases
                if self.method_period >= 12:
                    if self.company_id.fiscalyear_last_month:
                        asset_date = date(year=int(self.date.year),
                                          month=int(
                                              self.company_id.fiscalyear_last_month),
                                          day=int(
                                              self.company_id.fiscalyear_last_day)) + relativedelta(
                            days=1) + \
                                     relativedelta(year=int(
                                         self.date.year))  # e.g. 2018-12-31 +1 -> 2019
                    else:
                        asset_date = datetime.strptime(
                            str(self.date)[:4] + '-01-01', DF).date()
                else:
                    asset_date = datetime.strptime(str(self.date)[:7] + '-01',
                                                   DF).date()
                # if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if posted_depreciation_line_ids and \
                        posted_depreciation_line_ids[-1].depreciation_date:
                    last_depreciation_date = datetime.strptime(str(
                        posted_depreciation_line_ids[-1].depreciation_date),
                        DF).date()
                    depreciation_date = last_depreciation_date + relativedelta(
                        months=+self.method_period)
                else:
                    depreciation_date = asset_date
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(
                depreciation_date, total_days)

            # for x in range(len(posted_depreciation_line_ids),
            #                undone_dotation_number):
            for x in range(0,
                           undone_dotation_number):
                sequence = x + 1
                amount = self._compute_board_amount(sequence, residual_amount,
                                                    amount_to_depr,
                                                    undone_dotation_number,
                                                    posted_depreciation_line_ids,
                                                    total_days,
                                                    depreciation_date)

                amount = self.currency_id.round(amount)
                if float_is_zero(amount,
                                 precision_rounding=self.currency_id.rounding):
                    continue
                residual_amount -= amount
                vals = {
                    'amount': amount,
                    'asset_id': self.id,
                    'sequence': sequence,
                    'name': (self.code or '') + '/' + str(sequence),
                    'remaining_value': residual_amount,
                    'depreciated_value': self.value - (
                                self.salvage_value + residual_amount),
                    'depreciation_date': depreciation_date.strftime(DF),
                    'method': self.method,
                }
                commands.append((0, False, vals))
                # Considering Depr. Period as months
                depreciation_date = date(year, month, day) + relativedelta(
                    months=+self.method_period)
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year

        self.write({'depreciation_line_ids': commands})

        return True

    def _compute_board_amount(self, sequence, residual_amount, amount_to_depr,
                              undone_dotation_number,
                              posted_depreciation_line_ids, total_days,
                              depreciation_date):
        amount = 0
        if sequence == undone_dotation_number:
            amount = residual_amount
        else:
            if self.method == 'linear':
                amount = amount_to_depr / undone_dotation_number
                if self.prorata:
                    amount = amount_to_depr / self.method_number
                    if sequence == 1:
                        if self.method_period % 12 != 0:
                            date = datetime.strptime(str(self.date), '%Y-%m-%d')
                            month_days = \
                            calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (
                                                 amount_to_depr / self.method_number) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(
                                depreciation_date)[
                                        'date_to'] - depreciation_date).days + 1
                            amount = (
                                                 amount_to_depr / self.method_number) / total_days * days
            elif self.method == 'degressive':
                amount = residual_amount * self.method_progress_factor
                if self.prorata:
                    if sequence == 1:
                        if self.method_period % 12 != 0:
                            date = datetime.strptime(str(self.date), '%Y-%m-%d')
                            month_days = \
                            calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (
                                                 residual_amount * self.method_progress_factor) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(
                                depreciation_date)[
                                        'date_to'] - depreciation_date).days + 1
                            amount = (
                                                 residual_amount * self.method_progress_factor) / total_days * days
        return amount


class AccountAssetDepreciationLine(models.Model):
    _inherit = 'account.asset.depreciation.line'

    method = fields.Selection([('linear', 'Straight Line Method'), ('degressive', 'Written Down Value Method')])


class AssetModify(models.TransientModel):
    _inherit = 'asset.modify'

    method = fields.Selection([('linear', 'Straight Line Method'), ('degressive', 'Written Down Value Method')], required=True, string='Computation Method')

    @api.model
    def default_get(self, fields):
        res = super(AssetModify, self).default_get(fields)
        asset_id = self.env.context.get('active_id')
        asset = self.env['account.asset.asset'].browse(asset_id)
        if 'name' in fields:
            res.update({'method': asset.method})
        return res

    def modify(self):
        """ Modifies the duration of asset for calculating depreciation
        and maintains the history of old values, in the chatter.
        """
        asset_id = self.env.context.get('active_id', False)
        asset = self.env['account.asset.asset'].browse(asset_id)
        old_values = {
            'method_number': asset.method_number,
            'method_period': asset.method_period,
            'method_end': asset.method_end,
            'method': asset.method,
        }
        asset_vals = {
            'method_number': self.method_number,
            'method_period': self.method_period,
            'method_end': self.method_end,
            'method': self.method,
        }
        asset.write(asset_vals)
        asset.compute_depreciation_board()
        tracked_fields = self.env['account.asset.asset'].fields_get(['method_number', 'method_period', 'method_end'])
        changes, tracking_value_ids = asset._mail_track(tracked_fields, old_values)
        if changes:
            asset.message_post(subject=_('Depreciation board modified'), body=self.name, tracking_value_ids=tracking_value_ids)
        return {'type': 'ir.actions.act_window_close'}
