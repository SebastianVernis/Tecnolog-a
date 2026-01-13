# 🗞️ News Generator - Sistema Completo de Generación de Sitios de Noticias

Sistema completo para **generar automáticamente múltiples sitios de noticias** con contenido único, layouts diversos y metadatos completos. Incluye panel de administración web y API REST.

**Versión:** 2.0.0  
**Última actualización:** 13 de enero de 2026

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│  Frontend (React + Vite)                   │
│  - Panel de administración                  │
│  - Gestión de sitios                        │
│  - Deploy: Vercel                           │
└──────────────┬──────────────────────────────┘
               │ REST API
               ↓
┌─────────────────────────────────────────────┐
│  Backend (Flask API)                        │
│  - Endpoints REST                           │
│  - Orquestación de scripts                  │
│  - Deploy: Render                           │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│  Scripts Python                             │
│  - Generación de sitios                     │
│  - Procesamiento de noticias                │
│  - Layouts y CSS                            │
└─────────────────────────────────────────────┘
```

---

## ✨ Características Principales

### 🎮 Modo Interactivo
- Interfaz guiada paso a paso
- Configuración intuitiva
- Validación de inputs
- Confirmación antes de ejecutar

### 🎨 Layouts Dinámicos
- **8 tipos de layouts** diferentes por sitio
- **5 estilos de header** únicos
- **5 estilos de navegación** variados
- **5 disposiciones de destacados**
- Categorías randomizadas por sitio
- Distribución dinámica de contenido

### 📦 Sistema de Pre-Creación
- Generación automática de nombres convincentes
- Verificación de disponibilidad de dominios (opcional)
- Metadatos completos en JSON
- Paletas de colores únicas
- Especificaciones de logo

### 🚀 Flujo Automatizado
```
Configuración → Metadatos → Noticias → Layouts → Sitios HTML
```

---

## 🏃 Inicio Rápido

### 1. Panel Web (Recomendado)

**Frontend:** https://news-generator-admin.vercel.app  
**Backend API:** https://news-generator-backend-ae62.onrender.com

1. Accede al panel de administración
2. Configura tus API keys en **Settings**
3. Ve a **Create Sites** y genera sitios
4. Consulta resultados en **Sites List**

### 2. Instalación Local

```bash
# Clonar repositorio
git clone <repo-url>
cd Tecnología

# Backend
cd backend
pip install -r requirements.txt
python3 app.py  # Corre en puerto 5000

# Frontend (nueva terminal)
cd frontend
npm install
npm run dev  # Corre en puerto 5173
```

### 3. Configuración

Crea un archivo `.env` en la raíz:

```env
NEWSAPI_KEY=tu_clave_aqui
NEWSDATA_KEY=tu_clave_aqui
BLACKBOX_API_KEY=tu_clave_aqui
```

### 4. Generar Sitios (CLI)

```bash
cd scripts
python3 master_orchestrator.py --sitios 5
```

Los sitios se generan en `sites/site*.html`

---

## 💻 Uso

### Modo Interactivo (Recomendado)

```bash
cd scripts
python3 generate-sites.py
```

### Modo No-Interactivo (CLI)

```bash
# Generar 5 sitios
python3 generate-sites.py --cantidad 5 --no-interactivo

# Generar 10 sitios con verificación de dominios
python3 generate-sites.py --cantidad 10 --verificar-dominios --no-interactivo

# Usar metadatos existentes
python3 generate-sites.py --cantidad 20 --metadata-file ../data/sites_metadata/sites_metadata_20260108.json
```

### Script Rápido

```bash
cd scripts
./run.sh              # Modo interactivo
./run.sh --cantidad 5 # Generar 5 sitios rápido
```

---

## 📊 Parámetros CLI

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--cantidad N` | Número de sitios a crear (1-100) | `--cantidad 10` |
| `--verificar-dominios` | Verificar disponibilidad con whois | `--verificar-dominios` |
| `--metadata-file PATH` | Usar metadatos específicos | `--metadata-file ../data/sites_metadata/archivo.json` |
| `--generar-metadata` | Forzar generación de metadatos nuevos | `--generar-metadata` |
| `--no-interactivo` | Desactivar modo interactivo | `--no-interactivo` |

