# -*- coding: utf-8 -*-
{
    'name': "Project Wise Registration Report",

    'summary': """
        Odoo 15 Project Wise Registration Report
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
