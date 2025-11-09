# -*- coding: utf-8 -*-
{
    'name': "Employee Project Details",

    'summary': """
        Odoo 15 Employee Project Details
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
