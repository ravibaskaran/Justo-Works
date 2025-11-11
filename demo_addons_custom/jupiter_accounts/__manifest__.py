# -*- coding: utf-8 -*-
{
    'name': "Jupiter Accounts (Odoo 18)",

    'summary': """
        Jupiter Accounts - Account Move, Payment, and Incentive Management (Migrated to Odoo 18)""",

    'description': """
        Jupiter Accounts Module

        Features:
        - Account move customizations
        - Payment processing and tracking
        - Incentive voucher management
        - Incentive generation workflow
        - Booking integration
        - Project-account linking
        - Region management
        - Partner extensions
        - Asset management
        - Account head configurations
        - Journal customizations
        - Opening balance updater

        Migrated to Odoo 18:
        - Version updated to 18.0.1.0.0
        - Python models reviewed for compatibility

        REQUIRES TESTING:
        - Account move workflows
        - Payment processing
        - Incentive calculations
        - Booking integrations
        - Project transactions
        - Opening balance updates
        - Asset depreciation
        - Journal entries
        - All model methods and computed fields
    """,

    'author': "Justo Works",
    'website': "http://www.yourcompany.com",

    'category': 'Accounting',
    'version': '18.0.1.0.0',

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
