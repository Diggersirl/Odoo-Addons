# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
	_inherit = "product.template"
	
	is_translation_service = fields.Boolean(string="Translation Service", help="Defines whether source and target language fields are editable on product Sale Order Line")
	translation_service_type = fields.Selection([('translation','Translation'),('proofread','Proofread'),('combined','Translation & Proofreading')], string="Service Type", help="[translation] Automatic Rate picker will choose Translation rates in conjunction with unit of measure. <br/>[proofread] Automatic Rate picker will choose Proofread rates in conjunction with unit of measure.[combined] Uses Flat Rate.")
	group_sol = fields.Boolean(string="Group Product Sale Order Lines")
	grouped_product = fields.Many2one(comodel_name='product.product', string="Related Product", help="Product for which an additional sale order line will be generated when this product is used in a sale order line")