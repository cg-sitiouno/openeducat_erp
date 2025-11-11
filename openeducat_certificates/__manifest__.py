{
    "name": "OpenEduCat Certificates ITSU",
    "version": "18.0.1.0.0",
    "summary": "Certificados públicos por cédula integrados con Admission",
    "author": "ITSU",
    "license": "LGPL-3",
    "depends": ["openeducat_admission", "website"],
    "data": [
        "security/ir.model.access.csv",

    # Acciones y vistas de certificados
    "views/certificate_views.xml",

    # Vistas + acción de plantillas
    "views/certificate_template_views.xml",

    # Menús (usan las acciones anteriores)
    "views/certificate_menu.xml",

    # Inherits
    "views/admission_register_inherit.xml",
    "views/admission_inherit.xml",

    # Reportes
    "report/certificate_report.xml",
    "report/certificate_qweb.xml",

    # Website
    "views/website_verify_templates.xml",
    ],
    "application": False,
    "installable": True,
}
