# -*- coding: utf-8 -*-
{
    'name': "Freight Charges",
    'summary': """
        Freight Charges
        """,
    'description': """
        Freight Charges
    """,
    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",
    'category': 'account',
    'version': '0.1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_views.xml',
        'views/invoice_document.xml',
    ],
    'assets': {
            'web.assets_qweb': [
                'inexoft_freight_charges/static/src/xml/taxTotal.xml',
            ],
        },
}
