# -*- coding: utf-8 -*-
{
    'name': "Developer Ageing Report",

    'summary': """
        Odoo 15 Developer Ageing
    """,

    'author': "",
    'category': 'Real Estate',
    'version': '18.0.1',

    'depends': ['base', 'beta_reports_base', 'itsys_real_estate'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
    ],
}
