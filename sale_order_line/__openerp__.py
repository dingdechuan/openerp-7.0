# -*- coding: utf-8 -*-
# © 2014 Elico corp(www.elico-corp.com)
# Licence AGPL-3.0 or later(http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Sale Order Line',
    'version': '7.0.1.0.0',
    'category': 'Sales',
    'sequence': 19,
    'summary': 'Sale Order Line',
    'description': """
        Standard OpenERP manages Sales by Orders.
        
        In Sales Module after Sales Order Menu,
        it was added Sales by Product Menu.
        User will open a tree view displaying SOLs,
        with group by Product set as default Group.

        Main Information Displayed:
        - Order Reference (and icon to open it)
        - Customer
        - Quantity
        - Final Quantity (to be added)
        - Order Status
        - Product State
        - Product Type
        According to Product State, lines will have different colors:
        - Red: Catalogue, 
        - Yellow (orange for viewing purposes): Preorder
        - Green: Order
    """,
    'author': 'Elico Corp',
    'website': 'http://www.elico-corp.com',
    'images': [],
    'depends': ['product', 'purchase', 'warning', 'mmx_product_advance', 'sale_menu'],
    'data': [
        'security/ir.model.access.csv',
        'sale_view.xml',
        #'wizard/wizard_update_qty_store_view.xml',
    ],
    'test': [],
    'demo': [],
    'css': ['static/src/css/sale_order_line.css', ],
    #'js':['static/src/js/sale_order_line.js',],
    'installable': True,
    'auto_install': False,
    'application': False,
}


