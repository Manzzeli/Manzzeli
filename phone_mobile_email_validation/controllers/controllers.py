# -*- coding: utf-8 -*-
# from odoo import http


# class PhoneMobileEmailValidation/home/mohamedAli/odoo15C/custom(http.Controller):
#     @http.route('/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom.listing', {
#             'root': '/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom',
#             'objects': http.request.env['phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom.phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom'].search([]),
#         })

#     @http.route('/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom/objects/<model("phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom.phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phone_mobile_email_validation/home/mohamed_ali/odoo15_c/custom.object', {
#             'object': obj
#         })
