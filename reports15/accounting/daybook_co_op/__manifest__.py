# -*- coding: utf-8 -*-
{
    'name': " ♦ Daybook Co-Op ♦ ",

    'summary': """ Daybook Co-Op Odoo 15 """,

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Accounts Report',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'beta_reports_base',
        'account',
        'base_setup',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/panel.xml',
        'views/template.xml',
        'views/pdf_report.xml',
        'views/config_strict.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'daybook_co_op/static/src/js/report.js',
        ],
    }
}
