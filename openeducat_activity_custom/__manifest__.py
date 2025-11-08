{
    'name': 'OpenEduCat Activity Customization',
    'version': '18.0.1.0.0',
    'summary': ' prioridad y otros campos personalizados al módulo de actividad',
    'depends': [
        'openeducat_activity', # DEPENDENCIA CLAVE
    ],
    'data': [
        #'security/ir.model.access.csv',
         'views/op_activity_view_custom.xml',  # form inherit
         'views/op_activity_list_view.xml',    # lista propia (list)
         'views/activity_menu.xml',            # acción + menú (list,form)
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
}