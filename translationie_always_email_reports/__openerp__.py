# -*- coding: utf-8 -*-
{
    'name': "translationie_always_email_reports",

    'summary': """
        Changes behaviour of sending emails so that quotations and invoices/purchase orders are always emailed to the recipient even notify_email is set to never""",

    'description': """
        Changes behaviour of sending emails so that quotations and invoices/purchase orders are always emailed to the recipient even notify_email is set to never
    """,

    'author': "Translation.ie",
    'website': "http://www.translation.ie",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}