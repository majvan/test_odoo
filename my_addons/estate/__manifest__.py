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
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',  # Model declaration. It is important that the filename has dots.
        'security/record_rules.xml',  # Model declaration. It is important that the filename has dots.
        'views/estate_property_views.xml',  # Actions and views for properties
        'views/estate_property_type_views.xml',  # Actions and views for property types
        'views/estate_property_tags_views.xml',  # Actions and views for property tags
        'views/estate_property_offer_views.xml',  # Actions and views for property offers
        'views/res_user_views.xml',  # Views for users (extended the inherited view)
        'views/estate_menus.xml',  # A menu items declaration linked to the actions
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,  # Will show in the App window
    'auto_install': False,
}