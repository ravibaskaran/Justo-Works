# -*- coding: utf-8 -*-
{
    'name': " ♦ Partner Ledger ♦ ",

    'summary': """ Shows receivable and payable journal entries of the partners """,

    'author': " Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Accounts Report',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'beta_reports_base',
        'account'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/panel.xml',
        'views/template.xml',
    ],
}
