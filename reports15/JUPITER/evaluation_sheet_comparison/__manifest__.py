# -*- coding: utf-8 -*-
{
    'name': "Evaluation Sheet Comparison",

    'summary': """
        Odoo 15 Evaluation Sheet Comparison
    """,

    'author': "",
    'category': 'Accounting',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'real_estate_sheets'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
    ],
}
