{
    'name': 'OpenEduCat Activity Customization',
    'version': '18.0.1.0.0',
    'summary': 'Añade prioridad y otros campos personalizados al módulo de actividad.',
    'depends': [
        'openeducat_activity', # DEPENDENCIA CLAVE
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/op_activity_view_custom.xml',
        'views/activity_menu.xml',
        'views/op_activity_tree_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
}