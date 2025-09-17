# -*- coding: utf-8 -*-
{
    'name': "Project Evaluation Sheet",

    'summary': """
            Project Evaluation Sheet,
            Competition Sheet,
            Retention Sheet,
            Term Sheet,
            Term Sheet Template,
            Walk in Configuration
        """,

    'category': 'Real Estate',
    'version': '15.0',

    'depends': [
        'base',
        'itsys_real_estate',

    ],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/sequences.xml',
        'views/evaluation_sheet.xml',
        'views/competition_sheet.xml',
        'views/term_sheet_template.xml',
        'views/term_sheet.xml',
        'views/retention_receipt.xml',
        'views/evaluation_configuration.xml',
        'views/budget_sheet.xml',
        'views/project.xml',
        'reports/term_sheet.xml',
        'views/competition_sheet_import.xml',
        'views/mail_templates.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'real_estate_sheets/static/src/js/button_generate.js',
            'real_estate_sheets/static/src/js/relational_fields.js',
            'real_estate_sheets/static/src/js/import.js',
            'real_estate_sheets/static/src/js/abstract_field.js',
            'real_estate_sheets/static/src/js/list_renderer.js'
        ]
    },
}
