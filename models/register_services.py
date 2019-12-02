# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *


class ProductInherit(models.Model):
    _inherit = 'product.template'
    rental_ok = fields.Boolean(string='Can be Rental')

    @api.onchange('type')
    def _onchange_type_for_expense(self):
        # storable can not be expensed.
        if self.type not in ['service']:
            self.rental_ok = False

    @api.model
    def create(self, vals_list):
        res = super(ProductInherit, self).create(vals_list)
        print('Created product ID ' + res.name + ' rental:' +
              ('true' if res.rental_ok else 'false'))
        # do something with res.partner
        return res


class InvoiceInherit(models.Model):
    _inherit = "account.move"

    @api.model
    def post(self):
        super(InvoiceInherit, self).post()
        # do something
        if self.invoice_line_ids:
            for rec in self.invoice_line_ids:
                if rec.product_id.rental_ok:
                    # create register service
                    vals = {
                        "partner_id": self.partner_id.id,
                        "user_id": self.create_uid.id,
                        "product_id": rec.product_id.id,
                        "register_date": self.create_date,
                        "months": rec.quantity,
                        "invoice_id": self.id
                    }
                    self.env['rental.registerservice'].create(vals)

                    services = self.env['rental.customerservice'].search(
                        [('partner_id', '=', self.partner_id.id), ('product_id', '=', rec.product_id.id)])

                    services_count = self.env['rental.customerservice'].search_count(
                        [('partner_id', '=', self.partner_id.id), ('product_id', '=', rec.product_id.id)])

                    if services_count == 0:
                        # create customer service if not exist in customer service
                        vals = {
                            "partner_id": self.partner_id.id,
                            "product_id": rec.product_id.id,
                            "start_date": self.create_date,
                            "expried_date": self.create_date + relativedelta(months=+int(rec.quantity)),
                        }
                        self.env['rental.customerservice'].create(vals)
                    else:
                        # update expried_date if exist
                        services.expried_date = services.expried_date + \
                            relativedelta(months=+int(rec.quantity))


class RegisterServices(models.Model):
    _name = 'rental.registerservice'
    _description = 'Register Service Record'

    partner_id = fields.Many2one('res.partner', string="Customer")
    user_id = fields.Many2one('res.users', string="User")
    product_id = fields.Many2one('product.template', string="Service")
    invoice_id = fields.Many2one('account.move', string="Invoice")
    register_date = fields.Date(string="Register Date")
    months = fields.Integer(string="Months")
