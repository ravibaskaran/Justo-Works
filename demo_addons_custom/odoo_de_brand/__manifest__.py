# -*- coding: utf-8 -*-
{
    'name': "De-brand Module 15",
    'summary': """
        De-brand Module for odoo 15
        """,
    'description': """
        De-brand Module
        with Error De-branding,
        Prevent form auto-save on close and reload 
    """,
    'author': "",
    'website': "",
    'category': 'Uncategorized',
    'version': '15.0.0.0.1',
    'depends': ['base', 'web', 'mail', 'mail_bot'],
    'data': [
        'views/templates.xml',
        'views/views.xml',
        'views/email.xml',
        'views/data.xml',
    ],

    'assets': {
        'web.assets_qweb': [
            'odoo_de_brand/static/src/xml/debrand.xml',
        ],
        'web.assets_backend': [
            "odoo_de_brand/static/src/js/user_menu_items.js",
            'odoo_de_brand/static/src/js/error_dialogs.js',
            'odoo_de_brand/static/src/js/basic_controller.js'
        ]
    },

    'auto_install': True,
}
