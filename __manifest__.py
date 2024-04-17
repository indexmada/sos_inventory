# -*- coding: utf-8 -*-
{
    'name': "sos_inventory",

    'summary': """
        Champ compte analytique dans stock.picking""",

    'description': """
        Champ compte analytique dans stock.picking
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'analytic'],

    # always loaded
    'data': [
        'views/stock.xml',
    ],
}
