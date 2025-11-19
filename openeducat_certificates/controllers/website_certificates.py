# controllers/website_certificates.py
from odoo import http
from odoo.http import request
import re
from werkzeug.exceptions import NotFound

class WebsiteCertificates(http.Controller):

    @http.route("/certificates/verify", type="http", auth="public", website=True)
    def verify_form(self, **kwargs):
        return request.render("openeducat_certificates.verify_form", {})

    @http.route("/certificates/verify/result", type="http", auth="public", methods=["POST"], website=True, csrf=True)
    def verify_result(self, **post):
        nid = (post.get("national_id") or "").strip()
        cert = request.env["op.certificate"].sudo().search([
            ("national_id", "=", nid),
            ("state", "=", "issued")
        ], limit=1)
        tpl = "openeducat_certificates.verify_ok" if cert else "openeducat_certificates.verify_fail"
        return request.render(tpl, {"cert": cert})

    # -------------------------------------------------------
    # Descarga/impresión: redirige a /report/html ... ?print=1
    # -------------------------------------------------------
    @http.route(['/certificates/print/<path:anything>'], type='http', auth='public', website=True)
    def print_certificate(self, anything, **kwargs):
        """
        Acepta:
          - /certificates/print/2
          - /certificates/print/certificado-de-participacion-2
        Extrae el ID y abre el HTML listo para imprimir (texto no se quema).
        """
        m = re.search(r'(\d+)$', (anything or ''))
        if not m:
            raise NotFound()
        cert_id = int(m.group(1))

        Cert = request.env['op.certificate'].sudo()
        cert = Cert.browse(cert_id)
        if not cert.exists():
            raise NotFound()

        # Acción definida como qweb-html
        report_name = 'openeducat_certificates.report_certificate_document'
        url = "/report/html/%s/%s?print=1" % (report_name, cert.id)
        return request.redirect(url)
