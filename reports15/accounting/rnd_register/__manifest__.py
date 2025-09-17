# -*- coding: utf-8 -*-
{
    'name': "Receipt and Disbursement",

    'summary': """ Used to construct a cash flow forecast """,

    'author': " Inexoft Technologies ",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Accounts Report',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'beta_reports_base',
        'account',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/panel.xml',
        'views/template.xml',
        'views/pdf_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'rnd_register/static/src/js/report.js',
        ],
    }

}
