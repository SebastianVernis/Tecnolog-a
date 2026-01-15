# ✅ Checklist de Despliegue - News Generator

**Fecha**: 13 de Enero, 2026  
**Estado**: Listo para Despliegue

---

## 🚀 Pasos Inmediatos (Hacer Ahora)

### 1. Configurar Variables de Entorno (15 min)

#### A. Crear `.env` en la raíz del proyecto

```bash
cd /vercel/sandbox
nano .env
```

Contenido:
```bash
# APIs de Noticias
NEWSAPI_KEY=tu_newsapi_key_aqui
NEWSDATA_KEY=tu_newsdata_key_aqui

# IA para Parafraseo (REQUERIDO)
BLACKBOX_API_KEY=tu_blackbox_api_key_aqui

# Vercel (para deploy automático de sitios)
VERCEL_TOKEN=tu_vercel_token_aqui
VERCEL_TEAM_ID=  # Opcional

# Storage (opcional - usar 'disk' para empezar)
STORAGE_TYPE=disk
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=
AWS_REGION=us-east-1

# Flask
FLASK_ENV=production
```

**Dónde obtener las API Keys**:
- **BLACKBOX_API_KEY**: https://www.blackbox.ai/ → Settings → API Keys
- **NEWSAPI_KEY**: https://newsapi.org/register
- **VERCEL_TOKEN**: https://vercel.com/account/tokens → Create Token

#### B. Crear `frontend/.env`

```bash
cd /vercel/sandbox/frontend
nano .env
```

Contenido:
```bash
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=News Generator Admin
VITE_APP_VERSION=2.0.0
```

**Nota**: Cambiar `VITE_API_URL` a tu URL de Render después del deploy.

---

### 2. Probar en Local (15 min)

#### A. Instalar dependencias Python

```bash
cd /vercel/sandbox
pip3 install -r backend/requirements.txt
```

#### B. Iniciar backend

```bash
cd backend
python3 app.py
```

Verificar: http://localhost:5000/api/health

#### C. Iniciar frontend (en otra terminal)

```bash
cd /vercel/sandbox
npm run dev
```

Verificar: http://localhost:3000

#### D. Generar sitio de prueba

```bash
cd /vercel/sandbox/scripts
python3 generate-sites.py --cantidad 1 --no-interactivo
```

Verificar: `../sites/site1.html` existe

---

### 3. Preparar Repositorio Git (10 min)

#### A. Verificar estado

```bash
cd /vercel/sandbox
git status
```

#### B. Actualizar render.yaml

Editar `/vercel/sandbox/render.yaml`:

```yaml
# Línea 23 - Cambiar por tu repositorio
repo: https://github.com/TU_USUARIO/TU_REPO
branch: main  # o master
```

#### C. Commit y push

```bash
git add .
git commit -m "Preparar para deployment en Render + Vercel"
git push origin main
```

**Si no tienes repositorio en GitHub**:
1. Crear repo en https://github.com/new
2. Seguir instrucciones para push

---

### 4. Deploy Backend en Render (20 min)

#### A. Crear cuenta en Render

1. Ir a https://render.com
2. Sign up con GitHub
3. Autorizar acceso a repositorios

#### B. Crear servicio desde Blueprint

1. Dashboard → **New +** → **Blueprint**
2. Conectar repositorio GitHub
3. Render detectará `render.yaml` automáticamente
4. Click **Apply**

#### C. Configurar Secrets

En Render Dashboard → Service → Environment:

```
BLACKBOX_API_KEY = tu_blackbox_api_key
NEWSAPI_KEY = tu_newsapi_key (opcional)
VERCEL_TOKEN = tu_vercel_token (para auto-deploy)
STORAGE_TYPE = disk
```

Click **Save Changes** → Service se redesplegará automáticamente

#### D. Verificar deployment

Esperar 5-10 minutos para el build.

```bash
# Reemplazar con tu URL de Render
curl https://news-generator-backend.onrender.com/api/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-01-13T...",
  "uptime": "active"
}
```

#### E. Anotar URL

```
Backend URL: https://news-generator-backend.onrender.com
```

---

### 5. Deploy Frontend en Vercel (15 min)

#### A. Actualizar vercel.json

Editar `/vercel/sandbox/vercel.json`:

```json
{
  "env": {
    "VITE_API_URL": "https://TU-SERVICIO.onrender.com",
    ...
  }
}
```

Reemplazar `TU-SERVICIO` con tu URL real de Render.

#### B. Commit cambios

```bash
git add vercel.json
git commit -m "Actualizar API URL para producción"
git push
```

#### C. Deploy en Vercel

**Opción 1: Via Dashboard (Recomendado)**

1. Ir a https://vercel.com/new
2. Import Git Repository → Seleccionar tu repo
3. Configurar:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (dejar por defecto)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. Environment Variables:
   ```
   VITE_API_URL = https://TU-SERVICIO.onrender.com
   VITE_APP_NAME = News Generator Admin
   VITE_APP_VERSION = 2.0.0
   ```

5. Click **Deploy**

**Opción 2: Via CLI**

```bash
npm install -g vercel
vercel login
cd /vercel/sandbox
vercel --prod
```

Seguir prompts y configurar variables de entorno.

#### D. Verificar deployment

