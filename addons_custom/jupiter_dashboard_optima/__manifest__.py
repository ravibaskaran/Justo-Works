# -*- coding: utf-8 -*-
# Migrated to Odoo 18 - 2025-11-10
# JavaScript migrated from Odoo 15 AbstractAction to OWL Component
# - dashboard.js: MASSIVE migration (4326→4189 lines, -137 lines)
#   - 92 event handlers converted to addEventListener (most complex yet!)
#   - 65 RPC calls converted (ajax.jsonRpc/rpc.query → this.rpc)
#   - 21 chart methods preserved (Highcharts/ApexCharts)
#   - ~104 methods converted
#   - Proper cleanup on unmount (charts + event listeners)
#   - Complex region/cluster_head/cluster/project hierarchy
#   - Many2many select boxes with modals
#   - Financial year container logic preserved
# - template.xml: Added owl="1" attribute
# - Depends on jupiter_dashboard_tres (migrated ✅)
# - jQuery and select2 usage maintained (compatible with Odoo 18)
{
    'name': "Jupiter Dashboard Optima",

    'summary': """
        Jupiter Dashboard Optima - Ultimate Analytics Dashboard
    """,

    'description': """
        Jupiter Dashboard Optima - Migrated to Odoo 18 OWL Framework
        Most comprehensive dashboard with advanced region, cluster, and project analytics
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Dashboard',
    'version': '18.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup', 'jupiter_dashboard_tres'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/settings.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'jupiter_dashboard_optima/static/src/xml/template.xml',
        ],
        'web.assets_backend': [
            'jupiter_dashboard_optima/static/src/js/dashboard.js',
        ],
    }
}
