# -*- coding: utf-8 -*-
{
    'name': "Category Wise Asset Report",

    'summary': """
        Odoo 15 Category Wise Asset Report
    """,

    'author': "",
    'category': 'Real Estate',
    'version': '15.0.1',

    'depends': ['base', 'beta_reports_base', 'base_accounting_kit', 'account_vouchers'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
    ],
}
