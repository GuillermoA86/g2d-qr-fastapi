# ==========================================
# Project: Dynamic QR Contact Landing (FastAPI PREMIUM UI)
# Company: G2D Data Science Solutions
# ==========================================

import qrcode

# URL dinámica (local)
url = "http://127.0.0.1:8000/contact"

qr = qrcode.make(url)
qr.save("g2d_dynamic_qr.png")

print("QR dinámico generado: g2d_dynamic_qr.png")

# ==========================================
# FastAPI APP
# ==========================================

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image, ImageDraw, ImageFont
import io

app = FastAPI()

# ---- DATOS ----
COMPANY = "G2D Data Science Solutions"
CCO = "Genaro García"
EMAIL = "g2d.datascience@gmail.com"
PHONE = "+52 722 636 9157"

# ---- IMAGEN DINÁMICA PREMIUM ----
@app.get("/contact-image")
def contact_image():
    img = Image.new("RGB", (1000, 600), color="white")
    draw = ImageDraw.Draw(img)

    # ---- LOGO GRANDE CENTRADO ----
    try:
        logo = Image.open("assets/logo.png")
        logo = logo.resize((820, 620))  # MÁS GRANDE QUE EL TEXTO
        img.paste(logo, ((600 - 320)//2, 20))  # centrado horizontal
    except:
        pass

    # ---- FUENTES ----
    try:
        font_title = ImageFont.truetype("arial.ttf", 44)
        font_sub = ImageFont.truetype("arial.ttf", 30)
        font_text = ImageFont.truetype("arial.ttf", 26)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # ---- TEXTO CENTRADO ----
    def center_text(text, y, font):
        bbox = draw.textbbox((0,0), text, font=font)
        width = bbox[2] - bbox[0]
        x = (1000 - width) // 2
        draw.text((x, y), text, fill="black", font=font)

#    center_text(COMPANY, 360, font_title)
#    center_text(f"CCO: {CCO}", 420, font_sub)
#    center_text(EMAIL, 470, font_text)
#    center_text(PHONE, 510, font_text)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")


# ---- LANDING PREMIUM ----
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
                width: 240px;
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


# ---- VCARD ----
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


