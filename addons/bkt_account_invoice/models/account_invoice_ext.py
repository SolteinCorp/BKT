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
