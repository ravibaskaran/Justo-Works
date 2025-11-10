# -*- coding: utf-8 -*-
# Migrated to Odoo 18 - 2025-11-10
# All 3 JavaScript files migrated/fixed:
# - user_menu_items.js: Fixed legacy session/rpc imports, updated patch syntax
# - error_dialogs.js: Removed invalid top-level await, fixed _super calls
# - basic_controller.js: Full migration from odoo.define to OWL (FormController patch)
# Purpose: De-branding (remove Odoo branding from UI and error dialogs)
#          + Prevent form auto-save on close/reload with confirmation dialog
{
    'name': "De-brand Module (Odoo 18)",
    'summary': """
        De-brand Module for Odoo 18 - Migrated to OWL
        """,
    'description': """
        De-brand Module - Migrated to Odoo 18 OWL Framework
        Features:
        - Error dialog de-branding
        - User menu de-branding (removes Odoo account, documentation, support links)
        - Prevent form auto-save on close and reload with confirmation dialog
    """,
    'author': "",
    'website': "",
    'category': 'Customization',
    'version': '18.0.0.1',
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
