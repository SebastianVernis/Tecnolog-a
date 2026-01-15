# 📁 Estructura Organizada del Proyecto

> Reorganización propuesta para mejor navegabilidad

---

## 🎯 Estructura Actual

```
Tecnología/
├── menu.py                     ⭐ MENÚ PRINCIPAL INTERACTIVO
├── menu.sh                     ⭐ Launcher bash
│
├── scripts/                    📁 Scripts de generación (16 módulos)
│   ├── master_orchestrator.py  ⭐ Orquestador principal
│   │
│   ├── api/                    📁 APIs de noticias
│   │   ├── newsapi.py
│   │   ├── newsdata.py
│   │   └── worldnews.py
│   │
│   ├── test/                   📁 Tests (5 archivos)
│   │   ├── test_modulos_completo.py    ⭐ Verificar 16 módulos
│   │   ├── test_flujo_completo.py      ⭐ Test end-to-end
│   │   ├── test_blackbox.py
│   │   ├── test_paraphrase_quick.py
│   │   └── test_integration.py
│   │
│   ├── paraphrase.py           📄 Parafraseo (8 estilos)
│   ├── article-expander.py     📄 Expansión a 800 palabras
│   ├── generate-images-ai.py   📄 Imágenes AI (Flux Schnell)
│   ├── site_pre_creation.py    📄 Metadata completa
│   ├── template_combiner.py    📄 CSS modular (6,000 combos)
│   ├── layout_generator.py     📄 HTML layouts
│   ├── header_generator.py     📄 Headers (12 estilos)
│   ├── footer_generator.py     📄 Footers responsivos
│   ├── legal_pages_generator.py📄 Páginas legales
│   └── ...otros módulos
│
├── generated_sites/            📁 Output de sitios
│   └── site_N/
│       ├── index.html
│       ├── article_*.html
│       ├── style.css
│       └── images/
│
├── data/                       📁 Datos y metadata
│   ├── noticias_*.json
│   └── sites_metadata/
│
├── templates/                  📁 Templates CSS
│   └── css/
│       └── template*.css
│
└── docs/                       📁 Documentación adicional
    ├── PROJECT-STRUCTURE.md
    ├── DEPLOYMENT-GUIDE-RENDER-VERCEL.md
    └── ...
```

---

## 📋 Categorización de Scripts

### 🎮 **Scripts Interactivos (para usuarios)**
- `menu.py` / `menu.sh` - Menú principal unificado ⭐
- `scripts/generate-interactive.py` - Generador interactivo legacy
- `scripts/master_orchestrator.py` - Orquestador principal

### 🧪 **Tests (para verificación)**
- `scripts/test/test_modulos_completo.py` - Verificar 16 módulos ⭐
- `scripts/test/test_flujo_completo.py` - Test end-to-end ⭐
- `scripts/test/test_blackbox.py` - Test API Blackbox
- `scripts/test/test_paraphrase_quick.py` - Test parafraseo
- `scripts/test/test_integration.py` - Test integración

### 🔧 **Core Modules (librerías del sistema)**

**Contenido:**
- `api/newsapi.py` - Descarga noticias
- `paraphrase.py` - Parafraseo
- `article-expander.py` - Expansión
- `generate-images-ai.py` - Imágenes AI
- `legal_pages_generator.py` - Páginas legales

**Branding:**
- `site_name_generator.py` - Nombres únicos
- `domain_verifier.py` - Verificación WHOIS
- `site_pre_creation.py` - Metadata completa

**Diseño CSS:**
- `color_palette_generator.py` - 20 paletas
- `font_family_generator.py` - 15 fuentes
- `layout_css_generator.py` - 20 layouts
- `template_combiner.py` - Combinación modular

**Diseño HTML:**
- `layout_generator.py` - Configuraciones
- `header_generator.py` - Headers
- `footer_generator.py` - Footers

### 🗄️ **Scripts Legacy (archivo)**
- `scripts/generate-sites.py` - Generador legacy
- `scripts/generate-images.py` - Generador imágenes legacy
- `scripts/archive/` - Scripts deprecated

---

## 🎯 Uso Recomendado

### Para Usuarios Finales:

```bash
# Usar el menú interactivo (RECOMENDADO)
./menu.sh
# o
python menu.py
```

### Para Desarrollo:

