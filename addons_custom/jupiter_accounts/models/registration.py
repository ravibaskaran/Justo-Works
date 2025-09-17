from odoo import models, fields
from odoo.exceptions import UserError


class ProjectRegistration(models.Model):
    _inherit = 'project.registration'

    employee_invoice_ids = fields.Many2many('account.move')
    employee_invoice_count = fields.Integer(compute='compute_employee_invoice_count')
    developer_invoice_id = fields.Many2one('account.move')

    def compute_employee_invoice_count(self):
        for rec in self:
            rec.employee_invoice_count = len(rec.employee_invoice_ids)

    def view_developer_invoice(self):
        form_view_id = self.env.ref("account.view_move_form").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [(form_view_id, 'form')],
            'res_id': self.developer_invoice_id.id,
        }

    def view_employee_incentives(self):
        form_view_id = self.env.ref("account.view_move_form").id
        tree_view_id = self.env.ref("account.view_invoice_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incentives',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'domain': [('id', 'in', self.employee_invoice_ids.ids)],
        }

    def employee_invoice_creation(self, employee, amount, config, role):
        if employee:
            partner = employee.partner_id
            if not partner:
                partner = employee.user_id.partner_id
                employee.partner_id = partner.id
            if not partner:
                partner = self.env['res.partner'].search([('name', '=', employee.name)], limit=1)
                employee.partner_id = partner.id
            if not partner:
                partner = self.env['res.partner'].sudo().create({
                    'name': employee.name,
                    'company_id': self.env.company.id,
                    'is_employee': True
                })
                employee.partner_id = partner.id
            product = config.incentive_product
            vals = {
                'project_invoice_type': 'employee_invoice',
                'ref': '',
                'narration': role,
                'move_type': 'in_invoice',
                'direct_move_type': 'incoming',
                'currency_id': self.env.company.currency_id.id,
                'partner_id': partner.id,
                'payment_reference': '',
                'invoice_origin': self.flat_id.name,
                'company_id': self.env.company.id,
                'l10n_in_gst_treatment': False,
                'is_project_invoice': True,
                'project_id': self.project_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': product.name,
                    'product_id': product.id,
                    'quantity': 1,
                    'price_unit': amount,
                    'tax_ids': [(6, 0, product.supplier_taxes_id.ids)],
                    'currency_id': self.env.company.currency_id.id
                })]
            }
            invoice_id = self.env['account.move'].create(vals)
            self.employee_invoice_ids += invoice_id
            invoice_id.action_post_custom()
            return invoice_id

    def action_confirm(self):
        res = super(ProjectRegistration, self).action_confirm()
        config = self.env['project.configurations'].search([('activate', '=', True)], limit=1)
        # If the project has Incentives enabled
        if self.project_id.incentive_type == '1':
            if not config:
                raise UserError('Configuration not found!')
            if not config.incentive_product:
                raise UserError('Incentive service product not found in configurations!')
            booking = self.env['unit.reservation'].search([('building_unit', '=', self.flat_id.id), ('state', 'not in', ('draft', 'cancel'))], limit=1)
            if booking:
                # Create Incentive Invoices for Employees
                incentive_voucher = self.env['employee.incentive.move'].search([('date', '<', booking.date), ('project_id', '=', self.project_id.id)], order='date desc', limit=1)
                if incentive_voucher:
                    self.employee_invoice_creation(booking.closing_manager_id, incentive_voucher.closing_manager_amount, config, 'Closing Manager')
                    self.employee_invoice_creation(booking.sourcing_manager_id, incentive_voucher.sourcing_manager_amount, config, 'Sourcing Manager')
                    self.employee_invoice_creation(booking.closing_tl_id, incentive_voucher.closing_tl_amount, config, 'Closing TL')
                    self.employee_invoice_creation(booking.sourcing_tl_id, incentive_voucher.sourcing_tl_amount, config, 'Sourcing TL')
                    self.employee_invoice_creation(booking.crm_id, incentive_voucher.crm_amount, config, 'CRM')
                    self.employee_invoice_creation(booking.marketing_id, incentive_voucher.marketing_amount, config, 'Marketing')
                else:
                    raise UserError('No Incentive Rate Slab Found!')
            else:
                raise UserError('No Booking Found!')
        booking = self.env['unit.reservation'].search(
            [('building_unit', '=', self.flat_id.id), ('state', 'not in', ('draft', 'canceled'))], limit=1)
        # booking spot booking & cp brokerage invoice creation
        booking.create_cp_brokerage_invoice()
        booking.create_spot_booking_invoice()
        # Developer Invoice Creation
        developer_commission_percentage = booking.developer_commission_percentage
        if developer_commission_percentage > 0:
            if not config:
                raise UserError('Configuration not found!')
            if not config.developer_invoice_product:
                raise UserError('Incentive service product not found in configurations!')
            product = config.developer_invoice_product
            # Developer Partner
            # Create the developer Invoice
            partner = self.project_id.partner_id
            if not partner:
                raise UserError('No developer in project!')

            if booking:
                # Calculate Invoice Amount
                amount = booking.flat_cost_real * developer_commission_percentage / 100
                vals = {
                    'project_invoice_type': 'developer_invoice',
                    'ref': '',
                    'move_type': 'out_invoice',
                    'currency_id': self.env.company.currency_id.id,
                    'partner_id': partner.id,
                    'payment_reference': '',
                    'invoice_origin': self.flat_id.name,
                    'company_id': self.env.company.id,
                    'l10n_in_gst_treatment': False,
                    'is_project_invoice': True,
                    'project_id': self.project_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': product.name,
                        'product_id': product.id,
                        'quantity': 1,
                        'price_unit': amount,
                        'tax_ids': [(6, 0, product.taxes_id.ids)],
                        'currency_id': self.env.company.currency_id.id
                    })]
                }
                # Create the developer Invoice
                invoice_id = self.env['account.move'].create(vals)
                self.developer_invoice_id = invoice_id
                #  Post the Invoice if Required
                if self.env['ir.config_parameter'].sudo().get_param('jupiter_accounts.developer_invoice_creation_state') == 'posted':
                    invoice_id.action_post_custom()
            else:
                raise UserError('No Booking Found!')
        return res
