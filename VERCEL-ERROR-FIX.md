# Corrección de Error 500 en Vercel

## Problemas Identificados

### 1. **Importaciones Incorrectas en `master_orchestrator.py`**
**Problema:** Los archivos `article-expander.py` y `generate-images-ai.py` tienen guiones en sus nombres, pero se intentaba importar como `article_expander` y `generate_images_ai`.

**Solución:** Implementado un sistema de importación dinámica usando `importlib.util` para cargar módulos desde archivos con guiones.

```python
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"No se pudo importar {module_name} desde {file_path}")
```

### 2. **Rutas Relativas en Render**
**Problema:** `master_orchestrator.py` usaba rutas relativas (`../data`, `../templates`) que fallan en el entorno de Render.

**Solución:** Cambiado a rutas absolutas basadas en la ubicación del script:

```python
script_dir = Path(__file__).parent
base_dir = script_dir.parent

self.data_dir = base_dir / "data"
self.templates_dir = base_dir / "templates"
```

### 3. **Manejo de Errores Deficiente**
**Problema:** El endpoint `/api/sites/generate` no capturaba ni reportaba errores detallados.

**Solución:** Mejorado el manejo de excepciones con traceback completo:

```python
except Exception as e:
    import traceback
    error_details = traceback.format_exc()
    return jsonify({
        'success': False,
        'error': str(e),
        'details': error_details,
        'stdout': result.stdout if 'result' in locals() else None,
        'stderr': result.stderr if 'result' in locals() else None
    }), 500
```

### 4. **Dependencias Faltantes**
**Problema:** `backend/requirements.txt` no incluía todas las dependencias necesarias para los scripts.

**Solución:** Agregadas dependencias faltantes:
- `beautifulsoup4>=4.12.0`
- `pandas>=2.0.0`
- `python-whois>=0.8.0`

## Cambios Realizados

### Archivos Modificados

1. **`scripts/master_orchestrator.py`**
   - Sistema de importación dinámica para módulos con guiones
   - Rutas absolutas en lugar de relativas
   - Mejor manejo de errores con traceback

2. **`backend/app.py`**
   - Mejora en captura de errores con detalles completos
   - Nuevo endpoint `/api/debug/paths` para verificar rutas
   - Variables de entorno `PYTHONUNBUFFERED=1` para logs en tiempo real

3. **`backend/requirements.txt`**
   - Agregadas dependencias: `beautifulsoup4`, `pandas`, `python-whois`

## Endpoint de Debug

Se agregó un nuevo endpoint para verificar el estado del sistema en producción:

```bash
GET /api/debug/paths
```

Retorna:
- Rutas de directorios (base, scripts, sites, metadata)
- Existencia de directorios críticos
- Existencia de scripts necesarios
- Versión de Python y ruta del ejecutable

## Próximos Pasos para Deploy

1. **Commit y Push de Cambios:**
```bash
git add scripts/master_orchestrator.py backend/app.py backend/requirements.txt
git commit -m "Fix: Corrige error 500 en generación de sitios

- Implementa importación dinámica para archivos con guiones
- Cambia rutas relativas a absolutas
- Mejora manejo de errores con traceback detallado
- Agrega dependencias faltantes en backend/requirements.txt"
git push origin master
```

2. **Render se actualizará automáticamente** (auto-deploy está habilitado)

3. **Verificar Deploy:**
```bash
# Verificar health check
curl https://news-generator-backend-ae62.onrender.com/api/health

# Verificar rutas y scripts
curl https://news-generator-backend-ae62.onrender.com/api/debug/paths
```

4. **Probar Generación desde Frontend:**
   - Ir a https://news-generator-admin.vercel.app
   - Click en "Crear Nuevos Sitios"
   - Configurar cantidad y opciones
   - Generar

## Monitoreo de Errores

Si vuelve a fallar, revisar:

1. **Logs de Render:**
   - Dashboard → news-generator-backend → Logs

2. **Response del endpoint debug:**
```bash
curl https://news-generator-backend-ae62.onrender.com/api/debug/paths
```

3. **Test local del script:**
```bash
cd /home/sebastianvernis/news-prototype/Tecnología/scripts
python3 master_orchestrator.py --sitios 1
```

## Notas Importantes

- **Timeout:** El flujo completo puede tardar hasta 1 hora (timeout configurado en 3600s)
- **Free Tier Render:** Puede dormir después de 15 minutos de inactividad
- **Keep-Alive:** Usar el endpoint `/api/keep-alive` o configurar UptimeRobot para mantenerlo activo

## Arquitectura del Sistema

```
Frontend (Vercel)
    ↓ /api/* requests
Backend (Render)
    ↓ subprocess.run()
Scripts (Python)
    - master_orchestrator.py
    - paraphrase.py
    - article-expander.py
    - generate-images-ai.py
    - site_name_generator.py
    - domain_verifier.py
    - site_pre_creation.py
    - template_combiner.py
    - layout_generator.py
```

## Contacto y Soporte

Para más información sobre el flujo completo, revisar:
- `docs/FLUJO-COMPLETO-INTEGRADO.md`
- `docs/DEPLOYMENT-GUIDE-RENDER-VERCEL.md`
