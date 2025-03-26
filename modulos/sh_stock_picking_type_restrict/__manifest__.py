# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Stock Picking Types Restrict For Users",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Warehouse",
    "summary": "Inventory Picking Types Restrict For Users Stock Picking Type Restrict Inventory Picking Type Restrict Restrict Picking Type Operation Type Restrictions Restrict Incoming Order Restrict Receipt Order Restrict Delivery Order Restrict Internal Transfer Restrict Operation Type Odoo",
    "description": """This module restricts stock-picking types for specific users. You can add access users on inventory configuration, only allowed users can access that picking type. Users are allocated in specific picking types like delivery order, incoming order/receipt order, internal transfer.""",
    "version": "0.0.2",
    "depends": [
        "stock"
    ],
    "application": True,
    "data": [

        "security/sh_stock_picking_type_restrict_security.xml",
        "views/sh_picking.xml",

    ],

    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": "22",
    "currency": "EUR"
}
