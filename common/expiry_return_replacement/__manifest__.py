{
    'name': 'Expiry Return and Replacement',
    'summary': """ Expiry Return and Replacement """,
    'description': """
        Contains\n
            ♦ Expiry Return \n
            ♦ Expiry Replacement
           
    """,
    'author': 'Inexoft Technologies',
    'category': 'Expiry Return and Replacement',

    'depends': [
        'base',
        'account',
        'stock',
        'purchase',
        'inexoft_direct_sales_purchase',
        'inexoft_freight_charges',
        'uom',
    ],

    'data': [
        'data/data.xml',
        'views/expiry_replacement.xml',
        'views/expiry_return.xml',
        'views/expiry_menus.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'expiry_return_replacement/static/src/scss/expiry_rtn_rpc.scss',
        ],
    }
}
# -*- coding: utf-8 -*-
