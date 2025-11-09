# -*- coding: utf-8 -*-
{
    'name': "Project Transactions",

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
