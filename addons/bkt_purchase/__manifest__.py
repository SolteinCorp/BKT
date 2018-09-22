# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'PURCHASE Ext',
    'version': '1.0',
    'category': 'PURCHASE',
    'sequence': 35,
    'summary': 'PURCHASE Ext',
    'description': """
Purchase Access Rights
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['purchase','sale'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/purchase_ext_views.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}
