# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_contact_bkt = fields.Char(string='Nombre de la persona de contacto')

