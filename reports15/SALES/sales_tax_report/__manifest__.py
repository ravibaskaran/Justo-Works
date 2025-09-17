# -*- coding: utf-8 -*-
{
    'name': "Sales Tax Report",

    'summary': """
        Odoo 15 Sales Tax Reports
    """,

    'author': "",
    'category': 'Sales',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/sale_tax_view.xml',
    ],
}