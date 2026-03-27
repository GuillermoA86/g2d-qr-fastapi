# 🚀 G2D QR Contact Landing (FastAPI)

Aplicación web construida con **FastAPI** que genera un **QR dinámico** que redirige a una **tarjeta digital de contacto premium**, incluyendo:

* Logo corporativo
* Información de contacto
* Botones de acción (llamada, email)
* Descarga de contacto (vCard)

---

## 📌 Demo

Una vez desplegado, el acceso principal es:

```
https://TU-APP.onrender.com/contact
```

---

## 🧱 Estructura del proyecto

```
g2d-qr-fastapi/
│
├── app.py                # API principal (FastAPI)
├── generate_qr.py        # Generador de QR
├── requirements.txt      # Dependencias
├── Procfile              # Configuración para Render
├── runtime.txt           # Versión de Python
│
└── assets/
    └── logo.png          # Logo de la empresa
```

---

## ⚙️ Instalación local

### 1. Clonar repositorio

```
git clone https://github.com/TU_USUARIO/g2d-qr-fastapi.git
cd g2d-qr-fastapi
```

---

### 2. Crear entorno (opcional pero recomendado)

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

### 4. Ejecutar servidor

```
uvicorn app:app --reload
```

---

### 5. Abrir en navegador

```
http://127.0.0.1:8000/contact
```

---

## 📱 Generación del QR

Actualizar la URL en:

```python
url = "https://TU-APP.onrender.com/contact"
```

Luego ejecutar:

```
python generate_qr.py
```

Esto generará:

```
g2d_dynamic_qr.png
```

---

## 🌐 Endpoints disponibles

| Endpoint         | Descripción                  |
| ---------------- | ---------------------------- |
| `/contact`       | Landing page premium         |
| `/contact-image` | Imagen dinámica del contacto |
| `/vcard`         | Descarga de contacto (.vcf)  |

---

## 🚀 Deploy en Render

### Configuración:

* **Build Command:**

```
pip install -r requirements.txt
```

* **Start Command:**

```
uvicorn app:app --host 0.0.0.0 --port 10000
```

---

## ⚠️ Notas importantes

* En plan gratuito de Render, el servicio puede entrar en modo reposo (cold start).
* Asegúrate de incluir:

  * `assets/logo.png`
  * `requirements.txt`
  * `Procfile`

---

## 📊 Roadmap (mejoras futuras)

* [ ] Tracking de escaneos
* [ ] Base de datos de visitas
* [ ] Dashboard analítico
* [ ] Multi-contactos (modo SaaS)

---

## 👤 Información

**Empresa:** G2D Data Science Solutions
**CCO:** Genaro García

---

## 📄 Licencia

Uso interno / proyecto privado.
