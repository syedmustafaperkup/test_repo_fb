# -*- coding: utf-8 -*-
{
    "name": """POS Order Report Filter""",
    "summary": """POS Order Report Filter""",
    "category": "Point of Sale",
    "version": "1.0",
    "application": False,
    "author": "Perkup",
    "depends": [
        'point_of_sale',
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/views.xml",
    ],
    'qweb': [        
    ],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
