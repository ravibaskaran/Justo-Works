# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/


{
    'name': "Hide Menu (Odoo 18)",
    'summary': """
        Restrict Menu Items from Specific Users (Migrated to Odoo 18)""",
    'description': """
        Restrict Menu Items from Specific Users

        Migrated to Odoo 18:
        - Version updated to 18.0.1.0.0

        REQUIRES TESTING:
        - Menu loading methods (load_menus_custom, load_web_menus) override Odoo core
        - Odoo 18 has refactored menu loading system - may need updates
        - Controller uses basic patterns (compatible)
        - Models use standard ORM (compatible)

        TEST PRIORITY: HIGH - Menu system changes in v18 may affect functionality
        """,
    'author': 'Klystron Global',
    'maintainer':'Kiran K',
    'website': "https://www.klystronglobal.com/",
    'images': ["static/description/banner.png"],
    'category': 'Extra Rights',
    'version': "18.0.1.0.0",
    'license': 'AGPL-3',
    'depends': [
        'base', 'web'
    ],
    'data': [
        'views/res_users.xml',
    ],
}
