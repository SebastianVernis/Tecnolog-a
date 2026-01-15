# 📁 Estructura del Proyecto - News Prototype

**Última actualización**: 2026-01-15 03:04

---

## 🎯 Objetivo del Proyecto

Sistema automatizado que genera sitios web de noticias únicos con:
- Contenido parafraseado y expandido (800 palabras)
- Imágenes generadas con IA (Flux Schnell)
- Diseños únicos (paletas de color + fuentes + layouts)
- Páginas legales completas
- Headers y footers personalizados

---

## 📂 Estructura de Directorios Reorganizada

```
Tecnología/
├── 📋 AGENTS.md                    # Guía para agentes IA
├── 📋 README.md                    # Documentación principal
├── 📋 ESTRUCTURA-PROYECTO.md       # Este archivo
├── 📋 requirements.txt             # Dependencias Python
├── 📋 package.json                 # Dependencias Node.js
│
├── 📂 scripts/                     # Scripts de generación
│   ├── master_orchestrator.py      # 🎯 Orquestador principal
│   ├── article-expander.py         # Expansión de artículos
│   ├── paraphrase.py               # Parafraseado con IA
│   ├── generate-images-ai.py       # Generación de imágenes IA
│   ├── layout_generator.py         # Generador de layouts
│   ├── template_combiner.py        # Combinador de CSS
│   ├── header_generator.py         # Generador de headers
│   ├── footer_generator.py         # Generador de footers
│   ├── color_palette_generator.py  # 20 paletas de color
│   ├── font_family_generator.py    # 15 familias de fuentes
│   ├── layout_css_generator.py     # 20 layouts CSS
│   ├── site_name_generator.py      # Generador de nombres
│   ├── site_pre_creation.py        # Pre-creación de sitios
│   ├── legal_pages_generator.py    # Páginas legales
│   ├── domain_verifier.py          # Verificador de dominios
│   │
│   ├── api/                        # Módulos de APIs
│   │   ├── newsapi.py              # NewsAPI.org
│   │   ├── apitube.py              # APITube.io
│   │   ├── newsdata.py             # Newsdata.io
│   │   └── worldnews.py            # WorldNewsAPI
│   │
│   ├── test/                       # Tests de integración
│   │   ├── test_integration.py     # Test de APIs
│   │   ├── test_blackbox.py        # Test de Blackbox IA
│   │   ├── test_paraphrase_quick.py # Test de parafraseado
│   │   └── test_flujo_completo.py  # ✨ Test end-to-end (2 artículos)
│   │
│   └── utils/                      # Utilidades
│       └── utils.py                # Funciones auxiliares
│
├── 📂 data/                        # Datos del proyecto
│   ├── raw/                        # ✨ Datos sin procesar
│   │   ├── newsapi_*.json          # Noticias descargadas
│   │   └── newsapi_*.csv           # Noticias en CSV
│   ├── sites_metadata/             # Metadata de sitios generados
│   └── archive/                    # Datos históricos
│
├── 📂 generated_sites/             # ✨ Sitios generados (producción)
│   ├── site_1/
│   │   ├── index.html              # Página principal
│   │   ├── style.css               # Estilos únicos
│   │   ├── logo.jpg                # Logo del sitio
│   │   ├── article_*.html          # Páginas de artículos
│   │   ├── terminos.html           # Términos y condiciones
│   │   ├── privacidad.html         # Política de privacidad
│   │   ├── faqs.html               # Preguntas frecuentes
│   │   ├── acerca.html             # Acerca de nosotros
│   │   └── images/                 # Imágenes del sitio
│   │       ├── news_1.jpg
│   │       ├── news_2.jpg
│   │       └── ...
│   └── site_2/
│       └── ...
│
├── 📂 generated_sites_test/        # ✨ Sitios de prueba (tests)
│   └── site_1/
│       └── ... (misma estructura)
│
├── 📂 generated_images/            # ✨ Imágenes generadas por IA
│   ├── article_*.jpg               # Imágenes de artículos
│   └── article_logo_*.jpg          # Logos generados
│
├── 📂 templates/                   # Templates HTML/CSS
│   ├── base.html                   # Template base
│   ├── index.html                  # Template index
│   └── css/                        # CSS modulares
│       ├── template1.css           # Combinación 1
│       ├── template2.css           # Combinación 2
│       └── ...
│
├── 📂 docs/                        # Documentación
│   ├── screenshots/                # ✨ Capturas de pantalla
│   │   ├── site_review.png
│   │   ├── site_review_updated.png
│   │   └── site_improved_final.png
│   ├── QUICKSTART.md
│   ├── FLUJO-COMPLETO-INTEGRADO.md
│   ├── COMANDOS-FLUJO-COMPLETO.md
│   └── archive/                    # Docs antiguos
│
├── 📂 archive/                     # Código legacy
│   ├── test_headers_footers.py
│   ├── test_orchestrator.py
│   └── docs_old/
│
├── 📂 frontend/                    # Frontend React (opcional)
├── 📂 backend/                     # Backend Flask (opcional)
├── 📂 reference-sites/             # Sitios de referencia HTML
└── 📂 public/                      # Assets públicos (deployment)
```

