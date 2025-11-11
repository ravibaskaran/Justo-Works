# -*- coding: utf-8 -*-
{
    'name': 'PDF Report Options (Odoo 18)',
    'version': '18.0.1.0.0',
    'summary': """Shows a modal window with options for printing, downloading or opening PDF reports (Migrated to Odoo 18)""",
    'description': """
        PDF Report Options (Migrated to Odoo 18)

        Features:
        - Choose one of the following options when printing a PDF report:
          * Print - print the PDF report directly with the browser
          * Download - download the PDF report on your computer
          * Open - open the PDF report in a new tab
        - Set a default option for each report

        Migrated to Odoo 18:
        - Version updated to 18.0.1.0.0
        - JavaScript already uses modern OWL Dialog pattern
        - Uses registry.category("ir.actions.report handlers")
        - Service injection (dialog, rpc, notification, ui)

        REQUIRES TESTING:
        - PDF report generation
        - Print option (browser print dialog)
        - Download option (file download)
        - Open option (new tab)
        - Default option settings per report
        - Modal dialog display
        - wkhtmltopdf integration

        Status: JavaScript code already compatible with Odoo 18
    """,
    'author': 'Luis Rodrigo Mejia Mateus',
    'category': 'Productivity',
    'images': ['images/main_1.png', 'images/main_screenshot.png'],
    'depends': ['web'],
    'data': [
        'views/ir_actions_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_qweb': [
            'report_pdf_options/static/src/**/*.xml',
        ],
        'web.assets_backend': [
            'report_pdf_options/static/src/js/PdfOptionsModal.js',
            'report_pdf_options/static/src/js/qwebactionmanager.js',
        ]
    }
}
