# -*- coding: utf-8 -*-
{
	'name' : 'Translation Process Management System Resources',
	'version' : '1.0',
	'summary' : 'Resources for managing Translation Services Supplier',
	'description' """
Translation Management System Resources
============================================
Adds functionality to store:
	- Language List for Linguists.
	- CAT Tool List for Linguists.
	- Rating System for Linguists.
	"""
	'category' : 'TMS',
	'depends' : ['base'],
	'data' : [
		'security/tms_res_security.xml',
		'security/ir.model.access.csv',
		'tms_res_menu.xml',
		'tms_languages/tms_languages.xml',
		
	],
	'installable' : True,
	'application': False,
	'auto_install' : False,
}
