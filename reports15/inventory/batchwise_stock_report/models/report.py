from odoo import models, api,fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning
import pytz

class ReportBatchWiseProduct(models.TransientModel):
    _name = 'batch.product'
    _inherit = 'beta.reports'
    _description = 'Batchwise Stock Report'

    name = fields.Char(default='Report')  # change this
    date = fields.Date(string="Date")
    location = fields.Many2many('stock.location')

    @api.model
    def default_get(self, fields_list):
        res = super(ReportBatchWiseProduct, self).default_get(fields_list)
        today = datetime.today()
        res['date'] = today
        loc_default = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        res['location'] = loc_default.lot_stock_id
        return res

    def get_report_values(self, data=None):
        date = False
        branch = ''
        if 'branch_id' in self.env.user._fields:
            branch_obj = self.env['res.branch']
            if data['branch_ids']:
                for locati in data['branch_ids']:
                    branch += branch_obj.browse(locati).name + ","

        if data['date']:
            try:
                date = datetime.strptime(data['date'], "%Y-%m-%d").strftime('%d/%m/%Y')
            except TypeError:
                raise Warning("Invalid Date Format")

        return {
            'data': data,
            'date': date,
            'type': data['type'],
            'branch_name': data['branch_name'],
            'company_ids': data['company_ids'],
            'location_ids': data['location_ids'],
            'lines': self.get_batchwise_stock(data),
        }

    def get_batchwise_stock(self, data):
        doc = []
        product_final = []
        move_lines = ''
        if data['date']:
            date = data['date']
            datet = date + ' 23:59:59'
            datef = date + ' 00:00:00'
            move_l = self.env['stock.move.line'].search(
                [('date', '<=', datet), ('company_id', 'in', data['location_ids']), ('state', '=', 'done')]).ids
            location = self.env['stock.warehouse'].search([('company_id', 'in', data['location_ids'])]).lot_stock_id.ids
            transfer_out = self.env['stock.move.line'].search(
                [('date', '<=', datet), ('company_id', 'not in', data['location_ids']), ('location_id', 'in', location),
                 ('state', '=', 'done')]).ids
            transfer_in = self.env['stock.move.line'].search(
                [('date', '<=', datet), ('company_id', 'not in', data['location_ids']),
                 ('location_dest_id', 'in', location),
                 ('state', '=', 'done')]).ids
            # move_l = self.env['stock.move.line'].search(
            #     [('date', '>=', datef),('date', '<=', datet), ('branch_id', 'in', data['location_ids']), ('state', '=', 'done')]).ids
            #
            # location = self.env['stock.warehouse'].search([('branch_id', 'in', data['location_ids'])]).lot_stock_id.ids
            # transfer_out = self.env['stock.move.line'].search(
            #     [('date', '>=', datef),('date', '<=', datet), ('branch_id', 'not in', data['location_ids']), ('location_id', 'in', location),
            #      ('state', '=', 'done')]).ids
            # transfer_in = self.env['stock.move.line'].search(
            #     [('date', '>=', datef),('date', '<=', datet), ('branch_id', 'not in', data['location_ids']),
            #      ('location_dest_id', 'in', location),
            #      ('state', '=', 'done')]).ids
            ids = move_l + transfer_out + transfer_in
            # print(ids,"ids")
            # ids = move_l

            move_lines = self.env['stock.move.line'].search([('id', 'in', ids)], order="product_id, lot_id").sorted(
                lambda line: line.product_id.name)

        if move_lines:

            for line in move_lines:
                if line.date:
                    try:
                        date = line.date.astimezone(pytz.timezone(self.env.context.get('tz')))
                    except:
                        raise Warning("Please set User Time Zone")
                    tax = 0
                    for i in line.product_id.taxes_id:
                        for j in i.children_tax_ids:
                            tax += j.amount
                doc.append({
                    'product_id': line.product_id.id,
                    'date': date,
                    'product_name': line.product_id.name,
                    'lot_id': line.lot_id.id,
                    'lot_name': line.lot_id.name if line.lot_id else 'Not Tracking Product',
                    'qty': float(line.qty_done),
                    'location': line.location_id.id,
                    'dest_location': line.location_dest_id.id,
                    'expiry': line.lot_id.expiry if line.lot_id else None,
                    'prate': line.lot_id.p_rate if line.lot_id else line.product_id.list_price,
                    'rate': line.lot_id.sales_rate if line.lot_id else line.product_id.list_price,
                    'tax': tax,
                    'pcs': line.lot_id.packing.name if line.lot_id else line.product_id.uom_id.name,
                    'unit_rate': line.lot_id.mrp if line.lot_id else line.product_id.list_price,
                    'factor': line.lot_id.packing.factor if line.lot_id else line.product_id.uom_id.factor,
                    'uom_type': line.lot_id.packing.uom_type if line.lot_id else line.product_id.uom_id.uom_type,
                    'uom_id': line.lot_id.product_uom_id.name if line.lot_id else line.product_id.uom_id.name
                })

        if len(doc) > 0:
            i = 0
            pid = doc[0]['product_id']
            lot_id = doc[0]['lot_id']
            out_qty = 0
            in_qty = 0
            qty = 0
            count = 0
            rate_update = False
            taxable_value_total = 0
            tax_value_total = 0
            mrp_value_total = 0
            cost_value_total = 0
            mrp_with_disc_total = 0
            product_final.append({'name': 5,
                                  'product_name': doc[0]['product_name'],
                                  'lot_name': None,
                                  'qty': None,
                                  'expiry': None,
                                  'prate': None,
                                  'rate': None,
                                  'tax': None,
                                  'pcs': None,
                                  'unit_rate': None,
                                  'taxable_value': None,
                                  'tax_value': None,
                                  'mrp_value': None,
                                  'cost_value': None,
                                  })

            while i < len(doc):
                if pid == doc[i]['product_id']:
                    if lot_id == doc[i]['lot_id']:
                        if doc[i]['uom_type'] == 'smaller':
                            factor = 1
                        else:
                            factor = doc[i]['factor']
                        sales_rate = doc[i]['rate']
                        if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                            out_qty += doc[i]['qty']
                        elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                            in_qty += doc[i]['qty']
                        qty = in_qty - out_qty
                        tax = doc[i]['tax']
                        prate = doc[i]['prate']
                        lot_name = doc[i]['lot_name']
                        expiry = doc[i]['expiry']
                        pcs = doc[i]['pcs']
                        unit_rate = doc[i]['unit_rate']
                        pname = doc[i]['product_name']
                        uom_type = doc[i]['uom_type']
                        uom_id = doc[i]['uom_id']
                    else:
                        if qty < 1:
                            count += 1
                        if qty != 0:
                            if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                                rate_update = self.env['rate.update.line'].search(
                                    [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', datet),
                                     ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')], order='id',
                                    limit=1)

                            if rate_update:
                                ur = rate_update.c_mrp * factor
                                taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                            else:
                                print(factor,doc[i]['product_name'],"484585")
                                taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)

                            tax_value = (taxable * tax) / 100
                            mrp_value = taxable + tax_value
                            cost_value = (prate / (1 / factor)) * qty
                            taxable_value_total += taxable
                            tax_value_total += tax_value
                            mrp_value_total += mrp_value
                            cost_value_total += cost_value
                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'lot_name': lot_name,
                                                  'qty': qty,
                                                  'expiry': expiry,
                                                  'prate': prate,
                                                  'rate': rate_update.c_mrp if rate_update else sales_rate,
                                                  'tax': tax,
                                                  'pcs': pcs,
                                                  'unit_rate': (rate_update.c_mrp * (
                                                      factor if uom_type != 'smaller' else 1)) if rate_update else unit_rate,
                                                  'taxable_value': taxable,
                                                  'tax_value': tax_value,
                                                  'mrp_value': mrp_value,
                                                  'cost_value': cost_value,
                                                  })

                        lot_id = doc[i]['lot_id']
                        out_qty = 0
                        in_qty = 0
                        qty = 0
                        if doc[i]['uom_type'] == 'smaller':
                            factor = 1
                        else:
                            factor = doc[i]['factor']
                        sales_rate = doc[i]['rate']
                        if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                            out_qty += doc[i]['qty']
                        elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                            in_qty += doc[i]['qty']
                        qty = in_qty - out_qty
                        tax = doc[i]['tax']
                        prate = doc[i]['prate']
                        lot_name = doc[i]['lot_name']
                        expiry = doc[i]['expiry']
                        pcs = doc[i]['pcs']
                        unit_rate = doc[i]['unit_rate']
                        pname = doc[i]['product_name']
                        uom_type = doc[i]['uom_type']
                        uom_id = doc[i]['uom_id']

                else:

                    if qty < 1:
                        count += 1
                    if qty != 0:
                        if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                            rate_update = self.env['rate.update.line'].search(
                                [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', datet),
                                 ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')], order='id',
                                limit=1)

                        if rate_update:
                            ur = rate_update.c_mrp * factor
                            taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                        else:
                            taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                        tax_value = (taxable * tax) / 100
                        mrp_value = taxable + tax_value
                        cost_value = (prate / (1 / factor)) * qty
                        taxable_value_total += taxable
                        tax_value_total += tax_value
                        mrp_value_total += mrp_value
                        cost_value_total += cost_value
                        product_final.append({'name': 1,
                                              'product_name': None,
                                              'lot_name': lot_name,
                                              'qty': qty,
                                              'expiry': expiry,
                                              'prate': prate,
                                              'rate': rate_update.c_mrp if rate_update else sales_rate,
                                              'tax': tax,
                                              'pcs': pcs,
                                              'unit_rate': rate_update.c_mrp * factor if rate_update else unit_rate,
                                              'taxable_value': taxable,
                                              'tax_value': tax_value,
                                              'mrp_value': mrp_value,
                                              'cost_value': cost_value,
                                              })
                    if product_final[-1]['product_name'] == pname:
                        product_final.pop()

                    pid = doc[i]['product_id']
                    lot_id = doc[i]['lot_id']
                    out_qty = 0
                    in_qty = 0
                    qty = 0
                    pname = doc[i]['product_name']
                    product_final.append({'name': 5,
                                          'product_name': pname,
                                          'lot_name': None,
                                          'qty': None,
                                          'expiry': None,
                                          'prate': None,
                                          'rate': None,
                                          'tax': None,
                                          'pcs': None,
                                          'sales_disc': None,
                                          'unit_rate': None,
                                          'taxable_value': None,
                                          'tax_value': None,
                                          'mrp_value': None,
                                          'cost_value': None,
                                          'mrp_with_disc': None,
                                          })

                    if lot_id == doc[i]['lot_id']:
                        if doc[i]['uom_type'] == 'smaller':
                            factor = 1
                        else:
                            factor = doc[i]['factor']
                        sales_rate = doc[i]['rate']
                        if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                            out_qty += doc[i]['qty']
                        elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                            in_qty += doc[i]['qty']
                        qty = in_qty - out_qty
                        tax = doc[i]['tax']
                        prate = doc[i]['prate']
                        lot_name = doc[i]['lot_name']
                        expiry = doc[i]['expiry']
                        pcs = doc[i]['pcs']
                        unit_rate = doc[i]['unit_rate']
                        pname = doc[i]['product_name']
                        uom_type = doc[i]['uom_type']
                        uom_id = doc[i]['uom_id']
                    else:
                        if qty < 1:
                            count += 1
                        if qty != 0:
                            if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                                rate_update = self.env['rate.update.line'].search(
                                    [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', datet),
                                     ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')], order='id',
                                    limit=1)

                            if rate_update:
                                ur = rate_update.c_mrp * factor
                                taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                            else:
                                taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                            tax_value = (taxable * tax) / 100
                            mrp_value = taxable + tax_value
                            cost_value = (prate / (1 / factor)) * qty
                            taxable_value_total += taxable
                            tax_value_total += tax_value
                            mrp_value_total += mrp_value
                            cost_value_total += cost_value

                            product_final.append({'name': 1,
                                                  'product_name': None,
                                                  'lot_name': lot_name,
                                                  'qty': qty,
                                                  'expiry': expiry,
                                                  'prate': prate,
                                                  'rate': rate_update.c_mrp if rate_update else sales_rate,
                                                  'tax': tax,
                                                  'pcs': pcs,
                                                  'unit_rate': rate_update.c_mrp * factor if rate_update else unit_rate,
                                                  'taxable_value': taxable,
                                                  'tax_value': tax_value,
                                                  'mrp_value': mrp_value,
                                                  'cost_value': cost_value,
                                                  })

                        lot_id = doc[i]['lot_id']
                        out_qty = 0
                        in_qty = 0
                        qty = 0
                        if doc[i]['uom_type'] == 'smaller':
                            factor = 1
                        else:
                            factor = doc[i]['factor']
                        sales_rate = doc[i]['rate']
                        if doc[i]['location'] in location and doc[i]['dest_location'] not in location:
                            out_qty += doc[i]['qty']
                        elif doc[i]['dest_location'] in location and doc[i]['location'] not in location:
                            in_qty += doc[i]['qty']
                        qty = in_qty - out_qty
                        tax = doc[i]['tax']
                        prate = doc[i]['prate']
                        lot_name = doc[i]['lot_name']
                        expiry = doc[i]['expiry']
                        pcs = doc[i]['pcs']
                        unit_rate = doc[i]['unit_rate']
                        pname = doc[i]['product_name']
                        uom_type = doc[i]['uom_type']
                        uom_id = doc[i]['uom_id']

                i = i + 1

            if qty != 0:
                if self.env['ir.model'].search([('model', '=', 'rate.update.line')], limit=1):
                    rate_update = self.env['rate.update.line'].search(
                        [('prod_lot_id', '=', lot_id), ('move_id.date', '>=', datet),
                         ('move_id.state', '=', 'done'), ('move_id.is_onhand', '=', 'True')], order='id', limit=1)

                if rate_update:
                    ur = rate_update.c_mrp * factor
                    taxable = ((ur * qty) / (1 / factor) * 100) / (100 + tax)
                else:
                    print(factor, pname, "33333")
                    taxable = ((unit_rate * qty) / (1 / factor) * 100) / (100 + tax)
                tax_value = (taxable * tax) / 100
                mrp_value = taxable + tax_value
                cost_value = (prate / (1 / factor)) * qty

                taxable_value_total += taxable
                tax_value_total += tax_value
                mrp_value_total += mrp_value
                cost_value_total += cost_value
                product_final.append({'name': 1,
                                      'product_name': None,
                                      'lot_name': lot_name,
                                      'qty': qty,
                                      'expiry': expiry,
                                      'prate': prate,
                                      'rate': sales_rate,
                                      'tax': tax,
                                      'pcs': pcs,
                                      'unit_rate': rate_update.m_mrp * factor if rate_update else unit_rate,
                                      'taxable_value': taxable,
                                      'tax_value': tax_value,
                                      'mrp_value': mrp_value,
                                      'cost_value': cost_value,
                                      })
            if product_final[-1]['product_name'] == pname:
                product_final.pop()

            product_final.append({'name': 10,
                                  'product_name': None,
                                  'lot_name': 'Grand Total',
                                  'qty': None,
                                  'expiry': None,
                                  'prate': None,
                                  'rate': None,
                                  'tax': None,
                                  'pcs': None,
                                  'unit_rate': None,
                                  'taxable_value': taxable_value_total,
                                  'tax_value': tax_value_total,
                                  'mrp_value': mrp_value_total,
                                  'cost_value': cost_value_total,
                                  })

            print(count)
            return {
                'date': date,
                'docsnn': product_final,
            }


    def get_html(self):
        res = self._get_report_data(date=self.date.strftime('%Y-%m-%d'))
        self.template_area= self.env.ref('batchwise_stock_report.report_batchwise_stock')._render(
            {'lines': res['lines']['lines'],
             'date':self.date.strftime('%d-%m-%Y'),
             'data': res['lines']['data'],
             'type': res['lines']['type'],
             'branch_name': res['lines']['branch_name']
             })
        return res


    def _get_report_data(self, date=False):
        tk = self.env['product.product'].search([], order='name')
        is_branch = False
        branch_name = ''
        companies = self._context.get('allowed_company_ids')
        if 'branch_id' in self.env.user._fields:
            branch = self._context.get('branch')
            location = self.env['stock.warehouse'].search([('branch_id', '=', branch)])
            branch_default = self.env['res.branch'].search([('id', '=', self.env.user.branch_id.id)])
            company_ids = self.env.user.branch_ids.ids
            company = self.env['res.branch'].search(
                [('id', 'in', self.env.user.branch_ids.ids)])
            is_branch = True
        else:
            location = self.env['stock.warehouse'].search([('company_id', 'in', companies)])
            branch_default = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            company_ids = self.env.user.company_ids.ids
            company = self.env['res.company'].search([('id', 'in', self.env.user.company_ids.ids)], order='name')
            is_branch = False

        rl = ''
        # if report_location:
        #     rl = [int(i) for i in report_location]

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['res.branch'].search([('id', 'in', rl)])
                branch_name = ', '.join(branch.mapped('name'))

        data = {
            'date': date if date else False,
            'branch_default': branch_default,
            'branch_ids': company_ids,
            'company_ids': company_ids,
            'branch_name': branch_name,
             'type': type if type else False,
            'location_ids': rl if rl else (branch_default.id,),

        }
        dat = self.get_report_values(data=data)

        lo = {}

        for l in company:
            if l.id != branch_default.id:
                lo[l.id] = l.name
        return {
            'lines': dat,
            'branch': lo,
            'bid': branch_default.id,
            'bname': branch_default.name,
            'is_branch': is_branch,
        }
