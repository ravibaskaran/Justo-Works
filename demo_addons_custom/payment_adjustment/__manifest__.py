{
    "name": "Payment Adjustment (Odoo 18)",
    "version": "18.0.1.1.0",
    "summary": "Payment adjustment and reconciliation tools (Migrated to Odoo 18)",
    "description": """
        Payment Adjustment (Migrated to Odoo 18)

        Features:
        - Payment adjustments and corrections
        - Payment reconciliation tools
        - Warning wizard for adjustment validation

        Migrated to Odoo 18:
        - Version updated from 13.0.1.1.0 to 18.0.1.1.0
        - Python models reviewed for compatibility

        REQUIRES TESTING:
        - Payment adjustment workflow
        - Warning wizard functionality
        - Account payment integration
        - Reconciliation features
        - Security access rules

        Note: Migrated from Odoo 13, requires careful testing
    """,
    "category": "Accounting",
    "author": "Justo Works",
    "depends": [
        'account'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
        # 'report/report.xml',
        # 'report/form_template.xml',
        'wizard/warning_wizard_view.xml',
    ],
}