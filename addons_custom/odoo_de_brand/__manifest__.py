# -*- coding: utf-8 -*-
{
    'name': "De-brand Module 18",
    'summary': """
        De-brand Module for Odoo 18 (Migrated from v15)
        """,
    'description': """
        De-brand Module for Odoo 18
        - Error Dialog De-branding (removes Odoo references)
        - User Menu De-branding (removes Odoo menu items)
        - Browser title replacement with company name
        - Form auto-save prevention on close/reload
        - Confirmation dialog for unsaved changes
    """,
    'author': "",
    'website': "",
    'category': 'Technical',
    'version': '18.0.1.0.0',
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
