# -*- coding: utf-8 -*-
{
    'name': "Cancel Direct Sales & Purchase",
    'summary': """
        Cancel Direct Sales & Purchase""",
    'description': """
        Cancel Direct Sales & Purchase
    """,
    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",
    'category': 'sales',
    'version': '18.0.0.1',
    'depends': ['account','inexoft_direct_sales_purchase','stock_picking_cancel_extended'],
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
    ],
}