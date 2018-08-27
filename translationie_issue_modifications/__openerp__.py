# -*- coding: utf-8 -*-
{
    'name': "translationie_issue_modifications",

    'summary': """
        Adds issue type field to allow better filtering of issues""",

    'description': """
        
    """,

    'author': "Translation.ie",
    'website': "http://www.translation.ie",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project_issue'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'translationie_issue_mod_view.xml',
		'template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}