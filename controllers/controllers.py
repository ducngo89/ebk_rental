# -*- coding: utf-8 -*-
from odoo import http

# class EbkRental(http.Controller):
#     @http.route('/ebk_rental/ebk_rental/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ebk_rental/ebk_rental/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ebk_rental.listing', {
#             'root': '/ebk_rental/ebk_rental',
#             'objects': http.request.env['ebk_rental.ebk_rental'].search([]),
#         })

#     @http.route('/ebk_rental/ebk_rental/objects/<model("ebk_rental.ebk_rental"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ebk_rental.object', {
#             'object': obj
#         })