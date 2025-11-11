# -*- coding: utf-8 -*-
{
    'name': "Partner Account Creation (Odoo 18)",

    'summary': """
        Partner Account Creation - Automatic account generation for partners (Migrated to Odoo 18)""",

    'description': """
        Partner Account Creation (Migrated to Odoo 18)

        Features:
        - Automatic account code generation for partners
        - Configurable account sequences
        - Partner-specific accounting setup

        Migrated to Odoo 18:
        - Version updated to 18.0.0.1
        - Python models reviewed for compatibility

        REQUIRES TESTING:
        - Partner creation workflow
        - Account code generation
        - Sequence configuration
        - Account assignment to partners
        - Integration with partner forms
    """,

    'author': "Justo Works",

    'category': 'Accounting',
    'version': '18.0.0.1',

    'depends': ['account'],

    'data': [
        'data/sequence.xml',
        'views/res_config_views.xml',
    ],
}
