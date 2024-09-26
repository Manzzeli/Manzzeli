# -*- coding: utf-8 -*-
# from odoo import http


# class NameSearchByPhoneNumber(http.Controller):
#     @http.route('/name_search_by_phone_number/name_search_by_phone_number', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/name_search_by_phone_number/name_search_by_phone_number/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('name_search_by_phone_number.listing', {
#             'root': '/name_search_by_phone_number/name_search_by_phone_number',
#             'objects': http.request.env['name_search_by_phone_number.name_search_by_phone_number'].search([]),
#         })

#     @http.route('/name_search_by_phone_number/name_search_by_phone_number/objects/<model("name_search_by_phone_number.name_search_by_phone_number"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('name_search_by_phone_number.object', {
#             'object': obj
#         })
