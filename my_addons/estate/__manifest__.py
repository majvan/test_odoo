# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real estate',
    'version': '1.0',
    'author': 'majvan',
    'license': 'OPL-1',
    'category': 'Sales/CRM',
#    'sequence': 15,
    'summary': 'Manages real estates market',
    'description': "",
    'depends': [
        'base',
        'base_setup',
    ],
    'data': [
        # 'security/crm_security.xml',
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,  # Will show in the App window
    'auto_install': False,
}