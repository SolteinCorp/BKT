# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class Project(models.Model):
    _inherit = 'project.project'

    sale_order_id = fields.Many2one('sale.order', string='Orden de venta', index=True)



