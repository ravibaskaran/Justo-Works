# -*- coding: utf-8 -*-
{
    'name': "Project Transactions (Odoo 18)",

    'summary': """
        Project and Real Estate Transaction Management (Migrated to Odoo 18)""",

    'description': """
        Project Transactions (Migrated to Odoo 18)

        Features:
        - Building and project management
        - Inventory creation for projects
        - Project employee assignment
        - Project target tracking
        - Loan status marking
        - Registration workflows
        - Flat/product templates
        - Real estate integration

        Migrated to Odoo 18:
        - Version updated to 18.0.1.0.0
        - Python models reviewed for compatibility

        REQUIRES TESTING:
        - Building creation and management
        - Project assignment workflows
        - Employee assignment to projects
        - Inventory creation processes
        - Loan status updates
        - Registration forms and validation
        - Target tracking and reporting
        - Integration with itsys_real_estate
        - Integration with real_estate_extension
        - Security rules and access rights
    """,

    'author': "Justo Works",
    'website': "http://www.yourcompany.com",

    'category': 'Real Estate/Project Management',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'itsys_real_estate', 'real_estate_extension'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/create_inventory.xml',
        'security/security.xml',
        'views/building.xml',
        'views/project_assigning.xml',
        'views/loan_status_marking.xml',
        'views/registration.xml',
        'views/res_config.xml',
        'views/project_employee_assigning.xml',
        'views/project_target.xml',
        'views/employee.xml',
        'views/flat_product_temp.xml',
        'views/menu.xml',
    ],
}
