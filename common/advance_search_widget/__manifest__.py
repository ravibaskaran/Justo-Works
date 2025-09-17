# See LICENSE file for full copyright and licensing details.

{
    "name": "Advance Search Widget",
    "version": "13.0.1.0.0",
    "author": "",
    "maintainer": "",
    "complexity": "easy",
    "depends": ["web", 'product'],
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
    To display Advance search widget use widget="advance_search_many2one" in <field> tag.
    To display fields in autocomplete popup you have to provide 'adv_fields' attribute in <field> tag
    with value as Dict.
    Dict contain field name as key and value as a list which contains 'heading' of the field and 'alignment' of head
    eg:-
    
     <field name="product_id" 
            widget="advance_search_many2one" 
            adv_fields='{"virtual_available":["Stock","r"],"uom_id":["Unit","l"],"list_price":["Price","r"]}' />
    note:- Many2many fields are
    """,
    "summary": """
        
    """,
    # "images": ["static/description/Digital_Signature.jpg"],
    "data": [
             # "views/assets.xml"
             ],
    'assets': {
            'web.assets_backend': [
                'advance_search_widget/static/src/css/product_autocomplete.css',
                'advance_search_widget/static/src/js/product_autocomplete_many2one.js',
            ],
            'web.assets_common': [
                'advance_search_widget/static/src/js/jquery.js',
            ],
        },
        "website": "",
        # "qweb": ["static/src/xml/digital_sign.xml"],
        "installable": True,
        "auto_install": False,
}
