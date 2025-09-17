▼ Changes ▼

22-05-2023 → [ Jassir Masdook ]
    1. inherit_hr_payroll.py → changes made in onchange_employee() → per day salary calculation has been changed
    2. hr_contract.py → added new selection with daily,weekly,biweekly and monthly
    3. Form view modification in two newly created xml file [ hr_payslip_form.xml and hr_contract.xml ]
        3.1 → removed day per
        3.2 → added a new field [ pay_type ] in hr.payslip model
        3.3 → brought schedule_pay selection near wage → hr.contract salary information


▼ Sql Query ▼
1. To replace contract.wage with new code → amount_python_code
Ref:  update hr_salary_rule set amount_python_compute=REPLACE(amount_python_compute, 'contract.wage', '(payslip.no_of_days * payslip.salary_per_day) - payslip.leave_deduction_amount')