# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class BetaFlatInventory(models.TransientModel):  # change this
    _name = 'beta.flat.inventory'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Flat Inventory')  # change this
    project_ids = fields.Many2many('building')
    project_filter = fields.Selection([('all', 'All Projects'), ('selected', 'Selected Project')], default='all')
    flat_type_ids = fields.Many2many('building.unit')
    state = fields.Selection([('all', 'All'),
                                ('free', 'Available'),
                                ('reserved', 'Booked'),
                                ('sold', 'Sold')], default='all')
    status_filter = fields.Selection([
        ('both', 'Both'),
        ('rtb', 'RTB'),
        ('rts', 'RTS'),
    ], string="State (Flat)", default='both')

    def get_html(self):
        res = self._get_report_data()
        self.template_area = self.env.ref('flat_inventory.report_flat_inventory')._render({
            'table': res,
        })

    def _get_report_data(self):
        table = """<table id="tableId" rules="groups" frame="hsides" border="1"
                   class="table table-bordered table-striped"
                   style="width: 100%;font-size:12px;border-top: 2px solid black;margin-top:10px;">
                <style>.table td{ padding: .8px !important;}</style>
                <thead>
                    <th class="text-right" style="width: 5%">SNo.</th>
                    <th class="text-left" style="width: 30%">Flat</th>
                    <th class="text-left">Wing</th>
                    <th class="text-left">Number</th>
                    <th class="text-left">Flat Type</th>
                    <th class="text-right">Saleable Area</th>
                    <th class="text-right">Flat Cost</th>
                    <th class="text-center" style="width: 6%">RTB/RTS</th>
                    <th class="text-center" style="width: 5%">Hold</th>
                    <th class="text-left">Status</th>
                </thead>
                <tbody>"""
        domain = ''
        if self.project_filter == 'selected':
            domain += " and b.id in " + str(tuple(self.project_ids.ids)).replace(',)', ')')
        if self.flat_type_ids:
            domain += " and bu.id in " + str(tuple(self.flat_type_ids.ids)).replace(',)', ')')
        if self.state != 'all':
            domain += " and pt.state='" + self.state + "'"
            # right after you build `domain` from project/flat_type/state:
        if self.status_filter != 'both':
            domain += " AND pt.flat_state = '%s'" % self.status_filter

        query = """
            select b.name as project, b.id as project_id, pt.id as flat_id, pt.name as flat, rp.name as developer,
            bu.name as flat_type, pt.saleable_area, pt.flat_cost, pt.state, bw.name as wing, pt.flat_number,
                pt.flat_state AS flat_state, pt.on_hold AS on_hold
            from product_template pt 
            left join building b on b.id=pt.building_id
            left join res_partner rp on rp.id=b.partner_id
            left join building_unit bu on bu.id=pt.flat_type
            left join building_wing bw on bw.id=pt.wing_id
            where pt.is_property=True """ + domain + """
            order by pt.name, b.name
        """
        self.env.cr.execute(query)
        data = {}
        sl = 0
        for row in self.env.cr.dictfetchall():
            sl += 1
            if row['state'] == 'free':
                state = 'Available'
            elif row['state'] == 'reserved':
                state = 'Booked'
            elif row['state'] == 'sold':
                state = 'Sold'
            else:
                state = ''
            display_state = (row.get('flat_state') or '').upper()
            display_hold = 'Yes' if row.get('on_hold') else 'No'
            form = self.env.ref('itsys_real_estate.building_unit_form', False)
            flat_link = """
                <a href="#" class="o_beta_report_action"
                   data-res-id="%s"
                   data-model="product.template"
                   data-form="%s">%s
                </a>
            """ % (row['flat_id'], form.id, (row['flat'] or ''))
            if row['project_id'] in data:
                data[row['project_id']]['table'] += """<tr><td class="text-right"><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td class="text-right" style="mso-number-format:'0.00';"><span class="px-2">%s</span></td>
                <td class="text-right" style="mso-number-format:'0.00';"><span class="px-2">%s</span></td>
                <td class="text-center"><span class="px-2">%s</span></td>    <!-- RTB/RTS -->
                <td class="text-center"><span class="px-2">%s</span></td>    <!-- Hold -->
                <td class="text-left"><span class="px-2">%s</span></td></tr>""" % (sl, flat_link,
                                                                                   (row['wing'] or ''),
                                                                                   (row['flat_number'] or ''),
                                                                                    (row['flat_type'] or ''),
                                                                                    "{:.2f}".format(
                                                                                        row['saleable_area']),
                                                                                    "{:.2f}".format(row['flat_cost']),
                                                                                   display_state, display_hold,
                                                                                    state)
                data[row['project_id']]['no_of_flats'] += 1
            else:
                data[row['project_id']] = {'table': """<tr><td/><td class="font-weight-bold"
                 style="padding: .5rem !important;" colspan='9'>%s</td></tr>
                <tr><td class="text-right"><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td><span class="px-2">%s</span></td>
                <td class="text-right" style="mso-number-format:'0.00';"><span class="px-2">%s</span></td>
                <td class="text-right" style="mso-number-format:'0.00';"><span class="px-2">%s</span></td>
                <td class="text-center"><span class="px-2">%s</span></td>    <!-- RTB/RTS -->
                <td class="text-center"><span class="px-2">%s</span></td>    <!-- Hold -->
                <td class="text-left"><span class="px-2">%s</span></td></tr>""" % ((row['project'] or '') + ' (' + (row['developer'] or '') + ')',
                                                                                    sl, flat_link,
                                                                                    (row['wing'] or ''),
                                                                                    (row['flat_number'] or ''),
                                                                                    (row['flat_type'] or ''),
                                                                                    "{:.2f}".format(
                                                                                        row['saleable_area']),
                                                                                        "{:.2f}".format(row['flat_cost']), display_state, display_hold, state),
                                           'no_of_flats': 1
                                           }

        for project in data:
            table += data[project]['table']
            table += """<tr><td/><td class="text-center"><strong class="px-2">Total No. of Flats (%s)</strong>
            </td><td colspan='8'/>""" % data[project]['no_of_flats']
        return table
