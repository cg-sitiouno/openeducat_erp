from odoo import models, fields

class OpActivity(models.Model):
    _inherit = 'op.activity'

    _rec_name = 'x_rec_name'  # nombre seguro

    x_rec_name = fields.Char(
        string='Descripción',
        compute='_compute_x_rec_name',
        store=False,
        index=True,
    )

    x_priority = fields.Selection(
        [('0', 'Bajatest'), ('1', 'Mediatest'), ('2', 'Altatest')],
        string='Prioridad',
        default='1',
        required=True,
        index=True,
        help='Nivel de prioridad de esta actividad o tarea.'
    )

    def _compute_x_rec_name(self):
        for rec in self:
            base = (
                getattr(rec, 'name', False)
                or getattr(rec, 'description', False)
                or getattr(rec, 'title', False)
                or getattr(rec, 'subject', False)
            )
            rec.x_rec_name = base or f'Actividad #{rec.id}'

    def name_get(self):
        return [(rec.id, rec.x_rec_name or f'Actividad #{rec.id}') for rec in self]
