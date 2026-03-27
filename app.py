# ==========================================
# Project: Dynamic QR Contact Landing (FastAPI PREMIUM UI)
# Company: G2D Data Science Solutions
# ==========================================

import os
import io
import qrcode

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image

app = FastAPI()

# ==========================================
# CONFIG
# ==========================================

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ---- DATOS ----
COMPANY = "G2D Data Science Solutions"
CCO = "Genaro García"
EMAIL = "g2d.datascience@gmail.com"
PHONE = "+52 722 636 9157"

# ==========================================
# ROOT (HEALTH CHECK)
# ==========================================

@app.get("/")
def root():
    return {"status": "ok", "service": "G2D QR API"}

# ==========================================
# QR DINÁMICO
# ==========================================

@app.get("/qr")
def generate_qr():
    url = f"{BASE_URL}/contact"

    qr = qrcode.make(url)

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

# ==========================================
# IMAGEN (SOLO LOGO, SIN TEXTO)
# ==========================================

@app.get("/contact-image")
def contact_image():
    img = Image.new("RGB", (1000, 600), color="white")

    # ---- PATH ABSOLUTO ----
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

    try:
        logo = Image.open(logo_path)
        logo = logo.resize((500, 500))

        # centrado perfecto
        x = (1000 - 500) // 2
        y = (600 - 500) // 2

        img.paste(logo, (x, y))
    except Exception as e:
        print("ERROR cargando logo:", e)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

# ==========================================
# LANDING PAGE (INFO LIMPIA)
# ==========================================

@app.get("/contact", response_class=HTMLResponse)
def contact_page():
    html = f"""
    <html>
    <head>
        <title>{COMPANY}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI';
                text-align: center;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: white;
            }}
            .card {{
                background: white;
                color: black;
                padding: 40px;
                margin: 60px auto;
                width: 420px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            img {{
                width: 200px;
                display: block;
                margin: 0 auto 20px auto;
            }}
            h2 {{
                margin: 10px 0;
            }}
            .subtitle {{
                color: #555;
                margin-bottom: 15px;
            }}
            a {{
                display: block;
                margin: 10px auto;
                padding: 10px;
                width: 80%;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
            }}
            .btn-call {{ background: #28a745; color: white; }}
            .btn-mail {{ background: #007bff; color: white; }}
            .btn-save {{ background: #333; color: white; }}
        </style>
    </head>
    <body>
        <div class="card">
            <img src="/contact-image" />
            <h2>{COMPANY}</h2>
            <div class="subtitle">CCO: {CCO}</div>
            <p>{EMAIL}</p>
            <p>{PHONE}</p>
            <a class="btn-call" href="tel:+527226369157">📞 Llamar</a>
            <a class="btn-mail" href="mailto:{EMAIL}">✉️ Email</a>
            <a class="btn-save" href="/vcard">💾 Guardar contacto</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ==========================================
# VCARD
# ==========================================

@app.get("/vcard")
def vcard():
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
FN:{COMPANY}
ORG:{COMPANY}
TITLE:CCO {CCO}
TEL:{PHONE}
EMAIL:{EMAIL}
END:VCARD"""

    return StreamingResponse(
        io.BytesIO(vcard_data.encode()),
        media_type="text/vcard",
        headers={"Content-Disposition": "attachment; filename=contact.vcf"}
    )