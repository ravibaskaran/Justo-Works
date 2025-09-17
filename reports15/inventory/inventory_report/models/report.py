from odoo import models, api,fields
from datetime import datetime, timedelta
from odoo.exceptions import Warning
from pytz import timezone

class ReportInventory(models.TransientModel):
    _name = 'report.inventory'
    _inherit = 'beta.reports'
    _description = 'Inventory Report'

    name = fields.Char(default='Report')  # change this
    type=fields.Selection([('current', 'Current Inventory'),
        ('date', 'At A Specific Date')], string="Type",default="current")
    category = fields.Boolean(string="Category")
    last_purchase_cost=fields.Boolean(string="Last Purchase Cost")
    include_zero = fields.Boolean(string="Include Zero")
    category_ids = fields.Many2many('product.category')
    location = fields.Many2many('stock.location')
    date=fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(ReportInventory, self).default_get(fields_list)
        today = datetime.today()
        res['date'] = today
        loc_default = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        res['location'] = loc_default.lot_stock_id
        return res

    def get_report_values(self, data=None):
        date = False
        loc_obj = self.env['stock.location']
        location = ''
        if data['type'] == 'date':
            date = datetime.strptime(
                data['date'], "%Y-%m-%d").strftime('%d/%m/%Y')
        if data['type'] == 'current':
            today = datetime.now()
            date = today.strftime('%d/%m/%Y')
        if data['location_ids']:
            for loc in data['location_ids']:
                location += loc_obj.browse(loc).complete_name + ","
        return {
            'data': data,
            'date': date,
            'type': data['type'],
            'category': data['category'],
            'branch_name': data['branch_name'],
            'company_ids': data['company_ids'],
            'location': location,
            'lines': self.get_inventory_report(data),
        }

    # ♦ Inventory Report Function ♦
    def get_inventory_report(self, data):
        category = data['category']
        final_data = {
            'data': [],
        }
        date = data['date']
        location_ids = data['location_ids']
        category_ids = data['category_ids']
        include_zero = data['include_zero']
        last_purchase_cost = data['last_purchase_cost']

        if data['type']:
            if data['type'] == 'date':
                closing_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
            else:
                date = datetime.now().date()
                closing_date = datetime.strptime(str(date), "%Y-%m-%d") + timedelta(days=1)

            if not category:
                products = self.env['product.product'].search(
                    [('type', 'in', ['product', 'consu'])], order='name')
                actual_date = self.get_actual_date(str(closing_date))
                move_obj = self.env['stock.move.line']
                for product in products:
                    in_moves = move_obj.search([
                        ('location_dest_id', 'in', location_ids),
                        ('product_id', '=', product.id),
                        ('date', '<', actual_date),
                        ('state', '=', 'done')
                    ])

                    out_moves = move_obj.search([
                        ('location_id', 'in', location_ids),
                        ('product_id', '=', product.id),
                        ('date', '<', actual_date),
                        ('state', '=', 'done')
                    ])

                    qty_in = 0
                    qty_out = 0
                    lot_list = {}
                    for in_move in in_moves:
                        in_q = in_move.product_uom_id._compute_quantity(
                            in_move.qty_done, in_move.product_id.uom_id)
                        qty_in += in_q
                        if in_move.lot_id:
                            if in_move.lot_id.id not in lot_list:
                                lot_list[in_move.lot_id.id] = {
                                    'quantity_in': in_q,
                                    'quantity_out': 0,
                                    'balance': in_q,
                                }
                            else:
                                lot_list[in_move.lot_id.id]['quantity_in'] += in_q
                                lot_list[in_move.lot_id.id]['balance'] += in_q

                    for out_move in out_moves:
                        out_q = out_move.product_uom_id._compute_quantity(out_move.qty_done, out_move.product_id.uom_id)
                        qty_out += out_q
                        if out_move.lot_id:
                            if out_move.lot_id.id not in lot_list:
                                lot_list[out_move.lot_id.id] = {
                                    'quantity_out': out_q,
                                    'quantity_in': 0,
                                    'balance': out_q,
                                }
                            else:
                                lot_list[out_move.lot_id.id]['quantity_out'] += out_q
                                lot_list[out_move.lot_id.id]['balance'] -= out_q
                    qty = qty_in - qty_out
                    lot = [key for key, values in lot_list.items() if values['balance'] > 0]
                    if float('{:.2f}'.format(qty)) != 0.00:
                        cost_value = self.get_product_cost_value(lot,
                            product, qty, False, closing_date, last_purchase_cost)
                        pur_rate = float('{:.2f}'.format(
                            cost_value)) / float('{:.2f}'.format(qty))
                        if data['type'] == 'date':
                            rate = self.get_product_avg_sale_rate(
                                product, qty, date,location_ids, False,lot)
                        else:
                            rate = self.get_product_avg_sale_rate(
                                product, qty, str(date), location_ids, False,lot)

                        mrp_value = rate * \
                            float('{:.2f}'.format(qty))
                        final_data['data'].append((product.name, product.l10n_in_hsn_code, qty, product.uom_id.name, pur_rate, rate, mrp_value, cost_value))
                    elif qty == 0 and include_zero:
                        cost_value = self.get_product_cost_value(lot,
                            product, qty, True, closing_date, last_purchase_cost)
                        pur_rate = float('{:.2f}'.format(
                            cost_value))
                        if data['type'] == 'date':
                            rate = self.get_product_avg_sale_rate(
                                product, qty, date, location_ids, True,lot)
                        else:
                            rate = self.get_product_avg_sale_rate(
                                product, qty, str(date), location_ids, True,lot)

                        mrp_value = rate
                        final_data['data'].append((product.name, product.l10n_in_hsn_code, qty, product.uom_id.name, pur_rate, rate, mrp_value, cost_value))
            else:
                if category_ids:
                    products = self.env['product.product'].search(
                        [('type', 'in', ['product', 'consu']), ('categ_id', 'in', category_ids)],
                        order="categ_id, name")
                else:
                    products = self.env['product.product'].search(
                        [('type', 'in', ['product', 'consu'])], order="categ_id, name")
                actual_date = self.get_actual_date(str(closing_date))
                move_obj = self.env['stock.move.line']
                for product in products:
                    in_moves = move_obj.search([
                        ('location_dest_id', 'in', location_ids),
                        ('product_id', '=', product.id),
                        ('date', '<', actual_date),
                        ('state', '=', 'done')
                    ])
                    out_moves = move_obj.search([
                        ('location_id', 'in', location_ids),
                        ('product_id', '=', product.id),
                        ('date', '<', actual_date),
                        ('state', '=', 'done')
                    ])
                    qty_in = 0
                    qty_out = 0
                    lot_list = []
                    for in_move in in_moves:
                        in_q = in_move.product_uom_id._compute_quantity(
                            in_move.qty_done, in_move.product_id.uom_id)
                        qty_in += in_q
                        if in_move.lot_id:
                            if in_move.lot_id.id not in lot_list:
                                lot_list[in_move.lot_id.id] = {
                                    'quantity_in': in_q,
                                    'quantity_out': 0,
                                    'balance': in_q,
                                }
                            else:
                                lot_list[in_move.lot_id.id]['quantity_in'] += in_q
                                lot_list[in_move.lot_id.id]['balance'] += in_q
                    for out_move in out_moves:
                        out_q = out_move.product_uom_id._compute_quantity(
                            out_move.qty_done, out_move.product_id.uom_id)
                        qty_out += out_q
                        if out_move.lot_id:
                            if out_move.lot_id.id not in lot_list:
                                lot_list[out_move.lot_id.id] = {
                                    'quantity_out': out_q,
                                    'quantity_in': 0,
                                    'balance': out_q,
                                }
                            else:
                                lot_list[out_move.lot_id.id]['quantity_out'] += out_q
                                lot_list[out_move.lot_id.id]['balance'] -= out_q
                    qty = qty_in - qty_out
                    lot = [key for key, values in lot_list.items() if values['balance'] > 0]
                    print(lot_list, "list of lots", lot)
                    if float('{:.2f}'.format(qty)) != 0.00:
                        cost_value = self.get_product_cost_value(lot,
                            product, qty, False, closing_date, last_purchase_cost)
                        pur_rate = float('{:.2f}'.format(
                            cost_value)) / float('{:.2f}'.format(qty))
                        if data['type'] == 'date':
                            rate = self.get_product_avg_sale_rate(
                                product, qty, date,location_ids, False,lot)
                        else:
                            rate = self.get_product_avg_sale_rate(
                                product, qty, str(date), location_ids, False,lot)
                        mrp_value = rate * \
                                    float('{:.2f}'.format(qty))
                        final_data['data'].append((product.name, product.l10n_in_hsn_code, qty,
                                                    product.uom_id.name, pur_rate, rate, mrp_value, cost_value,
                                                    product.categ_id.name,product.categ_id.id))
                    elif qty == 0 and include_zero:
                        cost_value = self.get_product_cost_value(lot,
                            product, qty, True, closing_date, last_purchase_cost)
                        pur_rate = float('{:.2f}'.format(
                            cost_value))
                        if data['type'] == 'date':
                            rate = self.get_product_avg_sale_rate(
                                product, qty, date, location_ids, True,lot)
                        else:
                            rate = self.get_product_avg_sale_rate(
                                product, qty, str(date), location_ids, True,lot)
                        mrp_value = rate
                        final_data['data'].append((product.name, product.l10n_in_hsn_code, qty,
                                                    product.uom_id.name, pur_rate, rate, mrp_value, cost_value,
                                                    product.categ_id.name, product.categ_id.id))
        if not category:
            return final_data
        else:
            category_data = {
                'data': [],
            }
            if len(final_data['data']) > 0:
                i = 0
                mrp_total = 0
                cost_total = 0
                qty = 0
                cid = final_data['data'][0][9]
                cname = final_data['data'][0][8]

                category_data['data'].append((cname, 'Heading', 0, 0, 0, 0, 0, 0, 0, 0))
                while i < len(final_data['data']):
                    if cid == final_data['data'][i][9]:

                        category_data['data'].append((
                            final_data['data'][i][0],
                            final_data['data'][i][1],
                            final_data['data'][i][2],
                            final_data['data'][i][3],
                            final_data['data'][i][4],
                            final_data['data'][i][5],
                            final_data['data'][i][6],
                            final_data['data'][i][7]
                        ))

                        mrp_total += final_data['data'][i][6]
                        cost_total += final_data['data'][i][7]
                        qty += final_data['data'][i][2]
                    else:
                        category_data['data'].append((cname, 'Heading', qty, 'Total', 0, 0, mrp_total, cost_total,))
                        cid = final_data['data'][i][9]
                        cname = final_data['data'][i][8]
                        mrp_total = 0
                        cost_total = 0
                        qty = 0

                        category_data['data'].append((cname, 'Heading', 0, 0, 0, 0, 0, 0, 0, 0))

                        category_data['data'].append((
                            final_data['data'][i][0],
                            final_data['data'][i][1],
                            final_data['data'][i][2],
                            final_data['data'][i][3],
                            final_data['data'][i][4],
                            final_data['data'][i][5],
                            final_data['data'][i][6],
                            final_data['data'][i][7]
                        ))
                        mrp_total += final_data['data'][i][6]
                        cost_total += final_data['data'][i][7]
                        qty += final_data['data'][i][2]
                    i = i + 1
                category_data['data'].append((cname, 'Heading', qty, 'Total', 0, 0, mrp_total, cost_total,))

            return category_data

    def get_actual_date(self, TZ_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        try:
            now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        except:
            raise Warning("Please set User Time Zone")
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(TZ_datetime, fmt)
        result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime(fmt)

    #  ♦ Actual Date ♦
    def get_actual_date_from_date(self, TZ_datetime):
        fmt = "%Y-%m-%d %H:%M:%S"
        now_utc = datetime.now(timezone('UTC'))
        try:
            now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        except:
            raise Warning("Please set User Time Zone")
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        result_utc_datetime = TZ_datetime - UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime('%d/%m/%Y')

    # ♦ Average Product Cost ♦
    def get_product_cost_value(self,lot, product, qty, include_zero, date, last_purchase_cost, moveid=None):
        value = 0
        stock_production_lot_obj = self.env['stock.production.lot'].sudo().search([('id','in',lot)])
        if 'direct_move_type' in self.env['account.move']._fields:
            domain = [
                ('product_id', '=', product.id),
                ('move_id.move_type', '=', 'in_invoice'),
                ('move_id.direct_move_type', '=', 'incoming'),
                ('move_id.state', '=', 'posted'),
                ('exclude_from_invoice_tab', '=', False)
            ]
        else:
            domain = [
                ('product_id', '=', product.id),
                ('move_id.move_type', '=', 'in_invoice'),
                ('move_id.state', '=', 'posted'),
                ('exclude_from_invoice_tab', '=', False)
            ]

        if date:
            domain.append(('date', '<', date))
        if moveid:
            domain.append(('id', '!=', moveid))
        moveline = self.env['account.move.line'].search(
            domain, order='date desc,id desc', limit=1)
        if moveline:
            if include_zero:
                return moveline.price_unit
            if last_purchase_cost:
                return qty * moveline.price_unit
            if moveline.quantity >= qty:
                value += qty * moveline.price_unit
            else:
                if 'generate_serial_number' in product._fields and product.generate_serial_number:
                    if stock_production_lot_obj:
                        total_purchase_rate = sum(stock_production_lot_obj.mapped('p_rate'))
                        average_purchase_rate = total_purchase_rate / len(stock_production_lot_obj) if len(stock_production_lot_obj) > 0 else 0
                        value += qty * average_purchase_rate
                    else:
                        value += qty * moveline.price_unit
                else:
                    value += moveline.quantity * moveline.price_unit
                    value += self.get_product_cost_value(lot, product, qty - moveline.quantity, False, moveline.date, False, moveid=moveline.id)
        else:
            if include_zero:
                return product.standard_price
            if last_purchase_cost:
                return qty * product.standard_price
            value += qty * product.standard_price
        return value

    #  ♦ Average Product MRP ♦
    def get_product_avg_sale_rate(self, product, qty, date,location_ids, include_zero,lot):
        user_fields = self.env.user._fields                         # → Contains the list of Existing fields in res users
        account_move_line_obj = self.env['account.move.line']
        aml_fields = account_move_line_obj._fields                  # → Contains the list of Existing fields in account move line
        stock_picking_fields = self.env['stock.picking']._fields    # → Contains the list of Existing fields in stock picking
        stock_production_lot_obj = self.env['stock.production.lot'].sudo().search([('id', 'in', lot)])
        rate = 0
        total_sales_value_in = 0
        total_sales_value_out = 0
        loc_dom = ""
        rate_updt_dom = ""
        transfer_date = ""
        in_transfer = False
        out_transfer = False
        rate_difference = 0
        domain_purchase_sales = " and am.move_type='in_invoice'"
        qry_domain = " "

        if 'branch_id' in user_fields:
            warehouse_ids = self.env['stock.warehouse'].search(
                [('lot_stock_id', 'in', location_ids)])
            branch_ids = warehouse_ids.mapped('branch_id').ids

            if len(branch_ids) == 1:
                qry_domain += " and aml.branch_id =" + str(branch_ids[0])
                rate_updt_dom += " and rum.branch_id =" + str(branch_ids[0])
            else:
                qry_domain += " and aml.branch_id in" + str(branch_ids)
                rate_updt_dom += " and rum.branch_id in" + str(branch_ids)
            if len(location_ids) == 1:
                loc_dom = " and location_id =" + str(location_ids[0])
            else:
                loc_dom = " and location_id in" + str(location_ids)

        if 'direct_move_type' in self.env['account.move']._fields:
            domain = [
                ('product_id', '=', product.id),
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.direct_move_type', '=', 'outgoing'),
                ('move_id.state', '=', 'posted'),
                ('exclude_from_invoice_tab', '=', False)
            ]
        else:
            domain = [
                ('product_id', '=', product.id),
                ('move_id.move_type', '=', 'in_invoice'),
                ('move_id.state', '=', 'posted'),
                ('exclude_from_invoice_tab', '=', False)
            ]

        if date:

            # ♦ Assigning date to domain and query's ♦
            qry_domain += " and am.invoice_date <= '" + date+ " 18:29:59'"
            transfer_date += " and sp.scheduled_date <='" + date+ " 18:29:59'"        # → usage in [in_transfer and out_transfer]
            loc_dom += " and si.date <='" + date+ " 18:29:59'"              # → usage in [opening_qry, adj_issue, adj_recep, adj_damage]
            rate_updt_dom += " and rum.date <='" + date+ " 18:29:59'"
            domain.append(('date', '<=',datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)))

        if 'branch_id' in user_fields and 'sales_value' in aml_fields:

            # ♦ Account Move ♦
            qry1 = """
                select sum(((aml.quantity/uom1.factor)*uom2.factor)*aml.price_unit) as price_total,
                sum(aml.sales_rate*(aml.free_qty+aml.quantity)) as sales_value, sum(aml.quantity) as qty 
                from account_move_line as aml 
                left join account_move as am on am.id = aml.move_id 
                left join uom_uom as uom1 on uom1.id = aml.product_uom_id
                left join product_product as pp on pp.id = aml.product_id
                left join product_template as pt on pt.id = pp.product_tmpl_id
                left join uom_uom as uom2 on uom2.id = pt.uom_id
                where am.state='posted' and aml.exclude_from_invoice_tab = False and aml.product_id=
                """+str(product.id)

            #  ♦ Stock Inventory Opening Stock ♦
            opening_qry = """
                select sum(product_qty*s_price) as sales_value,  sum(product_qty) as qty  
                from stock_inventory_line as sil 
                left join stock_inventory as si on si.id = sil.inventory_id 
                where si.adj_type = '' and si.state='done' and sil.product_id ="""+str(product.id)+loc_dom

            #  ♦ Stock Adjustment Issue ♦
            adj_issue = """
                select sum(prod_qty*s_price) as sales_value,  sum(prod_qty) as qty  
                from stock_inventory_line as sil 
                left join stock_inventory as si on si.id = sil.inventory_id 
                where si.adj_type = 'issue' and si.state='done' and sil.product_id ="""+str(product.id)+loc_dom

            #  ♦ Stock Adjustment Receipt ♦
            adj_recep = """
                select sum(prod_qty*s_price) as sales_value,  sum(prod_qty) as qty  
                from stock_inventory_line as sil 
                left join stock_inventory as si on si.id = sil.inventory_id 
                where si.adj_type = 'receipt' and si.state='done' and sil.product_id ="""+str(product.id)+loc_dom

            # ♦ Stock Adjustment Damage ♦
            adj_damage = """
                select sum(prod_qty*s_price) as sales_value,  sum(prod_qty) as qty  
                from stock_inventory_line as sil
                left join stock_inventory as si on si.id = sil.inventory_id
                where si.adj_type = 'damage' and si.state='done' and sil.product_id ="""+str(product.id)+loc_dom

            if 'dest_branch_id' in stock_picking_fields:

                # ♦ Transfer Receipt ♦
                in_transfer = """
                    select sum(sm.product_uom_qty*sm.price_unit) as sales_value,  sum(sm.product_uom_qty) as qty  
                    from stock_move as sm
                    left join stock_picking as sp on sp.id = sm.picking_id
                    where sp.type = 'True' and sp.transfer_type = 'stock' and sp.dest_branch_id in (""" + (str(branch_ids).replace('[', '')).replace(']', '') + """) and sp.state='done' and sm.product_id ="""+str(product.id)+transfer_date

                #  ♦ Transfer Issue ♦
                out_transfer = """
                    select sum(sm.product_uom_qty*sm.price_unit) as sales_value,  sum(sm.product_uom_qty) as qty  
                    from stock_move as sm
                    left join stock_picking as sp on sp.id = sm.picking_id
                    where sp.type = 'True' and sp.transfer_type = 'stock' and sp.branch_id in (""" + (str(branch_ids).replace('[', '')).replace(']', '') + """) and sp.state='done' and sm.product_id ="""+str(product.id)+transfer_date

            # ♦ Rate Update ♦
            if self.env['ir.model'].sudo().search([('model', '=', 'rate.update.move')]):
                rate_update_qry = """
                    select sum((rul.qty*rul.m_mrp)-(rul.qty*rul.c_mrp)) as rate_difference
                    from rate_update_line as rul
                    left join rate_update_move as rum on rul.move_id = rum.id
                    where product_id= 
                """ + str(product.id)+rate_updt_dom

                self.env.cr.execute(rate_update_qry)
                rate_update_qry_res = self.env.cr.dictfetchall()
                if rate_update_qry_res[0]['rate_difference']:
                    rate_difference += rate_update_qry_res[0]['rate_difference']

            # ♦ Purchase ♦
            self.env.cr.execute(qry1+domain_purchase_sales+qry_domain)
            qry_res_purchase = self.env.cr.dictfetchall()

            if qry_res_purchase[0]['sales_value']:
                total_sales_value_in += qry_res_purchase[0]['sales_value']

            # ♦ Sales Return ♦
            domain_purchase_sales = " and am.move_type='out_refund'"
            self.env.cr.execute(qry1+domain_purchase_sales+qry_domain)
            qry_res_sales_ret = self.env.cr.dictfetchall()

            if qry_res_sales_ret[0]['price_total']:
                total_sales_value_in += qry_res_sales_ret[0]['price_total']

            # ♦ Opening Stock ♦
            self.env.cr.execute(opening_qry)
            qry_res_inv_opening = self.env.cr.dictfetchall()
            if qry_res_inv_opening[0]['sales_value']:
                total_sales_value_in += qry_res_inv_opening[0]['sales_value']

            # ♦ Adj Receipt ♦
            self.env.cr.execute(adj_recep)
            qry_res_adj_recep = self.env.cr.dictfetchall()
            if qry_res_adj_recep[0]['sales_value']:
                total_sales_value_in += qry_res_adj_recep[0]['sales_value']

            # ♦ Adj Issue ♦
            self.env.cr.execute(adj_issue)
            qry_res_adj_issue = self.env.cr.dictfetchall()
            if qry_res_adj_issue[0]['sales_value']:
                total_sales_value_out += qry_res_adj_issue[0]['sales_value']

            # ♦ Adj Damage ♦
            self.env.cr.execute(adj_damage)
            qry_res_adj_damage = self.env.cr.dictfetchall()
            if qry_res_adj_damage[0]['sales_value']:
                total_sales_value_out += qry_res_adj_damage[0]['sales_value']

            # ♦ Stock Transfer Issue ♦
            if out_transfer:
                self.env.cr.execute(out_transfer)
                qry_res_trans_issue = self.env.cr.dictfetchall()
                if qry_res_trans_issue[0]['sales_value']:
                    total_sales_value_out += qry_res_trans_issue[0]['sales_value']

            # ♦ Stock Transfer Receipt ♦
            if in_transfer:
                self.env.cr.execute(in_transfer)
                qry_res_trans_receipt = self.env.cr.dictfetchall()
                if qry_res_trans_receipt[0]['sales_value']:
                    total_sales_value_in += qry_res_trans_receipt[0]['sales_value']

            # ♦ Sales ♦
            domain_purchase_sales = " and am.move_type='out_invoice'"
            self.env.cr.execute(qry1+domain_purchase_sales+qry_domain)
            qry_res_sales = self.env.cr.dictfetchall()
            if qry_res_sales[0]['price_total']:
                total_sales_value_out += qry_res_sales[0]['price_total']

            # ♦ Purchase Return ♦
            domain_purchase_sales = " and am.move_type='in_refund'"
            self.env.cr.execute(qry1+domain_purchase_sales+qry_domain)
            qry_res_sales = self.env.cr.dictfetchall()
            if qry_res_sales[0]['sales_value']:
                total_sales_value_out += qry_res_sales[0]['sales_value']
            rate = total_sales_value_in - total_sales_value_out + rate_difference
        else:
            movelines = account_move_line_obj.search(domain)
            total = 0
            if movelines:
                for moveline in movelines:
                    total += moveline.price_unit
                if len(movelines) != 0:
                    rate = total / len(movelines)
            else:
                if stock_production_lot_obj:
                    total_sales_rate = sum(stock_production_lot_obj.mapped('sales_rate'))
                    average_sales_rate = total_sales_rate / len(stock_production_lot_obj) if len(stock_production_lot_obj) > 0 else 0
                    rate = average_sales_rate
                else:
                    rate = product.list_price
            return rate

        if include_zero:
            return rate
        rate = rate/qty
        return rate

    # ♦ Get Html ♦

    def get_html(self):
        res = self._get_report_data(type=self.type,date=self.date.strftime('%Y-%m-%d'), category=self.category,category_ids=self.category_ids,
                                    include_zero=self.include_zero, last_purchase_cost=self.last_purchase_cost)

        self.template_area =  self.env.ref('inventory_report.report_inventory')._render({
            'lines': res['lines']['lines'],
            'date': res['lines']['date'],
            'data': res['lines']['data'],
            'type': self.type,
            'category':self.category,
            'date':self.date.strftime('%d-%m-%Y'),
            'category_ids':self.category_ids,
            'include_zero':self.include_zero,
            'last_purchase_cost':self.last_purchase_cost,
            'location': res['lines']['location'],
            'category': res['lines']['category'],
            'branch_name': res['lines']['branch_name'],
        })
        return res

    # ♦ Get Report Date ♦

    def _get_report_data(self,type=False, date=False, category=False,category_ids=False, include_zero=False, last_purchase_cost=False):
        branch_name = ''
        companies = self._context.get('allowed_company_ids')
        cate = self.env['product.category'].search([], order='name')
        rl = ''
        cl =''
        if 'branch_id' in self.env.user._fields:

            loc_default = self.env['stock.warehouse'].search([
                ('branch_id', '=', self.env.user.branch_id.id)
            ])

            location_ids = self.env['stock.warehouse'].search([
                ('branch_id', 'in', self.env.user.branch_ids.ids)
            ])

            is_branch = True
        else:
            loc_default = self.env['stock.warehouse'].search([
                ('company_id', '=', self.env.user.company_id.id)
            ])

            location_ids = self.env['stock.warehouse'].search([
                ('company_id', 'in', self.env.user.company_ids.ids)
            ])

            is_branch = False
        # #if report_location:
        #     rl = [int(i) for i in report_location]

        if category_ids:
            cl = [int(i) for i in category_ids]

        if 'branch_id' in self.env.user._fields:
            if rl:
                branch = self.env['stock.warehouse'].search([('lot_stock_id','in',rl)])
                branch_name = ', '.join(branch.branch_id.mapped('name'))

        data = {
            'date': date,
            'company_ids': companies,
            'type': type,
            'branch_name': branch_name,
            'location_ids': rl if rl else (loc_default.lot_stock_id.id,),
            'category': category if category else False,
            'category_ids': cl if cl else False,
            'include_zero': include_zero,
            'last_purchase_cost': last_purchase_cost
        }
        dat = self.get_report_values(data=data)

        do = {}
        lo = {}
        catego = {}
        for c in cate:
            catego[c.id] = c.name
        if 'branch_id' in self.env.user._fields:
            for loc in location_ids:
                if loc.lot_stock_id.id != loc_default.lot_stock_id.id:
                    lo[loc.lot_stock_id.id] = loc.branch_id.name
            lid = loc_default.lot_stock_id.id
            lname = loc_default.branch_id.name
        else:
            for loc in location_ids:
                if loc.lot_stock_id.id != loc_default.lot_stock_id.id:
                    lo[loc.lot_stock_id.id] = loc.lot_stock_id.complete_name
            lid = loc_default.lot_stock_id.id
            lname = loc_default.lot_stock_id.complete_name
        return {
            'lines': dat,
            'variants': do,
            'location': lo,
            'lid': lid,
            'category': catego,
            'lname': lname,
            'is_branch': is_branch,
        }
