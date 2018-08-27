# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning, UserError
from datetime import datetime
import datetime
import logging

_logger = logging.getLogger(__name__)

class multipleStatusWizard(models.TransientModel):
	_name = "project.task.status.wizard"
	
	@api.multi
	def mark_complete_multiple(self):
		try:
			tasks = self.env['project.task'].browse(self._context.get('active_ids', []))
			for task in tasks:
				if  task.x_status == 'open':
					mark_complete = True
					if not task.x_purchase_order.exists():
						task._create_po(task)
				elif task.x_status == 'draft' and task.x_translator.exists():
					mark_complete = True
				else:
					mark_complete = False
				if mark_complete:
					task.write({'x_completed':True, 'x_status':'complete'})
		except Exception:
			_logger.error("error marking multiple tasks complete", exc_info=True)
		
	@api.multi
	def set_inhouse_translator(self):
		try:
			tasks = self.env['project.task'].browse(self._context.get('active_ids', []))
			for task in tasks:
				# _logger.debug("CREATE DATE: " + str(task.create_date)  + " LIMIT: " + str(datetime.datetime(2018, 1, 1)))
				if task.x_status == 'draft' and not task.x_translator.exists() and task.create_date < str(datetime.datetime(2018, 1, 1)):
					translator = self.env['res.partner'].search([('name','like','In House')])
					# _logger.debug("translator is: " + str(translator))
					data = {
						'x_translator': translator.id,
						'x_status': 'complete',
						'x_completed': True,
						}
					task.write(data)
					if not task.x_purchase_order.exists():
						task._create_po(task)
		except Exception:
			_logger.error("error setting translator as in house", exc_info=True)
	
	@api.multi
	def delete_task(self):
		try:
			tasks = self.env['project.task'].browse(self._context.get('active_ids', []))
			for task in tasks:
				if task.sale_line_id.exists():
					task.sale_line_id = False
				task.unlink()
		except Exception:
			_logger.error("error deleting task", exc_info=True)