---

## 🔄 Flujo Principal (master_orchestrator.py)

```
1. Descarga Noticias → NewsAPI
   └─> data/raw/newsapi_TIMESTAMP.json

2. Parafraseo + Expansión → Artículos únicos (800 palabras)
   └─> Memoria (no se guarda, se procesa en runtime)

3. Generación de Imágenes → IA (Flux Schnell)
   └─> generated_images/article_*.jpg

4. Metadata de Sitios → Nombres, dominios, taglines
   └─> data/sites_metadata/sites_metadata_TIMESTAMP.json

5. Generación de Logos → IA
   └─> generated_images/article_logo_*.jpg

6. Templates CSS → Combinaciones (paletas + fuentes + layouts)
   └─> templates/css/templateN.css

7. Generación HTML → Sitios completos
   └─> generated_sites/site_N/
       ├── index.html (grid de noticias)
       ├── style.css (copia del template)
       ├── logo.jpg (copia de generated_images)
       ├── article_*.html (artículos completos + sidebar)
       ├── terminos.html, privacidad.html, faqs.html, acerca.html
       └── images/news_*.jpg (copias de generated_images)
```

---

## 🎯 Cambios en la Reorganización (2026-01-15)

### ✨ Nuevos Directorios

1. **`data/raw/`**
   - Contiene noticias sin procesar de APIs
   - Archivos JSON y CSV de NewsAPI
   - Antes estaban en la raíz del proyecto

2. **`docs/screenshots/`**
   - Capturas de pantalla del proyecto
   - Antes estaban en la raíz (`site_review.png`, etc.)

3. **`generated_images/`**
   - Directorio temporal para imágenes generadas por IA
   - Antes: `images/news/` y `scripts/images/news/`
   - Ahora: Consolidado en un solo lugar

4. **`generated_sites_test/`**
   - Sitios generados por tests (separados de producción)
   - Usado por `test_flujo_completo.py`

### 🔄 Rutas Actualizadas en Scripts

- `generate-images-ai.py`: `output_dir='generated_images'`
- `generate-images.py`: `output_dir='generated_images'`
- `master_orchestrator.py`: Busca noticias en `data/`
- `test_flujo_completo.py`: Genera en `generated_sites_test/`

---

## 🔧 Comandos Principales

### Limpiar Todo
```bash
rm -rf generated_sites/* generated_sites_test/* generated_images/* data/raw/* data/sites_metadata/* templates/css/template*.css
```

### Limpiar Solo Tests
```bash
rm -rf generated_sites_test/*
```

### Generar Sitios (Producción)
```bash
# Flujo completo con cache
python scripts/master_orchestrator.py --usar-cache

# Con verificación de dominios
python scripts/master_orchestrator.py --verificar-dominios

# Descarga en vivo (sin cache)
python scripts/master_orchestrator.py
```

### Test Rápido (2 artículos)
```bash
python scripts/test/test_flujo_completo.py
```

### Ver Sitio Localmente
```bash
cd generated_sites/site_1
python -m http.server 8001
# Abrir: http://localhost:8001
```

