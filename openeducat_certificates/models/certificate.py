# models/certificate.py
import hashlib
from urllib.parse import quote
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

    # Campos de firma digital
    verification_hash = fields.Char(
        string="Hash de verificación",
        readonly=True,
        index=True,
        copy=False,
        help="Hash SHA-256 único para verificación de autenticidad del certificado."
    )

    qr_code_url = fields.Char(
        string="URL del código QR",
        compute="_compute_qr_code_url",
        help="URL del código QR generado dinámicamente para verificación."
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
    # Firma digital y QR
    # ---------------------------

    def _generate_verification_hash(self):
        """Genera un hash SHA-256 único basado en los datos del certificado."""
        self.ensure_one()
        # Datos que conforman el hash: student_id, national_id, issue_date, template_id
        data_string = f"{self.student_id.id}-{self.national_id}-{self.issue_date}-{self.template_id.id}"
        hash_value = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
        return hash_value

    @api.depends('verification_hash')
    def _compute_qr_code_url(self):
        """Genera la URL del código QR usando QRServer.com API."""
        for rec in self:
            if rec.verification_hash:
                # Obtener la URL base del sistema
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                # URL de verificación pública
                verify_url = f"{base_url}/certificates/verify/qr/{rec.verification_hash}"
                # URL del QR usando QRServer.com API (300x300 px)
                # Más confiable que Google Charts API
                rec.qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={quote(verify_url)}"
            else:
                rec.qr_code_url = False

    # ---------------------------
    # Acciones de cambio de estado
    # ---------------------------

    def action_set_draft(self):
        """Volver el certificado a borrador."""
        self.write({"state": "draft"})

    def action_issue(self):
        """Emitir el certificado y generar hash de verificación."""
        for rec in self:
            # Generar hash solo si no existe
            if not rec.verification_hash:
                hash_value = rec._generate_verification_hash()
                rec.write({
                    "state": "issued",
                    "issue_date": fields.Date.today(),
                    "verification_hash": hash_value,
                })
            else:
                rec.write({
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
