# -*- coding: utf-8 -*-
# Migrated to Odoo 18 - 2025-11-10
# JavaScript migrated from Odoo 15 AbstractAction to OWL Component
# - dashboard.js: Massive migration (2754→3067 lines)
#   - 63 event handlers converted to addEventListener
#   - 58 RPC calls converted (ajax.jsonRpc → this.rpc)
#   - 22+ Highcharts rendering methods preserved
#   - Proper cleanup on unmount (charts + event listeners)
# - template.xml: Added owl="1" attribute
# - Highcharts library preserved (loaded from manifest)
# - jQuery and select2 usage maintained (compatible with Odoo 18)
{
    'name': "Jupiter Dashboard III",

    'summary': """
        Jupiter Dashboard III - Advanced Analytics Dashboard
    """,

    'description': """
        Jupiter Dashboard III - Migrated to Odoo 18 OWL Framework
        Comprehensive dashboard with region, cluster, and project analytics
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Dashboard',
    'version': '18.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/dashboard_configuration.xml',
        'views/settings.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'jupiter_dashboard_tres/static/src/xml/template.xml',
        ],
        'web.assets_backend': [
            'jupiter_dashboard_tres/static/src/js/highcharts.js',
            # 'jupiter_dashboard_tres/static/src/js/exporting.js',
            # 'jupiter_dashboard_tres/static/src/js/export-data.js',
            # 'jupiter_dashboard_tres/static/src/js/accessibility.js',
            'jupiter_dashboard_tres/static/src/js/dashboard.js',
        ],
    }
}
