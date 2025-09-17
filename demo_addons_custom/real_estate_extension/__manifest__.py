# -*- coding: utf-8 -*-
{
    'name': "Real Estate Masters",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'base_accounting_kit',
        'bank_reconciliation',
        'itsys_real_estate',
        'inexoft_account_voucher',
        'inexoft_account_payments',
        'purchase',
        'account_vouchers',
        'purchase_extension',

        'cash_book',
        'day_book',
        'general_ledger',
        'trial_balance',
        'manufacturing_trading',
        'profit_loss_balance_sheet',
        'purchase_detail',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/employee_fetching_api.xml',
        'demo/demo.xml',
        'views/views.xml',
        'views/employee.xml',
        'views/partner.xml',
        'views/bank.xml',
        'views/account_head.xml',
        'views/menu.xml',
        'views/payment.xml',
        'views/sequences.xml',
        'views/product.xml',
        'views/purchase_order.xml',
        'views/account_move.xml',
        'views/invoice_print.xml',
        'views/cost_center.xml',
        'views/api.xml',
        'views/asset.xml',
        'views/api_log.xml',
        'views/settings.xml',
        'views/mail_templates.xml',
        'views/users.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'real_estate_extension/static/src/js/fields.js',
            'real_estate_extension/static/src/js/one2manySearch.js',
        ]
    },
}
