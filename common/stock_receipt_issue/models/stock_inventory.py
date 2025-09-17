from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import date


class StockInventoryInh(models.Model):
    _name = 'stock.inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Inventory"
    _order = "date desc, id desc"

    remarks = fields.Char()
    move_ids = fields.One2many(
        'stock.move', 'inventory_id', string='Created Moves',
        states={'done': [('readonly', True)]})
    adj_type = fields.Selection([('issue', 'issue'), ('receipt', 'receipt'),('damage', 'damage')])
    seq = fields.Char('Number', required=True, index=True,
                      copy=False, default=lambda self: _('Draft'))
    date_wo_time = fields.Date(store=True)
    # branch_id = fields.Many2one('res.branch', string='Branch', readonly=True)
    line_ids = fields.One2many(
        'stock.inventory.line', 'inventory_id', string='Inventories',
        copy=False, readonly=False,
        states={'done': [('readonly', True)]})
    state = fields.Selection(string='Status', selection=[
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'In Progress'),
        ('done', 'Validated')],
                             copy=False, index=True, readonly=True,
                             default='draft')
    date = fields.Datetime(
        'Inventory Date',
        readonly=True, required=True,
        default=fields.Datetime.now,
        help="If the inventory adjustment is not validated, date at which the theoritical quantities have been checked.\n"
             "If the inventory adjustment is validated, date at which the inventory adjustment has been validated.")
    company_id = fields.Many2one(
        'res.company', 'Company',
        readonly=True, index=True, required=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
                                  default=lambda self: self.env.company.currency_id.id)
    location_ids = fields.Many2many(
        'stock.location', string='Locations',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)]},
        domain="[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit'])]")
    product_ids = fields.Many2many(
        'product.product', string='Products', check_company=True,
        domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Specify Products to focus your inventory on particular Products.")
    sl_no=fields.Integer()
    name = fields.Char(
        'Inventory Reference', default="Inventory",
        readonly=True,
        states={'draft': [('readonly', False)]})
    amount_total = fields.Float(string='Total Amount', store=True, readonly=True, compute='_amount_all',digits='Product Price')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        # res = super(StockInventoryInh, self)._onchange_company_id()
        if self.company_id and self.adj_type in ('receipt', 'issue', 'damage'):
            if 'branch_id' in self.env.user._fields:
                com = self.env['stock.warehouse'].search(
                    [('company_id', '=', self.company_id.id), ('branch_id', '=', self.env.user.branch_id.id)])
            else:
                com = self.env['stock.warehouse'].search(
                    [('company_id', '=', self.env.user.company_id.id)])
            self.location_ids = com.lot_stock_id.ids
        # return res

    # @api.model
    # def default_get(self, fieldsname):
    #     # res = super(StockInventoryInh, self).default_get(fieldsname)
    #     if res.get'('adj_type') in ('receipt', 'issue'):
    #         branch = self._context.get('branch')
    #         if branch:
    #             com = self.env['stock.warehouse'].search(
    #                 [('branch_id', '=', branch)])
    #         else:
    #             com = self.env['stock.warehouse'].search(
    #                 [('company_id', '=', self.env.user.company_id.id)])
    #
    #         res['location_ids'] = com.lot_stock_id.ids
    #         res['branch_id'] = branch
    #     return res

    @api.onchange('date')
    def set_date_wo_time(self):
        self.date_wo_time = self.date

    #@api.model
    #def create(self, vals):
        #if vals.get('adj_type') and vals['adj_type'] in ('receipt', 'issue') and vals.get('date') and self.env['stock.inventory'].search([('date', '>', vals['date'])]):
            #raise Warning('Previous date entry not possible')
        #return super(StockInventoryInh, self).create(vals)

    # def write(self, vals):
    #     if self.adj_type in ('receipt', 'issue') and self.env['stock.inventory'].search([('date', '>', self.date)]):
    #         # raise Warning('Previous date entry not possible')
    #         pass
    #     return super(StockInventoryInh, self).write(vals)

    def action_post_inventory_custom(self):
        if not self.line_ids:
            raise UserError(_('Please add some items to move.'))
        for i in self.line_ids:
            if i.inventory_id.adj_type in ('issue','damage'):
                if i.product_id.qty_available < i.prod_qty:
                    raise ValidationError(_('Not enough stock for product %s') %
                                  i.product_id.display_name)
            elif i.product_id.tracking != 'none':
                i.lot_create_edit()
            i.generate_moves_custom()
        self.post_inventory()
        self.write({'state': 'done'})
        self.seq = self.get_sequence_adj()
        # self.message_post(body='Status: Draft --> Posted')
        stock_move_line = self.env['stock.move.line'].search(
            [
                ('move_id.inventory_id','=',self.id),
            ]
        )
        for line in stock_move_line:
            line.date = self.date
            # line.write({'date':})


    def post_inventory(self):
        # The inventory is posted as a single step which means quants cannot be moved from an internal location to another using an inventory
        # as they will be moved to inventory loss, and other quants will be created to the encoded quant location. This is a normal behavior
        # as quants cannot be reuse from inventory location (users can still manually move the products before/after the inventory if they want).
        self.mapped('move_ids').filtered(lambda move: move.state != 'done')._action_done()
        return True

    def _get_inventory_lines_values(self):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location']
        if self.location_ids:
            locations = self.env['stock.location'].search([('id', 'child_of', self.location_ids.ids)])
        else:
            locations = self.env['stock.location'].search(
                [('company_id', '=', self.company_id.id), ('usage', 'in', ['internal', 'transit'])])
        domain = ' sq.location_id in %s AND sq.quantity != 0 AND pp.active'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']

        # If inventory by company
        if self.company_id:
            domain += ' AND sq.company_id = %s'
            args += (self.company_id.id,)
        if self.product_ids:
            domain += ' AND sq.product_id in %s'
            args += (tuple(self.product_ids.ids),)

        self.env['stock.quant'].flush(
            ['company_id', 'product_id', 'quantity', 'location_id', 'lot_id', 'package_id', 'owner_id'])
        self.env['product.product'].flush(['active'])
        self.env.cr.execute("""SELECT sq.product_id, sum(sq.quantity) as product_qty, sq.location_id, sq.lot_id as prod_lot_id, sq.package_id, sq.owner_id as partner_id
            FROM stock_quant sq
            LEFT JOIN product_product pp
            ON pp.id = sq.product_id
            WHERE %s
            GROUP BY sq.product_id, sq.location_id, sq.lot_id, sq.package_id, sq.owner_id """ % domain, args)

        for product_data in self.env.cr.dictfetchall():
            product_data['company_id'] = self.company_id.id
            product_data['inventory_id'] = self.id
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if self.prefill_counted_quantity == 'zero':
                product_data['product_qty'] = 0
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
            vals.append(product_data)
        return vals

    def get_sequence_adj(self):
        if self.adj_type == 'issue':
            return self.env['ir.sequence'].next_by_code(
                'adjustment.issue.sequence')
        if self.adj_type == 'receipt':
            return self.env['ir.sequence'].next_by_code(
                'adjustment.receipt.sequence')
        if self.adj_type == 'damage':
            return self.env['ir.sequence'].next_by_code(
                'adjustment.damage.sequence')




    def domain_filter(self):
        # print('this is working')
        branch = self.env.user.branch_id.id
        warehouse = self.env['stock.warehouse'].search(
            [('branch_id', '=', branch)])
        loc = warehouse.lot_stock_id.id
        tree_view = self.env.ref(
            'stock_receipt_issue_note.adjustments_receipt_tree').id
        form_view = self.env.ref(
            'stock_receipt_issue_note.adjustments_receipt_form').id
        search_view = self.env.ref(
            'stock_receipt_issue_note.view_inventory_filter_custom').id
        return {
            'name': 'Stock Receipt Note',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'search_view_id': search_view,
            'views': [(tree_view, 'tree'), (form_view, 'form')],
            'domain': [('adj_type', '=', 'receipt'), ('location_ids', '=', loc)],
            'context': {'default_adj_type': 'receipt', 'search_default_today': 1},
            'res_model': 'stock.inventory',
            'target': 'current'

            # ,('location_dest_id','=',transfer_to)
        }

    @api.onchange('line_ids')
    def set_sl_no(self):
        self.line_ids.compute_sl_no()
        lenn = len(self.line_ids)
        for i in range(lenn):
            self.line_ids[i].sl_no = i + 1

    @api.depends('line_ids.amount')
    def _amount_all(self):
        for order in self:
            amount_total = 0.0
            for line in order.line_ids:
                amount_total += line.amount
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id

        self.amount_total=currency.round(amount_total)
        return self.amount_total


    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StockInventoryInh, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu)
        if self._context.get('default_adj_type') in ('issue', 'receipt','damage'):
            if res.get('toolbar', False) and res.get('toolbar').get('print', False):
                reports = res.get('toolbar').get('print')
                for report in reports:
                    if report.get('report_file', False) and report.get('report_file') == 'stock.report_inventory':
                        res['toolbar']['print'].remove(report)
        else:
            if res.get('toolbar', False) and res.get('toolbar').get('print', False):
                reports = res.get('toolbar').get('print')
                for report in reports:
                    if report.get('report_file', False) and report.get('report_file') == 'stock_receipt_issue_note.report_stock_receipt_issue_note':
                        res['toolbar']['print'].remove(report)
        return res


