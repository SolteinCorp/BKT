# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleCommission(models.Model):
    _name = "sale.commission"
    _description = "Sale Commissions"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    @api.multi
    @api.depends('sales_order_ids')
    def _get_pay(self):
        total = 0
        for record in self:
            partial_amount = 0
            for sorder in record.sales_order_ids:
                partial_amount += record.clasifi_invoice_by_commision(sorder)
            record.amount_total = partial_amount

    def clasifi_invoice_by_commision(self, order):
        if order.team_id.team_type == 'website':
            partial_amount = order.amount_total
            total = partial_amount * (self.percent_commission_vs / 100)
            return total
        if order.team_id.team_type != 'website':
            partial_amount = order.amount_total
            total = partial_amount * (self.percent_commission_vcn / 100)
            return total

    @api.multi
    @api.depends('employee_id')
    def _get_percent_vs(self):
        self.check_status()
        for comm in self:
            comm.percent_commission_vs = comm.employee_id.percent_commission_vs

    @api.multi
    @api.depends('employee_id')
    def _get_percent_v2(self):
        self.check_status()
        for comm in self:
            comm.percent_commission_v2 = comm.employee_id.percent_commission_v2

    @api.multi
    @api.depends('employee_id')
    def _get_percent_vce(self):
        self.check_status()
        for comm in self:
            comm.percent_commission_vce = comm.employee_id.percent_commission_vce

    @api.multi
    @api.depends('employee_id')
    def _get_percent_vcn(self):
        self.check_status()
        for comm in self:
            comm.percent_commission_vcn = comm.employee_id.percent_commission_vcn

    code = fields.Char(string='Codigo de la comisión', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    name = fields.Char(string='Nombre de la comisión', required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    create_date = fields.Datetime(string='Fecha de creación', index=True, required=True, readonly=True,
                                  help="Fecha en la que se crea la comisión",
                                  states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', string='Empleado', index=True, required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
    commission_type = fields.Selection([
        ('commision', 'Comisión'),
        ('bono', 'Bono')], string='Tipo de comisión', required=True, default='commision', readonly=True,
        states={'draft': [('readonly', False)]})

    percent_commission_vs = fields.Float(string='% Comisión ventas asignadas vía Sistema', compute='_get_percent_vs',
                                         readonly=True, states={'draft': [('readonly', False)]})
    percent_commission_v2 = fields.Float(string='% Comisión a partir de la segunda Venta', compute='_get_percent_v2',
                                         readonly=True, states={'draft': [('readonly', False)]})
    percent_commission_vce = fields.Float(string='% Comisión ventas a cliente existente', compute='_get_percent_vce',
                                          readonly=True, states={'draft': [('readonly', False)]})
    percent_commission_vcn = fields.Float(string='% Comisión ventas a clientes nuevos', compute='_get_percent_vcn',
                                          readonly=True, states={'draft': [('readonly', False)]})

    amount_total = fields.Float(string='Total a pagar', compute='_get_pay', store=True,
                                readonly=True)
    note = fields.Text('Detalle de la comisión')

    sales_order_ids = fields.Many2many('sale.order', required=True, string='Órdenes de ventas', readonly=True,
                                       states={'draft': [('readonly', False)]})

    account_invoice_ids = fields.Many2many('account.invoice', required=True, string='Vía de pago',
                                           domain=[('type', '=', 'in_invoice')],
                                           readonly=True,
                                           states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('validated_admin', 'Validada por administrador'),
        ('validated_employee', 'Validada por el empleado'),
        ('done', 'Pagada'),
    ], string='Estados', readonly=True, copy=False, index=True, default='draft')

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        if not vals.get('sales_order_ids') or not vals.get('account_invoice_ids'):
            raise UserError(
                _('Debe adicionar Órdenes de ventas y Vías de pago'))
        else:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('sale.commissions.seq') or _('New')
            flag = self.validate_amount_invoice(vals)
            if flag:
                result = super(SaleCommission, self).create(vals)
                self.sale_commision_rel(result)
                return result
            else:
                raise UserError(
                    _('La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))

    def sale_commision_rel(self, comm):
        for order in comm.sales_order_ids:
            order.write({'sale_commision_rel': True})

    @api.multi
    def write(self, vals):
        flag_sales = self.validate_sales_order(vals)
        flag_invoices = self.validate_account_invoice(vals)
        if flag_sales and flag_invoices:
            if 'account_invoice_ids' in vals:
                flag_1 = self.validate_amount_invoice(vals)
                if flag_1:
                    super(SaleCommission, self).write(vals)
                    self.sale_commision_rel(self)
                else:
                    raise UserError(
                        _('La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))
            else:
                if 'sales_order_ids' in vals:
                    flag_1 = self.validate_amount_sales(vals)
                    if flag_1:
                        super(SaleCommission, self).write(vals)
                        self.sale_commision_rel(self)
                    else:
                        raise UserError(
                            _(
                                'La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))
                else:
                    super(SaleCommission, self).write(vals)
                    self.sale_commision_rel(self)
        else:
            raise UserError(
                _('Debe adicionar Órdenes de ventas y Vías de pago'))

    @api.multi
    def validate_amount_invoice(self, vals):
        amount = 0
        for fact_id in vals.get('account_invoice_ids'):
            for obj in fact_id[2]:
                amount += self.env['account.invoice'].browse(obj).amount_total
        pay = self.get_pay(vals)
        if amount >= pay:
            return True
        else:
            return False

    @api.multi
    def validate_amount_sales(self, vals):
        amount = 0
        for fact_id in self.account_invoice_ids:
            amount += fact_id.amount_total
        if amount >= self.get_pay(vals):
            return True
        else:
            return False

    @api.multi
    def validate_account_invoice(self, vals):
        if 'account_invoice_ids' in vals:
            for invoices in vals.get('account_invoice_ids'):
                if invoices[2]:
                    return True
            return False
        return True

    @api.multi
    def validate_sales_order(self, vals):
        if 'sales_order_ids' in vals:
            for sales in vals.get('sales_order_ids'):
                if sales[2]:
                    return True
            return False
        return True

    @api.onchange('commission_type', 'employee_id')
    def _onchangeCommisionType(self):
        if self.commission_type == 'commision':
            dom = [('invoice_status', '=', 'invoiced'), ('user_id', '=', self.employee_id.user_id.id),
                   ('invoice_paid_all', '=', True),('sale_commision_rel', '=', False)]
        else:
            dom = [('state', '=', 'sale'), ('user_id', '=', self.employee_id.user_id.id),('sale_commision_rel', '=', False)]
        return {'domain': {'sales_order_ids': dom}}

    @api.multi
    def get_pay(self, vals):
        total = 0.0
        if 'sales_order_ids' in vals:
            for order in vals.get('sales_order_ids'):
                for sorder in order[2]:
                    total += self.clasifi_invoice_by_commision(self.env['sale.order'].browse(sorder))
            return total
        else:
            return self.amount_total

    @api.multi
    def action_validated_admin(self):
        return self.write({'state': 'validated_admin'})

    @api.multi
    def action_validated_employee(self):
        return self.sudo().write({'state': 'validated_employee'})

    @api.multi
    def check_status(self):
        for commision in self:
            flag = True
            if commision.state == 'validated_employee':
                accounts_invoice = commision.account_invoice_ids
                for acc in accounts_invoice:
                    if str(acc.state) == 'paid':
                        flag = False
            if not flag:
                commision.write({'state': 'done'})


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_salesman = fields.Boolean('Es vendedor', help='Marcar si el empleado es vendedor')
    percent_commission_vs = fields.Float(string='% Comisión ventas asignadas vía Sistema')
    percent_commission_v2 = fields.Float(string='% Comisión a partir de la segunda Venta')
    percent_commission_vce = fields.Float(string='% Comisión ventas a cliente existente')
    percent_commission_vcn = fields.Float(string='% Comisión ventas a clientes nuevos')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_commission_id = fields.Many2one('sale.commission', string='Comisiones de venta', index=True)
