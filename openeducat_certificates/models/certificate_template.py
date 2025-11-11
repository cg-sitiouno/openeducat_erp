# models/certificate_template.py
from odoo import models, fields

class OpCertificateTemplate(models.Model):
    _name = "op.certificate.template"
    _description = "Plantilla de certificado"

    name = fields.Char(required=True, translate=True)
    course_id = fields.Many2one("op.course", string="Curso (por defecto)")
    hours = fields.Float(string="Horas (por defecto)", default=0.0)
    # Imagen de fondo del certificado (se usará en web y PDF)
    bg_image = fields.Binary(string="Fondo del certificado", attachment=True)

    def action_open_bg(self):
        """Abrir la imagen de fondo en una pestaña nueva (si existe)."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/image/op.certificate.template/{self.id}/bg_image",
            "target": "new",
        }
