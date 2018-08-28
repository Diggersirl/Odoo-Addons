# -*- coding: utf-8 -*-
{
	'name': 'Translation Process Management System Sale',
	'version' : '1.0',
	'summary' : 'Functionality for Quoting and Selling Translation Services',
	'description' : """
Translation Process Management System - Sale
=============================================
Add option to product to define a product as a Translation Service.

Adds option to group Sale Order Lines 
-------------------------------------------
By selecting this option and assigning a related product, two sale order lines are created 
and grouped sharing wordcount and source and target language. If those Sale Order Lines create tasks then those tasks will be linked together too.

Adds source and target languages to Sale Order Lines and improves Sale order Line Autocomplete features
-------------------------------------------
 Automatically fills in rate based on most expensive language selected between Source and Target Language fields and the unit of measure field.
 """,
	'category' : 'TMS',
	'depends' : ['tms_res', 'sale_timesheet','product'],
	'data' : [
		'security/ir.model.access.csv',
		'views/product_view.xml',
		'views/sale_view.xml',
		'data/ir_sequence_data.xml',
		'data/product_data.xml',
		'data/ir_cron_data.xml',
	],
	'installable' : True,
	'application' : False,
	'auto_install' : False,
}