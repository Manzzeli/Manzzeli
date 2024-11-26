# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Sales Report',
    'version': '1.2',
    'category': 'Sales/Sales',
    'summary': 'Sales internal machinery',
    'description': """
Sale Reports custom.
    """,
    'depends': ['sale_management', 'account', 'purchase'],
    'data': [
        # 'report/sale_report.xml',
        'report/sale_report_templates.xml',
        'report/account_move_report.xml',
    ],

    'installable': True,
    'auto_install': False,

}
