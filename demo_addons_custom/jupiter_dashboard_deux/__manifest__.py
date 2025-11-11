# -*- coding: utf-8 -*-
{
    'name': "Jupiter Dashboard II (Odoo 18)",

    'summary': """
        Jupiter Dashboard II - Bookings, Registrations, Collections (Migrated to Odoo 18)
    """,

    'description': """
        Jupiter Dashboard II (Migrated to Odoo 18)

        Features:
        - Real-time booking and registration metrics
        - Collection and billing tracking
        - Channel Partner (CP) analytics
        - ApexCharts integration (bar and line charts)
        - Horizontal scrollable dashboard with drag-and-drop
        - Interactive report and list view links

        Migrated to Odoo 18:
        - Version updated to 18.0.0.1
        - dashboard.js migrated to OWL Component (600 lines)
        - Native DOM queries replace jQuery
        - Service injection (rpc, action)
        - ApexCharts library preserved

        REQUIRES TESTING:
        - Dashboard loading and rendering
        - All RPC endpoints
        - ApexCharts display
        - Click events (report/list links)
        - Horizontal scroll with drag
        - Arrow navigation
        - Data accuracy
    """,

    'author': "ks-subinraj / Migrated by Justo Works",
    'website': " ",
    'category': 'Dashboards',
    'version': '18.0.0.1',
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
