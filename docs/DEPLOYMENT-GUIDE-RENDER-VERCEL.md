# Guía de Despliegue: Render + Vercel

## 📋 Resumen

Esta guía cubre el despliegue completo del sistema usando:
- **Render**: Backend API (Flask/Python)
- **Vercel**: Frontend Admin + Sitios Generados

## 🎯 Arquitectura Final

```
Usuario → Vercel (Admin) → Render (API) → AWS S3/R2 (Storage)
                    ↓
          Vercel (Sitios Generados)
```

## 📦 Requisitos Previos

### 1. Cuentas Necesarias
- [ ] GitHub account
- [ ] Render account (https://render.com)
- [ ] Vercel account (https://vercel.com)
- [ ] AWS account (opcional, para S3)
- [ ] Blackbox AI API key

### 2. Configurar Repositorio Git

```bash
# Si aún no está en Git
cd /home/sebastianvernis/news-prototype/Tecnología
git init
git add .
git commit -m "Initial commit"

# Crear repo en GitHub y pushear
git remote add origin https://github.com/YOUR_USERNAME/news-prototype.git
git push -u origin main
```

---

## 🚀 PASO 1: Desplegar Backend en Render

### A. Conectar Repositorio

1. Ve a https://render.com/dashboard
2. Click en **New +** → **Blueprint**
3. Conecta tu repositorio GitHub
4. Render detectará automáticamente `render.yaml`

### B. Configurar Secrets

En el dashboard de Render, ve a tu servicio y añade:

```bash
# Required
BLACKBOX_API_KEY=tu_blackbox_api_key

# Optional - NewsAPI
NEWSAPI_KEY=tu_newsapi_key

# Optional - Vercel auto-deploy
VERCEL_TOKEN=tu_vercel_token

# Optional - AWS S3
AWS_ACCESS_KEY_ID=tu_aws_key
AWS_SECRET_ACCESS_KEY=tu_aws_secret
AWS_S3_BUCKET=tu-bucket-name
```

**Obtener Vercel Token:**
```bash
# Ir a: https://vercel.com/account/tokens
# Crear nuevo token con scope: Full Access
```

**Obtener Blackbox API Key:**
```bash
# Ir a: https://www.blackbox.ai/
# Crear cuenta → Settings → API Keys
```

### C. Desplegar

1. Click en **Deploy**
2. Render construirá y desplegará automáticamente
3. Anota la URL: `https://news-generator-backend.onrender.com`

### D. Verificar Health Check

```bash
curl https://news-generator-backend.onrender.com/api/health

# Respuesta esperada:
# {"status": "healthy", "version": "2.0.0"}
```

---

## 🎨 PASO 2: Desplegar Frontend en Vercel

### A. Instalar Vercel CLI (Opcional)

```bash
npm install -g vercel
vercel login
```

### B. Opción 1: Deploy via Dashboard

1. Ve a https://vercel.com/new
2. Importa tu repositorio GitHub
3. Configura:
   - **Framework Preset**: Vite
   - **Root Directory**: `Tecnología/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. Añade variables de entorno:
```
VITE_API_URL=https://news-generator-backend.onrender.com
```

5. Click **Deploy**

### B. Opción 2: Deploy via CLI

```bash
cd /home/sebastianvernis/news-prototype/Tecnología

# Primera vez
vercel

# Seguir prompts:
# - Set up and deploy? Yes
# - Which scope? (tu cuenta)
# - Link to existing project? No
# - Project name? news-generator-admin
# - Directory? ./frontend
# - Override settings? No

# Deployments posteriores
vercel --prod
```

### C. Configurar Variables de Entorno

```bash
# Via CLI
vercel env add VITE_API_URL production
# Pegar: https://news-generator-backend.onrender.com

# O via dashboard:
# https://vercel.com/YOUR_USERNAME/news-generator-admin/settings/environment-variables
```

### D. Verificar Deployment

```bash
# Abrir en navegador
open https://news-generator-admin.vercel.app

# O la URL que te dió Vercel
```

---

## 🗄️ PASO 3: Configurar Almacenamiento (Opcional)

### Opción A: Usar Render Disk (Simple, Costoso)

**Ya configurado en render.yaml**
- Pros: Simple, integrado
- Contras: $1/GB/mes, no persistente en free tier

### Opción B: Usar AWS S3 (Recomendado)

#### 1. Crear Bucket S3

```bash
# Via AWS CLI
aws s3 mb s3://news-generator-sites --region us-east-1

# Configurar CORS
aws s3api put-bucket-cors --bucket news-generator-sites --cors-configuration file://s3-cors.json
```

**s3-cors.json:**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

#### 2. Crear IAM User

```bash
# Via AWS Console:
# 1. IAM → Users → Add User
# 2. Nombre: news-generator-s3-user
# 3. Permissions: Attach policy directly
# 4. Policy: AmazonS3FullAccess (o custom policy)
# 5. Crear y guardar Access Key + Secret Key
```

**Custom Policy (Más seguro):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::news-generator-sites",
        "arn:aws:s3:::news-generator-sites/*"
      ]
    }
  ]
}
```

#### 3. Configurar en Render

Añade las secrets en Render dashboard:
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalr...
AWS_S3_BUCKET=news-generator-sites
AWS_REGION=us-east-1
STORAGE_TYPE=s3
```

#### 4. Actualizar Backend

```python
# backend/app.py ya tiene soporte para S3
# Solo necesitas configurar las variables de entorno
```

### Opción C: Usar Cloudflare R2 (Más Barato)

#### 1. Crear Bucket R2

```bash
# Via Cloudflare Dashboard:
# 1. R2 → Create Bucket
# 2. Nombre: news-generator-sites
# 3. Location: Automatic
```

#### 2. Crear API Token

```bash
# Via Cloudflare Dashboard:
# 1. R2 → Manage R2 API Tokens
# 2. Create API Token
# 3. Permissions: Object Read & Write
# 4. Guardar Access Key ID + Secret Access Key
```

#### 3. Configurar en Render

```
AWS_ACCESS_KEY_ID=<R2_ACCESS_KEY>
AWS_SECRET_ACCESS_KEY=<R2_SECRET_KEY>
AWS_S3_BUCKET=news-generator-sites
AWS_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
STORAGE_TYPE=r2
```

---

## 🌐 PASO 4: Deploy Automático de Sitios Generados

### A. Obtener Vercel Token

```bash
# Via Vercel Dashboard:
# https://vercel.com/account/tokens
# Crear token → Full Access
```

### B. Configurar en Render

```bash
VERCEL_TOKEN=tu_vercel_token_aqui
VERCEL_TEAM_ID=tu_team_id  # Opcional, si usas Vercel Team
```

### C. Usar Deploy Script

```python
# scripts/deploy_to_vercel.py ya está configurado
# Se usa automáticamente desde master_orchestrator.py

# O manual:
python3 scripts/deploy_to_vercel.py generated_sites/site_1 --name mi-sitio-noticias
```

### D. Integrar en Master Orchestrator

```python
# Ya integrado en master_orchestrator.py
# Automáticamente deploya cada sitio a Vercel después de generarlo
```

---

## 🧪 PASO 5: Probar el Sistema Completo

### A. Generar Sitio desde Frontend

```bash
# 1. Abrir frontend
open https://news-generator-admin.vercel.app

# 2. Click en "Generate Sites"
# 3. Configurar:
#    - Quantity: 1
#    - Verify Domains: No
#    - Use Full Flow: Yes
# 4. Click "Generate"
# 5. Esperar ~5-10 minutos
```

### B. Generar Sitio via API

```bash
curl -X POST https://news-generator-backend.onrender.com/api/sites/generate \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 1,
    "verifyDomains": false,
    "useFullFlow": true
  }'

# Respuesta:
# {
#   "success": true,
#   "sitesGenerated": 1,
#   "executionTime": "300s",
#   "output": "..."
# }
```

### C. Generar Sitio via CLI (Directo en Render)

```bash
# Conectar a Render Shell
# Dashboard → Service → Shell

cd /opt/render/project/src/scripts
python3 master_orchestrator.py --sitios 1
```

---

## 📊 PASO 6: Monitoreo y Logs

### A. Ver Logs en Render

```bash
# Via Dashboard
# Service → Logs (live tail)

# Via CLI
render logs -f -s news-generator-backend
```

### B. Ver Logs en Vercel

```bash
# Via Dashboard
# Project → Deployments → [deployment] → Function Logs

# Via CLI
vercel logs news-generator-admin
```

### C. Health Checks

```bash
# Backend
curl https://news-generator-backend.onrender.com/api/health

# Frontend
curl https://news-generator-admin.vercel.app

# Sitio generado
curl https://mi-sitio-noticias.vercel.app
```

---

## 🔧 Troubleshooting

### Backend no responde (Render)

**Problema**: Cold start en free tier
```bash
# Solución: Upgrade a Starter plan ($7/mes)
# O hacer warm-up request cada 10 minutos
```

**Problema**: Error de módulos
```bash
# Verificar requirements.txt
# Rebuild servicio en Render
```

### Frontend no se conecta al Backend

**Problema**: CORS error
```bash
# Verificar CORS en backend/app.py
# Verificar VITE_API_URL en Vercel
```

**Problema**: URL incorrecta
```bash
# Verificar variable de entorno
vercel env ls
vercel env pull
```

### Deployment de sitio falla

**Problema**: Vercel token inválido
```bash
# Regenerar token en Vercel dashboard
# Actualizar en Render secrets
```

**Problema**: Archivos muy grandes
```bash
# Vercel limite: 100MB por deployment
# Optimizar imágenes
# Usar CDN externo para imágenes grandes
```

### Almacenamiento lleno (Render Disk)

```bash
# Opción 1: Limpiar archivos viejos
rm -rf /opt/render/project/src/generated_sites/old_*

# Opción 2: Migrar a S3/R2
# Configurar storage type en environment variables
```

---

## 💰 Costos Estimados

### Setup Mínimo (Free Tier)
```
Render Web Service (Free):        $0/mes (con sleep)
Vercel (Hobby):                    $0/mes
AWS S3 (5GB):                      ~$0.12/mes
TOTAL:                             ~$0.12/mes
```

### Setup Recomendado (Producción)
```
Render Web Service (Starter):     $7/mes
Render Disk (10GB):                $1/mes
Vercel (Hobby):                    $0/mes
AWS S3 (50GB + requests):          ~$1.50/mes
Blackbox API:                      Variable (por uso)
TOTAL:                             ~$9.50/mes + API costs
```

### Setup Profesional
```
Render Web Service (Standard):     $25/mes
Render Disk (50GB):                $5/mes
Vercel Pro:                        $20/mes
AWS S3 (200GB):                    ~$5/mes
CloudFront CDN:                    ~$10/mes
TOTAL:                             ~$65/mes + API costs
```

---

## ✅ Checklist de Deployment

### Pre-deployment
- [ ] Código en GitHub
- [ ] `.env` con todas las keys
- [ ] `requirements.txt` actualizado
- [ ] `package.json` actualizado
- [ ] Tests pasando localmente

### Backend (Render)
- [ ] Servicio creado
- [ ] Secrets configurados
- [ ] Deploy exitoso
- [ ] Health check OK
- [ ] Logs sin errores

### Frontend (Vercel)
- [ ] Proyecto creado
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso
- [ ] Se conecta al backend
- [ ] UI funcional

### Storage
- [ ] Bucket creado (S3/R2)
- [ ] Credentials configurados
- [ ] Permisos correctos
- [ ] Upload/download funcionando

### Auto-deploy
- [ ] Vercel token configurado
- [ ] Script de deploy probado
- [ ] Sitio de prueba deployado
- [ ] URL pública accesible

---

## 🔄 CI/CD Automático

### GitHub Actions (Opcional)

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Trigger Render Deploy
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
  
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --token ${{ secrets.VERCEL_TOKEN }} --prod
```

---

## 📚 Recursos Adicionales

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **AWS S3 Docs**: https://docs.aws.amazon.com/s3/
- **Cloudflare R2 Docs**: https://developers.cloudflare.com/r2/

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisar logs en Render/Vercel
2. Verificar variables de entorno
3. Consultar troubleshooting section
4. Abrir issue en GitHub

**¡Deployment completado! 🎉**
