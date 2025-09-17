# -*- coding: utf-8 -*-
{
    'name': "Incentive Invoice Report",

    'summary': """
        Odoo 15 Incentive Invoice Reports
    """,

    'author': "",
    'category': 'Sales',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'real_estate_extension'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/panel.xml',
    ],
}