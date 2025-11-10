# -*- coding: utf-8 -*-
# Migrated to Odoo 18 - 2025-11-10
# JavaScript migrated from Odoo 15 AbstractAction to OWL Component
# - dashboard.js: Converted to OWL with custom scroll functionality
# - template.xml: Added owl="1" attribute
# - ApexCharts integration preserved (2 charts)
# - Custom horizontal scroll with drag-and-drop functionality maintained
{
    'name': "Jupiter Dashboard II",

    'summary': """
        Jupiter Dashboard II
    """,

    'description': """
        Jupiter Dashboard II - Migrated to Odoo 18 OWL Framework
    """,

    'author': "ks-subinraj",
    'website': " ",
    'category': 'dashboard',
    'version': '18.0.0.2',
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