---

## 🏗️ Estructura del Proyecto

```
Tecnología/
├── frontend/                     # 🎨 Panel de administración (React)
│   ├── src/
│   │   ├── pages/               # Dashboard, CreateSites, Settings
│   │   ├── services/            # API client
│   │   └── components/          # Header, etc.
│   └── package.json
│
├── backend/                      # 🔧 API REST (Flask)
│   ├── app.py                   # ⭐ API principal
│   └── requirements.txt
│
├── scripts/                      # 🐍 Scripts de generación Python
│   ├── master_orchestrator.py   # ⭐ Orquestador principal
│   ├── generate-sites.py        # Generador legacy
│   ├── paraphrase.py            # Parafraseo de noticias
│   ├── article-expander.py      # Expansión de artículos
│   ├── generate-images-ai.py    # Generación de imágenes
│   ├── site_name_generator.py   # Generador de nombres
│   ├── layout_generator.py      # Layouts dinámicos
│   ├── layout_css_generator.py  # Estilos CSS
│   ├── domain_verifier.py       # Verificador WHOIS
│   ├── api/                     # APIs de noticias
│   │   ├── newsapi.py
│   │   ├── newsdata.py
│   │   └── worldnews.py
│   └── utils/                   # Utilidades
│
├── data/                         # 📊 Datos y metadatos
│   ├── noticias_final_*.json
│   ├── noticias_paraphrased_*.json
│   └── sites_metadata/
│
├── sites/                        # 🌐 Sitios HTML generados
│   └── site*.html
│
├── templates/                    # 📄 Templates base
│   ├── base.html
│   └── css/                     # 40+ estilos CSS
│
├── images/                       # 🖼️ Imágenes generadas
│   └── news/
│
└── docs/                         # 📚 Documentación
    ├── ERROR-FIX-20260113.md    # ⭐ Correcciones recientes
    ├── PROJECT-STRUCTURE.md     # ⭐ Estructura detallada
    ├── DEPLOYMENT-GUIDE-RENDER-VERCEL.md
    └── QUICKSTART.md
```

Ver [docs/PROJECT-STRUCTURE.md](docs/PROJECT-STRUCTURE.md) para detalles completos.

---

## 🎨 Diversidad de Layouts

Cada sitio generado tiene estructura **única**:

### Tipos de Layout
- **Classic** - Periódico tradicional
- **Magazine** - Estilo revista con grid
- **Modern Cards** - Tarjetas modernas
- **Masonry** - Tipo Pinterest
- **Featured Sidebar** - Destacado con sidebar
- **Grid Equal** - Grid uniforme
- **Timeline** - Línea de tiempo vertical
- **Asymmetric** - Asimétrico moderno

### Estilos de Header
- **Centered** - Logo centrado
- **Left Aligned** - Logo a la izquierda
- **Split** - Logo izq, menú der
- **Minimal** - Minimalista
- **Bold** - Audaz con espacio

### Navegación
- Horizontal
- Horizontal Center
- Hamburger Menu
- Sidebar Nav
- Mega Menu

### Sección Destacada
- Hero Full Width
- Hero Split (60/40)
- Carousel
- Grid Featured
- Stacked

---

## 📋 Metadatos Generados

Cada sitio incluye metadatos completos en JSON:

