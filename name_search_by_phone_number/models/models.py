from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re



class searchphonenumber(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('mobile', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    _sql_constraints = [
        ('mobile_id', 'unique (mobile)', 'The mobile must be unique!')
    ]

    @api.constrains('mobile')
    def mobile_z_method_res(self):
        for rec in self:
            if rec.mobile and re.match("^01[0125][0-9]{10}$", rec.mobile) == None:
                raise ValidationError('Mobile Must Be Valid & 11 Number')

