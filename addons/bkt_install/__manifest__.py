# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'BKT INSTALL',
    'version': '1.0',
    'category': 'INSTALL',
    'sequence': 35,
    'summary': 'INSTALL',
    'description': """
Install for BKT
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['crm','sale_management','sale','purchase','stock','mrp','account_invoicing','project','hr','website','bkt_purchase','bkt_project',
                'bkt_otp','bkt_crm','bkt_account_invoice','bkt_sale_comision','bkt_sales'],
    'data': [ 
            # 'views/crm_ext_views.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}
