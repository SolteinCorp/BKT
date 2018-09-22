# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    user_id = fields.Many2one('res.users', string='Comercial', track_visibility='onchange',
                              readonly=True, states={'draft': [('readonly', False)],
                                                     'open': [('invisible', True)]},
                              default=lambda self: self.env.user, copy=False)

    team_id = fields.Many2one('crm.team', string='Canal de ventas', default=_get_default_team, oldname='section_id',
                              states={'open': [('invisible', True)]})

    code_invoice_external = fields.Char(string='Nro factura proveedor', readonly=True,
                                        states={'draft': [('readonly', False)]})

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('approved', 'Aprobada'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * El estado 'Aprobada' solo será para facturas de proveedor y es permitido para el rol Aprobacion de compras .\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

    def btn_approved(self):
        self.write({'state':'approved'})
