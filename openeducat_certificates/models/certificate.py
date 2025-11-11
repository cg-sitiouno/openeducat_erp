# models/certificate.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OpCertificate(models.Model):
    _name = "op.certificate"
    _description = "Certificado emitido"
    _order = "issue_date desc, id desc"

    # Nombre fijo para todos los certificados
    name = fields.Char(
        string="Nombre",
        default="Certificado de participación",
        readonly=True
    )

    student_id = fields.Many2one(
        "op.student",
        string="Estudiante",
        required=True,
        index=True
    )

    admission_id = fields.Many2one(
        "op.admission",
        string="Admisión relacionada"
    )

    register_id = fields.Many2one(
        "op.admission.register",
        string="Admission",
        required=True,
        index=True
    )

    course_id = fields.Many2one(
        "op.course",
        string="Curso"
    )

    template_id = fields.Many2one(
        "op.certificate.template",
        string="Plantilla de certificado",
        required=True
    )

    national_id = fields.Char(
        string="Cédula",
        index=True,
        required=True
    )

    issue_date = fields.Date(
        string="Fecha de emisión",
        required=True,
        default=fields.Date.today,
        help="Fecha en la que se emitió el certificado."
    )

    hours = fields.Float(
        string="Horas académicas"
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("issued", "Emitido"),
            ("revoked", "Revocado"),
        ],
        string="Estado",
        default="draft",
        index=True,
        tracking=True
    )

    _sql_constraints = [
        (
            "unique_cert_per_register_student",
            "unique(student_id, register_id)",
            "Ya existe un certificado para este estudiante en esta cohorte.",
        ),
    ]

    # ---------------------------
    # Validaciones
    # ---------------------------

    @api.constrains("national_id")
    def _check_national_id(self):
        for rec in self:
            if not rec.national_id:
                raise ValidationError("El certificado debe tener cédula (national_id).")

    # ---------------------------
    # Acciones de cambio de estado
    # ---------------------------

    def action_set_draft(self):
        """Volver el certificado a borrador."""
        self.write({"state": "draft"})

    def action_issue(self):
        """Emitir el certificado."""
        self.write({
            "state": "issued",
            "issue_date": fields.Date.today(),
        })

    def action_revoke(self):
        """Revocar el certificado."""
        self.write({"state": "revoked"})

    # ---------------------------
    # Visualización amigable
    # ---------------------------

    def name_get(self):
        """Personaliza cómo se muestra el certificado en los campos Many2one."""
        result = []
        for rec in self:
            display = f"{rec.student_id.name or ''} - {rec.register_id.name or ''}"
            result.append((rec.id, display))
        return result
