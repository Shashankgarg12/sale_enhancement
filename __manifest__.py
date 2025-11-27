{
    'name': 'Sale Enhancement',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Sale Enhancement for v18',
    'description': """
        Sale Enhancement for v18
    """,
    'author': 'Shashank Garg',
    'depends': ['base','sale_management','portal'],
    'data': [
        'security/sale_group.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/portal_sale_templates.xml',
        'views/website_menus.xml'
    ],
    'installable': True,
    'application': False,
    "pre_init_hook":  "pre_init_check",
}
