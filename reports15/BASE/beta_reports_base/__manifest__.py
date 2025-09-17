# -*- coding: utf-8 -*-
{
    'name': "Beta Report Base 15",
    'category': 'Reports',
    'version': '15.0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/paper_formats.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'beta_reports_base/static/src/js/jquery.printarea.js',
            'beta_reports_base/static/src/js/report.js',
        ],
    }
}