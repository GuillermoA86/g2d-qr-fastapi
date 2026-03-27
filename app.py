# ==========================================
# Project: Dynamic QR Contact Landing (APP-LIKE)
# Company: G2D Data Science Solutions
# ==========================================

import os
import io
import qrcode

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image

# ==========================================
# CONFIG
# ==========================================

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

COMPANY = "G2D Data Science Solutions"
CCO = "Genaro García"
EMAIL = "g2d.datascience@gmail.com"
PHONE = "+52 722 636 9157"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def health():
    return {"status": "ok", "service": COMPANY}


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
# IMAGEN (SOLO LOGO CENTRADO)
# ==========================================

@app.get("/contact-image")
def contact_image():
    img = Image.new("RGB", (800, 400), color="white")

    try:
        logo_path = os.path.join(BASE_DIR, "assets", "Logo.png")
        logo = Image.open(logo_path)

        logo.thumbnail((500, 300))

        x = (800 - logo.width) // 2
        y = (400 - logo.height) // 2

        img.paste(logo, (x, y))
    except Exception as e:
        print("Error loading logo:", e)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")


# ==========================================
# LANDING (APP-LIKE FULLSCREEN)
# ==========================================

@app.get("/contact", response_class=HTMLResponse)
def contact_page():
    html = f"""
    <html>
    <head>
        <title>{COMPANY}</title>

        <!-- MOBILE CRÍTICO -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI';
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                margin: 0;
                padding: 0;
                color: white;

                /* APP-LIKE */
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .card {{
                background: white;
                color: black;
                width: 92%;
                max-width: 420px;
                min-height: 80vh;

                border-radius: 24px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);

                padding: 30px;

                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;

                text-align: center;
            }}

            img {{
                width: 160px;
                margin-bottom: 20px;
            }}

            h2 {{
                margin: 10px 0;
                font-size: 22px;
            }}

            .subtitle {{
                color: #555;
                margin-bottom: 10px;
            }}

            p {{
                margin: 4px 0;
                font-size: 16px;
            }}

            .actions {{
                width: 100%;
                margin-top: 20px;
            }}

            a {{
                display: block;
                margin: 10px 0;
                padding: 14px;
                width: 100%;

                border-radius: 12px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
            }}

            .btn-call {{
                background: #28a745;
                color: white;
            }}

            .btn-mail {{
                background: #007bff;
                color: white;
            }}

            .btn-save {{
                background: #333;
                color: white;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <img src="/contact-image" />

            <h2>{COMPANY}</h2>
            <div class="subtitle">CCO: {CCO}</div>

            <p>{EMAIL}</p>
            <p>{PHONE}</p>

            <div class="actions">
                <a class="btn-call" href="tel:+527226369157">📞 Llamar</a>
                <a class="btn-mail" href="mailto:{EMAIL}">✉️ Email</a>
                <a class="btn-save" href="/vcard">💾 Guardar contacto</a>
            </div>
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