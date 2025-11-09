# -*- coding: utf-8 -*-
{
    'name': "Profit Loss & Balance Sheet",

    'summary': """
        Odoo 15 Profit Loss & Balance Sheet
    """,

    'author': "",
    'category': 'Accounting',
    'version': '18.0.1',

    'depends': ['base', 'beta_reports_base', 'account', 'base_accounting_kit', 'manufacturing_trading'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/panel.xml',
        'views/pdf_report.xml',

    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'profit_loss_balance_sheet/static/src/js/report.js',
    #     ],
    # }
}
