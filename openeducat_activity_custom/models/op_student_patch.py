from odoo import models

class OpStudent(models.Model):
    _inherit = 'op.student'

    # Forzamos el "nombre mostrado" del alumno para que NO dependa de certificate_number
    def name_get(self):
        res = []
        for rec in self:
            # usa el name (heredado de res.partner vía _inherits) o un fallback
            label = rec.name or f'Student #{rec.id}'
            res.append((rec.id, label))
        return res
