from odoo import models, fields, api
from lxml import etree


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_normal_user = fields.Boolean()
    enable_menu_hide = fields.Boolean()

    menu_project = fields.Boolean('Project')
    menu_property_masters = fields.Boolean('Property Masters')
    menu_masters = fields.Boolean('Masters')

    menu_transactions = fields.Boolean('Transactions')
    menu_project_evaluation_sheet = fields.Boolean('Project Evaluation Sheet')
    menu_competition_sheet = fields.Boolean('Competition Sheet')
    menu_term_sheet = fields.Boolean('Term Sheet')
    menu_retention_receipt_voucher = fields.Boolean('Retention Receipt Voucher')
    menu_project_assigning = fields.Boolean('Project Assigning')
    menu_loan_status_marking = fields.Boolean('Loan Status Marking')
    menu_registration = fields.Boolean('Registration')
    menu_budgeting = fields.Boolean('Budgeting')
    menu_project_employee_assigning = fields.Boolean('Project Employee Assigning')
    menu_project_target = fields.Boolean('Project Target')
    menu_incentive_generation = fields.Boolean('Incentive Generation')

    menu_property_booking = fields.Boolean('Property Booking')
    menu_invoices = fields.Boolean('Invoices')
    menu_config = fields.Boolean('Config')
    menu_settings = fields.Boolean('Settings')

    menu_accounting = fields.Boolean('Accounting')
    menu_gst = fields.Boolean('GST')
    menu_dashboard_1 = fields.Boolean('Dashboard 1')
    menu_dashboard_2 = fields.Boolean('Dashboard 2')
    menu_reports = fields.Boolean('Reports')
    menu_purchase_reports = fields.Boolean('Purchase Reports')
    menu_inventory_reports = fields.Boolean('Inventory Reports')
    menu_invoice_reports = fields.Boolean('Invoice Reports')
    menu_project_reports = fields.Boolean('Project Reports')

    menu_employees = fields.Boolean('Employees')

    allow_booking_confirm_backdate = fields.Boolean()
    show_booking_cancel = fields.Boolean()
    show_booking_reset_to_draft_in_confirm_state = fields.Boolean()
    booking_cancel_anytime = fields.Boolean()
    show_booking_reset_to_draft = fields.Boolean()
    show_evaluation_sheet_term_sheet_budgeting_confirm_button = fields.Boolean('Show Evaluation Sheet, Term Sheet & Budgeting Confirm Button')
    all_projects_access = fields.Boolean()
    booking_confirm_anytime = fields.Boolean()
    project_configurations = fields.Boolean()
    dashboard_3 = fields.Boolean('Show Dashboard')
    show_ctc_btn = fields.Boolean('Show CTC')
    booking_by_region = fields.Boolean('')



    def action_access_control(self):
        data = {
            'allow_booking_confirm_backdate': 'itsys_real_estate.group_booking_confirm_backdate',
            'show_booking_cancel': 'itsys_real_estate.group_booking_cancel',
            'show_booking_reset_to_draft_in_confirm_state': 'itsys_real_estate.group_booking_reset_to_draft_confirmed',
            'booking_cancel_anytime': 'itsys_real_estate.group_booking_cancel_anytime',
            'show_booking_reset_to_draft': 'itsys_real_estate.group_booking_reset_to_draft',
            'show_evaluation_sheet_term_sheet_budgeting_confirm_button': 'real_estate_sheets.group_evaluation_budgeting_confirm',
            'all_projects_access': 'project_transactions.view_all_projects',
            'booking_by_region': 'project_transactions.group_region_booking_user',
            'booking_confirm_anytime': 'itsys_real_estate.group_booking_confirm_anytime',
            'project_configurations': 'jupiter_accounts.group_project_configurations',
            'dashboard_3': 'jupiter_dashboard_tres.group_jupiter_dashboard_tres',
            'show_ctc_btn': 'real_estate_extension.group_user_ctc_show',
        }
        for field_name, group_xml_id in data.items():
            group_id = self.env.ref(group_xml_id)
            field_value = getattr(self, field_name)
            group_id.sudo().write({'users': [((4 if field_value else 3), self.id)]})

    @api.onchange('menu_project')
    def onchange_menu_project(self):
        if self.menu_project:
            value = True
        else:
            value = False
        self.menu_property_masters = value
        self.menu_masters = value
        self.menu_transactions = value
        self.menu_property_booking = value
        self.menu_invoices = value
        self.menu_config = value
        self.menu_settings = value


    @api.onchange('menu_transactions')
    def onchange_menu_transactions(self):
        if self.menu_transactions:
            value = True
        else:
            value = False
        self.menu_project_evaluation_sheet = value
        self.menu_competition_sheet = value
        self.menu_term_sheet = value
        self.menu_retention_receipt_voucher = value
        self.menu_project_assigning = value
        self.menu_loan_status_marking = value
        self.menu_registration = value
        self.menu_budgeting = value
        self.menu_project_employee_assigning = value
        self.menu_project_target = value
        self.menu_incentive_generation = value

    @api.onchange('menu_reports')
    def onchange_menu_reports(self):
        if self.menu_reports:
            value = True
        else:
            value = False
        self.menu_purchase_reports = value
        self.menu_inventory_reports = value
        self.menu_invoice_reports = value
        self.menu_project_reports = value

    def hide_menus_by_user(self):
        if self.enable_menu_hide:
            menu_field_mapping = {
                'itsys_real_estate.menu_building_list': 'menu_property_masters',
                'itsys_real_estate.menu_masters': 'menu_masters',
                'real_estate_sheets.evaluation_sheet_menu': 'menu_project_evaluation_sheet',
                'real_estate_sheets.competition_sheet_menu': 'menu_competition_sheet',
                'real_estate_sheets.term_sheet_menu': 'menu_term_sheet',
                'real_estate_sheets.retention_receipt_voucher_menu': 'menu_retention_receipt_voucher',
                'project_transactions.project_assigning_menu': 'menu_project_assigning',
                'project_transactions.loan_status_marking_menu': 'menu_loan_status_marking',
                'project_transactions.project_registration_menu': 'menu_registration',
                'real_estate_sheets.budget_sheet_menu': 'menu_budgeting',
                'project_transactions.project_employee_assigning_menu': 'menu_project_employee_assigning',
                'project_transactions.project_target_menu': 'menu_project_target',
                'jupiter_accounts.incentive_generation_menu': 'menu_incentive_generation',
                'itsys_real_estate.menu_reservation_main': 'menu_property_booking',
                'jupiter_accounts.project_invoices_menu': 'menu_invoices',
                'jupiter_accounts.project_config_menu': 'menu_config',
                'itsys_real_estate.menu_settings': 'menu_settings',
                'account_vouchers.accounting_menu_main': 'menu_accounting',
                'gst_invoice.gst_parent_menu': 'menu_gst',
                'jupiter_dashboard.menu_jupiter_dashboard': 'menu_dashboard_1',
                'jupiter_dashboard_deux.menu_jupiter_dashboard_deux': 'menu_dashboard_2',
                'reports_menu.purchase_menu': 'menu_purchase_reports',
                'reports_menu.inventory_root_menu': 'menu_inventory_reports',
                'real_estate_extension.project_invoice_reports': 'menu_invoice_reports',
                'itsys_real_estate.real_estate_report_menu': 'menu_project_reports',
                'hr.menu_hr_root': 'menu_employees'
            }
            update_list = []

            all_required_menus_true = (
                self.menu_project_evaluation_sheet and
                self.menu_competition_sheet and
                self.menu_term_sheet and
                self.menu_retention_receipt_voucher and
                self.menu_project_assigning and
                self.menu_loan_status_marking and
                self.menu_registration and
                self.menu_budgeting and
                self.menu_project_employee_assigning and
                self.menu_project_target and
                self.menu_incentive_generation
            )
            menu_transactions = self.env.ref('itsys_real_estate.project_transaction_main_menu')
            if all_required_menus_true:
                update_list.append((4, menu_transactions.id))
            else:
                update_list.append((3, menu_transactions.id))

            all_additional_menus_true = (
                    self.menu_property_masters and
                    self.menu_masters and
                    self.menu_transactions and
                    self.menu_property_booking and
                    self.menu_invoices and
                    self.menu_config and
                    self.menu_settings
            )
            menu_project = self.env.ref('itsys_real_estate.menu_itsys_real_estate')
            if all_additional_menus_true and all_required_menus_true:
                update_list.append((4, menu_project.id))
            else:
                update_list.append((3, menu_project.id))

            all_report_menus_true = (
                self.menu_purchase_reports and
                self.menu_inventory_reports and
                self.menu_invoice_reports and
                self.menu_project_reports
            )
            menu_reports = self.env.ref('reports_menu.report_menu')
            if all_report_menus_true:
                update_list.append((4, menu_reports.id))
            else:
                update_list.append((3, menu_reports.id))

            for menu_xml_id, field_name in menu_field_mapping.items():
                menu_item = self.env.ref(menu_xml_id)
                field_value = getattr(self, field_name)
                if field_value:
                    update_list.append((4, menu_item.id))
                else:
                    update_list.append((3, menu_item.id))
            self.sudo().hide_menu_access_ids = update_list

    @api.model
    def create(self, values):
        res = super(ResUsers, self).create(values)
        if res.is_normal_user:
            res.hide_menus_by_user()
            default_hide_menus = [
                (4, self.env.ref('sale.sale_menu_root').id),
                (4, self.env.ref('account.menu_finance').id),
                (4, self.env.ref('purchase.menu_purchase_root').id),
                (4, self.env.ref('stock.menu_stock_root').id),
                (4, self.env.ref('base.menu_management').id),
                (4, self.env.ref('base.menu_administration').id),
            ]
            res.sudo().hide_menu_access_ids = default_hide_menus
            res.action_access_control()
        return res

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if self.is_normal_user and 'hide_menu_access_ids' not in vals:
            self.hide_menus_by_user()
            self.action_access_control()
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self._context.get('default_is_normal_user'):
            if res.get('toolbar', False) and res.get('toolbar').get('action', False):
                action_list = []
                actions = res.get('toolbar').get('action')
                for action in actions:
                    if action.get('name', False) and action.get('name') == 'Change Password':
                        action_list.append(action)
                res['toolbar']['action'] = action_list
            if view_type in ['form', 'tree']:
                view_xml = res.get('arch')
                if view_xml:
                    doc = etree.XML(res['arch'])
                    doc.set('delete', '0')
                    # doc.set('duplicate', '0')
                    res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
