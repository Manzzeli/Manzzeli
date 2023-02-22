from odoo import models


class contactsemailandphone(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('unique_mobile', 'unique (mobile)', 'The mobile must be unique!'),
        ('unique_phone', 'unique (phone)', 'The phone must be unique!'),
    ]


class contactsemailandphonecrm(models.Model):
    _inherit = 'crm.lead'
    _sql_constraints = [
        ('phone_uniq', 'unique(phone)', 'The phone must be unique!'),
        ('mobile_uniq', 'unique(mobile)', 'The mobile must be unique!'),
    ]
