# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_ids = fields.One2many('project.project', 'sale_order_id', string='Proyectos')
    project_count = fields.Integer(compute='_compute_project_number', string='Proyectos')

    project_instalation_ids = fields.One2many('project.project', 'sale_order_id2', string='Proyectos instalación')
    project_instalation_count = fields.Integer(compute='_compute_project_instalation_number',
                                               string='Proyectos instalación')

    mrp_ids = fields.One2many('mrp.production', 'sale_order_id', string='Producciones')
    mrp_count = fields.Integer(compute='_compute_mrp_number', string='Producciones')

    otp_order_ids = fields.One2many('stock.picking', 'sale_order_id', string='Transportaciones')
    otp_count = fields.Integer(compute='_compute_otp_number', string='Transportaciones')

    purchase_ids = fields.One2many('purchase.order', 'sale_order_id', string='Compras')
    purchase_count = fields.Integer(compute='_compute_purchase_number', string='Compras')

    sale_commission_id = fields.Many2one('sale.commission', string='Comisiones de venta', index=True)

    state = fields.Selection([
        ('draft', 'Cotización'),
        ('sent', 'Cotización Enviada'),
        ('holden', 'Esperando anticipo'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    invoice_paid_all = fields.Boolean('facturas pagada ?', compute='_check_invoice_paid')
    oport_code = fields.Integer('generado codigo ?')
    sale_commision_rel = fields.Boolean('commision')
    date_promise_oportunity = fields.Date(string='Fecha promesa de la oportunidad', readonly=True)
    code_oportunity = fields.Char('Código de la oportunidad', store=True, readonly=True, related='opportunity_id.code')

    date_promise = fields.Date(string='Fecha promesa',
                               states={'draft': [('invisible', True)],
                                       'sent': [('invisible', True)],
                                       'holden': [('invisible', False)],
                                       'sale': [('invisible', False)],
                                       'done': [('invisible', True)]})

    advance_amount = fields.Float(string='Monto de anticipo', default=0.00,
                                  states={'draft': [('invisible', True)],
                                          'sent': [('invisible', True)],
                                          'holden': [('invisible', False)],
                                          'sale': [('invisible', False)],
                                          'done': [('invisible', True)]})

    contact_delivery_id = fields.Many2one('res.partner', string='Contacto de entrega', readonly=True,
                                          states={'draft': [('readonly', False)],
                                                  'sent': [('readonly', False)],
                                                  'holden': [('readonly', False)]})
    home_delivery = fields.Char(string='Domicilio de entrega', readonly=True,
                                states={'draft': [('readonly', False)],
                                        'sent': [('readonly', False)],
                                        'holden': [('readonly', False)]})
    terms_delivery = fields.Text(string='Cond. de entrega', readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'sent': [('readonly', False)],
                                         'holden': [('readonly', False)]})

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)],
                                         'done': [('readonly', True), ('invisible', False)]}, copy=True,
                                 auto_join=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='onchange', states={'done': [('invisible', True)]})

    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 states={'done': [('invisible', True)]})
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always', states={'done': [('invisible', True)]})

    modify_sale = fields.Boolean(string='Enable Sales ?', compute='_set_access_for_sale')

    @api.multi
    def _check_invoice_paid(self):
        for record in self:
            result = 0
            for inv in record.invoice_ids:
                if inv.state == 'paid':
                    result = result + 1
            if result != 0 and result == len(record.invoice_ids):
                record.invoice_paid_all=True
            else:
                record.invoice_paid_all = False

    @api.one
    def _set_access_for_sale(self):
        if self.env.user.has_group('sales_team.group_sale_manager'):
            self.modify_sale = False
        else:
            self.modify_sale = True

    @api.multi
    @api.depends('purchase_ids')
    def _compute_purchase_number(self):
        for record in self:
            record.purchase_count = len(record.purchase_ids)

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
    @api.depends('project_ids')
    def _compute_project_instalation_number(self):
        for project in self:
            project.project_instalation_count = len(project.project_instalation_ids)

    @api.multi
    @api.depends('mrp_ids')
    def _compute_mrp_number(self):
        for mrp in self:
            mrp.mrp_count = len(mrp.mrp_ids)

    @api.model
    def create(self, vals):
        if 'order_line' in vals:
            for line in vals.get('order_line', False):
                rec = line[2]
                if self.env.user.has_group('sales_team.group_sale_manager'):
                    if rec and rec.get('discount', False) and rec['discount'] > 7:
                        raise UserError('El Responsable de Ventas solo puede especificar descuentos de hasta 7%.')
                else:
                    if rec and rec.get('discount', False) and rec['discount'] > 5:
                        raise UserError('El Usuario de Ventas solo puede especificar descuentos de hasta 5%.')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id',
                                                   partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result

    @api.multi
    def action_confirm(self):
        for record in self:
            super(SaleOrder, record).action_confirm()
            name = record.env['ir.sequence'].next_by_code('sale.order.ext') or _('New')
            record.name = name
            record.cancel_opportunity_rel()
            record.move_stage_oportunity()
            return True

    @api.multi
    def cancel_opportunity_rel(self):
        for record in self:
            if record.opportunity_id:
                oport = record.opportunity_id
                obs = record.search([('opportunity_id', '=', oport.id)])
                if len(obs) > 0:
                    for sales in obs:
                        if sales.id != record.id:
                            sales.write({'state': 'cancel'})

    @api.multi
    def move_stage_oportunity(self):
        for record in self:
            if record.opportunity_id:
                oport = record.opportunity_id
                stages = record.env['crm.stage'].search([])
                for sta in stages:
                    if sta.probability == 100:
                        oport.write({'stage_id': sta.id})

    @api.multi
    def action_hold(self):
        for record in self:
            return record.write({'state': 'holden'})

    @api.multi
    def write(self, vals):
        if 'order_line' in vals:
            for line in vals.get('order_line', False):
                rec = line[2]
                if self.env.user.has_group('sales_team.group_sale_manager'):
                    if rec and rec.get('discount', False) and rec['discount'] > 7:
                        raise UserError('El Responsable de Ventas solo puede especificar descuentos de hasta 7%.')
                else:
                    if rec and rec.get('discount', False) and rec['discount'] > 5:
                        raise UserError('El Usuario de Ventas solo puede especificar descuentos de hasta 5%.')
        return super(SaleOrder, self).write(vals)

    @api.multi
    def action_print_saleorder(self):
        return self.env.ref('bkt_sales.sales_work_order_report').report_action(self)

class Partner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Persona física'), ('company', 'Persona moral')],
                                    compute='_compute_company_type', inverse='_write_company_type')

    vat = fields.Char(string='TIN', required=True, help="Tax Identification Number. "
                                                        "Fill it if the company is subjected to taxes. "
                                                        "Used by the some of the legal statements.")
    _sql_constraints = [
        ('vat_uniq', 'unique (name)', "El campo RFC no debe repetirse !")
    ]


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    def _set_modify_tree(self):
        if self.order_id.state == 'done':
            self.modify_tree = True
        else:
            self.modify_tree = False

    modify_tree = fields.Boolean(string='Enable tree ugly ?', compute='_set_modify_tree')
