# -*- coding: utf-8 -*-
{
    'name': "Cash Book",

    'summary': """
        Odoo 15 Cash Book
    """,

    'author': "",
    'category': 'Accounting',
    'version': '18.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config.xml',
        'views/templates.xml',
        'views/panel.xml',
        'views/pdf_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cash_book/static/src/js/report.js',
        ],
    }
}
