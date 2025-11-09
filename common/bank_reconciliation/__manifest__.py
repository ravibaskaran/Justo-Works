# -*- coding: utf-8 -*-
{
    'name': 'Manual Bank Reconciliation',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Replacing default bank statement reconciliation method by traditional way',
    'description': """Replacing default bank statement reconciliation method by traditional way""",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_line_view.xml',
        'views/account_journal_dashboard_view.xml',
        'wizard/bank_statement_wiz_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'bank_reconciliation/static/css/custom.css',
        ],
    }
}
