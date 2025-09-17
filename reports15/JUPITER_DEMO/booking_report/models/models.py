# -*- coding: utf-8 -*-
from pytz import timezone

from odoo import models, fields, api
from datetime import datetime


class BetaBookingReport(models.TransientModel):  # change this
    _name = 'beta.booking.report'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Booking Report')  # change this
    project_ids = fields.Many2many('building')
    project_filter = fields.Selection([('all', 'All Projects'), ('selected', 'Selected Project')], default='all')
    date_from = fields.Date()
    date_to = fields.Date()
    state = fields.Selection([('confirmed', 'Booked'), ('canceled', 'Canceled'), ('both', 'Both')], default='confirmed')
    consolidate = fields.Boolean()
    region_wise = fields.Boolean(string="Region Wise", default=False)
    region_ids = fields.Many2many('regions', string="Regions")

    @api.onchange('region_wise','project_filter')
    def _onchange_region_wise(self):
        if not self.region_wise:
            self.region_ids = [(5, 0, 0)]
        if self.project_filter == 'all':
            self.project_ids = [(5, 0, 0)]

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
        fmt = "%d/%m/%Y %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        utc_offset_timedelta = datetime.strptime(now_timezone.strftime(fmt), fmt) - datetime.strptime(
            now_utc.strftime(fmt), fmt)
        local_datetime = datetime.strptime(tz_datetime, fmt)
        result_utc_datetime = local_datetime + utc_offset_timedelta
        return result_utc_datetime.strftime('%d/%m/%Y')

    @api.model
    def default_get(self, fields_list):
        res = super(BetaBookingReport, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        # Get employee linked to current user
        employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.user.id)], limit=1
        )
        if employee and self.env.user.has_group('project_transactions.group_region_booking_user') and not self.env.user.has_group('project_transactions.view_all_projects'):
            res['region_wise'] = True
            # prefill only the regions assigned to that employee
            res['region_ids'] = [(6, 0, employee.region_ids.ids)]

        return res

    def get_html(self):
        res = self._get_report_data()
        self.template_area = self.env.ref('booking_report.report_booking_report')._render({
            'table': res,
            'date_start': self.date_from,
            'date_end': self.date_to
        })

    def _get_report_data(self):
        table = """<table id="tableId" rules="groups" frame="hsides" border="1"
                   class="table table-bordered table-striped"
                   style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px; table-layout:auto !important;">
                <style>.table td{ padding: .8px !important;}</style>
                <thead>
                    <th class="text-center">Booking No.</th>
                    <th class="text-center">Project</th>
                    <th class="text-center">Date</th>
                    <th class="text-center">Wing</th>
                    <th class="text-center">Flat</th>
                    <th class="text-center">Number</th>
                    <th class="text-center">Applicant</th>
                    <th class="text-center">Co-Applicant</th>
                    
                    <th class="text-center">Sourcing Manager</th>
                    <th class="text-center">Closing Manager</th>
                    <th class="text-center">Closing TL</th>
                    <th class="text-center">Sourcing TL</th>
                    <th class="text-center">Contact No.</th>
                    <th class="text-center">Email</th>
                    <th class="text-left">Location</th>
                    <th class="text-center">Pin Code</th>
                    <th class="text-center">Source of Booking</th>
                    <th class="text-center">CP Employee</th>
                    <th class="text-center">CP Firm Name</th>
                    <th class="text-center">Configuration</th>
                    <th class="text-center">Carpet Area</th>
                    
                    <th class="text-center">Saleable Sq.Ft</th>
                    <th class="text-center">Sq.Ft Rate</th>
                    <th class="text-center">Flat Cost</th>
                    <th class="text-center">Infra Charge</th>
                    <th class="text-center">Other Charges</th>
                    <th class="text-center">Agreement Value</th>
                    <th class="text-center">Source of Funding</th>
                    <th class="text-center">Sub Source</th>
                    <th class="text-center">Banker</th>
                    
                    <th class="text-center">Amount Received</th>
                    <th class="text-center">Amount %</th>
                    
                    <th class="text-center">GST</th>
                    <th class="text-center">Stamp Duty</th>
                    <th class="text-center">Registration Charge</th>
                    <th class="text-center">All Inclusive Amount</th>
                    <th class="text-center">Advance Amount</th>
                    
                    <th class="text-center">CP%</th>
                    <th class="text-center">CP Brokerage</th>
                    <th class="text-center">Spot Amount</th>
                    <th class="text-center">Registration Status</th>
                    <th class="text-center">Date of Registration</th>
                    <th class="text-center">Status</th>
                    <th class="text-center">Cancellation Date</th>
                    <th class="text-center">Cancellation Reason</th>
                </thead>
                <tbody>"""
        form = self.env.ref('itsys_real_estate.unit_reservation_form_view', False)
        date_from = self.get_actual_date(self.date_from.strftime('%Y-%m-%d') + " 00:00:00")
        date_to = self.get_actual_date(self.date_to.strftime('%Y-%m-%d') + " 23:59:59")
        domain = " ur.date>='" + date_from + "' and ur.date<='" + date_to + "'"
        consolidate_domain = " ur.cancellation_date>='" + self.date_from.strftime('%Y-%m-%d') + "' and ur.cancellation_date<='" + self.date_to.strftime('%Y-%m-%d') + "'"
        if self.project_filter == 'selected':
            domain += " and b.id in " + str(tuple(self.project_ids.ids) or '(0)').replace(',)', ')')
            consolidate_domain += " and b.id in " + str(tuple(self.project_ids.ids) or '(0)').replace(',)', ')')
        if self.state in ('both', 'canceled') or self.consolidate:
            domain += " and ur.state in ('confirmed', 'canceled') "
            consolidate_domain += " and ur.state = 'canceled' "
        elif self.state == 'confirmed':
            domain += " and ur.state in ('confirmed', 'canceled') "
            # domain += " and ur.state = '%s' " % str(self.state)

        # Check if region_ids is not empty
        if self.region_wise:
            region_ids = self.region_ids.ids
            if region_ids:
                if len(region_ids) == 1:
                    # Single region: use equality
                    domain += f" and b.region_id = {region_ids[0]}"
                    consolidate_domain += f" and b.region_id = {region_ids[0]}"
                else:
                    # Multiple regions: use IN clause
                    region_ids_tuple = tuple(region_ids)
                    domain += f" and b.region_id in {region_ids_tuple}"
                    consolidate_domain += f" and b.region_id in {region_ids_tuple}"

        query = """
            select ur.id as booking_id, ur.name as booking, ur.date as booking_date,
            b.name as project, bu.name as configuration, pt.name as flat,
            p.name as applicant, cop.name as co_applicant, ur.state as booking_state,
            ur.total_saleable_area as saleable, ur.sq_ft_rate as rate,
            ur.flat_cost_real as flat_cost, ur.infra_charge as infra,
            ur.other_charges as other, ur.flat_cost as agreement,
            ur.stamp_duty as stamp, ur.legal_charge as legal,
            ur.registration_charge as registration, ur.net_amount, ur.advance_amount as advance,
            bw.name as wing, pt.flat_number, sm.name as sourcing_manager,
            cm.name as closing_manager, stl.name as sourcing_tl,
            ctl.name as closing_tl, UPPER(ur.source_of_booking) as source_of_booking,
            cp_emp.name as cp_employee, cp_firm.name as cp_firm, ur.carpet_area,
            ur.if_loan, ur.preferred_bank as sub_source, ur.bank_person as banker,
            ur.cp_brokerage, ur.spot_amount, b.pin_code, ur.cancellation_date,
            p.mobile as mobile, p.email, b.site_address, pr.registration_date, 
            pr.state as registration_state, sum(rps.ocr) + sum(rps.bank_payment) as amount_received,
            %s as index, b.region_id as region_id, r.name as region_name,
            bcr.name as cancellation_reason, b.cp_brokerage_percentage as cp_percentage,
            CASE 
                WHEN ur.state = 'confirmed' AND pr.state = 'confirmed' THEN 'Registered' 
                WHEN ur.state = 'confirmed' AND (pr.state IS NULL OR pr.state != 'confirmed') THEN 'Booked' 
                WHEN ur.state = 'canceled' THEN 'cancelled' 
                ELSE 'draft' 
            END AS registration_status 
            from unit_reservation ur 
            left join building b on b.id=ur.building
            left join res_partner p on p.id=ur.partner_id
            left join res_partner cop on cop.id=ur.co_partner_id
            left join building_unit bu on bu.id=ur.flat_type
            left join product_template pt on pt.id=ur.building_unit
            left join building_wing bw on bw.id=pt.wing_id
            left join hr_employee sm on sm.id = ur.sourcing_manager_id
            left join hr_employee cm on cm.id = ur.closing_manager_id
            left join hr_employee stl on stl.id = ur.sourcing_tl_id
            left join hr_employee ctl on ctl.id = ur.closing_tl_id
            left join res_partner cp_emp on cp_emp.id = ur.cp_employee_id
            left join res_partner cp_firm on cp_firm.id = ur.cp_id
            left join project_registration pr on pr.booking_id = ur.id and pr.state not in ('draft','canceled')
            left join reservation_payment_schedule rps on rps.monitoring_reservation_id = ur.id
            left join regions r on r.id = b.region_id
            left join booking_cancellation_reason bcr on bcr.id=ur.cancellation_reason
            where %s group by ur.id, b.id, bu.id, pt.id, p.id, 
            cop.id, bw.id, sm.id, cm.id, stl.id, ctl.id, cp_emp.id, cp_firm.id, pr.id, r.id, bcr.id
        """

        if self.region_wise:
            # If region_wise is True, order by region_name and booking_id
            query += " order by r.name, ur.id"
        # else:
        #     query += " order by ur.id"

        rows = []
        if self.state != 'canceled':
            qry = query % ('0', domain)
            self.env.cr.execute(query % ('0', domain))
            rows += self.env.cr.dictfetchall()
        totals = {
            'count': 0,
            'flat_cost': 0,
            'av': 0,
            'amount': 0,
        }
        if self.consolidate or self.state != 'confirmed':
            qry = query % ('1', consolidate_domain)
            # Step 2: Execute the query using the variable
            # print("Query:", qry)
            self.env.cr.execute(qry)
            rows += self.env.cr.dictfetchall()
            if self.state == 'both':
                table += "<tr><td colspan='42' style='padding-top: 1rem !important; font-size: 15px;'><strong style='text-wrap: nowrap;position: sticky; left: 50%; display: inline-block;height: 24px;'><span style='transform: translateX(-50%); position: absolute;'>Gross Booking</span></strong></td></tr>"
        cancelled_header_added = False
        booked_count = 0
        flat_cost_count = 0
        agreement_value_count = 0
        all_exclusive_amount_count = 0
        current_region = None
        row_index = 0

        for row in rows:
            row_index = row['index']
            if self.state == 'both' and row['index'] == 1 and not cancelled_header_added:
                table += """
                    <tr class="font-weight-bold">
                        <td class="text-center" colspan="8">(Count: %s)</td>
                        <td colspan="15"/>
                        <td class="text-right">%s</td>
                        <td colspan="2"/>
                        <td class="text-right">%s</td>
                        <td colspan="8"/>
                        <td class="text-right">%s</td>
                        <td colspan="9"/>
                    </tr>
                """ % (
                    totals['count'],
                    "{:.2f}".format(totals['flat_cost']),
                    "{:.2f}".format(totals['av']),
                    "{:.2f}".format(totals['amount']),
                )
                booked_count = totals['count']
                flat_cost_count = totals['flat_cost']
                agreement_value_count = totals['av']
                all_exclusive_amount_count = totals['amount']
                totals['count'] = 0
                totals['flat_cost'] = 0
                totals['av'] = 0
                totals['amount'] = 0
                table += "<tr><td colspan='42' style='padding-top: 1rem !important; font-size: 15px;'><strong style='position: sticky; left: 50%; display: inline-block;height: 24px;'><span style='transform: translateX(-50%); position: absolute;'>Cancelled</span></strong></td></tr>"
                cancelled_header_added = True
                current_region = None
            row_color = ''
            if (self.state in ('both', 'confirmed') or self.consolidate) and row['booking_state'] == 'canceled' and not cancelled_header_added:
                row_color = 'class="text-warning"'

            region_wise = self.region_wise
            if region_wise and current_region != row['region_name']:
                current_region = row['region_name']
                if current_region is not None:  # Skip adding header for the first region
                    table += f""" <tr> <td colspan='42' style='padding-top: 1rem !important; font-size: 15px;'> <strong style='text-wrap: nowrap; position: sticky; left: 3%; display: inline-block; height: 14px;'> <span style='transform: translateX(-25%); position: absolute;'>{current_region}</span> </strong> </td> </tr> """

            table += """
                <tr %s>
                    <td class="text-center">
                        <a href="#" class="o_beta_report_action"
                           data-res-id="%s"
                           data-model="unit.reservation"
                           data-form="%s">%s
                        </a>
                    </td>
                    <td class="text-left">%s</td>
                    <td class="text-center">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-center">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-right">%s</td>
                    
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-left">%s</td>
                    
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    
                    <td class="text-right">%s</td>
                    <td class="text-right">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-center">%s</td>
                    <td class="text-left">%s</td>
                    <td class="text-center">%s</td>
                    <td class="text-left">%s</td>
                </tr>
            """ % (
                row_color,
                row['booking_id'],
                form.id,
                row['booking'],
                row['project'],
                self.get_current_inv_date(row['booking_date'].strftime('%d/%m/%Y %H:%M:%S')),
                row['wing'] or '',
                row['flat'],
                row['flat_number'] or '',
                row['applicant'],
                row['co_applicant'] or '',

                row['sourcing_manager'] or '',
                row['closing_manager'] or '',
                row['closing_tl'] or '',
                row['sourcing_tl'] or '',
                row['mobile'] or '',
                row['email'] or '',
                row['site_address'] or '',
                row['pin_code'] or '',
                row['source_of_booking'] or '',
                row['cp_employee'] or '',
                row['cp_firm'] or '',
                row['configuration'],
                "{:.2f}".format(row['carpet_area'] or 0),

                "{:.2f}".format(row['saleable'] or 0),
                "{:.2f}".format(row['rate'] or 0),
                "{:.2f}".format(row['flat_cost'] or 0),
                "{:.2f}".format(row['infra'] or 0),
                "{:.2f}".format(row['other'] or 0),
                "{:.2f}".format(row['agreement'] or 0),
                'Bank' if row['if_loan'] else 'Self',
                row['sub_source'] or '',
                row['banker'] or '',

                "{:.2f}".format(row['amount_received'] or 0),
                "{:.2f}".format((((row['amount_received'] or 0) * 100) / row['agreement']) if row['agreement'] != 0 else 0),

                "{:.2f}".format(row['legal'] or 0),
                "{:.2f}".format(row['stamp'] or 0),
                "{:.2f}".format(row['registration'] or 0),
                "{:.2f}".format(row['net_amount'] or 0),
                "{:.2f}".format(row['advance'] or 0),

                "{:.2f}".format(row['cp_percentage'] or 0),
                "{:.2f}".format(row['cp_brokerage'] or 0),
                "{:.2f}".format(row['spot_amount'] or 0),
                'Done' if row['registration_state'] in ('confirmed', 'invoiced') else 'Pending',
                row['booking_date'].strftime('%d/%m/%Y') if row['booking_date'] and row['registration_state'] in ('confirmed', 'invoiced') else '',
                row['registration_status'],
                row['cancellation_date'].strftime('%d/%m/%Y') if row['cancellation_date'] and row['booking_state'] == 'canceled' else '',
                row['cancellation_reason'] if row['cancellation_reason'] else '',
            )
            totals['count'] += 1
            totals['flat_cost'] += row['flat_cost'] or 0
            totals['av'] += row['agreement'] or 0
            totals['amount'] += row['net_amount'] or 0
        table += """
            <tr class="font-weight-bold">
                <td class="text-center" colspan="8">(Count: %s)</td>
                <td colspan="15"/>
                <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                <td colspan="2"/>
                <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                <td colspan="8"/>
                <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                <td colspan="9"/>
            </tr>
        """ % (
            totals['count'],
            "{:.2f}".format(totals['flat_cost']),
            "{:.2f}".format(totals['av']),
            "{:.2f}".format(totals['amount']),
        )
        if self.state == 'both':
            table += """
                <tr class="font-weight-bold">
                    <td class="text-center" colspan="8">(Net: %s)</td>
                    <td class="text-center" colspan="15"></td>
                    <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                    <td colspan="2"></td>
                    <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                    <td colspan="8"></td>
                    <td class="text-right" style="mso-number-format:'0.00';">%s</td>
                    <td colspan="9"/>
                </tr>
            """ % ((booked_count - totals['count']) if booked_count or row_index == 1 else totals['count'], "{:.2f}".format(flat_cost_count - totals['flat_cost']) if flat_cost_count or row_index == 1 else "{:.2f}".format(totals['flat_cost']), "{:.2f}".format(agreement_value_count - totals['av']) if agreement_value_count or row_index == 1 else "{:.2f}".format(totals['av']), "{:.2f}".format(all_exclusive_amount_count - totals['amount']) if all_exclusive_amount_count or row_index == 1 else "{:.2f}".format(totals['amount']))
        return table
