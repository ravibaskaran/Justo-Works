{
    'name': "Product Ledger",

    'summary': """ Product Ledger """,

    'description': """
        A patient appointment is a scheduled meeting between a patient and a healthcare provider 
        for medical consultation or treatment.The appointment involves the patient checking in,
        meeting with the healthcare provider for examination, and receiving appropriate care or
        further instructions.
        Patient appointments ensure organized healthcare delivery, effective communication 
        between patients and providers, and timely access to medical services.
    """,

    'author': "Inexoft Technologies",
    'website': "http://www.inexoft.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Product Ledger',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base','beta_reports_base','account','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/panel.xml',
        'views/template.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'patient_appointment/static/src/scss/style.scss',
    #         'patient_appointment/static/src/js/custom.js',
    #     ],
    # }
}
# -*- coding: utf-8 -*-
