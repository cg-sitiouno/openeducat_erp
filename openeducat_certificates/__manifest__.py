{
    "name": "OpenEduCat Certificates ITSU",
    "version": "18.0.1.0.0",
    "summary": "Certificados públicos por cédula integrados con Admission",
    "author": "ITSU",
    "license": "LGPL-3",
    "depends": ["openeducat_admission", "website"],
    "data": [
        # Seguridad
        "security/ir.model.access.csv",

        # Vistas backend
        "views/certificate_views.xml",
        "views/certificate_template_views.xml",
        "views/certificate_menu.xml",
        "views/admission_register_inherit.xml",
        "views/admission_inherit.xml",

        # Assets para impresión HTML
        "views/assets_cert_print.xml",

        # Reporte: primero template, luego acción
        "report/certificate_qweb.xml",
        "report/certificate_report.xml",

        # Website
        "views/website_verify_templates.xml",
    ],
    "application": False,
    "installable": True,
}
