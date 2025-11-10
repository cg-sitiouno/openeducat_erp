from odoo import models, fields

class OpCertificateTemplate(models.Model):
    _name = "op.certificate.template"
    _description = "Plantilla de Certificado"
    _rec_name = "name"

    name = fields.Char("Nombre", required=True)
    course_id = fields.Many2one("op.course", string="Curso (opcional)")
    hours = fields.Float(string="Horas académicas")
    background_image = fields.Binary(string="Fondo del certificado")
    signer_name = fields.Char(string="Firmante")
    signer_role = fields.Char(string="Cargo del firmante")
    signer_signature = fields.Binary(string="Firma (opcional)")
