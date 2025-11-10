# -*- coding: utf-8 -*-
# Migrated to Odoo 18 - 2025-11-10
# All 5 JavaScript files migrated to OWL framework (266→369 lines, +39%)
# - abstract_field.js: include → patch, updated props access
# - import.js: ListController patch, buttons via getStaticButton
# - relational_fields.js: Many2One patch, dialog service
# - list_renderer.js: Full OWL lifecycle (setup, onMounted, onPatched)
# - button_generate.js: AbstractField.extend → OWL Component + XML template
# Created button_generate.xml template for OWL component
{
    'name': "Project Evaluation Sheet",

    'summary': """
            Project Evaluation Sheet,
            Competition Sheet,
            Retention Sheet,
            Term Sheet,
            Term Sheet Template,
            Walk in Configuration - Migrated to Odoo 18 OWL
        """,

    'category': 'Real Estate',
    'version': '18.0.1',

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
            'real_estate_sheets/static/src/js/list_renderer.js',
            'real_estate_sheets/static/src/xml/button_generate.xml',
        ]
    },
}
