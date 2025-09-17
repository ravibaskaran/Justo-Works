# -*- coding: utf-8 -*-
{
    'name': "General Ledger",

    'summary': """
        Odoo 15 General Ledger
    """,

    'author': "",
    'category': 'Accounting',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config.xml',
        'views/templates.xml',
        'views/panel.xml',
    ],
}