Abrir URL de Vercel (ej: https://news-generator-admin.vercel.app)

Verificar:
- ✅ Frontend carga
- ✅ Dashboard muestra estadísticas
- ✅ No hay errores de CORS en consola

#### E. Anotar URL

```
Frontend URL: https://news-generator-admin.vercel.app
```

---

### 6. Probar Sistema Completo (10 min)

#### A. Generar sitio desde Frontend

1. Abrir frontend en navegador
2. Ir a **Create Sites**
3. Configurar:
   - Quantity: 1
   - Verify Domains: No
   - Use Full Flow: Yes
4. Click **Generate**
5. Esperar 5-10 minutos

#### B. Verificar en Dashboard

1. Ir a **Dashboard**
2. Verificar que estadísticas se actualizaron
3. Ir a **Sites List**
4. Verificar que el sitio aparece

#### C. Probar via API (Opcional)

```bash
curl -X POST https://TU-SERVICIO.onrender.com/api/sites/generate \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 1,
    "verifyDomains": false,
    "useFullFlow": true
  }'
```

---

## 📋 Checklist Completo

### Pre-deployment
- [ ] `.env` creado con API keys
- [ ] `frontend/.env` creado
- [ ] Backend funciona en local
- [ ] Frontend funciona en local
- [ ] Generación de sitios funciona en local
- [ ] Código en GitHub

### Backend (Render)
- [ ] Cuenta de Render creada
- [ ] `render.yaml` actualizado con repo correcto
- [ ] Servicio creado desde Blueprint
- [ ] Secrets configurados (BLACKBOX_API_KEY, etc.)
- [ ] Deploy exitoso (sin errores en logs)
- [ ] Health check responde OK
- [ ] URL anotada

### Frontend (Vercel)
- [ ] Cuenta de Vercel creada
- [ ] `vercel.json` actualizado con URL de Render
- [ ] Proyecto creado en Vercel
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso
- [ ] Frontend carga sin errores
- [ ] Se conecta al backend (sin CORS errors)
- [ ] URL anotada

### Testing
- [ ] Generar sitio desde Frontend Admin
- [ ] Verificar que sitio se genera correctamente
- [ ] Verificar estadísticas en Dashboard
- [ ] Probar en móvil (responsive)
- [ ] Verificar logs sin errores críticos

---

## 🎯 URLs de Producción

Completar después del deployment:

```
Backend API:     https://_____________________.onrender.com
Frontend Admin:  https://_____________________.vercel.app
Sitios:          https://_____________________.vercel.app
```

---

## ⚠️ Notas Importantes

### Render Free Tier
- ⏰ **Sleep después de 15 min** de inactividad
- 🐌 **Cold start de 1-2 segundos** al despertar
- 💡 **Solución**: Upgrade a Starter ($7/mes) o usar keep-alive

### Vercel Free Tier
- ✅ **100 GB bandwidth** incluido
- ✅ **Deployments ilimitados**
- ✅ **HTTPS automático**
- ⚠️ **Límite de 100MB** por deployment

### API Keys
- 🔑 **BLACKBOX_API_KEY** es REQUERIDA para parafraseo
- 🔑 **NEWSAPI_KEY** es opcional (hay datos de ejemplo)
- 🔑 **VERCEL_TOKEN** es opcional (para auto-deploy de sitios)

### Storage
- 💾 Por defecto usa **disk** (no persistente en Render free tier)
- 💾 Para persistencia, usar **S3** o **R2** (configurar después)
- 💾 Render Starter incluye persistent disk ($1/GB/mes)

---

## 🆘 Troubleshooting Rápido

### Backend no responde
```bash
# Verificar logs en Render Dashboard
# Verificar que secrets están configurados
# Verificar que build fue exitoso
```

### CORS Error en Frontend
```bash
# Verificar VITE_API_URL en Vercel
# Debe ser: https://TU-SERVICIO.onrender.com (sin /api)
# Verificar CORS en backend/app.py (ya configurado)
```

### Build falla en Vercel
```bash
# Verificar que package.json existe en raíz
# Verificar que vite.config.js está correcto
# Probar build local: npm run build
```

### Generación de sitios falla
```bash
# Verificar BLACKBOX_API_KEY en Render
# Verificar logs en Render Dashboard
# Verificar que archivos de noticias existen en /data/
```

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs**:
   - Render: Dashboard → Service → Logs
   - Vercel: Dashboard → Project → Deployments → Logs

2. **Verificar configuración**:
   - Variables de entorno
   - URLs correctas
   - API keys válidas

3. **Consultar documentación**:
   - [ANALISIS-PROYECTO.md](ANALISIS-PROYECTO.md)
   - [docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md](docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md)

4. **Contactar**:
   - GitHub Issues
   - Render Support
   - Vercel Support

---

## 🎉 ¡Listo!

Después de completar estos pasos, tendrás:

✅ Backend API en producción (Render)  
✅ Frontend Admin en producción (Vercel)  
✅ Sistema de generación funcionando  
✅ Monitoreo básico configurado  

**Tiempo total estimado**: 1.5 - 2 horas

**Próximo paso**: Configurar storage persistente (S3/R2) y auto-deploy de sitios generados.

---

**Última actualización**: 13 de Enero, 2026  
**Versión**: 1.0.0
