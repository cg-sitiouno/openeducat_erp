from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    # Heredamos del modelo de configuración
    _inherit = 'res.config.settings'

    # Campos Fix de Clave API y otros genéricos
    api_key = fields.Char(string="API Key (Fix)")
    vapi_api_key = fields.Char(string="VAPI API Key (Fix)")
    odoo_api_key = fields.Char(string="Odoo API Key (Fix)")
    enable_finetuning_logs = fields.Boolean(string="Enable Finetuning Logs (Fix)")
    
    # Campos Fix de Módulos LMS
    module_openeducat_online_admission = fields.Boolean(string="Online Admission (Fix)")
    module_openeducat_lms_website = fields.Boolean(string="LMS Website (Fix)")
    module_openeducat_lms_interactive_video = fields.Boolean(string="LMS Interactive Video (Fix)")
    module_openeducat_lms_drag_into_text = fields.Boolean(string="LMS Drag Into Text (Fix)")
    module_openeducat_lms_match_following = fields.Boolean(string="LMS Match Following (Fix)")
    module_openeducat_lms_match_images = fields.Boolean(string="LMS Match Images (Fix)")
    module_openeducat_lms_multiple_choice = fields.Boolean(string="LMS Multiple Choice (Fix)")
    module_openeducat_lms_numeric = fields.Boolean(string="LMS Numeric (Fix)")
    module_openeducat_lms_sort_paragraphs = fields.Boolean(string="LMS Sort Paragraphs (Fix)")

    # Campos Fix de Módulos Quiz
    module_openeducat_quiz_drag_into_text = fields.Boolean(string="Quiz Drag Into Text (Fix)")
    module_openeducat_quiz_match_following = fields.Boolean(string="Quiz Match Following (Fix)")
    module_openeducat_quiz_match_images = fields.Boolean(string="Quiz Match Images (Fix)")
    # Nuevo Campo Fix
    module_openeducat_quiz_multiple_choice = fields.Boolean(string="Quiz Multiple Choice (Fix)")
    module_openeducat_quiz_numeric = fields.Boolean(string="Quiz Numeric (Fix)")
    module_openeducat_quiz_sort_paragraphs = fields.Boolean(string="Quiz Sort Paragraphs (Fix)")