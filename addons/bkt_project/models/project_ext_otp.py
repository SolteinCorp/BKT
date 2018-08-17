# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class Project(models.Model):
    _inherit = 'project.project'

    is_installation = fields.Boolean('Es de instalación', help='Marcar si el proyecto es de instalación')


class Task(models.Model):
    _inherit = 'project.task'

    is_installation = fields.Boolean('Es de instalación', help='Marcar si la tarea es de instalación')
