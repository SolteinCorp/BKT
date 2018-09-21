# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Project(models.Model):
    _inherit = 'project.project'
    is_installation = fields.Boolean('Es de instalación', help='Marcar si el proyecto es de instalación')
    visibility = fields.Boolean('Visible', default=True)
    sale_order_id2 = fields.Many2one('sale.order', string='Orden de venta asociada a proyectos de instalación',
                                     index=True)


class Task(models.Model):
    _inherit = 'project.task'

    is_installation = fields.Boolean('Es de instalación', help='Marcar si la tarea es de instalación')
    visibility = fields.Boolean('Visible', default=True)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('Por iniciar'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')

    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('En proceso'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')

    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Listo para la próxima etapa'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
