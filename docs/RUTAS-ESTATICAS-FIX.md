# Fix de Rutas Estáticas - Generación Multi-Sitio

**Fecha:** 2026-01-13  
**Estado:** ✅ Completado

## Problema Identificado

Al servir los sitios generados localmente (wrangler dev o HTTP server), se encontraban errores 404:

```
GET /generated_sites/templates/css/template1.css 404 Not Found
GET /generated_sites/images/news/article_1_1.jpg 404 Not Found
```

### Causa Raíz

El HTML generado usaba rutas relativas incorrectas que apuntaban a directorios externos:
- CSS: `href="../templates/css/template{site_num}.css"`
- Imágenes: `src="../images/news/article_{idx}_{site_num}.jpg"`

Sin embargo, el flujo de generación **ya copiaba** estos archivos al directorio de cada sitio:
- CSS → `generated_sites/site_X/style.css`
- Imágenes → `generated_sites/site_X/images/news_Y.jpg`

## Solución Implementada

### Cambios en `scripts/master_orchestrator.py`

#### 1. Ruta CSS (línea 494)
```diff
- <link rel="stylesheet" href="../templates/css/template{site_num}.css">
+ <link rel="stylesheet" href="style.css">
```

#### 2. Ruta de imágenes (línea 513)
```diff
- image_path = f"../images/news/article_{idx}_{site_num}.jpg"
+ image_path = f"images/news_{idx}.jpg"
```

## Estructura Final de Archivos

```
generated_sites/
├── site_1/
│   ├── index.html              # href="style.css", src="images/news_1.jpg"
│   ├── style.css               # CSS único del sitio
│   ├── logo.jpg
│   ├── images/
│   │   ├── news_1.jpg
│   │   ├── news_2.jpg
│   │   └── ...
│   └── article_*.html
├── site_2/
│   ├── index.html              # href="style.css", src="images/news_1.jpg"
│   ├── style.css               # CSS con layout diferente
│   ├── images/
│   │   └── ...
│   └── ...
└── site_3/
    └── ...
```

## Verificación

### Test con 3 sitios (layouts diferentes)

```bash
cd scripts
python3 master_orchestrator.py --sitios 3
```

**Resultado:**
- ✅ 3 sitios generados con layouts distintos
- ✅ Site 1: `modern_green` + `dynamic_contrast` + `minimal_clean`
- ✅ Site 2: `energetic_red` + `humanist_friendly` + `compact_dense`
- ✅ Site 3: `mystic_indigo` + `dynamic_contrast` + `masonry_dynamic`

### Test de servicio local

```bash
# Terminal 1
cd generated_sites/site_1 && python3 -m http.server 8000

# Terminal 2
cd generated_sites/site_2 && python3 -m http.server 8001

# Terminal 3
cd generated_sites/site_3 && python3 -m http.server 8002
```

**Verificación:**
```bash
curl -I http://localhost:8000/style.css         # 200 OK
curl -I http://localhost:8000/images/news_1.jpg # 200 OK (binary)
curl http://localhost:8000/                     # HTML renders
```

## Beneficios

1. **Sitios autosuficientes**: Cada directorio `site_X/` contiene todos sus recursos
2. **Portabilidad**: Los sitios pueden moverse, comprimirse o desplegarse independientemente
3. **Sin dependencias externas**: No necesitan acceso a `templates/` o `images/` globales
4. **Compatibilidad**: Funcionan con cualquier servidor HTTP estático (Python, Node, Nginx, Cloudflare Pages, etc.)
5. **Multi-generación**: El flujo de generación de múltiples sitios funciona correctamente con layouts únicos por sitio

## Flujo de Archivos

```
1. Template Combiner genera:
   templates/css/template1.css, template2.css, ...

2. Image Generator genera:
   images/news/article_article_1_1_1.jpg, ...

3. Master Orchestrator COPIA:
   templates/css/template1.css → generated_sites/site_1/style.css
   images/news/article_*_1_*.jpg → generated_sites/site_1/images/news_1.jpg

4. HTML generado referencia:
   <link rel="stylesheet" href="style.css">
   <img src="images/news_1.jpg">
```

## Deploy a Cloudflare Workers (siguiente paso)

Los sitios ya están listos para subirse a R2 o servirse mediante Workers Sites/Pages:

```bash
# Opción 1: R2 Bucket
wrangler r2 object put news-sites-bucket/site_1/index.html --file=generated_sites/site_1/index.html

# Opción 2: Pages
cd generated_sites/site_1
wrangler pages deploy .
```

## Notas

- Los archivos `article_*.html` también usan `href="style.css"` (línea 575)
- Las imágenes en artículos usan `images/news_{idx}.jpg` (línea 593)
- El logo se copia como `logo.jpg` en cada directorio de sitio
- Los templates CSS se generan con IDs únicos (e.g., `16_4_19`) que combinan paleta, fuente y layout

## Comandos Útiles

```bash
# Regenerar un sitio
cd scripts && python3 master_orchestrator.py --sitios 1

# Regenerar múltiples sitios
cd scripts && python3 master_orchestrator.py --sitios 5

# Servir localmente
cd generated_sites/site_1 && python3 -m http.server 8000

# Verificar estructura
tree generated_sites/site_1 -L 2

# Verificar rutas en HTML
grep -E "(href=|src=)" generated_sites/site_1/index.html
```
