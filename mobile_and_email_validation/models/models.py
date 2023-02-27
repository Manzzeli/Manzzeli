from odoo import models, _, api, fields
import re
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class contactsemailandphone(models.Model):
    _inherit = 'res.partner'

    @api.onchange('phone')


    def set_constrains_res_partner_phone(self):
        if self.phone:
            phone_number = self.env['res.partner'].search([('phone', '=', self.phone)])
            if phone_number:
                raise ValidationError(_("There is another Contact with same Phone."))


    @api.onchange('mobile')
    def set_constrains_res_partner_mobile(self):
        if self.mobile:
            mobile_number = self.env['res.partner'].search([('mobile', '=', self.mobile)])
            if mobile_number:
                raise ValidationError(_("There is another Contact with same mobile."))


class contactsemailandphonecrm(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('phone')
    def set_constrains_phone(self):
        if self.phone:
            phone_number = self.env['crm.lead'].search([('phone', '=', self.phone)])
            if phone_number:
                raise UserError(_("There is another Contact with same Phone."))

    @api.onchange('mobile')
    def set_constrains_mobile(self):
        if self.mobile:
            mobile_number = self.env['crm.lead'].search([('mobile', '=', self.mobile)])
            if mobile_number:
                raise UserError(_("There is another Contact with same mobile."))
