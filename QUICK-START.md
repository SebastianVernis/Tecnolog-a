# ⚡ Quick Start - News Generator

**Última actualización**: 13 de Enero, 2026

---

## 🎯 Estado Actual

✅ **Código**: 100% completo y funcional  
⚠️ **Configuración**: Requiere variables de entorno  
❌ **Despliegue**: Pendiente (2-3 horas)

---

## 🚀 Deployment en 3 Pasos

### 1️⃣ Configurar Variables (15 min)

```bash
# Crear .env en raíz
cat > .env << 'EOF'
BLACKBOX_API_KEY=tu_key_aqui
NEWSAPI_KEY=tu_key_aqui
VERCEL_TOKEN=tu_token_aqui
STORAGE_TYPE=disk
FLASK_ENV=production
EOF

# Crear frontend/.env
cat > frontend/.env << 'EOF'
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=News Generator Admin
VITE_APP_VERSION=2.0.0
EOF
```

**Obtener API Keys**:
- BLACKBOX: https://www.blackbox.ai/ → Settings → API Keys
- NEWSAPI: https://newsapi.org/register
- VERCEL: https://vercel.com/account/tokens

### 2️⃣ Deploy Backend en Render (20 min)

1. Actualizar `render.yaml` línea 23:
   ```yaml
   repo: https://github.com/TU_USUARIO/TU_REPO
   ```

2. Push a GitHub:
   ```bash
   git add .
   git commit -m "Preparar deployment"
   git push origin main
   ```

3. Render Dashboard:
   - New → Blueprint
   - Conectar repo
   - Configurar secrets (BLACKBOX_API_KEY, etc.)
   - Deploy

4. Verificar:
   ```bash
   curl https://TU-SERVICIO.onrender.com/api/health
   ```

### 3️⃣ Deploy Frontend en Vercel (15 min)

1. Actualizar `vercel.json`:
   ```json
   "VITE_API_URL": "https://TU-SERVICIO.onrender.com"
   ```

2. Vercel Dashboard:
   - New Project
   - Import repo
   - Framework: Vite
   - Add env vars
   - Deploy

3. Verificar:
   - Abrir URL de Vercel
   - Probar generación de sitio

---

## 📁 Estructura del Proyecto

```
/vercel/sandbox/
├── backend/app.py          ✅ API Flask completa
├── frontend/               ✅ React Admin compilado
├── scripts/                ✅ Generadores completos
│   ├── master_orchestrator.py
│   ├── generate-sites.py
│   └── deploy_to_vercel.py
├── sites/                  ✅ 5 sitios de ejemplo
├── data/                   ✅ Noticias disponibles
├── templates/css/          ✅ Layouts CSS
├── render.yaml             ⚠️ Actualizar repo URL
├── vercel.json             ⚠️ Actualizar API URL
└── .env                    ❌ Crear con API keys
```

---

## 🔑 API Keys Necesarias

| Key | Requerida | Para | Obtener en |
|-----|-----------|------|------------|
| BLACKBOX_API_KEY | ✅ Sí | Parafraseo IA | blackbox.ai |
| NEWSAPI_KEY | ⚠️ Opcional | Noticias | newsapi.org |
| VERCEL_TOKEN | ⚠️ Opcional | Auto-deploy | vercel.com/account/tokens |

---

## 💰 Costos

### Free Tier (MVP)
```
Render Free:    $0/mes (con sleep)
Vercel Hobby:   $0/mes
AWS S3 (5GB):   ~$0.12/mes
─────────────────────────────
TOTAL:          ~$0.12/mes
```

### Producción (Recomendado)
```
Render Starter: $7/mes (sin sleep)
Vercel Hobby:   $0/mes
AWS S3 (50GB):  ~$1.50/mes
─────────────────────────────
TOTAL:          ~$8.50/mes
```

---

## 🧪 Probar en Local

```bash
# Backend
cd backend
pip3 install -r requirements.txt
python3 app.py
# → http://localhost:5000/api/health

# Frontend (otra terminal)
cd /vercel/sandbox
npm run dev
# → http://localhost:3000

# Generar sitio
cd scripts
python3 generate-sites.py --cantidad 1 --no-interactivo
# → ../sites/site1.html
```

---

## 📊 Endpoints API

```
GET  /api/health              Health check
GET  /api/sites               Listar sitios
GET  /api/sites/stats         Estadísticas
POST /api/sites/generate      Generar sitios
GET  /api/sites/<id>/view     Ver sitio HTML
GET  /api/metadata            Listar metadatos
GET  /api/settings            Configuración
PUT  /api/settings            Actualizar config
```

---

## 🎨 Características

### Backend
- ✅ 15 endpoints REST
- ✅ CORS configurado
- ✅ Soporte S3/R2/disk
- ✅ Gunicorn para producción
- ✅ Health checks

### Frontend
- ✅ React 19 + Vite 7
- ✅ 4 páginas (Dashboard, Create, List, Settings)
- ✅ Responsive design
- ✅ Build compilado

### Generación
- ✅ 8 tipos de layouts
- ✅ Parafraseo con IA
- ✅ Metadatos completos
- ✅ Deploy automático a Vercel
- ✅ 1-100 sitios por batch

---

## 🔧 Troubleshooting

### Backend no responde
```bash
# Render free tier duerme después de 15 min
# Solución: Upgrade a Starter ($7/mes)
```

### CORS Error
```bash
# Verificar VITE_API_URL en Vercel
# Debe ser: https://TU-SERVICIO.onrender.com
```

### Build falla
```bash
# Probar local:
npm run build
# Verificar logs en Vercel/Render
```

---

## 📚 Documentación Completa

- **RESUMEN-ESTADO.md** - Resumen ejecutivo
- **ANALISIS-PROYECTO.md** - Análisis completo (40KB)
- **DEPLOYMENT-CHECKLIST.md** - Checklist detallado
- **docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md** - Guía paso a paso

---

## ✅ Checklist Mínimo

- [ ] Crear `.env` con BLACKBOX_API_KEY
- [ ] Actualizar `render.yaml` con repo URL
- [ ] Push a GitHub
- [ ] Deploy en Render
- [ ] Configurar secrets en Render
- [ ] Actualizar `vercel.json` con Render URL
- [ ] Deploy en Vercel
- [ ] Probar generación de sitio

**Tiempo total**: 2-3 horas

---

## 🎯 URLs de Producción

Completar después del deployment:

```
Backend:  https://_____________________.onrender.com
Frontend: https://_____________________.vercel.app
```

---

## 🆘 Ayuda

**Documentos**:
- [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md) - Paso a paso
- [ANALISIS-PROYECTO.md](ANALISIS-PROYECTO.md) - Análisis completo

**Soporte**:
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs

---

**¡Listo para desplegar! 🚀**
