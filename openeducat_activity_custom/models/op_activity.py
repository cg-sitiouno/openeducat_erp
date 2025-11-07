from odoo import models, fields

class OpActivity(models.Model):
    # Heredamos del modelo existente de OpenEduCat
    _inherit = 'op.activity' 

    # Definimos un campo de selección para la prioridad
    x_priority = fields.Selection(
        [
            ('0', 'Bajatest'),
            ('1', 'Mediatest'),
            ('2', 'Altatest'),
        ],
        string='Prioridad',
        default='1', # Establecer Media como prioridad por defecto
        required=True,
        help='Nivel de prioridad de esta actividad o tarea.'
    )