# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaBookingLogReport(models.TransientModel):  # change this
    _name = 'beta.booking.log.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Booking Log Report')  # change this
    date_from = fields.Date()
    date_to = fields.Date()
    date_filter = fields.Selection([('booking', 'Booking Date'), ('log', 'Log Date')], default='booking')
    project_ids = fields.Many2many('building', 'booking_log_project_rel', 'booking_log_id', 'project_id')

    def get_actual_date(self, tz_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    def get_current_inv_date(self, tz_datetime):
        fmt = "%d/%m/%Y"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_timezone.strftime(fmt), fmt) - datetime.strptime(
            now_utc.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime(fmt)

    @api.model
    def default_get(self, fields_list):
        res = super(BetaBookingLogReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def get_html(self):
        res = self._get_report_data()
        self.template_area = self.env.ref('booking_log_report.report_booking_log_report')._render({
            'table': res,
            'date_start': self.date_from,
            'date_end': self.date_to
        })

    def _get_report_data(self):
        final_data = []
        tracking_fields = """('carpet_area', 'balcony_area', 'total_saleable_area', 'sq_ft_area', 'flat_cost_real',
            'cp_brokerage', 'referral_amount', 'developer_commission_percentage',
            'spot_amount', 'infra_charge', 'other_charges', 'flat_cost', 'stamp_duty',
            'stamp_duty_percentage', 'legal_charge', 'gst_legal_charge', 'registration_charge',
            'net_amount', 'advance_amount', 'state')"""
        date_from = self.get_actual_date(self.date_from.strftime('%Y-%m-%d') + " 00:00:00")
        date_to = self.get_actual_date(self.date_to.strftime('%Y-%m-%d') + " 23:59:59")
        if self.date_filter == 'booking':
            where_clause = f" where date <= '{date_to}' and date >= '{date_from}' "
            if self.project_ids:
                where_clause += f' and building in ({",".join([str(item.id) for item in self.project_ids])})'
        else:
            where_clause = ''
            if self.project_ids:
                where_clause += f' where building in ({",".join([str(item.id) for item in self.project_ids])})'

        self.env.cr.execute(f'select name, id from unit_reservation {where_clause}')
        bookings = self.env.cr.dictfetchall()

        for booking in bookings:
            if self.date_filter == 'log':
                log_where = f" and mm.date <= '{date_to}' and mm.date >= '{date_from}' "
            else:
                log_where = ''
            draft_log = f"""
                select COALESCE(mtv.id, 0) from mail_tracking_value mtv 
                left join mail_message mm on mm.id = mtv.mail_message_id
                left join ir_model_fields imf on imf.id = mtv.field
                where mm.res_id = {booking['id']} and imf.name = 'state' and 
                mm.model = 'unit.reservation' and
                mtv.old_value_char = 'Confirmed' and mtv.new_value_char = 'Draft' 
                limit 1
            """
            self.env.cr.execute(draft_log)
            draft_log = self.env.cr.fetchone()
            if draft_log:
                log = f"""
                    select imf.name as field, imf.field_description, 
                    mtv.old_value_float, mtv.new_value_float, mtv.old_value_char, mtv.new_value_char, 
                    mm.date, rp.name
                    from mail_tracking_value mtv 
                    left join mail_message mm on mm.id = mtv.mail_message_id
                    left join ir_model_fields imf on imf.id = mtv.field
                    left join res_partner rp on rp.id = mm.author_id
                    where mm.res_id = {booking['id']} and imf.name in {tracking_fields} and 
                    mm.model = 'unit.reservation' and mtv.id > {draft_log[0]} {log_where}
            
                """
                self.env.cr.execute(log)
                logs = self.env.cr.dictfetchall()
                if logs:
                    header_appended = False
                    for log in logs:
                        if log['field'] == 'state':
                            if log['old_value_char'] == 'Draft' and log['new_value_char'] == 'Confirmed':
                                break
                            else:
                                continue
                        if not header_appended:
                            final_data.append({'type': 'header', 'name': booking['name']})
                            header_appended = True
                        final_data.append({
                            'type': 'line',
                            'field': log['field_description'],
                            'old': '{:.2f}'.format(log['old_value_float']) if log['old_value_float'] else '0.00',
                            'new': '{:.2f}'.format(log['new_value_float']) if log['new_value_float'] else '0.00',
                            'user': log['name'],
                            'date': log['date'].strftime('%d/%m/%Y')
                         })
        return final_data
