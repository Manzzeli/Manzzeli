import re

from odoo import api, models
from odoo.exceptions import ValidationError


class Contactvalidationmobile(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')


    @api.constrains('mobile')
    def mobile_z_method_res(self):
        for rec in self:
            if rec.mobile and re.match("^01[0125][0-9]{8}$", rec.mobile) == None:
                raise ValidationError('Mobile Must Be Valid & 11 Number')

    @api.onchange('mobile')
    def _onchange_mobile_validation(self):
        if self.mobile:
            self.mobile != self._phone_format(self.mobile)



class Crmvalidationmobile(models.Model):
    _inherit = 'crm.lead'

    @api.constrains('email_from')
    def validate_mail(self):
        if self.email_from:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_from)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    @api.constrains('mobile')
    def mobile_z_method_res(self):
        for rec in self:
            if rec.mobile and re.match("^01[0125][0-9]{8}$", rec.mobile) == None:
                raise ValidationError('Mobile Must Be Valid & 11 Number')

    @api.constrains('phone')
    def phone_z_method_res(self):
        for rec in self:
            if rec.phone and re.match("^01[0125][0-9]{8}$", rec.phone) == None:
                raise ValidationError('Phone Must Be Valid & 11 Number')

    @api.onchange('mobile', 'country_id', 'company_id')
    def _onchange_mobile_validation(self):
        if self.mobile:
            self.mobile != self.phone_get_sanitized_number(number_fname='mobile',force_format='INTERNATIONAL') or self.mobile

    @api.onchange('phone', 'country_id', 'company_id')
    def _onchange_phone_validation(self):
        if self.phone:
            self.phone != self.phone_get_sanitized_number(number_fname='phone',force_format='INTERNATIONAL') or self.phone

