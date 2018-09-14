# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class Picking(models.Model):
    _inherit = 'stock.picking'

    is_transportation = fields.Boolean('Es transportación', help='Marcar si la orden es de transportación')


    transportation_type = fields.Selection([
        ('external', 'Externa'),
        ('internal', 'Interna')], string='Tipo de transportacion', default='internal')

    transportista_id = fields.Many2one('hr.employee', 'Transportista')

    sale_order_id = fields.Many2one('sale.order', string='Orden de venta asociada', index=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Orden de compra asociada', index=True, )

    @api.model
    def create(self, vals):
        id_pikin = super(Picking, self).create(vals)
        if 'is_transportation':
            name = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('otp.order')

        self.env['stock.picking'].browse(id_pikin.id).write({'name': name})
        return id_pikin

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        for otp in self:
            otp.origin = otp.sale_order_id.name