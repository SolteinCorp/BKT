# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleCommission(models.Model):
    _name = "sale.commission"
    _description = "Sale Commissions"
    _inherit = ['mail.thread']
    _order = 'create_date desc, id desc'

    @api.multi
    @api.depends('sales_order_ids')
    def _get_pay(self):
        total = 0
        for order in self:
            partial_amount = 0
            for sorder in order.sales_order_ids:
                partial_amount += sorder.amount_total
            total += partial_amount * (order.percent_commission / 100)
            order.amount_total = total

    @api.multi
    @api.depends('employee_id')
    def _get_percent(self):
        self.check_status()
        for comm in self:
            comm.percent_commission = comm.employee_id.percent_commission

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

    percent_commission = fields.Float(string='% de comisión', compute='_get_percent',
                                      readonly=True)
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
                # for fact_id in vals.get('account_invoice_ids'):
                #     for obj in fact_id[2]:
                #         self.env['account.invoice'].browse(obj).write({'sale_commission_id', result.id})
                return result
            else:
                raise UserError(
                    _('La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))

    @api.multi
    def write(self, vals):
        flag_sales = self.validate_sales_order(vals)
        flag_invoices = self.validate_account_invoice(vals)
        if flag_sales and flag_invoices:
            if 'account_invoice_ids' in vals:
                flag_1 = self.validate_amount_invoice(vals)
                if flag_1:
                    super(SaleCommission, self).write(vals)
                else:
                    raise UserError(
                        _('La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))
            else:
                if 'sales_order_ids' in vals:
                    flag_1 = self.validate_amount_sales(vals)
                    if flag_1:
                        super(SaleCommission, self).write(vals)
                    else:
                        raise UserError(
                            _(
                                'La suma del monto de las vias de pago debe ser mayor o igual que el monto total a pagar'))
                else:
                    super(SaleCommission, self).write(vals)
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

    @api.onchange('commission_type')
    def _onchangeCommisionType(self):
        if self.commission_type == 'commision':
            dom = [('invoice_status', '=', 'invoiced')]
        else:
            dom = [('state', '=', 'sale')]
        return {'domain': {'sales_order_ids': dom}}

    @api.multi
    def get_pay(self, vals):
        total = 0.0
        if 'sales_order_ids' in vals:
            for order in vals.get('sales_order_ids'):
                partial_amount = 0.0
                for sorder in order[2]:
                    partial_amount += self.env['sale.order'].browse(sorder).amount_total
                if 'employee_id' in vals:
                    percent = self.env['hr.employee'].browse(vals.get('employee_id')).percent_commission
                else:
                    percent = self.employee_id.percent_commission
                total += partial_amount * (percent / 100)
            return total
        else:
            return self.amount_total

    @api.multi
    def action_validated_admin(self):
        return self.write({'state': 'validated_admin'})

    @api.multi
    def action_validated_employee(self):
        return self.write({'state': 'validated_employee'})

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
    percent_commission = fields.Float(string='% de comisión')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_commission_id = fields.Many2one('sale.commission', string='Comisiones de venta', index=True)
