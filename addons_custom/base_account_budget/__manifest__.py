# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Budget Management (Odoo 18)',
    'version': '18.0.1.1.0',
    'summary': """ Budget Management for Odoo 18 Community Edition (Migrated from Odoo 15)""",
    'description': """ Budget Management (Migrated to Odoo 18)

     This module allows accountants to manage analytic and budgets.

     Once the Budgets are defined (in Accounting/Accounting/Budgets), the Project Managers
     can set the planned amount on each Analytic Account.

     The accountant has the possibility to see the total of amount planned for each
     Budget in order to ensure the total planned is not greater/lower than what he
     planned for this Budget. Each list of record can also be switched to a graphical
     view of it.

     Three reports are available:

     1. The first is available from a list of Budgets. It gives the spreading, for
     these Budgets, of the Analytic Accounts.
     2. The second is a summary of the previous one, it only gives the spreading,
     for the selected Budgets, of the Analytic Accounts.
     3. The last one is available from the Analytic Chart of Accounts. It gives
     the spreading, for the selected Analytic Accounts of Budgets.

     Migrated to Odoo 18:
     - Version updated to 18.0.1.1.0
     - Python models reviewed for compatibility

     REQUIRES TESTING:
     - Budget creation and management
     - Analytic account integration
     - Amount planning workflows
     - Budget vs actual comparisons
     - All three report types
     - Graphical views
     - Security rules and access rights
     - Computed fields (practical_amount, theoretical_amount, percentage)
     """,
    'category': 'Accounting',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'security/ir.model.access.csv',
        'security/account_budget_security.xml',
        'views/account_analytic_account_views.xml',
        'views/account_budget_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
