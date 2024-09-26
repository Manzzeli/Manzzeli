# -*- coding: utf-8 -*-
# from odoo import http


# class ShipingManzili(http.Controller):
#     @http.route('/shiping_manzili/shiping_manzili', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shiping_manzili/shiping_manzili/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('shiping_manzili.listing', {
#             'root': '/shiping_manzili/shiping_manzili',
#             'objects': http.request.env['shiping_manzili.shiping_manzili'].search([]),
#         })

#     @http.route('/shiping_manzili/shiping_manzili/objects/<model("shiping_manzili.shiping_manzili"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shiping_manzili.object', {
#             'object': obj
#         })
