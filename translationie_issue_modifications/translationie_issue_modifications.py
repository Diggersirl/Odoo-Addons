# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

class translationie_Project_issue_modifications(models.Model):
	_inherit = 'project.issue'
	
	x_type = fields.Selection([('positive','Positive Feedback'),('constructive','Constructive Feedback'),('change','Procedure Change'),('complaint','Complaint')],string='Issue Type')
	x_follow_up = fields.Text(string='Follow Up')