```bash
# Generar sitio directo
python scripts/master_orchestrator.py

# Verificar módulos
python scripts/test/test_modulos_completo.py

# Test rápido end-to-end
python scripts/test/test_flujo_completo.py
```

### Para Revisión:

```bash
# Ver documentación desde el menú
./menu.sh
# → Opción 3 (Documentación)
# → Seleccionar documento
```

---

## 🔄 Migración de Archivos Antigua → Nueva

No se requiere migración - la estructura actual es óptima:

✅ **Scripts organizados** en `scripts/`  
✅ **Tests separados** en `scripts/test/`  
✅ **APIs agrupadas** en `scripts/api/`  
✅ **Archive para legacy** en `scripts/archive/`  
✅ **Documentación** en raíz para fácil acceso  
✅ **Menú unificado** en raíz (`menu.py`)  

---

## 📊 Navegación Rápida

| Quiero... | Comando |
|-----------|---------|
| **Generar un sitio** | `./menu.sh` → 1 → 1 |
| **Verificar módulos** | `./menu.sh` → 2 → 1 |
| **Ver documentación** | `./menu.sh` → 3 → seleccionar |
| **Limpiar archivos** | `./menu.sh` → 4 → 1 |
| **Ver estadísticas** | `./menu.sh` → 4 → 2 |
| **Generar directo (CLI)** | `python scripts/master_orchestrator.py` |
| **Test directo (CLI)** | `python scripts/test/test_modulos_completo.py` |

---

## 🎨 Ventajas de la Estructura Actual

✅ **Separación clara**: Scripts, tests, API, archive  
✅ **Documentación accesible**: Raíz del proyecto  
✅ **Menú unificado**: Acceso a todo desde un punto  
✅ **Tests organizados**: Directorio `test/` dedicado  
✅ **Legacy archivado**: No estorba pero está disponible  
✅ **Paths absolutos**: Funciona desde cualquier ubicación  

---

## 🚀 Comandos de Acceso Rápido

```bash
# MENÚ PRINCIPAL (Recomendado)
./menu.sh

# GENERACIÓN DIRECTA
python scripts/master_orchestrator.py
python scripts/master_orchestrator.py --verificar-dominios
python scripts/master_orchestrator.py --usar-cache

# TESTS
python scripts/test/test_modulos_completo.py      # Verificar 16 módulos
python scripts/test/test_flujo_completo.py        # Test end-to-end
python scripts/test/test_blackbox.py              # Test API

# DOCUMENTACIÓN (desde menú es mejor)
cat README-GENERADOR.md
bat DIAGRAMA-FLUJO-COMPLETO.md
less AGENTS.md
```

---

## 📝 Archivos en Raíz

| Archivo | Tipo | Propósito |
|---------|------|-----------|
| `menu.py` | Script | Menú interactivo principal ⭐ |
| `menu.sh` | Launcher | Ejecutar menú desde bash |
| `README.md` | Docs | README principal del proyecto |
| `README-GENERADOR.md` | Docs | Quick Start del generador |
| `RESUMEN-FLUJO.md` | Docs | Resumen ejecutivo (1 página) |
| `DIAGRAMA-FLUJO-COMPLETO.md` | Docs | Arquitectura detallada |
| `AGENTS.md` | Docs | Guía para desarrolladores |
| `VERIFICACION-MODULOS.md` | Docs | Verificación de integración |
| `INDEX-DOCUMENTACION.md` | Docs | Índice de toda la documentación |
| `ESTRUCTURA-ORGANIZADA.md` | Docs | Este archivo |
| `.env` | Config | Variables de entorno (no en repo) |
| `requirements.txt` | Config | Dependencias Python |
| `package.json` | Config | Configuración Node |

---

## ✅ Conclusión

La estructura actual es **óptima y bien organizada**:

✅ Scripts core en `scripts/`  
✅ Tests separados en `scripts/test/`  
✅ APIs agrupadas en `scripts/api/`  
✅ Documentación en raíz (fácil acceso)  
✅ Menú unificado `menu.py` en raíz  
✅ Legacy archivado en `scripts/archive/`  

**No se requieren cambios - solo agregar `menu.py` como punto de entrada unificado** ✅

---

**Recomendación:** Usar `./menu.sh` como punto de entrada principal para todos los usuarios.

---

**Última actualización:** 2026-01-15 15:20  
**Autor:** Sistema de Organización de Proyecto
