# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.addons.web.http import Controller, route, request
from openerp.http import request

from openerp.exceptions import Warning

import openerp.addons.report.controllers.main as main
from datetime import datetime

from openerp.addons.web.controllers.main import _serialize_exception, content_disposition
from openerp.tools import html_escape
import json
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
from reportlab.graphics.barcode import createBarcodeDrawing

class reportControllerExtension(main.ReportController):
	
	@route(['/report/download'], type='http', auth="user")
	def report_download(self, data, token):
		"""This function is used by 'qwebactionmanager.js' in order to trigger the download of
		a pdf/controller report.

		:param data: a javascript array JSON.stringified containg report internal url ([0]) and
		type [1]
		:returns: Response with a filetoken cookie and an attachment header
		"""
		requestcontent = json.loads(data)
		url, type = requestcontent[0], requestcontent[1]
		try:
			if type == 'qweb-pdf':
				reportname = url.split('/report/pdf/')[1].split('?')[0]

				

				
				#raise Warning('url is %s' % reportname)
				docids = None
				if '/' in reportname:
					reportname, docids = reportname.split('/')
					
				if docids:
					# Generic report:
					response = self.report_routes(reportname, docids=docids, converter='pdf')
				else:
					# Particular report:
					data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
					response = self.report_routes(reportname, converter='pdf', **dict(data))

				cr, uid = request.cr, request.uid
				report = request.registry['report']._get_report_from_name(cr, uid, reportname)
				if request.context:
					#act_ids = request.context.get('active_id')
					if report.model:
						m = request.session.model(report.model)
						try:
							report_id = url.split('/report/pdf/')[1].split('/')[1].split('?')[0]
						except IndexError:
							report_id = False
							file_name = False
						if report_id:
							report_id = int(report_id)
							r = m.read(report_id, False, request.context)
							#raise Warning("r is %s" % r)
							try:
								if r.has_key('name'):
									if str(report.model) == 'sale.order':
										file_name = '%s_%s_%s' % ('Quotation_Ref',r['name'],datetime.today().strftime('%d_%b_%Y'))
										if r.has_key('amount_total'):
											file_name = '%s_EUR%s' %(file_name, r['amount_total'])
									else:
										file_name = '%s_%s' % (r['name'],datetime.today().strftime('%d_%b_%Y'))
								elif r.has_key('number'):
									file_name = '%s_%s' % (r['number'],datetime.today().strftime('%d_%b_%Y'))
							except TypeError:
								raise Warning("r is %s \n act_ids is %s" % (r, act_ids))
								file_name = False
				filename = "%s.%s" % (report.name, "pdf")
				if file_name:
					response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf' % file_name)
				else:
					response.headers.add('Content-Disposition', content_disposition(filename))
				response.set_cookie('fileToken', token)
				return response
			elif type =='controller':
				reqheaders = Headers(request.httprequest.headers)
				response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
				response.set_cookie('fileToken', token)
				return response
			else:
				return
		except Exception, e:
			se = _serialize_exception(e)
			error = {
				'code': 200,
				'message': "Odoo Server Error",
				'data': se
			}
			return request.make_response(html_escape(json.dumps(error)))