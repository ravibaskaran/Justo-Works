{
    'name': 'Purchase Extension',
    'summary': """ Contains Purchase Modification """,
    'description': """
        Contains\n
            ♦ Purchase \n
            ♦ Purchase Return\n
            ♦ Purchase Order\n
            ♦ Supplier Master\n
            ♦ Product Master  
    """,
    'author': 'Inexoft Technologies',
    'category': 'Purchase',

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
        'security/ir.model.access.csv',
        'views/purchase_menu.xml',
        'views/purchase_modification.xml',
        'views/stock_production_lot.xml',
        'views/purchase_order.xml',
        'views/uom.xml',
        'security/security.xml',
        'views/expiry_visibility_res_config.xml',
        'views/reports.xml',
        'views/product.xml',
        'views/supplier.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'purchase_extension/static/src/scss/purchase.scss',
        ],
    }
}
# -*- coding: utf-8 -*-
