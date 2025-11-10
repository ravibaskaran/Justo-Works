# -*- coding: utf-8 -*-
{
    'name': "Jupiter Dashboard",

    'summary': """
        Jupiter Dashboard showing booking and registration details""",

    'description': """
        Jupiter Dashboard showing booking and registration details as charts
    """,

    'author': "ks-subinraj",
    'website': " ",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],

    'data': [
        'security/security.xml',
        'views/views.xml',
    ],

    'assets': {
        'web.assets_qweb': [
            'jupiter_dashboard/static/src/xml/template.xml',  # Migrated to OWL
        ],
        'web.assets_backend': [
            'jupiter_dashboard/static/src/js/apexcharts.js',  # Third-party library (no migration needed)
            'jupiter_dashboard/static/src/js/dashboard.js',   # Migrated to OWL - Phase 3
        ],
    }
}
