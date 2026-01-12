# Guía de Despliegue: Cloudflare Workers + Pages

## 📋 Resumen

Esta guía cubre el despliegue completo usando stack 100% Cloudflare:
- **Cloudflare Workers**: Backend API (Edge Functions)
- **Cloudflare Pages**: Frontend Admin + Sitios Generados
- **Cloudflare R2**: Almacenamiento de sitios e imágenes
- **Cloudflare D1**: Base de datos SQLite serverless
- **Cloudflare Queues**: Procesamiento asíncrono

## 🎯 Arquitectura

```
Usuario → Pages (Admin) → Workers API → Queue → Worker Consumer
                                ↓
                          ┌─────┴──────┐
                          │            │
                        R2 (Files)   D1 (DB)
                          │
                          ↓
                    Pages (Sitios)
```

## 💰 Costos Estimados

### Free Tier (Desarrollo)
```
Workers (100k requests/día):       $0/mes
Pages (unlimited):                 $0/mes
R2 (10GB):                         $0/mes
D1 (5GB):                          $0/mes
Queues (1M messages):              $0/mes
TOTAL:                             $0/mes
```

### Paid Tier (Producción)
```
Workers Paid ($5 + usage):         ~$5-10/mes
Pages Pro:                         $20/mes (opcional)
R2 (100GB):                        $1.50/mes
D1 (free tier suficiente):         $0/mes
Queues (10M messages):             $0.50/mes
TOTAL:                             ~$7-32/mes
```

## 📦 Requisitos Previos

### 1. Instalaciones

```bash
# Node.js 18+
node --version

# Wrangler CLI
npm install -g wrangler

# Login a Cloudflare
wrangler login
```

### 2. Cuentas y Tokens

- [ ] Cuenta Cloudflare (con método de pago para Workers Paid)
- [ ] Repositorio GitHub
- [ ] Blackbox AI API key

---

## 🚀 PASO 1: Configurar Recursos de Cloudflare

### A. Crear R2 Buckets

```bash
# Bucket para sitios generados
wrangler r2 bucket create news-generator-sites

# Bucket para imágenes
wrangler r2 bucket create news-generator-images

# Buckets de desarrollo
wrangler r2 bucket create news-generator-sites-dev
wrangler r2 bucket create news-generator-images-dev
```

### B. Crear Base de Datos D1

```bash
# Crear DB
wrangler d1 create news-generator-db

# Output mostrará:
# database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# Copiar este ID a wrangler.toml

# Ejecutar schema
wrangler d1 execute news-generator-db --file=./workers/schema.sql --remote
```

### C. Crear KV Namespace (Caché)

```bash
# Producción
wrangler kv:namespace create "CACHE"
# Output: id = "xxxxxxxx..."

# Preview
wrangler kv:namespace create "CACHE" --preview
# Output: preview_id = "yyyyyyyy..."

# Copiar IDs a wrangler.toml
```

### D. Crear Queue

```bash
# Queue para procesamiento de sitios
wrangler queues create site-generation-jobs

# Dead letter queue
wrangler queues create site-generation-dlq
```

### E. Configurar Secrets

```bash
# Blackbox API Key
wrangler secret put BLACKBOX_API_KEY
# Pegar tu API key cuando lo pida

# NewsAPI Key
wrangler secret put NEWSAPI_KEY

# Cloudflare API Token (para Pages deploy)
wrangler secret put CLOUDFLARE_API_TOKEN

# Cloudflare Account ID
wrangler secret put CLOUDFLARE_ACCOUNT_ID
```

---

## 🔧 PASO 2: Configurar wrangler.toml

Editar `/Tecnología/wrangler.toml`:

```toml
name = "news-generator-api"
main = "workers/src/index.ts"
compatibility_date = "2024-01-01"

# Reemplazar con tus valores
account_id = "tu_account_id"  # Obtener de dashboard

[[r2_buckets]]
binding = "SITES_BUCKET"
bucket_name = "news-generator-sites"
preview_bucket_name = "news-generator-sites-dev"

[[r2_buckets]]
binding = "IMAGES_BUCKET"
bucket_name = "news-generator-images"
preview_bucket_name = "news-generator-images-dev"

[[d1_databases]]
binding = "DB"
database_name = "news-generator-db"
database_id = "tu_database_id"  # Del paso anterior

[[kv_namespaces]]
binding = "CACHE"
id = "tu_kv_id"
preview_id = "tu_preview_kv_id"
```

---

## 💻 PASO 3: Desarrollar y Probar Worker

### A. Instalar Dependencias

```bash
cd /home/sebastianvernis/news-prototype/Tecnología/workers
npm install
```

### B. Desarrollo Local

