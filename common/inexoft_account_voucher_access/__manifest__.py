# -*- coding: utf-8 -*-
{
    'name': "Account Voucher Access by Inexoft",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '18.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'snailmail_account', 'inexoft_account_voucher', 'inexoft_freight_charges', 'l10n_in'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/menus.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
