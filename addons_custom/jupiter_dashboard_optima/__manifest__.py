# -*- coding: utf-8 -*-
{
    'name': "jupiter_dashboard_optima",

    'summary': """
        Ultimate analytics dashboard with comprehensive business intelligence""",

    'description': """
        Jupiter Dashboard Optima - Ultimate Analytics Dashboard

        Features:
        - Comprehensive business intelligence dashboard
        - Advanced analytics and reporting
        - Real-time metrics and KPIs
        - Interactive data visualizations
        - Multi-dimensional analysis

        MIGRATION STATUS:
        - Manifest updated to 18.0.0.1
        - JavaScript migration PENDING (4326 lines!)

        REQUIRES MIGRATION:
        - dashboard.js: 4326 lines (EXTREMELY COMPLEX)
        - Estimated effort: 12-16 hours
        - Requires systematic chunked migration approach

        Dependencies:
        - Depends on jupiter_dashboard_tres
        - Both modules need OWL migration together
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Productivity',
    'version': '18.0.0.1',

    'depends': ['base', 'base_setup', 'jupiter_dashboard_tres'],

    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'jupiter_dashboard_optima/static/src/js/dashboard.js',
            'jupiter_dashboard_optima/static/src/xml/template.xml',
        ],
    }
}