```bash
# Iniciar dev server
npm run dev

# El worker estará en http://localhost:8787
```

### C. Probar Endpoints

```bash
# Health check
curl http://localhost:8787/api/health

# Get sites
curl http://localhost:8787/api/sites

# Generate site (queue)
curl -X POST http://localhost:8787/api/sites/generate \
  -H "Content-Type: application/json" \
  -d '{"quantity": 1, "verifyDomains": false}'

# Response:
# {"success":true,"jobId":"xxx","status":"queued"}

# Check job status
curl http://localhost:8787/api/jobs/xxx
```

---

## 🌐 PASO 4: Desplegar Workers

### A. Deploy a Producción

```bash
cd /home/sebastianvernis/news-prototype/Tecnología

# Deploy worker
wrangler deploy

# Output:
# Published news-generator-api (X.XX sec)
#   https://news-generator-api.your-subdomain.workers.dev
```

### B. Deploy a Staging

```bash
wrangler deploy --env staging

# Output:
# Published news-generator-api-staging
#   https://news-generator-api-staging.your-subdomain.workers.dev
```

### C. Ver Logs en Tiempo Real

```bash
# Tail logs
wrangler tail

# O con filtros
wrangler tail --status error
```

---

## 🎨 PASO 5: Desplegar Frontend en Pages

### Opción A: Via Dashboard (Recomendado Primera Vez)

1. Ve a **Cloudflare Dashboard** → **Pages**
2. Click **Create a project**
3. Connect to Git → Selecciona tu repo
4. Configure build:
   ```
   Framework preset: None
   Build command: npm run build
   Build output directory: frontend/dist
   Root directory: Tecnología
   ```

5. Environment variables:
   ```
   VITE_API_URL=https://news-generator-api.your-subdomain.workers.dev
   ```

6. Click **Save and Deploy**

### Opción B: Via Wrangler CLI

```bash
cd /home/sebastianvernis/news-prototype/Tecnología

# Crear pages project
wrangler pages project create news-generator-admin

# Build frontend
cd frontend
npm install
npm run build

# Deploy
wrangler pages deploy dist --project-name=news-generator-admin
```

### C. Configurar Custom Domain (Opcional)

```bash
# Via dashboard: Pages → news-generator-admin → Custom domains
# O via CLI:
wrangler pages domain add news-admin.tudominio.com
```

---

## 🔄 PASO 6: Configurar CI/CD

### GitHub Actions

Crear `.github/workflows/deploy-cloudflare.yml`:

```yaml
name: Deploy to Cloudflare

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy-worker:
    runs-on: ubuntu-latest
    name: Deploy Worker
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        working-directory: ./Tecnología/workers
        run: npm ci
      
      - name: Deploy to Cloudflare Workers
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          workingDirectory: './Tecnología'
          command: deploy

  deploy-pages:
    runs-on: ubuntu-latest
    name: Deploy Pages
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install and Build
        working-directory: ./Tecnología/frontend
        run: |
          npm ci
          npm run build
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: news-generator-admin
          directory: ./Tecnología/frontend/dist
```

### Secrets en GitHub

1. Ve a repo → **Settings** → **Secrets and variables** → **Actions**
2. Añadir:
   - `CLOUDFLARE_API_TOKEN` (obtener de Cloudflare dashboard)
   - `CLOUDFLARE_ACCOUNT_ID` (obtener de dashboard)

---

## 🧪 PASO 7: Probar Sistema Completo

### A. Verificar Health

```bash
# Worker
curl https://news-generator-api.your-subdomain.workers.dev/api/health

# Frontend
curl https://news-generator-admin.pages.dev
```

### B. Generar Sitio de Prueba

```bash
# Via API
curl -X POST https://news-generator-api.your-subdomain.workers.dev/api/sites/generate \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 1,
    "verifyDomains": false
  }'

# Respuesta:
# {"success":true,"jobId":"uuid","status":"queued"}

# Verificar status
curl https://news-generator-api.your-subdomain.workers.dev/api/jobs/uuid
```

### C. Verificar en Dashboard

```bash
# Ver logs de Worker
wrangler tail

# Ver métricas en Dashboard
# Cloudflare → Workers & Pages → news-generator-api → Metrics
```

---

## 📊 PASO 8: Monitoreo y Observabilidad

### A. Workers Analytics

Dashboard → Workers & Pages → news-generator-api → Analytics:
- Requests/segundo
- CPU time
- Errors
- Success rate

### B. Logs en Tiempo Real

```bash
# All logs
wrangler tail

# Errors only
wrangler tail --status error

# Specific routes
wrangler tail --search "/api/sites/generate"
```

### C. D1 Database Queries

