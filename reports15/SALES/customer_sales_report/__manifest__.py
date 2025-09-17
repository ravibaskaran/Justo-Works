# -*- coding: utf-8 -*-
{
    'name': "Customer Sales Report",

    'summary': """
        Odoo 15 Customer Sales Reports
    """,

    'author': "",
    'category': 'Sales',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/customer_sales_report_view.xml',
    ],
}