# -*- coding: utf-8 -*-
{
    'name': "jupiter_accounts",

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
    'depends': ['base', 'purchase_extension', 'itsys_real_estate', 'project_transactions', 'real_estate_extension',
                'account_check_printing', 'base_accounting_kit'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/product.xml',
        'views/configurations.xml',
        'views/project.xml',
        'views/booking.xml',
        'views/incentive_voucher.xml',
        'views/registration.xml',
        'views/region.xml',
        'views/incentive_generation.xml',
        'views/invoices.xml',
        'views/account_head.xml',
        'views/partner.xml',
        'views/opening_updater.xml',
        'views/account_payment.xml',
        'views/settings.xml',
        'views/journals.xml',
        'views/menu.xml',
        'views/account_assets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
