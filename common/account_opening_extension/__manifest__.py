# -*- coding: utf-8 -*-
{
    'name': "Account Opening Extension",
    'summary': """ Financial Year """,
    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Accounts Opening',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'inexoft_account_opening'
    ],

    # always loaded
    'data': [
        'views/views.xml',
    ],

}
