# controllers/website_certificates.py
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
import re
import base64


class WebsiteCertificates(http.Controller):

    # -----------------------------
    # FORMULARIO DE BÚSQUEDA
    # -----------------------------
    @http.route("/certificates/verify", type="http", auth="public", website=True)
    def verify_form(self, **kwargs):
        return request.render("openeducat_certificates.verify_form", {})

    # -----------------------------
    # RESULTADO DE BÚSQUEDA
    # -----------------------------
    @http.route(
        "/certificates/verify/result",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def verify_result(self, **post):
        """Buscar certificado por cédula o hash de verificación."""
        nid = (post.get("national_id") or "").strip()
        hash_value = (post.get("verification_hash") or "").strip()
        
        # Buscar por hash si se proporciona, sino por cédula
        if hash_value:
            cert = (
                request.env["op.certificate"]
                .sudo()
                .search(
                    [
                        ("verification_hash", "=", hash_value),
                        ("state", "=", "issued"),
                    ],
                    limit=1,
                )
            )
        elif nid:
            cert = (
                request.env["op.certificate"]
                .sudo()
                .search(
                    [
                        ("national_id", "=", nid),
                        ("state", "=", "issued"),
                    ],
                    limit=1,
                )
            )
        else:
            cert = request.env["op.certificate"].sudo().browse()
        
        tpl = (
            "openeducat_certificates.verify_ok"
            if cert
            else "openeducat_certificates.verify_fail"
        )
        return request.render(tpl, {"cert": cert})

    # -----------------------------
    # VERIFICACIÓN POR QR (HASH)
    # -----------------------------
    @http.route(
        "/certificates/verify/qr/<string:hash_value>",
        type="http",
        auth="public",
        website=True,
    )
    def verify_qr(self, hash_value, **kwargs):
        """
        Verificación directa por hash desde código QR.
        Redirige al template de verificación con el certificado encontrado.
        """
        cert = (
            request.env["op.certificate"]
            .sudo()
            .search(
                [
                    ("verification_hash", "=", hash_value),
                    ("state", "=", "issued"),
                ],
                limit=1,
            )
        )
        tpl = (
            "openeducat_certificates.verify_ok"
            if cert
            else "openeducat_certificates.verify_fail"
        )
        return request.render(tpl, {"cert": cert})


    # -------------------------------------------------
    # IMAGEN DE FONDO DEL TEMPLATE (PÚBLICA)
    # /certificates/template_bg/<id>
    # -------------------------------------------------
    @http.route(
        "/certificates/template_bg/<int:template_id>",
        type="http",
        auth="public",
        website=True,
    )
    def certificate_template_bg(self, template_id, **kwargs):
        """
        Devuelve la imagen de fondo (bg_image) del template de certificado,
        siempre con sudo() para que funcione también como usuario público.
        """
        Template = request.env["op.certificate.template"].sudo()
        template = Template.browse(template_id)
        if not template.exists() or not template.bg_image:
            raise NotFound()

        try:
            # bg_image es binario base64 → lo decodificamos
            image_data = base64.b64decode(template.bg_image)
        except Exception:
            # Si algo va mal con la decodificación, devolvemos 404
            raise NotFound()

        # Si tu campo tiene un mime-type (por ejemplo bg_image_mime), úsalo:
        mime = getattr(template, "bg_image_mime", None) or "image/png"

        headers = [("Content-Type", mime)]
        return request.make_response(image_data, headers=headers)

    # -------------------------------------------
    # (OPCIONAL) RUTA DE IMPRESIÓN / PDF
    # La dejamos comentada por ahora, para no usar PDFs.
    # -------------------------------------------
    # @http.route(['/certificates/print/<path:anything>'], type='http', auth='public', website=True)
    # def print_certificate(self, anything, **kwargs):
    #     # Aquí iría la lógica de PDF si la vuelves a activar más adelante
    #     raise NotFound()
