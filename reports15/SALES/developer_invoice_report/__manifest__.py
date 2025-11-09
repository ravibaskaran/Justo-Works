# -*- coding: utf-8 -*-
{
    'name': "Developer Invoice Report",

    'summary': """
        Odoo 15 Developer Invoice Reports
    """,

    'author': "",
    'category': 'Sales',
    'version': '18.0.1',

    'depends': ['base', 'beta_reports_base', 'real_estate_extension'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/panel.xml',
    ],
}