# -*- coding: utf-8 -*-
{
    'name': "jupiter_dashboard_tres",

    'summary': """
        Comprehensive analytics dashboard with region, cluster, and project insights""",

    'description': """
        Jupiter Dashboard III - Advanced analytics dashboard featuring:
        - Regional, cluster, and project-level analytics
        - Booking and registration tracking
        - CP (Channel Partner) performance metrics
        - Manpower productivity analysis
        - Walk-in conversion tracking
        - Budget vs Actual comparison
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Productivity',
    'version': '18.0.0.1',

    'depends': ['base', 'base_setup'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/dashboard_configuration.xml',
        'views/settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'jupiter_dashboard_tres/static/src/js/highcharts.js',
            # 'jupiter_dashboard_tres/static/src/js/exporting.js',
            # 'jupiter_dashboard_tres/static/src/js/export-data.js',
            # 'jupiter_dashboard_tres/static/src/js/accessibility.js',
            'jupiter_dashboard_tres/static/src/js/dashboard.js',
            'jupiter_dashboard_tres/static/src/xml/template.xml',
        ],
    }
}
