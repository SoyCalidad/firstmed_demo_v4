# -*- coding: utf-8 -*-
# from odoo import http


# class Modulo1(http.Controller):
#     @http.route('/modulo_1/modulo_1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_1/modulo_1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_1.listing', {
#             'root': '/modulo_1/modulo_1',
#             'objects': http.request.env['modulo_1.modulo_1'].search([]),
#         })

#     @http.route('/modulo_1/modulo_1/objects/<model("modulo_1.modulo_1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_1.object', {
#             'object': obj
#         })
