# -*- coding: utf-8 -*-
{
    'name': "jupiter_dashboard_tres",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.0.1',

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
