# -*- coding: utf-8 -*-
{
    'name': "Direct Sales & Purchase",

    'summary': """ Direct Sales & Purchase""",

    'description': """ Direct Sales & Purchase """,

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    'category': 'sales',
    'version': '18.0.1',

    'depends': [
        'account',
        'purchase',
        'sale',
        'stock',
        'stock_account',
    ],

    'data': [
        'views/account_move_views.xml',
        'views/stock_views.xml',
    ],
}
