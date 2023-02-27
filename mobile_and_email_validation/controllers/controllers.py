# -*- coding: utf-8 -*-
# from odoo import http


# class MobileAndEmailValidation(http.Controller):
#     @http.route('/mobile_and__email__validation/mobile_and__email__validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile_and__email__validation/mobile_and__email__validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile_and__email__validation.listing', {
#             'root': '/mobile_and__email__validation/mobile_and__email__validation',
#             'objects': http.request.env['mobile_and__email__validation.mobile_and__email__validation'].search([]),
#         })

#     @http.route('/mobile_and__email__validation/mobile_and__email__validation/objects/<model("mobile_and__email__validation.mobile_and__email__validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile_and__email__validation.object', {
#             'object': obj
#         })
