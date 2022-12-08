{
    'name':'estate',
    'application': True,
    'installable':True,
    'depends':['base'],
    'category':'Real Estate/Brokerage',
    'data':[
        './security/estate_security.xml',
        './security/ir.model.access.csv',
        './views/estate_property_views.xml',
        './views/property_type_views.xml',
        './views/property_tag_views.xml',
        './views/property_offer_views.xml',
        './views/estate_menus.xml',
        './views/res_users_inherited_view.xml'
    ]
}