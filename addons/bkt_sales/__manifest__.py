# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales Ordeder Ext',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 35,
    'summary': 'Sales Order Ext',
    'description': """
""",
    'website': '',
    'depends': ['sale', 'sale_management', 'sale_mrp', 'stock', 'sale_stock', 'purchase', 'base'],
    'data': [
        'security/sale_security.xml',
        'data/ir_sequence_data.xml',
        'views/sales_ext_views.xml',
        'report/sales_report_template.xml',
        'report/sales_work_order_report_template.xml',
        'report/sales_offer_report_template.xml',
        'security/ir.model.access.csv',
        'views/partner_ext_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