---

## 📦 Rutas de Salida

### Imágenes Generadas
```
generated_images/
├── article_article_1_1_1.jpg       # Imagen artículo 1
├── article_article_1_2_2.jpg       # Imagen artículo 2
├── article_logo_site_1_1.jpg       # Logo sitio 1
└── ...
```
> **Nota**: Estas son temporales, se copian a cada sitio

### Sitios Generados
```
generated_sites/site_1/
├── index.html                      # Homepage con grid de noticias
├── style.css                       # CSS único (copia de template)
├── logo.jpg                        # Logo del sitio
├── article_1.html                  # Artículo completo + sidebar
├── article_2.html                  # ...
├── terminos.html                   # Términos y condiciones
├── privacidad.html                 # Política de privacidad
├── faqs.html                       # Preguntas frecuentes
├── acerca.html                     # Acerca de nosotros
└── images/
    ├── news_1.jpg                  # Imagen artículo 1
    ├── news_2.jpg                  # Imagen artículo 2
    └── ...
```

### Templates CSS
```
templates/css/
├── template1.css                   # Paleta 1 + Fuente 1 + Layout 1
├── template2.css                   # Paleta 2 + Fuente 2 + Layout 2
└── ...
```

---

## 🧪 Tests

### Test de Flujo Completo (2 artículos)
```bash
python scripts/test/test_flujo_completo.py
```

**Características:**
- Solo 2 artículos (rápido)
- 1 sitio generado
- Usa cache si existe
- Sin verificación de dominios
- Salida: `generated_sites_test/site_1/`

### Test de Integración (APIs)
```bash
cd scripts/test
python test_integration.py
```

### Test de Parafraseado
```bash
cd scripts/test
python test_paraphrase_quick.py
```

---

## 🎨 Sistema de Templates CSS

### Variables CSS Modernas
```css
/* Spacing Scale */
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */

/* Breakpoints */
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;

/* Radius & Shadows */
--radius-sm: 0.25rem;
--radius-md: 0.5rem;
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
```

### Componentes Generados
- **20 Paletas de Color** (color_palette_generator.py)
- **15 Combinaciones de Fuentes** (font_family_generator.py)
- **20 Layouts Estructurales** (layout_css_generator.py)
- **10 Estilos de Header** (header_generator.py)
- **10 Estilos de Footer** (footer_generator.py)

**Combinaciones posibles**: 20 × 15 × 20 = 6,000

---

## 🔑 Variables de Entorno

Archivo `.env` requerido:

```env
# IA para Parafraseado e Imágenes (REQUERIDA)
BLACKBOX_API_KEY=tu_clave_aqui

# APIs de Noticias (al menos una requerida)
NEWSAPI_KEY=tu_clave_aqui

# Opcionales (más fuentes de noticias)
APITUBE_KEY=tu_clave_aqui
NEWSDATA_KEY=tu_clave_aqui
WORLDNEWS_KEY=tu_clave_aqui
```

---

## 📝 Notas Importantes

### Rutas Absolutas
- Todos los scripts usan rutas absolutas basadas en `Path(__file__).parent`
- No es necesario ejecutar desde un directorio específico

### Imágenes
- `generated_images/` es temporal, se copian a cada sitio
- Cada sitio tiene su propio directorio `images/` independiente
- Se pueden limpiar las imágenes temporales sin afectar los sitios

### CSS Modular
- Template combiner crea CSS únicos por sitio
- Cada sitio tiene `style.css` independiente
- Variables CSS centralizadas para mantener consistencia

### Tests vs Producción
- `generated_sites/` → Producción
- `generated_sites_test/` → Tests
- No interfieren entre sí

---

## 📚 Referencias

- **Context7 Libraries**: CSS Grid, Flexbox, Tailwind v3
- **Documentación**: `AGENTS.md` - Guía completa para agentes
- **Templates**: `templates/css/template1.css`
- **Tests**: `scripts/test/test_flujo_completo.py`

---

**Mantenido por**: Sistema automatizado + Agentes IA  
**Versión**: 2.0 - Estructura Reorganizada
