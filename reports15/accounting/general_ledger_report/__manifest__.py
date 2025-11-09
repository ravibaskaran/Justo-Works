# -*- coding: utf-8 -*-
{
    'name': "General Ledger 15",

    'summary': """
        general ledger for 15""",

    'description': """
        general ledger 15
    """,

    'author': "",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'report/pdf_report.xml',
        'report/template.xml',
        'views/action.xml',
        'views/config_strict.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'general_ledger_report/static/src/js/main.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.js',
        ],
        'web.assets_qweb': [
            'general_ledger_report/static/src/xml/panel.xml',
        ],
    }
}
