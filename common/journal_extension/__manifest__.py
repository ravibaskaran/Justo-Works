# -*- coding: utf-8 -*-
{
    'name': "Journal Extension",

    'summary': """
        Account Opening
        """,

    'description': """
        Account Opening
    """,

    'author': "Inexoft technologies",
    'website': "https://www.inexoft.com",

    'category': 'account',
    'version': '18.0.0.1',

    'depends': ['base', 'account'],

    'data': [
        'views/account_journal.xml',
    ],
    'post_init_hook':'test_post_init_hook',
}
