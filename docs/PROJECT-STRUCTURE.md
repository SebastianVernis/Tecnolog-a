# Estructura del Proyecto - News Generator

## Organización General

```
Tecnología/
├── frontend/              # Aplicación React (Admin Panel)
├── backend/              # API Flask (Python)
├── workers/              # Cloudflare Workers (futuro)
├── scripts/              # Scripts Python de generación
├── templates/            # Templates HTML/CSS base
├── sites/                # Sitios HTML generados
├── images/               # Imágenes generadas
├── data/                 # Datos y metadatos
├── docs/                 # Documentación
└── public/               # Assets públicos
```

---

## Frontend (React + Vite)

**Ubicación:** `/frontend/`

```
frontend/
├── src/
│   ├── components/       # Componentes reutilizables
│   │   ├── Header.jsx
│   │   └── Header.css
│   ├── pages/           # Páginas principales
│   │   ├── Dashboard.jsx
│   │   ├── CreateSites.jsx
│   │   ├── SitesList.jsx
│   │   └── Settings.jsx
│   ├── services/        # Servicios de API
│   │   └── api.js
│   ├── App.jsx          # Componente raíz
│   ├── main.jsx         # Entry point
│   └── index.css        # Estilos globales
├── index.html
├── vite.config.js
└── package.json
```

**Propósito:**
- Panel de administración para generar y gestionar sitios
- SPA (Single Page Application) con React Router
- Deploy en Vercel

**Comandos:**
```bash
cd frontend
npm install
npm run dev      # Desarrollo
npm run build    # Producción
```

---

## Backend (Flask API)

**Ubicación:** `/backend/`

```
backend/
├── app.py              # API REST principal
└── requirements.txt    # Dependencias Python
```

**Endpoints:**
- `GET /api/health` - Health check
- `GET /api/sites` - Listar sitios
- `GET /api/sites/stats` - Estadísticas
- `POST /api/sites/generate` - Generar sitios
- `DELETE /api/sites/:id` - Eliminar sitio
- `GET /api/settings` - Obtener configuración
- `PUT /api/settings` - Actualizar configuración

**Deploy:** Render.com

**Comandos:**
```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

---

## Scripts de Generación

**Ubicación:** `/scripts/`

### Scripts Principales

| Script | Propósito | Uso |
|--------|-----------|-----|
| `master_orchestrator.py` | Flujo completo de generación | Principal |
| `generate-sites.py` | Generación legacy de sitios | Alternativo |
| `paraphrase.py` | Parafraseo de noticias | Interno |
| `article-expander.py` | Expansión de artículos | Interno |
| `generate-images.py` | Generación de imágenes | Interno |
| `site_name_generator.py` | Nombres de sitios | Interno |
| `domain_verifier.py` | Verificación WHOIS | Interno |
| `layout_generator.py` | Layouts HTML | Interno |
| `layout_css_generator.py` | Estilos CSS | Interno |

### Subdirectorios

```
scripts/
├── api/                 # Integraciones de APIs
│   ├── newsapi.py
│   ├── newsdata.py
│   ├── worldnews.py
│   └── apitube.py
├── utils/              # Utilidades compartidas
│   ├── __init__.py
│   └── utils.py
├── test/               # Tests y validación
│   ├── test_blackbox.py
│   ├── test_integration.py
│   └── test-interactive.sh
└── archive/            # Scripts deprecados
```

**Comandos:**
```bash
# Flujo completo (recomendado)
python3 scripts/master_orchestrator.py --sitios 5

# Flujo legacy
python3 scripts/generate-sites.py --cantidad 5 --generar-metadata
```

---

## Templates

**Ubicación:** `/templates/`

```
templates/
├── base.html           # Template HTML base
├── index.html          # Landing page
└── css/
    ├── template1.css   # Estilo 1
    ├── template2.css   # Estilo 2
    ├── template3.css   # Estilo 3
    ├── template4.css   # Estilo 4
    ├── template5.css   # Estilo 5
    └── responsive-images.css
```

**Propósito:**
- Templates base para generación de sitios
- 5 estilos CSS diferentes
- Sistema de layouts responsive

---

## Datos y Metadatos

**Ubicación:** `/data/`

```
data/
├── noticias_*.json              # Noticias sin procesar
├── noticias_paraphrased_*.json  # Noticias parafraseadas
├── noticias_final_*.json        # Noticias finales
├── sites_metadata/              # Metadatos de sitios
│   └── sites_metadata_*.json
└── archive/                     # Archivos antiguos
```

**Formatos:**
- **Noticias:** JSON con título, contenido, URL, imagen
- **Metadatos:** JSON con nombre, dominio, categorías, colores, fuentes

---

## Sitios Generados

**Ubicación:** `/sites/`

```
sites/
├── site1.html
├── site2.html
├── site3.html
├── ...
└── site100.html
```

**Características:**
- HTML completo standalone
- CSS inline optimizado
- 15 artículos por sitio
- SEO optimizado
- Responsive design

---

## Imágenes

**Ubicación:** `/images/`

```
images/
└── news/
    ├── image_1.jpg
    ├── image_2.jpg
    └── ...
