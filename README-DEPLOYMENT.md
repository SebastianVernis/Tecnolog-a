# 🚀 Guía de Despliegue - News Generator

## 📋 Opciones de Despliegue

Este proyecto soporta dos arquitecturas de despliegue completas:

### 🎯 Opción 1: Render + Vercel (MVP/Rápido)
**Ideal para**: Desarrollo rápido, MVP, prototipos

**Ventajas:**
- ✅ Setup en < 30 minutos
- ✅ Usa código Python existente sin cambios
- ✅ Free tier funcional
- ✅ Debugging más fácil
- ✅ Deploy automático desde Git

**Stack:**
- Backend: Render Web Service (Flask/Python)
- Frontend: Vercel (React/Vite)
- Sitios: Vercel (múltiples proyectos)
- Storage: AWS S3 / Cloudflare R2

**📖 Ver guía completa**: [docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md](docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md)

---

### ⚡ Opción 2: Cloudflare Workers + Pages (Producción/Escala)
**Ideal para**: Producción, escala global, alta performance

**Ventajas:**
- ✅ Latencia ultra-baja (edge global)
- ✅ No cold start (0ms)
- ✅ Escalabilidad ilimitada
- ✅ Costos muy bajos y predecibles
- ✅ Egress gratis (R2)

**Stack:**
- Backend: Cloudflare Workers (TypeScript)
- Frontend: Cloudflare Pages (React/Vite)
- Sitios: Cloudflare Pages (múltiples proyectos)
- Storage: Cloudflare R2
- Database: Cloudflare D1
- Queue: Cloudflare Queues

**📖 Ver guía completa**: [docs/DEPLOYMENT-GUIDE-CLOUDFLARE.md](docs/DEPLOYMENT-GUIDE-CLOUDFLARE.md)

---

## 📊 Comparativa Detallada

### Costos Mensuales

| Aspecto | Render + Vercel | Cloudflare |
|---------|----------------|------------|
| **Free Tier** | ~$0.12/mes | $0/mes |
| **MVP** | ~$11/mes | ~$6.50/mes |
| **Producción** | ~$65/mes | ~$32/mes |

### Performance

| Métrica | Render + Vercel | Cloudflare |
|---------|----------------|------------|
| **Cold Start** | 1-2s (Render free) | 0ms |
| **Latencia** | 50-200ms | 10-50ms (edge) |
| **Escalabilidad** | Media | Muy Alta |
| **Disponibilidad** | 99.9% | 99.99% |

### Desarrollo

| Aspecto | Render + Vercel | Cloudflare |
|---------|----------------|------------|
| **Setup Time** | 30 min | 2-3 horas |
| **Complejidad** | Baja | Media |
| **Debugging** | Fácil | Moderado |
| **Curva Aprendizaje** | Baja | Media |

---

## 🎯 Recomendaciones

### Usar Render + Vercel si:
- ✅ Necesitas MVP rápido
- ✅ Tienes código Python que no quieres reescribir
- ✅ Priorizas velocidad de desarrollo
- ✅ No necesitas escala masiva inmediata
- ✅ Debugging es prioritario

### Usar Cloudflare si:
- ✅ Necesitas máxima performance
- ✅ Planeas escalar globalmente
- ✅ Quieres costos predecibles y bajos
- ✅ Puedes invertir tiempo en migrar a TypeScript
- ✅ Necesitas latencia ultra-baja

---

## 🚀 Quick Start

### Render + Vercel

```bash
# 1. Push a GitHub
git push origin main

# 2. Conectar Render (backend)
# Dashboard → New → Blueprint → Conectar repo
# render.yaml será detectado automáticamente

# 3. Conectar Vercel (frontend)
# Dashboard → New Project → Import repo
# Configurar: Root = Tecnología/frontend

# 4. Configurar secrets
# Render: BLACKBOX_API_KEY, AWS_*
# Vercel: VITE_API_URL

# ✅ Listo!
```

### Cloudflare Workers + Pages

```bash
# 1. Instalar Wrangler
npm install -g wrangler
wrangler login

# 2. Crear recursos
wrangler r2 bucket create news-generator-sites
wrangler d1 create news-generator-db
wrangler queues create site-generation-jobs

# 3. Configurar wrangler.toml
# Editar con tus IDs de recursos

# 4. Deploy
cd Tecnología
wrangler deploy  # Worker
wrangler pages deploy frontend/dist  # Frontend

# ✅ Listo!
```

