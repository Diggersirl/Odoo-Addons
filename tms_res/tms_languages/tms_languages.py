# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError

import logging
_logger = logging.getLogger(__name__)



class tmsLanguages(models.Model):
	_name = 'tms.languages'
	_description = 'Translation Service Languages'
	
	name = fields.Char()
	code = fields.Char(string='Language Code')
	group = fields.Many2one(comodel_name='tms.language_group',string='Language Rate Group', help="Applies the default rates from the selected Rate group as the language rates. If you wish to have specific rates for a language select the 'Override Rate Group Defaults for this Language' option and enter your custom rates")
	#override settings if override_rate_group display rate fields
	override_rate_group = fields.Boolean(string='Use Custom Rates', help='Override Rate Group Defaults for this Language')
	trans_word = fields.Float(string='Translation Rate per Word')
	trans_page = fields.Float(string='Translation Rate per Page')
	trans_flat = fields.Float(string='Translation Rate Flat Fee')
	proof_flat = fields.Float(string='Proofread Rate Flat Fee')
	proof_word = fields.Float(string='Proofread Rate per Word')
	trans_cost = fields.Float(string='Translation Cost per Word')
	trans_cost_flat = fields.Float(string='Translation Cost Flat Fee')
	proof_cost = fields.Float(string='Proofread Cost per Word')
	proof_cost_flat = fields.Float(string='Proofread Cost Flat Fee')
	
	@api.onchange('group')
	def update_rate(self):
		if  self.group.exists():
			rate_group = self.group
			self.trans_word = rate_group.trans_word
			self.trans_page = rate_group.trans_page
			self.trans_flat = rate_group.trans_flat
			self.proof_flat = rate_group.proof_flat
			self.proof_word = rate_group.proof_word
			self.trans_cost = rate_group.trans_cost
			self.trans_cost_flat = rate_group.trans_cost_flat
			self.proof_cost = rate_group.proof_cost
			self.proof_cost_flat = rate_group.proof_cost_flat
			
	
	def get_unit_price(self, product_uom, translation_service_type):
		unit_price = 0
		uom_categ_name = product_uom.category_id.name
		if translation_service_type == 'combined':
			unit_price = self.trans_flat
		elif translation_service_type == 'translation':
			if uom_categ_name == 'Flat':
				unit_price = self.trans_flat
			elif uom_categ_name == 'Page':
				unit_price = self.trans_page
			else:
				unit_price = self.trans_word
		elif translation_service_type == 'proofread':
			if uom_categ_name == 'Flat':
				unit_price = self.proof_flat
			elif uom_categ_name == 'Page':
				unit_price = self.proof_flat
			else:
				unit_price = self.proof_word
		return unit_price
	
	
class tmsLanguageGroup(models.Model):
	_name = 'tms.language_group'
	_description = 'Rate groups for Translation Service Languages'
	
	name = fields.Char()
	
	trans_word = fields.Float(string='Translation Rate per Word')
	trans_page = fields.Float(string='Translation Rate per Page')
	trans_flat = fields.Float(string='Translation Rate Flat Fee')
	proof_flat = fields.Float(string='Proofread Rate Flat Fee')
	proof_word = fields.Float(string='Proofread Rate per Word')
	trans_cost = fields.Float(string='Translation Cost per Word')
	trans_cost_flat = fields.Float(string='Translation Cost Flat Fee')
	proof_cost = fields.Float(string='Proofread Cost per Word')
	proof_cost_flat = fields.Float(string='Proofread Cost Flat Fee')