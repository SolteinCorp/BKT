# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Restricciones de Visibilidad para Ventas y CRM',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 40,
    'summary': 'Restricciones de Visibilidad para Ventas y CRM',
    'description': """
Restricciones de Visibilidad para Ventas y CRM
===============================================
""",
    'website': '',
    'author': 'Soltein SA',
    'depends': ['sale','stock','purchase','crm', 'project','mrp'],
    'data': [
        'views/sales_restrictions_view.xml',
        'views/opportunity_restrictions_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
