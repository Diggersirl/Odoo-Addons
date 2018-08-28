# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	
	source_lang = fields.Many2one(comodel_name='tms.languages', string='Source', ondelete='set null')
	target_lang = fields.Many2one(comodel_name='tms.languages', string='Target', ondelete='set null')
	sol_group = fields.Many2one(comodel_name='sale.order.line.group', string="Group", help="Group of Sale Order Lines this line belongs to", ondelete='set null')
	translation_service = fields.Boolean()
	update_linked = fields.Boolean()
	
	
	@api.model
	def create(self, values):
		line = super(SaleOrderLine, self).create(values)
		if line.product_id.group_sol and not line.sol_group:
			data = {
				'order_id' : line.order_id.id,
				'order_line' : [(4, line.id)],
				}
			sol_group = self.env['sale.order.line.group'].create(data)
			line.write({'sol_group':sol_group.id})
		if line.product_id.group_sol:
			grouped_line = self._create_grouped_line(values, line)
		return line
		
		
	def _create_grouped_line(self, values, line):
		data = {
			'order_id' : line.order_id.id,
			'product_id' : line.product_id.grouped_product.id,
			'translation_service' : line.translation_service,
			'product_uom_qty': line.product_uom_qty,
			'product_uom' : line.product_uom.id,
		}
		
		if line.product_id.grouped_product.is_translation_service:
			data['source_lang'] = line.source_lang.id
			data['target_lang'] = line.target_lang.id
			data['translation_service'] = True
			
			source_price = source_lang.get_unit_price(line.product_uom, line.product_id.translation_service_type)
			target_price = target_lang.get_unit_price(line.product_uom, line.product_id.translation_service_type)
			if source_price >= target_price:
				unit_price = source_price
			else:
				unit_price = target_price
			
			data['price_unit'] = unit_price
		if line.sol_group:
			data['sol_group'] = line.sol_group.id
		
		values.update(data)

		grouped_line = super(SaleOrderLine, self).create(values)
		return grouped_line
	
	@api.multi
	@api.onchange('product_id')
	def product_id_change(self):
		result = super(SaleOrderLine, self).product_id_change()
		vals = {}
		if self.product_id.is_translation_service:
			vals['translation_service'] = True
		else:
			vals['translation_service'] = False
			
		if not self.product_id.group_sol and self.sol_group:
			sol_group = self.env['sale.order.line.group'].search([('id','=',self.sol_group.id)])
			sol_group.order_line = [('3',self.id)]
			vals['sol_group'] = False
		elif self.product_id.group_sol and not self.sol_group:
			next_seq = self.env['ir.sequence'].next_by_code('sale.order.line.group')
			group_name = self.order_id.name + '_' + str(next_seq)
			data = {
				'name' : group_name,
				'order_line': [(4,self.id)]
				}
			sol_group = self.env['sale.order.line.group'].create(data)
			
			vals['sol_group'] = sol_group.id
			
			
		self.update(vals)
		
	@api.multi
	@api.onchange('source_lang', 'target_lang', 'product_uom')
	def update_unit_price(self):
		vals = {}
		source_price = self.source_lang.get_unit_price(self.product_uom, self.product_id.translation_service_type)
		target_price = self.target_lang.get_unit_price(self.product_uom, self.product_id.translation_service_type)
		
		if source_price >= target_price:
			unit_price = source_price
		else:
			unit_price = target_price
		vals['price_unit'] = unit_price
		update = False
		
		if self.product_id.group_sol:
			update = True 
		vals['update_linked'] = update
		self.update(vals)
	
		
	@api.multi
	def write(self, values):
		try:
			order_id = self.env['sale.order'].search([('name','=',self.order_id.name)])
			
			result = super(SaleOrderLine, self).write(values)
			product_id = self.env['product.product'].browse(values.get('product_id'))
			if product_id.group_sol:
				
				line_group = self.env['sale.order.line.group'].browse(self.sol_group.id)
				
				line_exists = any(product_id == self.product_id.grouped_product for product_id in line_group.order_line.product_id)
				
				if not line_exists:
					data = {
						'order_id' : order_id.id,
						'product_id' : product_id.grouped_product.id,
						'sol_group' : self.sol_group.id,
					}
					if product_id.grouped_product.is_translation_service:
						data['source_lang'] = self.source_lang.id
						data['target_lang'] = self.target_lang.id
						data['translation_service'] = True
					values.update(data)
					grouped_line = self.env['sale.order.line'].create(data)
					
			if self.update_linked:
				line_group = self.env['sale.order.line.group'].browse(self.sol_group.id)
				source_lang = self.source_lang
				target_lang = self.target_lang
				for line in line_group.order_line:
					line_vals = {
						'product_uom': self.product_uom.id,
						'update_linked': False,
						}
					if line.product_id.is_translation_service:
						line_vals['translation_service'] = True
						line_vals['source_lang'] = source_lang.id
						line_vals['target_lang'] = target_lang.id
						
						source_price = source_lang.get_unit_price(self.product_uom, line.product_id.translation_service_type)
						target_price = target_lang.get_unit_price(self.product_uom, line.product_id.translation_service_type)
						if source_price >= target_price:
							unit_price = source_price
						else:
							unit_price = target_price
						
						line_vals['price_unit'] = unit_price
					line.write(line_vals)
					
					
			return result
		except Exception:
			_logger.error("ERROR IN WRITE", exc_info=True)
		
	
class SaleOrderLineGroup(models.Model):
	_name = 'sale.order.line.group'
	
	name = fields.Char()
	order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order")
	order_line = fields.One2many(comodel_name='sale.order.line', inverse_name='sol_group', ondelete="set null")
	
	def _prepare_name(self, values):
		order_id = values.get('order_id')
		order_id = self.env['sale.order'].search([('id','=',order_id)])
		next_seq = self.env['ir.sequence'].next_by_code('sale.order.line.group')
		group_name = str(order_id.name) + '_' + str(next_seq)
		data = {
				'name':group_name,
				}
		values.update(data)
		return values
	
	def update_line_values(self, values):
		try:
			for line in self.order_line:
				_logger.debug("UPDATING LINE: " + str(line))
				_logger.debug("UPDATING LINE ID: " + str(self.env['sale.order.line'].browse(line.id)))
				if self.env['sale.order.line'].browse(line.id):
					line.write(values)
		except Exception:
			_logger.error("ERROR UPDATING LINE GROUP", exc_info=True)
	
	@api.model
	def clean_empty_groups(self):
		_logger.debug("STARTING CLEAN")
		try:
			records = self.env['sale.order.line.group'].search([])
			_logger.debug("RECORDS: " + str(len(records)))
			for record in records:
				_logger.debug("CLEANING GROUP: " + str(record))
				if len(record.order_line) == 0:
					record.unlink()
					_logger.info("Deleted Sale order Group: " + str(record))
		except Exception:
			_logger.error("ERROR cleanign empty sale order line groups", exc_info=True)
		
	@api.model
	def create(self, values):
		_logger
		if not values.get('name'):
			values = self._prepare_name(values)
		result = super(SaleOrderLineGroup, self).create(values)
		return result