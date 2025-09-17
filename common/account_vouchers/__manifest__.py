{
    'name': 'Accounts Transaction and Report',
    'summary': """ To Fulfill all accounting needs""",
    'description': """
        Contains\n
            ♦ Receipt Voucher\n
            ♦ Payment Voucher\n
            ♦ Journal Voucher\n
            ♦ Customer Receipt\n
            ♦ Vendor Receipt\n
            ♦ Bank Reconciliation\n
            ♦ Fixed Asset\n
            ♦ All Accounts Reports\n
    """,
    'author': 'Inexoft Technologies',
    'category': 'Accounts Vouchers',

    'depends': [
        'base',
        'account',
        'base_accounting_kit',
        'bank_reconciliation',
        'base_account_budget',
        'inexoft_account_payments',
        'inexoft_account_voucher',
        'cash_book',
        'day_book',
        'daybook_co_op',
        'general_ledger',
        'trial_balance',
        'manufacturing_trading',
        'profit_loss_balance_sheet',
        'partner_ledger',
        'rnd_register',
        'l10n_in',
    ],

    'data': [
        'views/bank.xml',
        'views/accounts_menu.xml',
        'views/asset_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-
