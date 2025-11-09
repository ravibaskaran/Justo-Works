# -*- coding: utf-8 -*-
{
    'name': " ♦ Hr Payroll Customization ♦",
    'summary': """ Hr Payroll Customizationn""",

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",
    'category': 'sales',
    'version': '18.0',
    'depends': ['base', 'account', 'hr','om_hr_payroll', 'om_hr_payroll_account'],
    'data': [
            'views/hr_payroll_views.xml',
            'views/hr_employee_view.xml',
            'reports/inherit_payslip.xml',
            'reports/inherit_payslip_details_report.xml',
            'views/category.xml',
            'views/account_journal.xml',
            'views/journals.xml',
            'views/rules.xml',
            'views/hr_contract.xml',
            'views/hr_payslip_form.xml',
            'views/payslip_batch.xml',
    ],
}
