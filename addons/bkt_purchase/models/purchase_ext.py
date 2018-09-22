# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string='Documento origen', index=True)


    @api.model
    def create(self, vals):
        result = super(PurchaseOrder, self).create(vals)
        code = self.env['ir.sequence'].next_by_code('purchase.order.ext')
        result.write({'name': code})
        return result





