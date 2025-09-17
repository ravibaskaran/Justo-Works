# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.tools.float_utils import float_compare
from datetime import datetime, timedelta
from datetime import datetime
from odoo.exceptions import Warning, UserError
from pytz import timezone


class StockIssue(http.Controller):

    @http.route('/CreateStockInventory/Issue/<int:inventory_id>/<int:product_one>/<int:product_one_qty>/<int:seq>', auth='public')
    def index1(self, inventory_id,product_one,product_one_qty,seq):
        inv = request.env['stock.inventory'].sudo().search([('id','=',inventory_id)])
        sequence = seq
        product_list = []
        allocated_lots_per_product = {}
        lots = request.env['stock.production.lot'].sudo().search([('product_id', '=', product_one)], order='id').filtered(lambda x: x.product_qty > 0)
        total_quantity = product_one_qty
        lots_to_pass = []
        prd = request.env['product.product'].sudo().search([('id', '=', product_one)])
        if product_one not in allocated_lots_per_product:
            allocated_lots_per_product[product_one] = []
        remaining_quantity = total_quantity
        for lot in lots:
            if remaining_quantity <= 0:
                break
            previous_quantity = lot.product_qty
            for prev_lot, prev_quantity in allocated_lots_per_product[product_one]:
                if lot.id == prev_lot.id:
                    previous_quantity -= prev_quantity
            if previous_quantity >= remaining_quantity:
                lots_to_pass.append((lot, remaining_quantity))
                allocated_lots_per_product[product_one].append((lot, remaining_quantity))
                remaining_quantity = 0

            else:
                if previous_quantity > 0:
                    lots_to_pass.append((lot, previous_quantity))
                    allocated_lots_per_product[product_one].append((lot, previous_quantity))
                    remaining_quantity -= previous_quantity
        for lot, quantity in lots_to_pass:
            product_list.append((0, 0, {
                'sl_no': sequence,
                'product_id': product_one,
                'product_qty': quantity,
                'p_rate': lot.p_rate,
                'prod_lot_id': lot.id,
                'product_uom_id': prd.uom_id.id,
                'sales_rate': lot.sales_rate if lot.sales_rate else prd.list_price,
                'amount': quantity * (lot.sales_rate if lot.sales_rate else prd.list_price)
            }))
            sequence += 1

        inv.line_ids = product_list
        print(product_list,"product_list")