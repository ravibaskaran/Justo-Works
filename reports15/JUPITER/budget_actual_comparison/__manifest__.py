# -*- coding: utf-8 -*-
{
    'name': "Collection Target Report",

    'summary': """
        Odoo 15 Collection Target Report
    """,

    'author': "",
    'category': 'Real Estate',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'itsys_real_estate'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
    ],
}
