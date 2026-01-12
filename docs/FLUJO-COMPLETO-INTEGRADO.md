# Flujo Completo Integrado - Sistema de Generación de Sitios

## 📋 Visión General

Sistema modular completo para generación automatizada de sitios de noticias con contenido único, diseño personalizado y estructura independiente por sitio.

## 🔄 Flujo de Ejecución

### Flujo Secuencial Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO DESDE FRONTEND                         │
│                  (Backend API Endpoint)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 1: DESCARGA DE NOTICIAS                                   │
│  - Obtiene noticias desde APIs (NewsAPI, etc.)                  │
│  - ~50 noticias base de tecnología                              │
│  Script: news.py / api/*                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 2: PARAFRASEO Y ARTÍCULOS COMPLETOS                       │
│  - 1 variación parafraseada por noticia por sitio               │
│  - Genera artículo completo (~800 palabras)                     │
│  - Estilos variados: formal, técnico, narrativo, etc.           │
│  Script: paraphrase.py + article_expander.py                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 3: GENERACIÓN DE IMÁGENES DE NOTICIAS                     │
│  - 1 imagen por noticia parafraseada                            │
│  - Prompts ultra específicos basados en contenido               │
│  - Almacenadas en directorio del sitio                          │
│  Script: generate_images_ai.py                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 4: METADATA DE SITIOS                                     │
│  - Genera nombre único de sitio                                 │
│  - Verifica disponibilidad de dominio (opcional)                │
│  - Si no disponible: regenera nombre                            │
│  - Crea tagline y descripción                                   │
│  Script: site_pre_creation.py                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 5: GENERACIÓN DE LOGOS                                    │
│  - 1 logo por sitio                                             │
│  - Prompt ultra específico basado en nombre y tagline           │
│  - Estilo: minimalista, profesional, periodístico               │
│  Script: generate_images_ai.py                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 6: GENERACIÓN DE MÓDULOS CSS                              │
│  ┌──────────────┬──────────────┬──────────────┐                │
│  │   PALETA     │   FUENTES    │   LAYOUT     │                │
│  │  20 colores  │ 15 combos    │ 20 diseños   │                │
│  └──────┬───────┴──────┬───────┴──────┬───────┘                │
│         └──────────────┼──────────────┘                         │
│                        │                                         │
│                 TEMPLATE COMBINER                                │
│              (6,000 combinaciones)                               │
│  Script: template_combiner.py                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 7: GENERACIÓN DE SITIOS HTML                              │
│  - Index con grid de noticias                                   │
│  - Página individual por artículo (article_N.html)              │
│  - CSS personalizado copiado                                    │
│  - Imágenes y logo integrados                                   │
│  Script: master_orchestrator.py                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  RESULTADO: DIRECTORIO INDEPENDIENTE POR SITIO                  │
│                                                                  │
│  generated_sites/                                                │
│  ├── site_1/                                                     │
│  │   ├── index.html              (página principal)             │
│  │   ├── article_1.html          (artículo completo 1)          │
│  │   ├── article_2.html          (artículo completo 2)          │
│  │   ├── ...                                                     │
│  │   ├── article_N.html          (artículo completo N)          │
│  │   ├── style.css               (CSS único del sitio)          │
│  │   ├── logo.jpg                (logo del sitio)               │
│  │   └── images/                 (imágenes de noticias)         │
│  │       ├── news_1.jpg                                          │
│  │       ├── news_2.jpg                                          │
│  │       └── ...                                                 │
│  ├── site_2/                                                     │
│  │   └── ... (estructura idéntica)                              │
│  └── ...                                                         │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Componentes Modulares

### 1. Sistema de Colores
**Archivo**: `color_palette_generator.py`
- 20 paletas únicas
- Variables CSS: primary, secondary, accent, background, text
- Desde azul profesional hasta rosa suave

### 2. Sistema de Fuentes
**Archivo**: `font_family_generator.py`
- 15 combinaciones tipográficas
- Headers + Body fonts
- Google Fonts imports automáticos

### 3. Sistema de Layouts
**Archivo**: `layout_css_generator.py`
- 20 estructuras visuales
- Grid, masonry, sidebar, full-width, etc.
- Responsive por defecto

### 4. Combinador de Templates
**Archivo**: `template_combiner.py`
- Combina: paleta + fuente + layout
- 6,000 combinaciones únicas posibles (20 × 15 × 20)
- Genera CSS completo y cohesivo

### 5. Generador de Contenido
**Archivos**: 
- `paraphrase.py` - Parafrasea títulos y descripciones
- `article_expander.py` - Expande a artículos completos

### 6. Generador de Imágenes
**Archivo**: `generate_images_ai.py`
- Prompts específicos por contexto
- Logos minimalistas profesionales
- Imágenes de noticias relevantes

### 7. Gestión de Sitios
**Archivo**: `site_pre_creation.py`
- Genera nombres únicos
- Verifica dominios
- Crea metadata completa

## 🚀 Ejecución

### Desde Backend (Recomendado)

```bash
# Iniciar backend
cd backend
python3 app.py
```

**Endpoint API**:
```
POST /api/sites/generate
{
  "quantity": 5,
  "verifyDomains": false,
  "useFullFlow": true
}
```

### Desde Script Directo

```bash
cd scripts

# Flujo completo (5 sitios)
python3 master_orchestrator.py --sitios 5

# Con verificación de dominios
python3 master_orchestrator.py --sitios 10 --verificar-dominios

# Prueba rápida (1 sitio)
python3 test_orchestrator.py
```

### Desde Frontend

```javascript
// Llamada desde React/Vue/etc
const response = await fetch('http://localhost:5000/api/sites/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    quantity: 5,
    verifyDomains: false,
    useFullFlow: true
  })
});

const result = await response.json();
```

## 📊 Estadísticas del Sistema

### Capacidades
- **Combinaciones CSS**: 6,000 únicas
- **Estilos de escritura**: 8 variaciones
- **Estructuras de artículo**: 8 formatos
- **Tiempo por sitio**: ~5-10 minutos (con IA)

### Recursos Generados por Sitio
- 1 index.html (página principal)
- N article_*.html (1 por noticia)
- 1 style.css (único)
- 1 logo.jpg
- N news_*.jpg (1 por noticia)

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
BLACKBOX_API_KEY=tu_api_key_aqui
```

### Dependencias
```bash
# Instalar requirements
pip install -r requirements.txt

# Módulos principales:
# - requests (API calls)
# - python-dotenv (env vars)
# - flask, flask-cors (backend)
# - Pillow (imágenes)
```

## 📁 Estructura de Archivos

```
scripts/
├── master_orchestrator.py      # 🎯 Orquestador principal
├── template_combiner.py         # Combinador de módulos CSS
├── color_palette_generator.py   # 20 paletas
├── font_family_generator.py     # 15 combinaciones
├── layout_css_generator.py      # 20 layouts
├── paraphrase.py                # Parafraseo IA
├── article_expander.py          # Artículos completos
├── generate_images_ai.py        # Generación de imágenes
├── site_pre_creation.py         # Metadata de sitios
├── domain_verifier.py           # Verificación whois
└── test_orchestrator.py         # Script de prueba

backend/
└── app.py                       # API Flask

generated_sites/
├── site_1/
├── site_2/
└── ...

data/
├── noticias_final_*.json        # Noticias descargadas
└── sites_metadata/              # Metadata de sitios
```

## 🎨 Personalización

### Añadir Nueva Paleta de Colores
```python
# En color_palette_generator.py
{
    "nombre": "mi_paleta",
    "descripcion": "Descripción",
    "primary": "#HEX1",
    "secondary": "#HEX2",
    # ... resto de colores
}
```

### Añadir Nueva Combinación de Fuentes
```python
# En font_family_generator.py
{
    "nombre": "mi_fuente",
    "descripcion": "Descripción",
    "primary": "'Fuente Header', sans-serif",
    "secondary": "'Fuente Body', serif",
    # ... configuración
}
```

### Añadir Nuevo Layout
```python
# En layout_css_generator.py
{
    "nombre": "mi_layout",
    "descripcion": "Descripción",
    "tipo": "grid",
    # ... configuración CSS
}
```

## 🔍 Debugging

### Logs
El orquestador genera logs detallados con timestamps:
```
[HH:MM:SS] ℹ️ Mensaje informativo
[HH:MM:SS] ✅ Éxito
[HH:MM:SS] ⚠️ Advertencia
[HH:MM:SS] ❌ Error
[HH:MM:SS] 🔄 Progreso
```

### Archivo de Resumen
Cada ejecución genera:
```
generated_sites/run_summary_YYYYMMDD_HHMMSS.json
```

Contiene:
- Estadísticas completas
- Tiempo de ejecución
- Sitios generados
- Errores encontrados

## 🚨 Solución de Problemas

### Error: "BLACKBOX_API_KEY no encontrada"
```bash
# Crear/editar .env
echo "BLACKBOX_API_KEY=tu_key" > .env
```

### Error: Módulos no encontrados
```bash
cd scripts
# Asegurar estar en directorio correcto
python3 master_orchestrator.py
```

### Error: Timeout en generación
```bash
# Aumentar timeout en backend/app.py
timeout = 3600  # 1 hora
```

### Error: Sin noticias disponibles
```bash
# Ejecutar scraper primero
cd scripts
python3 news.py
```

## 📈 Mejoras Futuras

- [ ] Caché de imágenes generadas
- [ ] Pool de workers para paralelización
- [ ] Sistema de colas para procesamiento asíncrono
- [ ] Preview en tiempo real durante generación
- [ ] Exportación a ZIP por sitio
- [ ] Sistema de plantillas HTML personalizables
- [ ] Integración con CDN para hosting
- [ ] Analytics de sitios generados

## 📄 Licencia

Proyecto de demostración. Uso educativo.

## 👥 Contribución

Para añadir funcionalidades:
1. Crear nuevo módulo en `scripts/`
2. Importar en `master_orchestrator.py`
3. Añadir paso en método `ejecutar_flujo_completo()`
4. Actualizar esta documentación

---

**Última actualización**: Enero 2026  
**Versión**: 2.0.0 (Sistema Modular Integrado)
