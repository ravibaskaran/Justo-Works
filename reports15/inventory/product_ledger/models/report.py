# -*- coding: utf-8 -*-
from odoo import models, api,fields
from datetime import datetime,timedelta
from odoo.exceptions import Warning
from pytz import timezone

class StockMove(models.Model):
    _inherit='stock.move'

    inventory_id = fields.Many2one('stock.inventory.line', 'Inventory')

class ReportProductLedger(models.TransientModel):
    _name = 'product.ledger'
    _inherit = 'beta.reports'
    _description = 'Product Ledger'

    name = fields.Char(default='Report')  # change this
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    horizontal = fields.Boolean(string="Horizontal")
    product = fields.Many2many('product.product')
    location=fields.Many2many('stock.location')

    @api.model
    def default_get(self, fields_list):
        res = super(ReportProductLedger, self).default_get(fields_list)
        today = datetime.today()
        if today.month < 5:
            fin_start = str(today.year - 1) + '-04-01'
        else:
            fin_start = str(today.year) + '-04-01'
        res['date_from'] = fin_start
        res['date_to'] = today

        loc_default = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        res['location'] =loc_default.lot_stock_id
        return res

    def get_report_values(self, data=None):
        date_from = date_to = False
        product_obj = self.env['product.product']
        loc_obj = self.env['stock.location']
        products = ''
        location = ''

        if data['date_from'] and data['date_to']:
            date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(data['date_to'], "%Y-%m-%d")
            days = date_to - date_from



            for i in range(days.days + 1):
                day = date_from + timedelta(days=i)
                date = day.strftime("%Y-%m-%d")
                data['date'] = date
            date_from = date_from.strftime('%d/%m/%Y')
            date_to = date_to.strftime('%d/%m/%Y')

        if data['product_ids']:
            for product in data['product_ids']:
                products += product_obj.browse(product).name + ", "
        if data['location_ids']:
            for locati in data['location_ids']:
                location += loc_obj.browse(locati).complete_name + ","
        return {
            'data': data,
            'date_from': date_from,
            'date_to': date_to,
            'branch_name': data['branch_name'],
            'products': products,
            'location': location,
            'lines': self.get_product_ledger(data),
        }
        # print(lines)
    def get_product_ledger(self, data):
        move_line_obj = self.env['stock.move.line']
        move_obj = self.env['account.move']
        datas = {}
        if data['date_from'] and data['date_to'] and data['location_ids']:
            if data['location_ids']:
                domain = [('state', '=', 'done'), ('product_id.type', 'in', ['product']),
                          ('date', '>=', self.get_actual_date(data['date_from'] + " 00:00:00")),
                          ('date', '<=', self.get_actual_date(data['date_to'] + " 23:59:59")), '|',
                          ('location_id', 'in', data['location_ids']), ('location_dest_id', 'in', data['location_ids'])]

            else:
                domain = [('state', '=', 'done'), ('product_id.type', 'in', ['product']),
                          ('date', '>=', self.get_actual_date(data['date_from'] + " 00:00:00")),
                          ('date', '<=', self.get_actual_date(data['date_to'] + " 23:59:59"))]

            if data['product_ids']:
                domain.append(('product_id', 'in', data['product_ids']))
            if data.get('allowed_company_ids'):
                domain.append(('company_id', 'in', data.get('allowed_company_ids')))
            movelines = move_line_obj.search(domain, order="date asc")
            # for1st = time.time()
            for line in movelines:
                type = ''
                name = ''
                partner = ''
                in_qty = 0
                out_qty = 0
                if line.location_id.usage == 'supplier':
                    in_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                    if line.picking_id:
                        partner = line.picking_id.partner_id.name
                        try:
                            if line.picking_id.purchase_id:
                                name = line.picking_id.purchase_id.name
                                type = 'Purchase'
                        except TypeError:
                            pass
                        # try:
                        if 'direct_transaction_type' in line.picking_id._fields and line.picking_id.direct_transaction_type == 'purchase':
                            type = 'Purchase'
                            qury = "select name from account_move where direct_move_picking_id=" + str(line.picking_id.id)
                            # name = move_obj.search([('direct_move_picking_id','=', line.picking_id.id)]).name
                            self.env.cr.execute(qury)
                            fetch_data = self.env.cr.fetchall()
                            if fetch_data and fetch_data[0] and fetch_data[0][0]:
                                name = fetch_data[0][0]
                            else:
                                name = False
                            # name = self.env.cr.fetchall()[0][0] if self.env.cr.fetchall() else False
                            ##print(qury, line.picking_id.id, name)
                        # except Exception:
                        #     pass
                        if not name:
                            name = line.picking_id.name
                    if not type:
                        type = 'In Transfer'
                if line.location_id.usage == 'internal':
                    out_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                    # print(line.location_dest_id.id,data['location_ids'],'[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]')
                    if [line.location_dest_id.id] == data['location_ids']:
                        in_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                        out_qty = 0
                    if line.location_dest_id.usage == 'production':
                        type = 'Production'
                        try:
                            name = line.production_id.name
                        except Exception:
                            name = line.reference
                    elif line.location_dest_id.usage == 'customer':
                        if line.picking_id:
                            partner = line.picking_id.partner_id.name
                            try:
                                if line.picking_id.sale_id:
                                    name = line.picking_id.sale_id.name
                                    type = 'Sale'
                            except Exception:
                                pass
                            # try:
                            if 'direct_transaction_type' in line.picking_id._fields and line.picking_id.direct_transaction_type == 'sale':
                                type = 'Sale'
                                qury = "select name from account_move where direct_move_picking_id=" + str(
                                    line.picking_id.id)

                                self.env.cr.execute(qury)
                                fetch_data = self.env.cr.fetchall()
                                if fetch_data and fetch_data[0] and fetch_data[0][0]:
                                    name = fetch_data[0][0]
                                else:
                                    name = False

                            if not name:
                                name = line.picking_id.name
                        if not type:
                            type = 'Out Transfer'
                    elif line.location_dest_id.usage == 'supplier':
                        if line.picking_id:
                            partner = line.picking_id.partner_id.name
                            try:
                                if line.picking_id.purchase_id:
                                    name = line.picking_id.purchase_id.name + "/Return"
                                    type = 'Purchase Return'
                            except Exception:
                                pass
                            try:
                                if line.picking_id.direct_transaction_type == 'purchase':
                                    type = 'Purchase Return'
                                    qury = "select name from account_move where direct_move_picking_id=" + str(
                                        line.picking_id.id)

                                    self.env.cr.execute(qury)
                                    fetch_data = self.env.cr.fetchall()
                                    if fetch_data and fetch_data[0] and fetch_data[0][0]:
                                        name = fetch_data[0][0]
                                    else:
                                        name = False

                            except Exception:
                                pass
                        if not type:
                            type = 'Return'
                        if not name:
                            name = 'Return - ' + line.reference
                    elif line.location_dest_id.usage == 'inventory':
                        type = 'Adjustment'
                        name = line.reference
                if line.location_id.usage == 'production':
                    in_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                    type = 'Production'
                    name = line.reference
                if line.location_id.usage == 'inventory':
                    in_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                    type = 'Adjustment'
                    name = line.reference
                if line.location_id.usage == 'customer':
                    in_qty = line.product_uom_id._compute_quantity(line.qty_done, line.product_id.uom_id)
                    if line.picking_id:
                        partner = line.picking_id.partner_id.name
                        try:
                            if line.picking_id.sale_id:
                                name = line.picking_id.sale_id.name + "/Return"
                                type = 'Sales Return'
                        except Exception:
                            pass
                        try:
                            if line.picking_id.direct_transaction_type == 'sale':
                                type = 'Sales Return'
                                qury = "select name from account_move where direct_move_picking_id=" + str(
                                    line.picking_id.id)

                                self.env.cr.execute(qury)
                                fetch_data = self.env.cr.fetchall()
                                if fetch_data and fetch_data[0] and fetch_data[0][0]:
                                    name = fetch_data[0][0]
                                else:
                                    name = False

                        except Exception:
                            pass
                    if not type:
                        type = 'Return'
                    if not name:
                        name = 'Return - ' + line.reference
                if name == '':
                    name = line.picking_id.name if line.picking_id.name else ''
                if partner == '':
                    if 'is_removal' in line.picking_id._fields:
                        if line.picking_id.is_removal == True:
                            partner = 'Damage Entry'
                    if 'is_transfer_receipt' in line.picking_id._fields:
                        if line.picking_id.is_transfer_receipt == True:
                            partner = 'Transfer Receipt'
                            type = 'Transfer'
                            if [line.location_dest_id.id] != data['location_ids']:
                                partner = 'Transfer Issue'

                    if 'type' in line.picking_id._fields:
                        if line.picking_id.type == True:
                            partner = 'Transfer Issue'
                            type = 'Transfer'
                            if [line.location_dest_id.id] == data['location_ids']:
                                partner = 'Transfer Receipt'

                    if 'adj_type' in line.move_id.inventory_id._fields:
                        if line.move_id.inventory_id.adj_type == 'receipt':
                            partner = 'Stock Receipt Note'
                            name = line.move_id.inventory_id.seq
                        if line.move_id.inventory_id.adj_type == 'issue':
                            partner = 'Stock Issue Note'
                            name = line.move_id.inventory_id.seq
                move_date = self.get_actual_date_from_date(line.date)
                if data['horizontal']:
                    if line.product_id.id in datas:
                        if type == 'Purchase':
                            datas[line.product_id.id]['purchase'] += in_qty
                        elif type == 'Purchase Return':
                            datas[line.product_id.id]['purchase_return'] += out_qty
                        elif type == 'Sale':
                            datas[line.product_id.id]['sales'] += out_qty
                        elif type == 'Sales Return':
                            datas[line.product_id.id]['sales_return'] += in_qty
                        else:
                            datas[line.product_id.id]['other_receipt'] += in_qty
                            datas[line.product_id.id]['other_issue'] += out_qty
                        datas[line.product_id.id]['closing_balance'] += in_qty - out_qty
                    else:
                        opening_data = self.get_product_opening(line.product_id, data['date_from'],
                                                                data.get('allowed_company_ids'), data['location_ids'])
                        datas[line.product_id.id] = {
                            'name': line.product_id.name,
                            'opening_balance': opening_data[0] - opening_data[1],
                            'purchase': 0,
                            'purchase_return': 0,
                            'sales': 0,
                            'sales_return': 0,
                            'other_issue': 0,
                            'other_receipt': 0,
                            'closing_balance': opening_data[0] - opening_data[1] + in_qty - out_qty
                        }
                        if type == 'Purchase':
                            datas[line.product_id.id]['purchase'] = in_qty
                        elif type == 'Purchase Return':
                            datas[line.product_id.id]['purchase_return'] = out_qty
                        elif type == 'Sale':
                            datas[line.product_id.id]['sales'] = out_qty
                        elif type == 'Sales Return':
                            datas[line.product_id.id]['sales_return'] = in_qty
                        else:
                            datas[line.product_id.id]['other_receipt'] = in_qty
                            datas[line.product_id.id]['other_issue'] = out_qty
                else:
                    if line.product_id.id in datas:
                        datas[line.product_id.id]['data'].append((move_date, partner, name, type, in_qty,
                                                                  out_qty))
                        datas[line.product_id.id]['total_in'] += in_qty
                        datas[line.product_id.id]['total_out'] += out_qty
                    else:

                        opening_data = self.get_product_opening(line.product_id, data['date_from'],
                                                                data.get('allowed_company_ids'), data['location_ids'])

                        datas[line.product_id.id] = {
                            'name': line.product_id.name,
                            'data': [(move_date, partner, name, type, in_qty, out_qty)],
                            'opening_balance': opening_data[0] - opening_data[1],
                            'total_in': in_qty + opening_data[0],
                            'total_out': out_qty + opening_data[1],
                            'opening_issue': opening_data[1],
                            'opening_receipt': opening_data[0],
                        }


            product_obj = self.env['product.product']
            product_domain = [('id', 'not in', list(datas.keys())), ('type', 'in', ['product'])]
            if data['product_ids']:
                product_domain.append(('id', 'in', data['product_ids']))
            products = product_obj.search(product_domain)

            for product in products:
                opening = product.with_context(
                    {'to_date': self.get_actual_date(data['date_from'] + " 00:00:00")}).qty_available

                opening_data = self.get_product_opening(product, data['date_from'], data.get('allowed_company_ids'),
                                                        data['location_ids'])

                if opening != 0:
                    if data['horizontal']:
                        datas[product.id] = {
                            'name': product.name,
                            'opening_balance': opening_data[0] - opening_data[1],
                            'purchase': 0,
                            'purchase_return': 0,
                            'sales': 0,
                            'sales_return': 0,
                            'other_issue': 0,
                            'other_receipt': 0,
                            'closing_balance': opening_data[0] - opening_data[1]
                            }
                    else:
                        datas[product.id] = {
                            'name': product.name,
                            'data': [],
                            'opening_balance': opening_data[0] - opening_data[1],
                            'total_in': opening_data[0],
                            'total_out': opening_data[1],
                            'opening_issue': opening_data[1],
                            'opening_receipt': opening_data[0],
                        }

            sorted_dict = {}
            sorted_values = sorted(datas, key=lambda x: (datas[x]['name']))

            for i in sorted_values:
                sorted_dict[i] = datas[i]
            # print(sorted_dict,'sordertter',data['horizontal_view'])

            return sorted_dict

    def get_actual_date(self, TZ_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        try:
            now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        except:
            raise Warning("Please set User Time Zone in Preference")
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(TZ_datetime, fmt)
        result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime(fmt)

    def get_actual_date_from_date(self, TZ_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        try:
            now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        except:
            raise Warning("Please set User Time Zone in Preference")
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        result_utc_datetime = TZ_datetime - UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime('%d/%m/%Y')

    def get_product_opening(self, product, date, companies, location):
        actual_date = self.get_actual_date(date + " 00:00:00")

        move_obj = self.env['stock.move.line']
        if location:
            # locations = self.env['stock.location'].search([('company_id','in',companies),('usage','=','internal')])
            in_moves = move_obj.search(
                [('location_dest_id', 'in', location), ('product_id', '=', product.id), ('date', '<', actual_date),
                 ('state', '=', 'done')])
            out_moves = move_obj.search(
                [('location_id', 'in', location), ('product_id', '=', product.id), ('date', '<', actual_date),
                 ('state', '=', 'done')])
        else:
            locations = self.env['stock.location'].search([('company_id', 'in', companies), ('usage', '=', 'internal')])
            in_moves = move_obj.search(
                [('location_dest_id', 'in', locations.ids), ('product_id', '=', product.id), ('date', '<', actual_date),
                 ('state', '=', 'done')])
            out_moves = move_obj.search(
                [('location_id', 'in', locations.ids), ('product_id', '=', product.id), ('date', '<', actual_date),
                 ('state', '=', 'done')])

        # qty_in = sum(in_moves.mapped('qty_done'))
        # qty_out = sum(out_moves.mapped('qty_done'))
        qty_in = 0
        qty_out = 0
        for in_move in in_moves:
            qty_in += in_move.product_uom_id._compute_quantity(in_move.qty_done, in_move.product_id.uom_id)
        for out_move in out_moves:
            qty_out += out_move.product_uom_id._compute_quantity(out_move.qty_done, out_move.product_id.uom_id)
        #print(qty_in,"2!!!!", qty_out)
        return (qty_in, qty_out)


    def get_html(self):
        res = self._get_report_data(date_from=self.date_from.strftime('%Y-%m-%d'), date_to=self.date_to.strftime('%Y-%m-%d'),
                                    product=self.product,location=self.location, horizontal=self.horizontal)
        self.template_area = self.env.ref('product_ledger.report_product_ledger')._render(
            {'lines': res['lines']['lines'],
             'date_from': self.date_from.strftime('%d-%m-%Y'),
             'date_to': self.date_to.strftime('%d-%m-%Y'),
             'data': res['lines']['data'],
             'products': res['lines']['products'],
             'location': res['lines']['location'],
             })
        # print(res['lines']['lines'])
        return res

    def _get_report_data(self, date_from=False, date_to=False, product=False, location=False,horizontal=False):
        tk = self.env['product.product'].search([], order='name')
        # loc = self.env['stock.location'].search([('usage', '=', 'internal')])
        branch_name = ''
        is_branch = False
        if 'branch_id' in self.env.user._fields:
            loc_default = self.env['stock.warehouse'].search(
                [('branch_id', '=', self.env.user.branch_id.id)])
            is_branch = True
            loc = self.env['stock.warehouse'].search([('branch_id', 'in', self.env.user.branch_ids.ids)])
            if location:
                branch_name = self.env['stock.warehouse'].search(
                    [('lot_stock_id', '=', location)]).branch_id.name

        else:
            loc_default = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
            loc = self.env['stock.warehouse'].search([('company_id', 'in', self.env.user.company_ids.ids)])
            allowed_company_ids=self.env.user.company_ids.ids
            is_branch = False
        rp = ''

        if product:
            rp = [int(i) for i in product]

        # print(loc_default.lot_stock_id.id)
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'product_ids': rp if rp else False,
            'branch_name': branch_name if branch_name else False,
            'location_ids': [int(location)] if location else [loc_default.lot_stock_id.id],
            'horizontal': horizontal if horizontal else False,
            'allowed_company_ids': allowed_company_ids
        }

        dat = self.get_report_values(data=data)
        # print(dat)
        do = {}
        lo = {}
        lid = ''
        lname = ''
        for i in tk:
            do[i.id] = i.name
        if 'branch_id' in self.env.user._fields:
            for l in loc:
                if l.lot_stock_id.id != loc_default.lot_stock_id.id:
                    lo[l.lot_stock_id.id] = l.branch_id.name
            lid = loc_default.lot_stock_id.id
            lname = loc_default.branch_id.name
        else:
            for l in loc:
                if l.lot_stock_id.id != loc_default.lot_stock_id.id:
                    lo[l.lot_stock_id.id] = l.lot_stock_id.complete_name
            lid = loc_default.lot_stock_id.id
            lname = loc_default.lot_stock_id.complete_name

        return {
            'lines': dat,
            'variants': do,
            'location': lo,
            'lid':lid,
            'lname': lname,
            'is_branch': is_branch,
        }
