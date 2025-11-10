from odoo import http
from odoo.http import request

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