```json
{
  "id": "site_20260108_162536_1234",
  "nombre": "El Diario Nacional",
  "dominio": "eldiario.mx",
  "dominio_disponible": true,
  "tagline": "La Verdad en Cada Historia",
  "colores": {
    "primario": "#2C3E50",
    "secundario": "#3498DB",
    "acento": "#E74C3C"
  },
  "logo": {
    "estilo": "moderno",
    "prompt": "modern newspaper logo..."
  },
  "categorias": ["Inicio", "Nacional", "Internacional"],
  "contacto": {
    "email": "contacto@eldiario.mx",
    "telefono": "+52 55 1234 5678"
  },
  "seo": {
    "title": "El Diario Nacional - Noticias...",
    "description": "Tu fuente confiable...",
    "keywords": ["noticias", "méxico", ...]
  }
}
```

---

## 🎯 Casos de Uso

### Desarrollo Rápido (3-5 sitios)
```bash
python3 generate-sites.py
# Cantidad: 3
# Verificar: No
# ~10 segundos
```

### Producción (40+ sitios)
```bash
python3 generate-sites.py --cantidad 40 --no-interactivo
# ~2 minutos sin verificación
```

### Con Verificación de Dominios
```bash
python3 generate-sites.py --cantidad 10 --verificar-dominios --no-interactivo
# ~3-5 minutos (rate limiting whois)
```

### CI/CD Automatizado
```bash
python3 generate-sites.py --cantidad 25 --no-interactivo --generar-metadata
# Completamente automatizado
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# APIs de Noticias
NEWSAPI_KEY=tu_api_key_aqui
NEWSDATA_KEY=tu_api_key_aqui

# AI para Parafraseo e Imágenes
BLACKBOX_API_KEY=tu_api_key_aqui
```

### Personalización

#### Cambiar Cantidad de Templates CSS
```python
# En generate-sites.py
MAX_TEMPLATES = 100  # Ajustar según templates disponibles
```

#### Agregar Más Estilos de Nombres
```python
# En site_name_generator.py
self.prefijos_clasicos = ["El", "La", "Periódico", ...]
self.nucleos = ["Diario", "Prensa", "Noticias", ...]
```

---

## 📚 Documentación

### Principales
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Guía de inicio rápido
- **[docs/ERROR-FIX-20260113.md](docs/ERROR-FIX-20260113.md)** - ⭐ Correcciones recientes
- **[docs/PROJECT-STRUCTURE.md](docs/PROJECT-STRUCTURE.md)** - ⭐ Estructura del proyecto
- **[docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md](docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md)** - Deploy en producción
- **[docs/FLUJO-COMPLETO-INTEGRADO.md](docs/FLUJO-COMPLETO-INTEGRADO.md)** - Flujo de generación

### Deployment
- **[docs/DEPLOYMENT-ARCHITECTURE.md](docs/DEPLOYMENT-ARCHITECTURE.md)** - Arquitectura de deploy
- **[docs/README_FRONTEND.md](docs/README_FRONTEND.md)** - Documentación del frontend
- **[docs/KEEP-ALIVE-STRATEGY.md](docs/KEEP-ALIVE-STRATEGY.md)** - Estrategia para Render free tier

---

## 🚀 Flujo del Sistema

### Modo Web (Panel de Administración)

1. **Configurar** → Settings → Agregar API keys
2. **Generar** → Create Sites → Seleccionar opciones
3. **Revisar** → Sites List → Ver sitios generados
4. **Descargar** → Click en "View Site"

### Modo CLI (Scripts Python)

```bash
# Flujo completo automático
python3 scripts/master_orchestrator.py --sitios 5

# Pasos manuales
cd scripts/api
python3 newsapi.py           # 1. Obtener noticias
cd ..
python3 paraphrase.py        # 2. Parafrasear
python3 article-expander.py  # 3. Expandir artículos
python3 generate-images.py   # 4. Generar imágenes
python3 generate-sites.py    # 5. Generar sitios
```

### Vía API REST

```bash
# Generar 5 sitios
curl -X POST http://localhost:5000/api/sites/generate \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5, "useFullFlow": true}'

# Ver estadísticas
curl http://localhost:5000/api/sites/stats

# Listar sitios
curl http://localhost:5000/api/sites
```

