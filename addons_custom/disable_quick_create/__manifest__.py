{
    'name': 'Disable Quick Create',
    'version': '18.0.1.0.0',
    'author': 'Inexoft Technologies',
    'website': 'https://www.inexoft.com',
    'category': 'Web',
    'summary': 'Disable "quick create" for all and "create and edit" '
               'for specific models',
    'depends': [
        'web',
    ],
    'data': [
        # 'views/disable_quick_create.xml',
        'views/ir_model.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "disable_quick_create/static/src/js/disable_quick_create.js"
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