```

**Fuentes:**
- NewsAPI (URLs externas)
- Generación con IA (Blackbox)
- Placeholders responsive

---

## Documentación

**Ubicación:** `/docs/`

### Documentos Principales

| Documento | Propósito |
|-----------|-----------|
| `QUICKSTART.md` | Guía de inicio rápido |
| `ERROR-FIX-20260113.md` | Correcciones recientes |
| `DEPLOYMENT-GUIDE-RENDER-VERCEL.md` | Deploy en producción |
| `FLUJO-COMPLETO-INTEGRADO.md` | Flujo de generación completo |
| `STRUCTURE.md` | Estructura del proyecto |
| `README_FRONTEND.md` | Documentación del frontend |

### Archivo

```
docs/
├── archive/           # Documentos deprecados
│   ├── ARTICLE-EXPANSION.md
│   ├── FLUJO-OPTIMIZADO.md
│   ├── GUIA-INTERACTIVA.md
│   └── ...
└── *.md              # Documentación actual
```

---

## Archivos de Configuración

### Root Level

| Archivo | Propósito |
|---------|-----------|
| `package.json` | Dependencias Node.js (frontend) |
| `requirements.txt` | Dependencias Python (backend) |
| `vercel.json` | Configuración de Vercel |
| `render.yaml` | Configuración de Render |
| `wrangler.toml` | Cloudflare Workers config |
| `.env.example` | Variables de entorno template |
| `.gitignore` | Archivos ignorados por Git |

### Deploy

| Archivo | Servicio | Propósito |
|---------|----------|-----------|
| `vercel.json` | Vercel | Frontend SPA + API proxy |
| `render.yaml` | Render | Backend Flask API |
| `wrangler.toml` | Cloudflare | Workers (futuro) |

---

## Flujo de Datos

```
1. NewsAPI/NewsData
   ↓
2. scripts/api/*.py (fetch)
   ↓
3. data/noticias_*.json
   ↓
4. scripts/paraphrase.py
   ↓
5. data/noticias_paraphrased_*.json
   ↓
6. scripts/article-expander.py
   ↓
7. data/noticias_final_*.json
   ↓
8. scripts/master_orchestrator.py
   ├─> scripts/site_name_generator.py
   ├─> scripts/layout_generator.py
   └─> scripts/layout_css_generator.py
   ↓
9. sites/site*.html (output)
```

---

## Arquitectura de Deploy

```
┌─────────────────────────────────────────────┐
│          Usuario Final                      │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│  Vercel (Frontend - React SPA)             │
│  - Dashboard                                │
│  - Gestión de sitios                        │
│  - Configuración                            │
└──────────────┬──────────────────────────────┘
               │ /api/* proxy
               ↓
┌─────────────────────────────────────────────┐
│  Render (Backend - Flask API)              │
│  - REST endpoints                           │
│  - Ejecución de scripts Python              │
│  - Generación de sitios                     │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│  APIs Externas                              │
│  - NewsAPI                                  │
│  - NewsData                                 │
│  - Blackbox AI                              │
└─────────────────────────────────────────────┘
```

---

## Limpieza Recomendada

### Archivos a Eliminar (Safe)

```bash
# CSV antiguos de noticias
scripts/newsapi_*.csv
scripts/newsapi_*.json

# Archivos temporales
data/archive/*

# Documentación obsoleta
docs/archive/*
```

### Archivos a Mantener

- Todo en `/frontend/src/`
- Todo en `/backend/`
- Scripts principales en `/scripts/`
- Templates en `/templates/`
- Documentación activa en `/docs/`

---

## Variables de Entorno Requeridas

### Backend (Render)

```env
NEWSAPI_KEY=tu_clave_aqui
NEWSDATA_KEY=tu_clave_aqui
BLACKBOX_API_KEY=tu_clave_aqui
PORT=5000
```

### Frontend (Vercel)

```env
VITE_API_URL=https://news-generator-backend-ae62.onrender.com
VITE_APP_NAME=News Generator Admin
VITE_APP_VERSION=2.0.0
```

---

## Comandos Útiles

### Desarrollo Local

```bash
# Backend
cd backend && python3 app.py

# Frontend
cd frontend && npm run dev

# Generar sitios
python3 scripts/master_orchestrator.py --sitios 5
```

### Deploy

```bash
# Frontend (Vercel)
cd frontend && npm run build && vercel deploy

# Backend (Render)
# Git push automático en rama master
```

### Limpieza

```bash
# Limpiar sitios generados
rm sites/*.html

# Limpiar datos antiguos
rm data/archive/*

# Limpiar dependencias Node
rm -rf frontend/node_modules
cd frontend && npm install
```

---

**Última actualización:** 13 de enero de 2026  
**Mantenedor:** Equipo de desarrollo  
**Versión:** 2.0.0
