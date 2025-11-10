from odoo import models, fields

class OpAdmissionCertExtend(models.Model):
    _inherit = "op.admission"

    certificate_eligible = fields.Boolean(string="Apto p/ Certificado", default=False)
    certificate_id = fields.Many2one("op.certificate", string="Certificado", readonly=True)
