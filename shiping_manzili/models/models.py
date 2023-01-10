from odoo import api, fields, models



class shiping(models.Model):
    _inherit = 'sale.order.line'

    shipping = fields.Float(string="shiping",  required=False, )
    # is_new_field = fields.Boolean(string="TF",  )

    @api.depends('shipping')
    def _compute_amount(self):
        res = super(shiping, self)._compute_amount()
        for rec in self:
            if rec.shipping:
             rec.price_subtotal= rec.shipping + rec.price_subtotal
        return res
