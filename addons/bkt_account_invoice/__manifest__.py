# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Invoice Ext',
    'version': '1.0',
    'category': 'INVOICE',
    'sequence': 35,
    'summary': 'INVOICE Ext',
    'description': """
INVOICE Access Rights
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['account'],
    'data': [ 
            # 'views/crm_ext_views.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}
