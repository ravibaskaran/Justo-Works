# -*- coding: utf-8 -*-
{
    'name': "Journal Voucher Extension",

    'summary': """
        """,

    'description': """
    hide cash account from journal voucher accounts list
    """,

    'author': "Inexoft technologies",
    'website': "https://www.inexoft.com",

    'category': 'account',
    'version': '18.0.0.1',

    'depends': ['account'],

    'data': [
        'views/account_account.xml',
        'views/journal_voucher.xml',
    ],
}
