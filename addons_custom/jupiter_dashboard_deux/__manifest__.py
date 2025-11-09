# -*- coding: utf-8 -*-
{
    'name': "Jupiter Dashboard II",

    'summary': """
        Jupiter Dashboard II
    """,

    'description': """
        Jupiter Dashboard II
    """,

    'author': "ks-subinraj",
    'website': " ",
    'category': 'dashboard',
    'version': '18.0.0.1',
    'depends': ['base'],

    'data': [
        'security/security.xml',
        'views/views.xml',
    ],

    'assets': {
        'web.assets_qweb': [
            'jupiter_dashboard_deux/static/src/xml/template.xml',
        ],
        'web.assets_backend': [
            'jupiter_dashboard_deux/static/src/js/dashboard.js',
        ],
    }
}
