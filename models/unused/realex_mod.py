
from openerp import models, fields, api
import logging
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)

class translationie_realex_mod(models.Model):
	_inherit = 'res.config.settings'
	_name = 'custom_payments.realex_mod'

	url = fields.Char(string='Realex url', help='Url for realex hosted payment page', default='https://hpp.sandbox.realexpayments.com/pay')
	merchant_id = fields.Char(string='Merchant ID', help='Merchant ID provided by Realex, also known as Client ID', default='translation')
	account = fields.Char(default='internet')
	secret = fields.Char(help='Realex Shared Secret', default='tonys secret')
	response_url = fields.Char(string='Merchant Response Url', help='Url for Realex to respond with result of payment to.', default="https://erp.translation.ie/payment_processed")
	hpp_version = fields.Selection([('1','No Card Management'),('2','Card Management')], string='Payment Page Version', default='1', help='[no_management] = No Card Management available on Hosted Payment Page. [managment] = Card Management available on Hosted Payment Page')

	"""If an object of this model exists return it, if not create a new one and return it."""
	@api.model
	def initialisation(self):
		realex_mod = self.env['custom_payments.realex_mod'].browse(1)

		if not realex_mod:
			realex_mod = self.create({
				'url': 'https://hpp.sandbox.realexpayments.com/pay',
				'merchant_id': 'translation',
				'account': 'internet',
				'secret': 'secret',
				'response_url': 'https://erp.translation.ie/payment_processed',
				'hpp_version': '1'})

		return realex_mod

	"""docstring for ."""
	@api.one
	def update_realex_mod(self):
		realex_mod = self
		_logger.debug('')
		if realex_mod:
			realex_mod.url = self.url
			realex_mod.merchant_id = self.merchant_id
			realex_mod.account = self.account
			realex_mod.secret = self.secret
			realex_mod.response_url = self.response_url
			realex_mod.hpp_version = self.hpp_version
