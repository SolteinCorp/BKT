# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    code = fields.Char('Código', index=True, readonly=True)
    sale_number = fields.Integer(compute='_compute_sale_amount_total', string="Número de cotizaciones")
    date_promise = fields.Date(string='Fecha promesa')


    @api.depends('order_ids')
    def _compute_sale_amount_total(self):
        for lead in self:
            total = 0.0
            nbr = 0
            company_currency = lead.company_currency or self.env.user.company_id.currency_id
            for order in lead.order_ids:
                if order.state in ('draft', 'sent', 'sale'):
                    nbr += 1
                if order.state not in ('draft', 'sent', 'cancel'):
                    total += order.currency_id.compute(order.amount_untaxed, company_currency)
            lead.sale_amount_total = total
            lead.sale_number = nbr
            lead.generate_code(nbr)

    @api.multi
    def generate_code(self, number):
        if self.code == False and number == 1:
            for record in self:
                if record.user_id:
                    code = record.env['ir.sequence'].next_by_code('crm.lead.ext') or _('New')
                    name_user = record.user_id.name[0:3]
                    code = code + '/' + name_user
                    record.write({'code': code})
                else:
                    code = record.env['ir.sequence'].next_by_code('crm.lead.ext') or _('New')
                    record.env['crm.lead'].browse(record.id).write({'code': code})

    @api.multi
    def write(self, vals):
        bandera = True
        if vals.get('user_id'):
            if self.user_id == self.env['res.users'].browse(vals.get('user_id')):
                bandera = False
        super(CrmLead, self).write(vals)
        if bandera and vals.get('user_id'):
            if self.sale_number > 0:
                new_code = self.env['res.users'].browse(vals.get('user_id')).name
                code1 = self.env['crm.lead'].browse(self.id).code
                code = code1 + '/' + new_code[0:3]
                self.env['crm.lead'].browse(self.id).write({'code': code})
