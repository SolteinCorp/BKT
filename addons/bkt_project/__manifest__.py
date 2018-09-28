# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'BKT PROJECT',
    'version': '1.0',
    'category': 'PROJECT',
    'sequence': 35,
    'summary': 'Extension BKT de Proyectos',
    'description': """
Project Access Rights
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    'website': 'https://www.odoo.com/page/accounting',
    'depends': ['project','sale'],
    'data': [ 
            'views/project_otp_ext_views.xml',
            'report/project_report_template.xml',
            'security/ir.model.access.csv'
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}