---

## 📁 Archivos de Configuración

### Render + Vercel
```
Tecnología/
├── render.yaml              # Config Render (backend)
├── vercel.json              # Config Vercel (frontend)
├── .renderignore            # Ignorar en Render
├── .vercelignore            # Ignorar en Vercel
└── backend/requirements.txt # Dependencias Python
```

### Cloudflare
```
Tecnología/
├── wrangler.toml            # Config Workers
├── .pages.toml              # Config Pages
├── workers/
│   ├── package.json         # Dependencias Workers
│   ├── tsconfig.json        # TypeScript config
│   ├── schema.sql           # D1 schema
│   └── src/index.ts         # Worker code
└── frontend/                # Frontend (igual)
```

---

## 🧪 Testing en Local

### Backend Python (Render)
```bash
cd Tecnología
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python3 backend/app.py
# http://localhost:5000
```

### Backend Workers (Cloudflare)
```bash
cd Tecnología/workers
npm install
npm run dev
# http://localhost:8787
```

### Frontend (Ambos)
```bash
cd Tecnología/frontend
npm install
npm run dev
# http://localhost:5173
```

---

## 📚 Documentación Completa

### Arquitectura y Diseño
- [docs/DEPLOYMENT-ARCHITECTURE.md](docs/DEPLOYMENT-ARCHITECTURE.md) - Comparativa completa de arquitecturas
- [docs/FLUJO-COMPLETO-INTEGRADO.md](docs/FLUJO-COMPLETO-INTEGRADO.md) - Flujo de generación de sitios

### Guías de Despliegue
- [docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md](docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md) - Paso a paso Render + Vercel
- [docs/DEPLOYMENT-GUIDE-CLOUDFLARE.md](docs/DEPLOYMENT-GUIDE-CLOUDFLARE.md) - Paso a paso Cloudflare

### Scripts
- [scripts/master_orchestrator.py](scripts/master_orchestrator.py) - Orquestador principal
- [scripts/deploy_to_vercel.py](scripts/deploy_to_vercel.py) - Deploy automático a Vercel
- [workers/src/index.ts](workers/src/index.ts) - Worker de Cloudflare

---

## 🔧 Troubleshooting

### Problemas Comunes

**Backend no responde**
```bash
# Render: Verificar logs
render logs -f -s news-generator-backend

# Workers: Tail logs
wrangler tail
```

**CORS Errors**
```bash
# Verificar VITE_API_URL en frontend
# Verificar CORS config en backend
```

**Deploy falla**
```bash
# Render: Verificar requirements.txt
# Vercel: Verificar vercel.json
# Workers: Verificar wrangler.toml
```

### Soporte

1. Revisar logs del servicio
2. Consultar documentación específica
3. Verificar variables de entorno
4. Abrir issue en GitHub

---

## 🎓 Siguientes Pasos

### Después del Deployment

1. **Configurar Dominios Personalizados**
   - Render: Custom domain en dashboard
   - Vercel: Custom domain por proyecto
   - Cloudflare: DNS + Pages custom domain

2. **Configurar Monitoreo**
   - Render: Integrar con Datadog/New Relic
   - Cloudflare: Analytics nativo

3. **Optimizar Performance**
   - CDN para imágenes
   - Caché de contenido estático
   - Compresión de assets

4. **Security Hardening**
   - Rate limiting
   - API keys rotation
   - HTTPS enforcement

---

## 📊 Métricas de Éxito

### Objetivos de Performance
- ✅ TTFB < 200ms
- ✅ Uptime > 99.9%
- ✅ Cold start < 2s (Render) o 0s (Cloudflare)
- ✅ Generate site < 10min

### Monitorear
- Request rate
- Error rate
- Response time
- Storage usage
- API costs

---

## 💡 Tips Finales

### Para Empezar Rápido
1. Usa **Render + Vercel**
2. Comienza con free tier
3. Deploy un sitio de prueba
4. Escala cuando sea necesario

### Para Producción
1. Usa **Cloudflare** o **Render Paid**
2. Configura CI/CD
3. Implementa monitoreo
4. Configura backups

### Para Costos Óptimos
1. Cloudflare (más barato a escala)
2. Render Starter (balance precio/features)
3. Vercel Hobby (frontend gratis)
4. R2 (storage sin egress fees)

---

**¿Listo para deployar? Elige tu arquitectura y sigue la guía completa! 🚀**
