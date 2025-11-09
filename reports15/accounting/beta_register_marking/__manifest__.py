# -*- coding: utf-8 -*-
{
    'name': " Payroll register making ",

    'summary': """ Payroll Register Making """,

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Register Making',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'beta_reports_base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/panel.xml',
        'views/templates.xml',
    ],
}