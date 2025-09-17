# -*- coding: utf-8 -*-
{
    'name': "Stock Receipt Damage Issue Voucher",

    'summary': """ Stock Receipt Damage Issue Voucher """,


    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Stock Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',
        'views/adjustments_form.xml',
        'views/adjustments_sequence.xml',
        'views/damage.xml',
    ],

}
