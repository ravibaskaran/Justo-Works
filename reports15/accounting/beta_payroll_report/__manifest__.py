# -*- coding: utf-8 -*-
{
    'name': "Payroll Report",

    'summary': """ Payroll Report """,

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Payroll Report',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'beta_reports_base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'beta_payroll_report/static/src/js/report.js',
        ],
    }
}
