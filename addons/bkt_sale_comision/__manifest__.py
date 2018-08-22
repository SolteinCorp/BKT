# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales Commissions',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 35,
    'summary': 'Sales Commissions',
    'description': """
Sales Access Rights
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    'website': 'https://www.odoo.com/page/accounting',
    'depends': ['sale','bkt_sales','hr','account','sales_team'],
    'data': [ 
            'data/ir_sequence_data.xml',
            'views/sales_commission_views.xml',
            'security/ir.model.access.csv',
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}