```bash
# Query via CLI
wrangler d1 execute news-generator-db --command="SELECT * FROM sites LIMIT 10"

# Con archivo
wrangler d1 execute news-generator-db --file=query.sql
```

### D. R2 Storage Management

```bash
# List objects
wrangler r2 object list news-generator-sites

# Get object info
wrangler r2 object get news-generator-sites/site_1/index.html

# Delete object
wrangler r2 object delete news-generator-sites/old_site_1/index.html
```

---

## 🔧 Troubleshooting

### Error: CPU Time Exceeded

**Problema**: Request excede 10ms de CPU
```
Error: CPU time limit exceeded
```

**Solución**: Mover procesamiento pesado a Queue
```typescript
// En lugar de procesar inmediatamente:
app.post('/api/sites/generate', async (c) => {
  // ❌ No hacer esto (mucho CPU)
  // await generateSiteComplete(params);
  
  // ✅ Hacer esto (queue)
  await c.env.SITE_GENERATION_QUEUE.send({ params });
  return c.json({ jobId: 'xxx', status: 'queued' });
});
```

### Error: Binding Not Found

**Problema**: Worker no encuentra R2/D1/KV binding
```
Error: SITES_BUCKET is not defined
```

**Solución**: 
1. Verificar wrangler.toml tiene los bindings correctos
2. Verificar recursos existen: `wrangler r2 bucket list`
3. Re-deploy: `wrangler deploy`

### Error: Database Query Failed

**Problema**: Query a D1 falla
```
Error: D1_ERROR: no such table: sites
```

**Solución**: Ejecutar schema
```bash
wrangler d1 execute news-generator-db --file=./workers/schema.sql --remote
```

### Error: Queue Message Retry Limit

**Problema**: Job falla repetidamente
```
Error: Message moved to DLQ after max retries
```

**Solución**: Revisar Dead Letter Queue
```bash
wrangler queues consumer list site-generation-dlq
```

### Sitio Pages No Se Actualiza

**Problema**: Cambios no reflejan en Pages
```
# Limpiar caché
wrangler pages deployment list --project-name=news-generator-admin
wrangler pages deployment tail
```

---

## 🚀 Optimizaciones

### 1. Caché con KV

```typescript
// Cachear respuestas frecuentes
app.get('/api/sites', async (c) => {
  // Check cache
  const cached = await c.env.CACHE.get('sites_list');
  if (cached) {
    return c.json(JSON.parse(cached));
  }
  
  // Query DB
  const sites = await getSites(c.env.DB);
  
  // Store in cache (5 min TTL)
  await c.env.CACHE.put('sites_list', JSON.stringify(sites), {
    expirationTtl: 300
  });
  
  return c.json(sites);
});
```

### 2. Streaming Response

```typescript
// Para archivos grandes
app.get('/api/sites/:id/download', async (c) => {
  const object = await c.env.SITES_BUCKET.get('site.zip');
  if (!object) return c.notFound();
  
  return new Response(object.body, {
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': 'attachment; filename="site.zip"'
    }
  });
});
```

### 3. Batch Queue Processing

```typescript
// Procesar múltiples jobs en batch
async function handleQueue(batch: MessageBatch) {
  // Procesar en paralelo
  await Promise.all(
    batch.messages.map(msg => processJob(msg))
  );
}
```

---

## 📚 Recursos

- **Wrangler Docs**: https://developers.cloudflare.com/workers/wrangler/
- **Workers Docs**: https://developers.cloudflare.com/workers/
- **Pages Docs**: https://developers.cloudflare.com/pages/
- **R2 Docs**: https://developers.cloudflare.com/r2/
- **D1 Docs**: https://developers.cloudflare.com/d1/
- **Queues Docs**: https://developers.cloudflare.com/queues/

---

## ✅ Checklist de Deployment

### Pre-deployment
- [ ] Wrangler CLI instalado
- [ ] Logged in: `wrangler whoami`
- [ ] Código en Git

### Recursos Cloudflare
- [ ] R2 buckets creados
- [ ] D1 database creada y con schema
- [ ] KV namespace creado
- [ ] Queue creada
- [ ] Secrets configurados

### Worker
- [ ] wrangler.toml configurado
- [ ] Dependencias instaladas
- [ ] Tests locales pasando
- [ ] Deploy exitoso
- [ ] Health check OK

### Pages
- [ ] Proyecto creado
- [ ] Variables de entorno configuradas
- [ ] Build exitoso
- [ ] Deploy exitoso
- [ ] UI funcional

### CI/CD
- [ ] GitHub Actions configurado
- [ ] Secrets en GitHub
- [ ] Auto-deploy funcionando

---

**¡Deployment completado! 🎉**

Tu sistema está corriendo 100% en edge con latencia ultra-baja global.
