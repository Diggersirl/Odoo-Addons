# -*- coding: utf-8 -*-
{
    'name': "translationie_report_modifications",

    'summary': """
        Modifies the global report template""",

    'description': """
        Resizes the Company logo on the global report template and changes the placement of address information
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
		'views/translationie_report_mod_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}