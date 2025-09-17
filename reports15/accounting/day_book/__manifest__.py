# -*- coding: utf-8 -*-
{
    'name': "Day Book",

    'summary': """
        Odoo 15 Day Book
    """,

    'author': "",
    'category': 'Accounting',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
        'views/res_config.xml',
    ],
}
