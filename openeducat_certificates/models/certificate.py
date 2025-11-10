from odoo import models, fields, api
from odoo.exceptions import ValidationError

class OpCertificate(models.Model):
    _name = "op.certificate"
    _description = "Certificado emitido"
    _order = "issue_date desc, id desc"

    name = fields.Char(default="Certificado de participación")
    student_id = fields.Many2one("op.student", required=True, index=True)
    admission_id = fields.Many2one("op.admission", required=True, index=True)
    register_id = fields.Many2one("op.admission.register", required=True, index=True)
    course_id = fields.Many2one("op.course")
    template_id = fields.Many2one("op.certificate.template", required=True)
    issue_date = fields.Date(default=fields.Date.today)
    hours = fields.Float()
    national_id = fields.Char(string="Cédula", index=True)
    state = fields.Selection(
        [("draft","Borrador"), ("issued","Emitido"), ("revoked","Revocado")],
        default="issued", index=True
    )

    _sql_constraints = [
        ("unique_cert_per_register_student",
         "unique(student_id, register_id)",
         "Ya existe un certificado para este estudiante en esta cohorte."),
    ]

    @api.constrains("national_id")
    def _check_national_id(self):
        for rec in self:
            if not rec.national_id:
                raise ValidationError("El certificado debe tener cédula (national_id).")