---

## 📊 Rendimiento

| Operación | Sin Verificación | Con Verificación |
|-----------|------------------|------------------|
| 5 sitios | ~15 segundos | ~1-2 minutos |
| 10 sitios | ~30 segundos | ~3-5 minutos |
| 40 sitios | ~2 minutos | ~10-15 minutos |
| 100 sitios | ~5 minutos | ~25-30 minutos |

*Tiempos aproximados en hardware moderno con conexión estable*

---

## ✅ Verificación

El sistema siempre:
- ✅ Genera **exactamente** la cantidad de sitios solicitada
- ✅ Limpia sitios antiguos antes de generar nuevos
- ✅ Crea metadatos únicos por sitio
- ✅ Asigna layouts diferentes a cada sitio
- ✅ Randomiza categorías por sitio
- ✅ Distribuye contenido dinámicamente
- ✅ Valida imágenes y usa placeholders si faltan

---

## 🛠️ Solución de Problemas

### Error: "whois no está instalado"
```bash
# Ubuntu/Debian
sudo apt-get install whois

# Fedora
sudo dnf install whois

# macOS (preinstalado)
```

### Error: "No se pudieron cargar las noticias"
```bash
# Verificar archivo de noticias
ls ../data/noticias_final_*.json

# Regenerar si es necesario
python3 paraphrase.py
```

### Los sitios no tienen CSS
```bash
# Verificar templates CSS
ls ../templates/css/template*.css
```

---

## 🧹 Organización del Proyecto

### Archivos Activos
- **Root**: Scripts principales, configuración
- **data/**: Últimas noticias y 3 metadatos más recientes
- **docs/**: Documentación vigente

### Archivos Archivados
- **data/archive/**: Datos históricos
- **data/sites_metadata/archive/**: Metadatos antiguos
- **docs/archive/**: Documentación histórica
- **scripts/archive/**: Scripts deprecated

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

---

## 👤 Autor

**Sebastián Vernis**
- GitHub: [@sebastianvernis](https://github.com/sebastianvernis)

---

## 🔗 Enlaces Rápidos

- **Panel Web:** https://news-generator-admin.vercel.app
- **API Backend:** https://news-generator-backend-ae62.onrender.com
- **Documentación:** [docs/](docs/)
- **Reporte de Errores:** [docs/ERROR-FIX-20260113.md](docs/ERROR-FIX-20260113.md)

## 🎉 ¡Comienza Ahora!

### Opción 1: Panel Web (Más Fácil)
1. Visita https://news-generator-admin.vercel.app
2. Configura tus API keys
3. Genera sitios con un click

### Opción 2: CLI Local
```bash
cd scripts
python3 master_orchestrator.py --sitios 5
```

**Genera sitios de noticias únicos en minutos** 🚀

---

## 📝 Changelog Reciente

### [2.0.0] - 2026-01-13

**Agregado:**
- Panel de administración web completo (React + Vite)
- API REST con Flask
- Deploy en Vercel (frontend) y Render (backend)
- Documentación completa del proyecto

**Corregido:**
- Error 500/502 en endpoint `/api/sites/generate`
- React Error #31 en manejo de errores de API
- 404 en rutas SPA (`/create`, etc.)
- Warnings de autocomplete en inputs de password

**Ver:** [docs/ERROR-FIX-20260113.md](docs/ERROR-FIX-20260113.md) para detalles completos.

---

## 🆘 Soporte

**Problemas conocidos:** Ver [docs/ERROR-FIX-20260113.md](docs/ERROR-FIX-20260113.md)  
**Issues:** Abre un issue en GitHub  
**Documentación:** Revisa [docs/](docs/)

---

**Última actualización:** 13 de enero de 2026  
**Versión:** 2.0.0  
**Status:** ✅ Producción
