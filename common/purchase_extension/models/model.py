# ♦ Import ♦
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Date



# ♦ Inherited Res Bank ♦
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    purchase_order = fields.Many2many('purchase.order')
    bill_number = fields.Char()
    tax_summary_ids = fields.One2many("account.move.tax.summary", "move_id")
    purchase_bill_no = fields.Many2many('account.move', 'purchase_bill', 'pur_id', 'move_id', domain="[('move_type','=','in_invoice'),('state', '=', 'posted')]")
    is_asset_purchase = fields.Boolean(default=False)

    # tax_totals_json = fields.Char(compute='_compute_tax_totals_json')

    def print(self):
        self.env.ref('account.account_invoices').sudo().report_type = 'qweb-pdf'
        result = self.env.ref('account.account_invoices').report_action(self)
        self.env.ref('account.account_invoices').sudo().report_type = 'qweb-html'
        result['default_print_option'] = 'print'
        return result



    @api.model
    def default_get(self, default_fields):
        res = super(AccountMoveInherit, self).default_get(default_fields)
        if res.get('move_type') == 'in_invoice':
            res['invoice_date'] = Date.today()
        return res

    @api.depends('invoice_line_ids')
    def _compute_max_line_sequence(self):
        """Allow to know the highest sequence entered in invoice lines.
        Then we add 1 to this value for the next sequence.
        This value is given to the context of the o2m field in the view.
        So when we create new invoice lines, the sequence is automatically
        added as :  max_sequence + 1
        """
        for invoice in self:
            invoice.max_line_sequence = (
                    max(invoice.mapped('invoice_line_ids.sequence') or [0]) + 1)

    max_line_sequence = fields.Integer(string='Max sequence in lines', compute='_compute_max_line_sequence', store=True)

    # ♦ Function to reset Serial Number in Invoice Line Ids ♦
    def _reset_sequence(self):
        for rec in self:
            current_sequence = 1
            for line in rec.invoice_line_ids:
                line.sequence = current_sequence
                current_sequence += 1

    # Setting Serial Number in Write to avoid any disorder in serial
    def write(self, vals):
        self._reset_sequence()
        if not self._context.get('tax_update'):
            self.updateTaxSummary()
        return super(AccountMoveInherit, self).write(vals)

    # Setting Serial Number in Create to avoid any disorder in serial
    @api.model
    def create(self, vals):
        self._reset_sequence()
        return super(AccountMoveInherit, self).create(vals)

    # ▼ Update Tax Line onchange of invoice line ids ▼
    @api.onchange('invoice_line_ids')
    def onchange_invoice_tax_update(self):
        if self.invoice_line_ids and self.move_type in ['in_invoice', 'in_refund']:
            self.updateTaxSummary()
        else:
            self.tax_summary_ids = None

    # ▼ Update Tax ▼
    def updateTaxSummary(self):
        taxdata = {}
        final = [(5, 0, 0)]

        for line in self.invoice_line_ids.filtered(lambda p: p.tax_ids != False):
            price_unit = line.price_unit
            if line.discount != 0:
                price_unit = line.price_unit - (line.price_unit * line.discount / 100)
            for tax in line.tax_ids:
                cgst = 0
                sgst = 0
                igst = 0
                cess = 0
                taxes = tax.compute_all(price_unit, quantity=line.quantity)
                if taxes['taxes']:
                    for comtax in taxes['taxes']:
                        if 'cgst' in comtax['name'].lower():
                            cgst += comtax['amount']
                        elif 'sgst' in comtax['name'].lower():
                            sgst += comtax['amount']
                        elif 'igst' in comtax['name'].lower():
                            igst += comtax['amount']
                        elif 'cess' in comtax['name'].lower():
                            cess += comtax['amount']
                    if tax.id in taxdata:
                        taxdata[tax.id]['total_excluded'] += taxes['total_excluded']
                        taxdata[tax.id]['total_included'] += taxes['total_included']
                        taxdata[tax.id]['cgst'] += cgst
                        taxdata[tax.id]['sgst'] += sgst
                        taxdata[tax.id]['igst'] += igst
                        taxdata[tax.id]['cess'] += cess
                    else:
                        taxdata[tax.id] = {
                            'total_excluded': taxes['total_excluded'],
                            'total_included': taxes['total_included'],
                            'cgst': cgst,
                            'sgst': sgst,
                            'igst': igst,
                            'cess': cess,
                        }
        for item in taxdata:
            if taxdata[item]['cgst'] != 0 or taxdata[item]['sgst'] != 0 or taxdata[item]['igst'] != 0 or taxdata[item]['cess'] != 0:
                try:
                    final.append((0, 0, {
                        'tax_id': item.origin,
                        'cgst': taxdata[item]['cgst'],
                        'sgst': taxdata[item]['sgst'],
                        'igst': taxdata[item]['igst'],
                        'cess': taxdata[item]['cess'],
                        'total_excluded': taxdata[item]['total_excluded'],
                        'total_included': taxdata[item]['total_included'],
                    }))
                except:
                    final.append((0, 0, {
                        'tax_id': item,
                        'cgst': taxdata[item]['cgst'],
                        'sgst': taxdata[item]['sgst'],
                        'igst': taxdata[item]['igst'],
                        'cess': taxdata[item]['cess'],
                        'total_excluded': taxdata[item]['total_excluded'],
                        'total_included': taxdata[item]['total_included'],
                    }))
        self.with_context(tax_update=True).write({'tax_summary_ids': final})

    # ▼ Filtering in Purchase Bill Number ▼
    @api.onchange('partner_id')
    def onchangePartnerIdBillNo(self):
        res = {}
        if self.move_type == 'in_refund':
            if self.partner_id:
                self.update({'purchase_bill_no': None})
                rec = self.env['account.move'].search([
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'in_invoice'),
                    ('state', '=', 'posted')
                ])
                domain = {'purchase_bill_no': [('id', 'in', rec.ids)]}
                res['domain'] = domain
            else:
                rec = self.env['account.move'].search([
                    ('move_type', '=', 'in_invoice'),
                    ('state', '=', 'posted')
                ])
                domain = {'purchase_bill_no': [('id', 'in', rec.ids)]}
                res['domain'] = domain
        if self.bill_number:
            self.bill_number = None
            self.set_bill_number_products()
        if self.purchase_order:
            self.purchase_order = None
            self.display_purchase_order()
        return res

    #  ▼ Previous Purchase Bill ▼
    @api.onchange('purchase_bill_no')
    def purchaseBillNoOnchange(self):
        if self.move_type == 'in_refund' and self.purchase_bill_no:
            partner = self.partner_id
            m = 0
            res = {}
            products = []
            mve = []
            self.update({'invoice_line_ids': None})
            if self.journal_id.loss_account_id:
                account = self.journal_id.loss_account_id
            else:
                raise UserError(_('Please Set Profit and Loss Account in Journal'))
            bill_no = ''
            for i in self.purchase_bill_no.invoice_line_ids:
                m += 1
                if m == 1:
                    partner = i.move_id.partner_id
                if i.move_id not in mve:
                    mve.append(i.move_id)
                    b = (',' + i.move_id.bill_number) if len(mve) > 1 else i.move_id.bill_number
                    bill_no = bill_no + b

                lot = self.env['stock.production.lot'].search([
                    ('product_id', '=', i.product_id.id),
                    ('name', '=', i.lot_name),
                    ('p_rate', '=', i.price_unit)
                ], limit=1).id

                products.append((0, 0, {
                    'sequence': m,
                    'product_id': i.product_id,
                    'quantity': i.quantity,
                    'lot_id': lot,
                    'expiry': i.expiry,
                    'barcode_scan':i.product_id.barcode,
                    'price_unit': i.price_unit,
                    'discount': i.discount,
                    'product_uom_id': i.product_uom_id,
                    'currency_id':i.currency_id.id,
                    'hsn_code': i.product_id.l10n_in_hsn_code,
                    'debit': 0,
                    'credit': 0,
                    'tax_ids': i.tax_ids.ids,

                }))

            self.update({'invoice_line_ids': products})

            for i in self.invoice_line_ids:
                i.account_id = i._get_computed_account()
                i._onchange_price_subtotal()
                i._onchange_mark_recompute_taxes()

            self._onchange_invoice_line_ids()
            self._recompute_tax_lines()
            self.onchange_invoice_tax_update()
            self.partner_id = partner
            self.bill_number = bill_no
            if self.partner_id:
                rec = self.env['account.move'].search([
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'in_invoice'),
                    ('state', '=', 'posted')
                ])
                domain = {'purchase_bill_no': [('id', 'in', rec.ids)]}
                res['domain'] = domain
                return res
            else:
                rec = self.env['account.move'].search([
                    ('move_type', '=', 'in_invoice'),
                    ('state', '=', 'posted')
                ])
                domain = {'purchase_bill_no': [('id', 'in', rec.ids)]}
                res['domain'] = domain
                return res

    #  ▼ Previous Purchase Order ▼
    @api.onchange('purchase_order')
    def display_purchase_order(self):
        if self.move_type == 'in_invoice' and self.purchase_order:
            partner = self.partner_id
            order_products = []
            self.update({'invoice_line_ids': None})
            m = 0
            for i in self.purchase_order.order_line:
                m += 1
                order_quantity = i.product_qty
                order_products.append((0, 0, {
                    'sequence': m,
                    'product_id': i.product_id,
                    'quantity': order_quantity,
                    'price_unit': i.price_unit,
                    'product_uom_id': i.product_uom,
                    'barcode_scan': i.product_id.barcode,
                    'currency_id': i.currency_id,
                    'hsn_code': i.product_id.l10n_in_hsn_code,
                    'debit': 0,
                    'credit': 0,
                    'tax_ids': i.taxes_id,
                }))
            self.update({'invoice_line_ids': order_products})

            for i in self.invoice_line_ids:
                i.account_id = i._get_computed_account()
                i._onchange_price_subtotal()
                i._onchange_mark_recompute_taxes()

            self._onchange_invoice_line_ids()
            self._recompute_tax_lines()
            self.onchange_invoice_tax_update()
            self.partner_id = partner

    @api.onchange('bill_number')
    def vendor_warning(self):
        if self.bill_number:
            if not self.partner_id:
                self.bill_number = None
                return {
                    'warning': {
                        'title': _('Warning!'),
                        'message': _('Vendor not selected'),
                    },
                }

    @api.onchange('bill_number')
    def set_bill_number_products(self):
        partner = self.partner_id
        if self.move_type == 'in_invoice' and self.bill_number:
            if self.bill_number:
                inv = self.env['account.move'].search([
                    ('bill_number', '=', self.bill_number),
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'in_invoice')
                ])
                if inv:
                    return {
                        'warning': {
                            'title': _('Warning!'),
                            'message': _('Bill Number already exists for the vendor'),
                        },
                    }

        if self.move_type == 'in_refund' and self.bill_number:
            if self.bill_number:
                self.update({'invoice_line_ids': [(5, 0, 0)]})
                bill_products = self.env['account.move'].search([
                    ('bill_number', '=', self.bill_number),
                    ('move_type', '=', 'in_invoice'),
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'posted')
                ], order='id desc', limit=1)
                for rec in self:
                    bprod = []
                    for i in bill_products.invoice_line_ids:
                        if i.lot_name:
                            lot_id = rec.env['stock.production.lot'].search([
                                ('name', '=', i.lot_name),
                                ('product_id', '=', i.product_id.id)
                            ], limit=1).id
                            bprod.append((0, 0, {
                                'sequence': i.sl_no,
                                'product_id': i.product_id,
                                'lot_id': lot_id,
                                'hsn_code': i.hsn_code,
                                'barcode_scan': i.product_id.barcode,
                                'product_uom_id': i.product_uom_id,
                                'price_unit': i.price_unit,
                                'discount': i.discount,
                                'currency_id':i.currency_id.id,
                                'tax_ids': i.tax_ids,
                                'account_id': i._get_computed_account(),
                                'debit': 0,
                                'credit': 0,
                                'quantity': None,

                            }))
                        else:
                            bprod.append((0, 0, {

                                'sequence': i.sl_no,
                                'product_id': i.product_id,
                                'lot_id': None,
                                'hsn_code': i.hsn_code,
                                'product_uom_id': i.product_uom_id,
                                'barcode_scan': i.product_id.barcode,
                                'price_unit': i.price_unit,
                                'discount': i.discount,
                                'tax_ids': i.tax_ids,
                                'currency_id': i.currency_id.id,
                                'account_id': i._get_computed_account(),
                                'debit': 0,
                                'credit': 0,
                                'quantity': None,

                            }))

                    rec.update({'invoice_line_ids': bprod})
                    rec.purchase_bill_no = bill_products.ids


            else:
                self.update({'invoice_line_ids': [(5, 0, 0)]})
                self.write({'invoice_line_ids': [(5, 0, 0)]})
                self.purchase_bill_no = None
            self.partner_id = partner

    def action_post_custom(self):
        purchase_order = []
        if self.move_type == 'in_invoice':

            if self.purchase_order:
                for i in self.purchase_order:
                    purchase_order.append(i.id)
            generate_invoice_lines = []
            bill_no = 1
            last_bill_no = self.env['account.move'].search([('state','=','posted'),('move_type','=','in_invoice')],order='id desc', limit=1)
            if self.journal_id:
                if self.journal_id.sequence_id.date_range_ids:
                    for i in self.journal_id.sequence_id.date_range_ids[-1]:
                        bill_no = i.number_next_actual
            if last_bill_no:
                # bill_no = last_bill_no.name.split('/')
                # if len(bill_no) > 2:
                #     bill_no = int(bill_no[2]) + 1
                if last_bill_no.date > self.date:
                    raise ValidationError('Backdate Entry on Accounting Date is BLocked')

            for line in self.invoice_line_ids:
                if line.price_unit and line.product_id and line.product_id.type != 'service' and line.product_id.sale_ok is True:
                    line.product_id.standard_price = line.price_unit
                    line.product_id.list_price = line.price_unit
                if line.product_id.generate_serial_number:
                    qty = line.quantity
                    free_qty = line.free_qty
                    serial_number = int(line.sl_no)
                    first_index = 1
                    lot_name = line.lot_name
                    if qty > 0:
                        for i in range(int(qty)):
                            if first_index < 10:
                                first_inx = '00' + str(first_index)
                            elif first_index < 100:
                                first_inx = '0' + str(first_index)
                            else:
                                first_inx = str(first_index)
                            lot = lot_name + '-' + str(bill_no) + '-' + str(first_inx)
                            generate_invoice_lines.append((0, 0, {
                                'sequence': serial_number,
                                'product_id': line.product_id,
                                'lot_name': lot,
                                'hsn_code': line.hsn_code,
                                'expiry': line.expiry,
                                'barcode_scan': line.product_id.barcode,
                                'product_uom_id': line.product_uom_id,
                                'price_unit': line.price_unit,
                                'discount': line.discount,
                                'currency_id': line.currency_id.id,
                                'tax_ids': line.tax_ids,
                                'account_id': line._get_computed_account(),
                                'debit': 0,
                                'credit': 0,
                                'quantity': 1,
                            }))
                            first_index += 1
                            serial_number += 1
                    if free_qty > 0:
                        for i in range(int(free_qty)):
                            if first_index < 10:
                                first_inx = '00' + str(first_index)
                            elif first_index < 100:
                                first_inx = '0' + str(first_index)
                            else:
                                first_inx = str(first_index)
                            lot = lot_name + '-' + str(bill_no) + '-' + str(first_inx)
                            generate_invoice_lines.append((0, 0, {
                                'sequence': serial_number,
                                'product_id': line.product_id,
                                'lot_name': lot,
                                'hsn_code': line.hsn_code,
                                'expiry': line.expiry,
                                'barcode_scan': line.product_id.barcode,
                                'product_uom_id': line.product_uom_id,
                                'price_unit': line.price_unit,
                                'discount': line.discount,
                                'currency_id': line.currency_id.id,
                                'tax_ids': line.tax_ids,
                                'account_id': line._get_computed_account(),
                                'debit': 0,
                                'credit': 0,
                                'quantity': 0,
                                'free_qty': 1,
                            }))
                            first_index += 1
                            serial_number += 1
                    self.update({'invoice_line_ids': [(3, line.id)]})
            if generate_invoice_lines:
                self.invoice_line_ids = generate_invoice_lines
                self._recompute_dynamic_lines()
                self._reset_sequence()
        if not self.purchase_order and purchase_order:
            self.update({'purchase_order': [(6, 0, purchase_order)]})
        return super(AccountMoveInherit, self).action_post_custom()



