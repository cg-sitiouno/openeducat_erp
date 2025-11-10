from odoo import models, fields

class OpAdmissionRegisterCertExtend(models.Model):
    _inherit = "op.admission.register"

    certificate_template_id = fields.Many2one(
        "op.certificate.template", string="Plantilla de Certificado"
    )

    def action_issue_certificates(self):
        Cert = self.env["op.certificate"]
        for reg in self:
            tpl = reg.certificate_template_id
            if not tpl:
                continue
            for adm in reg.admission_ids.filtered(lambda a: a.certificate_eligible and not a.certificate_id):
                student = adm.student_id
                if not student:
                    continue
                cert = Cert.create({
                    "student_id": student.id,
                    "admission_id": adm.id,
                    "register_id": reg.id,
                    "course_id": adm.course_id.id if adm.course_id else False,
                    "template_id": tpl.id,
                    "hours": tpl.hours,
                    "national_id": getattr(student, "id_number", False),
                    "state": "issued",
                })
                adm.certificate_id = cert.id
        return True