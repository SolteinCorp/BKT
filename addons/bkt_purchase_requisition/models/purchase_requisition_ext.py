# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    name = fields.Char(string='Agreement Reference', required=True, copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('purchase.requisition.ext'))