# ♦ ▼ Inherited 'Account Move Line'. ▼ ♦
class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    sl_no = fields.Integer(related="sequence", help="Shows the sequence of this line in the "" invoice.")
    barcode_scan = fields.Char()
    hsn_code = fields.Char()
    purchase_order_id = fields.Char(store=True)
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

    @api.onchange('lot_id')
    def set_lot_values(self):
        if self.move_id.move_type == "in_refund":
            if self.lot_id:
                self.expiry = self.lot_id.expiry
                self.price_unit = self.lot_id.p_rate

    @api.onchange('product_id')
    def onchangeProductIdField(self):
        if self.product_id:
            self.hsn_code = self.product_id.l10n_in_hsn_code
            self.barcode_scan = self.product_id.barcode
            if self.move_id.move_type not in ['in_invoice','in_refund']:
                self.price_unit = self.product_id.standard_price
            else:
                self.price_unit = self.product_id.list_price

    @api.onchange('lot_id')
    def onchangeBatchIDField(self):
        if self.product_id and self.lot_id:
            self.price_unit = self.lot_id.p_rate

    # @api.onchange('product_id')
    # def onchange_purchase_product(self):
    #     if self.product_id and self.move_id.move_type == 'in_invoice':
    #         if self.product_id.tracking == 'lot':
    #             lot = self.env['account.move.line'].search(
    #                 [('move_id.move_type', '=', 'in_invoice'), ('product_id', '=', self.product_id.id),
    #                  ('lot_name', '!=', None)], order='id desc', limit=1)
    #             if lot:
    #                 self.lot_name = lot.lot_name
    #
    # @api.onchange('lot_name')
    # def set_price_unit(self):
    #     if self.product_id and self.move_id.move_type == 'in_invoice':
    #         if self.product_id.tracking == 'lot':
    #             if self.lot_name:
    #                 lot_id = self.env['stock.production.lot'].search(
    #                     [('product_id', '=', self.product_id.id), ('name', '=', self.lot_name)])
    #                 if lot_id:
    #                     self.price_unit = lot_id.p_rate
    #                     self.product_uom_id = lot_id.packing



