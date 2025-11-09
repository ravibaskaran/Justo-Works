# -*- coding: utf-8 -*-
{
    'name': "Account Voucher",
    'summary': """
        Account Voucher
        """,
    'description': """
        Account Voucher
    """,
    'author': "Inexoft Technologies",
    'website': "https://www.inexoft.com",

    'category': 'accounting',
    'version': '18.0.0.1',
    'depends': ['account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/direct_journal_entry_views.xml',
        'reports/reports.xml',
        'views/menu_views.xml',
    ],
}
