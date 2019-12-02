# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomerServices(models.Model):
    _name = 'rental.customerservice'
    _description = 'Customer Service Record'

    partner_id = fields.Many2one('res.partner', string="Customer")
    product_id = fields.Many2one('product.template', string="Service")
    start_date = fields.Date(string="Start Date")
    expried_date = fields.Date(string="Expried Date")
