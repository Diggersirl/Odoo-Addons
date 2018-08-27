# -*- coding: utf-8 -*-

from openerp import models, fields, api

class translationie_always_email_reports(models.Model):
	_inherit = 'res.partner'
#     _name = 'translationie_always_email_reports.translationie_always_email_reports'

#original method in addons\mail\models\res_partner.py
	def _notify(self, message, force_send=False, user_signature=True):
		# TDE TODO: model-dependant ? (like customer -> always email ?)
		message_sudo = message.sudo()
		email_channels = message.channel_ids.filtered(lambda channel: channel.email_send)
		if str(message_sudo.model) == 'sale.order' or str(message_sudo.model) == 'account.invoice':
			if message_sudo.attachment_ids:
						self.sudo().search([
						'|',
						('id', 'in', self.ids),
						('channel_ids', 'in', email_channels.ids),
						('email', '!=', message_sudo.author_id and message_sudo.author_id.email or message.email_from)
						])._notify_by_email(message, force_send=True, user_signature=user_signature)
		else:
			self.sudo().search([
				'|',
				('id', 'in', self.ids),
				('channel_ids', 'in', email_channels.ids),
				('email', '!=', message_sudo.author_id and message_sudo.author_id.email or message.email_from),
				('notify_email', '!=', 'none')])._notify_by_email(message, force_send=force_send, user_signature=user_signature)
		self._notify_by_chat(message)
		return True
