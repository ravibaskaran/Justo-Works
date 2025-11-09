# -*- coding: utf-8 -*-
{
    'name': "Sales Summary",

    'summary': """
        Odoo 15 Sales Summary
    """,

    'author': "",
    'category': 'Sales',
    'version': '18.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/panel.xml',
    ],
}