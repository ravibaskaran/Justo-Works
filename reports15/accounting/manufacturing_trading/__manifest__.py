# -*- coding: utf-8 -*-
{
    'name': "Manufacturing & Trading A/C",

    'summary': """
        Odoo 15 Manufacturing & Trading A/C
    """,

    'author': "",
    'category': 'Accounting',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'account', 'base_accounting_kit'],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_head_type.xml',
        'views/templates.xml',
        'views/panel.xml',
        'views/pdf_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'manufacturing_trading/static/src/js/report.js',
        ],
    }
}