class StockInvetoryLineInh(models.Model):
    _name = 'stock.inventory.line'
    _description = "Inventory Line"
    _order = "product_id, inventory_id, location_id, prod_lot_id"


    @api.model
    def _domain_location_id(self):
        if self.env.context.get('active_model') == 'stock.inventory':
            inventory = self.env['stock.inventory'].browse(self.env.context.get('active_id'))
            if inventory.exists() and inventory.location_ids:
                return "[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit']), ('id', 'child_of', %s)]" % inventory.location_ids.ids
        return "[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit'])]"

    @api.model
    def _domain_product_id(self):
        if self.env.context.get('active_model') == 'stock.inventory':
            inventory = self.env['stock.inventory'].browse(self.env.context.get('active_id'))
            if inventory.exists() and len(inventory.product_ids) > 1:
                return "[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('id', 'in', %s)]" % inventory.product_ids.ids
        return "[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]"

    def default_location(self):
        loc=self.env['stock.location'].search(
                    [('company_id', '=', self.env.user.company_id.id),('usage','=','internal')])
        print(loc)
        return loc

    inventory_id = fields.Many2one(
        'stock.inventory', 'Inventory', check_company=True,
        index=True, ondelete='cascade')
    prod_lot_name = fields.Char(string='Lot Name')
    sales_rate = fields.Float(digits='Product Price')
    p_rate = fields.Float(digits='Product Price')
    amount = fields.Float(digits='Product Price')
    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True,
        domain=lambda self: self._domain_product_id(),
        index=True, required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Owner', check_company=True)
    package_id = fields.Many2one(
        'stock.quant.package', 'Pack', index=True, check_company=True,
        domain="[('location_id', '=', location_id)]",
    )
    product_qty = fields.Float(
        'Counted Quantity',
        digits='Product Unit of Measure', default=0)
    prod_qty =fields.Float(
        'Theoretical Quantity',
        digits='Product Unit of Measure', readonly=True)
    date_wo_time = fields.Date()
    sl_no = fields.Integer(compute='compute_sl_no')
    product_tracking = fields.Selection('Tracking', related='product_id.tracking', readonly=True)
    prod_lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', check_company=True,
        domain="[('product_id','=',product_id), ('company_id', '=', company_id)]")
    company_id = fields.Many2one(
        'res.company', 'Company', related='inventory_id.company_id',
        index=True, readonly=True, store=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=True, required=True,
        check_company=True,default=default_location,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")
    prod_lot_name=fields.Char()
    expiry = fields.Date(string='Expiry')

    @api.onchange('expiry')
    def check_expiry_date_format(self):
        check = True
        if self.expiry and check:
            exp = str(self.expiry).split("-")
            mm = exp[1]
            yyyy = exp[0]
            dd = exp[2]
            if 0 < int(mm) < 13:
                pass
            else:
                raise ValidationError('Invalid Month!')
            today = date.today()
            if today.year > int(yyyy):
                raise ValidationError('Already expired')
            elif today.year == int(yyyy) and today.month >= int(mm) and today.day >= int(dd):
                raise ValidationError('Already expired')

    # @api.model
    # def default_get(self, fieldsname):
    #     res = super(StockInvetoryLineInh, self).default_get(fieldsname)
    #     li = []
    #     for i in self.inventory_id.line_ids:
    #         li.append(i.id)
    #     for j in self:
    #         try:
    #             j.sl_no = li.index(j.id) + 1
    #         except:
    #             pass
    #     return res



    @api.depends('inventory_id.line_ids')
    def compute_sl_no(self):
        li = []
        for i in self.inventory_id.line_ids:
            li.append(i.id)
        for j in self:
            j.sl_no = li.index(j.id) + 1

    @api.onchange('product_qty')
    def set_product_qty(self):
        if self.inventory_id.adj_type in ('receipt', 'issue','damage'):
            # self.product_qty = self.prod_qty
            self.amount = self.product_qty*self.sales_rate

    @api.onchange('product_qty','sales_rate')
    def set_amount_qty(self):
        if self.inventory_id.adj_type =='receipt':
            # self.product_qty = self.prod_qty
            self.amount = self.product_qty * self.sales_rate

    def _get_virtual_location(self):
        return self.product_id.with_context(force_company=self.company_id.id).property_stock_inventory


    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.inventory_id.adj_type in ('issue','damage'):
            self.product_qty = 0
            self.sales_rate = self.product_id.list_price
        if self.inventory_id.adj_type in ('receipt', 'issue','damage'):
            self.product_uom_id=self.product_id.uom_po_id
            self.amount = self.product_qty * self.sales_rate


            # self.lot_uom_id = self.product_id.uom_id

    @api.onchange('prod_lot_id')
    def onchange_prod_lot_id(self):
        if self.inventory_id.adj_type in ('issue','damage') and self.prod_lot_id:
            # self.product_qty = 0
            self.sales_rate = self.prod_lot_id.sales_rate
            self.p_rate = self.prod_lot_id.p_rate
            self.amount = self.product_qty * self.sales_rate
            # if self.sales_rate==0:
            #     self.sales_rate = self.product_id.list_price
            # self.lot_uom_id = self.prod_lot_id.packing
        if self.inventory_id.adj_type =='receipt' and self.prod_lot_id:
            self.prod_qty = self.prod_lot_id.product_qty

    def _check_no_duplicate_line(self):
        for line in self:
            domain = [
                ('id', '!=', line.id),
                ('product_id', '=', line.product_id.id),
                ('location_id', '=', line.location_id.id),
                ('partner_id', '=', line.partner_id.id),
                ('package_id', '=', line.package_id.id),
                ('prod_lot_id', '=', line.prod_lot_id.id),
                ('inventory_id', '=', line.inventory_id.id),
                ('prod_lot_name', '=', line.prod_lot_name)
            ]
            existings = self.search_count(domain)
            if existings:
                raise UserError(_("There is already one inventory adjustment line for this product,"
                                  " you should rather modify this one instead of creating a new one."))

    def generate_moves_custom(self):
        vals_list = []
        for line in self:
            virtual_location = line._get_virtual_location()
            lot_id = None
            if line.prod_lot_id:
                lot_id = line.prod_lot_id.id
            if self.inventory_id.adj_type == 'receipt':
                vals = line._get_move_values_custom(
                    line.product_qty, virtual_location.id, line.location_id.id, lot_id, False)
            else:
                vals = line._get_move_values_custom(
                    line.product_qty, line.location_id.id, virtual_location.id, lot_id, True)
            vals_list.append(vals)
        return self.env['stock.move'].create(vals_list)

    def _get_move_values_custom(self, qty, location_id, location_dest_id, lot_id, out):
        self.ensure_one()
        return {
            'name': _('INV:') + (self.inventory_id.name or ''),
            'product_id': self.product_id.id,
            'product_uom': self.product_uom_id.id,
            'product_uom_qty': qty,
            'date': self.inventory_id.date,
            'company_id': self.inventory_id.company_id.id,
            'inventory_id': self.inventory_id.id,
            'state': 'confirmed',
            'restrict_partner_id': self.partner_id.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'lot_id': lot_id,
                'product_uom_qty': 0,  # bypass reservation here
                'product_uom_id': self.product_uom_id.id,
                'qty_done': qty,
                'package_id': out and self.package_id.id or False,
                'result_package_id': (not out) and self.package_id.id or False,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
                'owner_id': self.partner_id.id,
            })]
        }

    @api.onchange('product_id')
    def set_company(self):
        if self.inventory_id.adj_type in ('receipt', 'issue','damage'):
            self.company_id = self.inventory_id.company_id

    def lot_create_edit(self):

        existing_lot = self.env['stock.production.lot'].search(
            [('name', '=', self.prod_lot_name),
             ('product_id', '=', self.product_id.id),
             ])
        if existing_lot:
            # print( 'name',existing_lot.name == self.prod_lot_name
            # ,'product_id',existing_lot.product_id == self.product_id
            # ,'p_rate',existing_lot.p_rate == self.p_rate
            # ,'packing',existing_lot.packing == self.lot_uom_id
            # ,'sales_rate',existing_lot.sales_rate == self.sales_rate
            # ,'sales_disc',existing_lot.sales_disc == self.sales_disc)
            if existing_lot.name == self.prod_lot_name \
                    and existing_lot.product_id == self.product_id \
                    and existing_lot.sales_rate == self.sales_rate \
                    and existing_lot.packing == self.product_uom_id and existing_lot.expiry == self.expiry:

                self.prod_lot_id = existing_lot
            else:
                raise ValidationError(
                    _(
                        'Lot/Serial number already exists for product %s !') % self.product_id.display_name)
        else:

            lot_id = self.env['stock.production.lot'].create(
                {'name': self.prod_lot_name,
                 'product_id': self.product_id.id,
                 'company_id': self.company_id.id,
                 'product_qty': self.product_qty,
                 'sales_rate': self.sales_rate,
                 'packing': self.product_uom_id.id,
                 'expiry': self.expiry,
                 'p_rate': self.p_rate,
                 }
            )
            self.prod_lot_id = lot_id
            # self.env['stock.production.lot'].search([('name','=',self.prod_lot_name)]).write({'product_qty':self.product_qty})

    def write(self, vals):
        res = super(StockInvetoryLineInh, self).write(vals)
        self._check_no_duplicate_line()
        return res

    def _check_no_duplicate_line(self):
        for line in self:
            domain = [
                ('id', '!=', line.id),
                ('product_id', '=', line.product_id.id),
                ('location_id', '=', line.location_id.id),
                ('partner_id', '=', line.partner_id.id),
                ('package_id', '=', line.package_id.id),
                ('prod_lot_id', '=', line.prod_lot_id.id),
                ('inventory_id', '=', line.inventory_id.id)]
            existings = self.search_count(domain)
            if existings:
                raise UserError(_("There is already one inventory adjustment line for this product,"
                                  " you should rather modify this one instead of creating a new one."))


class StockMove(models.Model):
    _inherit = "stock.move"

    inventory_id = fields.Many2one(
        'stock.inventory', 'Inventory', check_company=True,
        index=True, ondelete='cascade')