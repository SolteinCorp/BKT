# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_ids = fields.One2many('project.project', 'sale_order_id', string='Proyectos')
    project_count = fields.Integer(compute='_compute_project_number', string='Proyectos')

    mrp_ids = fields.One2many('mrp.production', 'sale_order_id', string='Producciones')
    mrp_count = fields.Integer(compute='_compute_mrp_number', string='Producciones')

    otp_order_ids = fields.One2many('stock.picking', 'sale_order_id', string='Transportaciones')
    otp_count = fields.Integer(compute='_compute_otp_number', string='Transportaciones')

    sale_commission_id = fields.Many2one('sale.commission', string='Comisiones de venta', index=True)


    @api.multi
    @api.depends('otp_order_ids')
    def _compute_otp_number(self):
        for otp in self:
            otp.otp_count = len(otp.otp_order_ids)

    @api.multi
    @api.depends('project_ids')
    def _compute_project_number(self):
        for project in self:
            project.project_count = len(project.project_ids)

    @api.multi
    @api.depends('mrp_ids')
    def _compute_mrp_number(self):
        for mrp in self:
            mrp.mrp_count = len(mrp.mrp_ids)


    @api.model
    def create(self, vals):
        id_so = super(SaleOrder,self).create(vals)
        if 'company_id' in vals:
            name = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sale.order.ext') or _('New')
        else:
            name = self.env['ir.sequence'].next_by_code('sale.order.ext') or _('New')
        self.env['sale.order'].browse(id_so.id).write({'name': name})
        return id_so



