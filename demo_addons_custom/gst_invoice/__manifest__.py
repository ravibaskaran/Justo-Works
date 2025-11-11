# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "GST - Returns and Invoices (Odoo 18)",
  "summary"              :  """Odoo GST - Returns and Invoices helps to file the monthly return that summarizes all outward supplies by registered taxpayers (Migrated to Odoo 18)""",
  "category"             :  "Accounting",
  "version"              :  "18.0.2.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-GST-Invoices.html",
  "description"          :  """GST - Returns and Invoices
GST
One Nation One Tax
Tax
Odoo Tax
Odoo GST
Returns and Invoices
Goods and Services Tax
Tax module
Tax App
GST module
Goods and Services Tax in Odoo""",
  "live_test_url"        :  "https://odoo13-demo.webkul.com/web/?db=gst_db#action=272&cids=1&menu_id=165&model=gst.dashboard&view_type=kanban",
  "depends"              :  [
                             'l10n_in',
                             'account_tax_python',
                            ],
  "data"                 :  [
                             'data/data_unit_quantity_code.xml',
                             'data/data_uom_mapping.xml',
                             'data/data_dashboard.xml',
                             'security/gst_security.xml',
                             'security/ir.model.access.csv',
                             'wizard/message_wizard_view.xml',
                             'wizard/invoice_type_wizard_view.xml',
      # 'wizard/branch_hsn.xml',
                             'data/gob_server_actions.xml',
                             'views/account_move_view.xml',
                             'views/gst_view.xml',
                             'views/gstr2_view.xml',
                             'views/res_partner_views.xml',
                             'views/gst_templates.xml',
                             'views/gst_dashboard_view.xml',
                             'views/account_fiscalyear_view.xml',
                             'views/ir_attachment_view.xml',
                             'views/account_period_view.xml',
                             'views/gst_sequence.xml',
                             'views/unit_quantity_code_view.xml',
                             'views/uom_map_view.xml',
                             'views/gst_action_view.xml',
                             'views/gst_menu_view.xml',
                             'views/account_tax_view_inherit.xml',
'views/gst_invoice.xml',

                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
    'assets': {
        'web.assets_backend': [
            'gst_invoice/static/src/scss/gst_dashboard.scss',
            'gst_invoice/static/src/js/gst_dashboard.js',
        ],
        'web.assets_qweb': [
            'gst_invoice/views/gst_templates.xml',
        ],
    },
  "description"          :  """GST - Returns and Invoices

Migrated to Odoo 18:
- Version updated to 18.0.2.0.0
- Dashboard JS widget migrated to OWL Component
- NVD3 chart integration preserved

REQUIRES TESTING:
- GST calculations and tax computations
- GSTR1/GSTR2 report generation
- Dashboard charts (line and bar)
- Invoice workflows
- Wizard functionality
- Controller endpoints

Original Features:
GST
One Nation One Tax
Tax
Odoo Tax
Odoo GST
Returns and Invoices
Goods and Services Tax
Tax module
Tax App
GST module
Goods and Services Tax in Odoo""",}
}
