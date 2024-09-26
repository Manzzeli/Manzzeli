from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from itertools import groupby
from datetime import date

from datetime import datetime


class shiping(models.Model):
    _inherit = 'sale.order.line'

    shipping = fields.Float(string="Shiping", required=False, )

    # new_field_id = fields.Many2one(comodel_name="purchase.order.line", string="", required=False, )
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    # price_subtotal = fields.Monetary(string='Subtotal', store=True, readonly=True,
    #                                  currency_field='currency_id')
    # is_new_field = fields.Boolean(string="TF",  )

    # @api.onchange('order_line')
    # for line in order_line:
    #     line.price_subtotal = line.shipping + line.price_subtotal

    @api.depends('shipping')
    def _compute_amount(self):
        res = super(shiping, self)._compute_amount()
        for rec in self:
            if rec.price_subtotal:
                rec.price_subtotal = rec.shipping + rec.price_subtotal
        return res

    def _prepare_invoice_line(self, **optional_values):
        res = super(shiping, self)._prepare_invoice_line()
        res.update({'re_shiping_test': self.shipping,

                    })
        return res


class accountmovelineshiping(models.Model):
    _inherit = 'account.move.line'

    re_shiping_test = fields.Float(string="Shiping", required=False, )
    purchase_shipping = fields.Float(string="P Shiping", required=False, )

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
        BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids', 're_shiping_test', 'purchase_shipping')

        for vals in vals_list:
            move = self.env['account.move'].browse(vals['move_id'])
            vals.setdefault('company_currency_id',
                            move.company_id.currency_id.id)  # important to bypass the ORM limitation where monetary fields are not rounded; more info in the commit message

            # Ensure balance == amount_currency in case of missing currency or same currency as the one from the
            # company.
            currency_id = vals.get('currency_id') or move.company_id.currency_id.id
            if currency_id == move.company_id.currency_id.id:
                balance = vals.get('debit', 0.0) - vals.get('credit', 0.0)
                vals.update({
                    'currency_id': currency_id,
                    'amount_currency': balance,
                })
            else:
                vals['amount_currency'] = vals.get('amount_currency', 0.0)

            if move.is_invoice(include_receipts=True):
                currency = move.currency_id
                partner = self.env['res.partner'].browse(vals.get('partner_id'))
                taxes = self.new({'tax_ids': vals.get('tax_ids', [])}).tax_ids
                tax_ids = set(taxes.ids)
                taxes = self.env['account.tax'].browse(tax_ids)

                # Ensure consistency between accounting & business fields.
                # As we can't express such synchronization as computed fields without cycling, we need to do it both
                # in onchange and in create/write. So, if something changed in accounting [resp. business] fields,
                # business [resp. accounting] fields are recomputed.
                if any(vals.get(field) for field in ACCOUNTING_FIELDS):
                    price_subtotal = self._get_price_total_and_subtotal_model(
                        vals.get('price_unit', 0.0),
                        vals.get('quantity', 0.0),
                        vals.get('discount', 0.0),
                        currency,
                        self.env['product.product'].browse(vals.get('product_id')),
                        partner,
                        taxes,
                        move.move_type,
                        vals.get('re_shiping_test', 0.0),
                        vals.get('purchase_shipping', 0.0),
                    ).get('price_subtotal', 0.0)
                    vals.update(self._get_fields_onchange_balance_model(
                        vals.get('quantity', 0.0),
                        vals.get('discount', 0.0),
                        vals['amount_currency'],
                        move.move_type,
                        currency,
                        taxes,
                        price_subtotal
                    ))
                    vals.update(self._get_price_total_and_subtotal_model(
                        vals.get('price_unit', 0.0),
                        vals.get('quantity', 0.0),
                        vals.get('discount', 0.0),
                        currency,
                        self.env['product.product'].browse(vals.get('product_id')),
                        partner,
                        taxes,
                        move.move_type,
                        vals.get('re_shiping_test', 0.0),
                        vals.get('purchase_shipping', 0.0),

                    ))
                elif any(vals.get(field) for field in BUSINESS_FIELDS):
                    vals.update(self._get_price_total_and_subtotal_model(
                        vals.get('price_unit', 0.0),
                        vals.get('quantity', 0.0),
                        vals.get('discount', 0.0),
                        currency,
                        self.env['product.product'].browse(vals.get('product_id')),
                        partner,
                        taxes,
                        move.move_type,
                        vals.get('re_shiping_test', 0.0),
                        vals.get('purchase_shipping', 0.0),

                    ))
                    vals.update(self._get_fields_onchange_subtotal_model(
                        vals['price_subtotal'],
                        move.move_type,
                        currency,
                        move.company_id,
                        move.date,
                    ))

        lines = super(accountmovelineshiping, self).create(vals_list)

        moves = lines.mapped('move_id')
        if self._context.get('check_move_validity', True):
            moves._check_balanced()
        moves._check_fiscalyear_lock_date()
        lines._check_tax_lock_date()
        moves._synchronize_business_models({'line_ids'})

        return lines

    def _get_price_total_and_subtotal(self, price_unit=None, quantity=None, discount=None, currency=None, product=None,
                                      partner=None, taxes=None, move_type=None, re_shiping_test=None,
                                      purchase_shipping=None):
        self.ensure_one()
        return self._get_price_total_and_subtotal_model(
            price_unit=price_unit or self.price_unit,
            quantity=quantity or self.quantity,
            discount=discount or self.discount,
            currency=currency or self.currency_id,
            product=product or self.product_id,
            partner=partner or self.partner_id,
            taxes=taxes or self.tax_ids,
            move_type=move_type or self.move_id.move_type,
            re_shiping_test=re_shiping_test or self.re_shiping_test,
            purchase_shipping=purchase_shipping or self.purchase_shipping,
        )

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes,
                                            move_type, re_shiping_test=0, purchase_shipping=0):
        ''' this method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  the current price unit.
        :param quantity:    the current quantity.
        :param discount:    the current discount.
        :param currency:    the line's currency.
        :param product:     the line's product.
        :param partner:     the line's partner.
        :param taxes:       the applied taxes.
        :param move_type:   the type of the move.
        :return:            a dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # compute 'price_subtotal'.
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))

        print(type(re_shiping_test))
        print(re_shiping_test)
        subtotal = quantity * line_discount_price_unit + re_shiping_test + purchase_shipping

        # compute 'price_total'.
        if taxes:
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(line_discount_price_unit,
                                                                                      quantity=quantity,
                                                                                      currency=currency,
                                                                                      product=product, partner=partner,
                                                                                      is_refund=move_type in (
                                                                                          'out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded'] + re_shiping_test + purchase_shipping
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        # in case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res

    @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids', 're_shiping_test', 'purchase_shipping')
    def _onchange_price_subtotal(self):
        res = super(accountmovelineshiping, self)._onchange_price_subtotal()
        for rec in self:
            if rec.price_subtotal:
                rec.price_subtotal = rec.re_shiping_test + rec.purchase_shipping + rec.price_subtotal
        return res

    # @api.depends('purchase_shipping')
    # def _compute_amount(self):
    #     res = super(accountmovelineshiping, self)._compute_amount()
    #     for rec in self:
    #         if rec.price_subtotal:
    #             rec.price_subtotal = rec.purchase_shipping + rec.price_subtotal
    #     return res


# class accountmoveone(models.Model):
#     _inherit = 'account.move'
#
#     shiping_one = fields.Float(string="",  required=False,compute='shipping_one_r',currency_field='company_currency_id' )
#     # tax_totals_json = fields.Float(
#     #     string="Invoice Totals JSON",
#     #     compute='_compute_tax_totals_json',
#     #     readonly=False,
#     #     help='Edit Tax amounts if you encounter rounding issues.')
#
#     @api.depends('shiping_one')
#     def shipping_one_r(self):
#         for rec in self:
#             if rec.invoice_line_ids:
#                 for line in rec.invoice_line_ids:
#                     rec.shiping_one += line.re_shiping_test
#
#             else:rec.shiping_one=0
#
#
#     @api.depends('shiping_one')
#     def _compute_amount(self):
#         res = super(accountmoveone, self)._compute_amount()
#         for rec in self:
#             if rec.shiping_one:
#                 rec.amount_total = rec.shiping_one + rec.amount_total
#                 rec.amount_residual = rec.shiping_one + rec.amount_residual
#                 # rec.price_subtotal = rec.shiping_one + rec.price_subtotal
#
#         return res

# def _compute_amount(self):
#     res = super(accountmoveone, self)._compute_amount()
#     for rec in self:
#         if rec.shiping_one:
#             rec.amount_residual = rec.shiping_one + rec.amount_residual
#     return res


# amount_residual = fields.Monetary(string='Amount Due', store=True,
#                                   compute='_c


# def test_meth(self):
#     for rec in self:
#         if rec.line_ids:
#             for line in rec.line_ids:
#                 rec.sum_amount += line.amount
#         else:
#             rec.sum_amount=0


class shipingpurchase(models.Model):
    _inherit = 'purchase.order.line'

    shipping_uu = fields.Float(string="Shiping", required=False, related='sale_line_id.shipping')

    # new_field_id = fields.Many2one(comodel_name="sale.order.line", string="Sale Order Line", required=False,)

    @api.depends('shipping_uu')
    def _compute_amount(self):
        res = super(shipingpurchase, self)._compute_amount()
        for rec in self:
            if rec.price_subtotal:
                rec.price_subtotal = rec.shipping_uu + rec.price_subtotal
        return res

    # def _prepare_invoice(self):
    #     res = super(shiping, self)._prepare_invoice()
    #     res.update({'purchase_shipping': self.shipping_uu,
    #
    #                 })
    #     return res

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'purchase_line_id': self.id,
            'purchase_shipping': self.shipping_uu,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res


# class NewModule(models.Model):
#     _inherit = 'sale.order'
#
#     def action_view_purchase_orders(self):
#         self.ensure_one()
#         purchase_order_ids = self._get_purchase_orders().ids
#         action = {
#             'res_model': 'purchase.order',
#             'type': 'ir.actions.act_window',
#
#         }
#         if len(purchase_order_ids) == 1:
#             action.update({
#                 'view_mode': 'form',
#                 'res_id': purchase_order_ids[0],
#             })
#         else:
#             action.update({
#                 'name': _("Purchase Order generated from %s", self.name),
#                 'domain': [('id', 'in', purchase_order_ids)],
#                 'view_mode': 'tree,form',
#             })
#         return action
#
#         # def _get_purchase_orders(self):
#         #     return self.order_line.purchase_line_ids.shipping
#         #
#


class accounttestmanzili(models.Model):
    _inherit = 'account.move'

    date_test = fields.Date(string=' Accounting Date',required=True,default=lambda self: datetime.now())

    date = fields.Date(
        string='Date',
        required=False,
        copy=False,
        tracking=True,
    )


