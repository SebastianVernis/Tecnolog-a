# 🖼️ Corrección del Sistema de Generación de Imágenes

**Fecha**: 2026-01-15  
**Problema**: Flux Schnell (Blackbox AI) no funciona por balance agotado en fal.ai  
**Solución**: Sistema unificado con fallback automático a Unsplash

---

## 📋 Problema Detectado

### Error Original
```
litellm.APIConnectionError: fal.ai request failed: 
User is locked. Reason: Exhausted balance. 
Top up your balance at fal.ai/dashboard/billing.
```

### Causa Raíz
- Blackbox AI usa fal.ai como backend para modelos de imagen
- El proveedor fal.ai tiene balance agotado
- Todos los modelos de imagen afectados:
  - `blackboxai/black-forest-labs/flux-schnell`
  - `blackboxai/stability-ai/stable-diffusion`
  - `blackboxai/google/imagen-3-fast`
  - Otros 20+ modelos de imagen

### Modelo Correcto (cuando esté disponible)
```python
# ANTES (incorrecto)
"model": "blackboxai/prunaai/flux.1-dev"

# AHORA (correcto)
"model": "blackboxai/black-forest-labs/flux-schnell"
```

---

## ✅ Solución Implementada

### Arquitectura de 3 Capas

```
┌─────────────────────────────────────────────┐
│   generate-images-unified.py               │
│   (Orquestador principal)                   │
├─────────────────────────────────────────────┤
│  1. Test disponibilidad IA                  │
│  2. Si OK → generate-images-ai.py           │
│  3. Si FALLA → generate-images-unsplash.py  │
└─────────────────────────────────────────────┘
```

### Nuevos Módulos

#### 1. `generate-images-unified.py` (Recomendado)
**Generador inteligente con fallback automático**

```python
from generate_images_unified import UnifiedImageGenerator

generator = UnifiedImageGenerator(
    output_dir='generated_images',
    prefer_ai=True  # Intenta IA primero
)

articles_with_images = generator.process_articles(articles)
```

**Features:**
- ✅ Test automático de disponibilidad de IA
- ✅ Fallback transparente a Unsplash
- ✅ Sin cambios en el código consumidor
- ✅ Logs claros del modo usado

#### 2. `generate-images-unsplash.py` (Nuevo)
**Generador confiable usando Unsplash API**

```python
from generate_images_unsplash import UnsplashImageGenerator

generator = UnsplashImageGenerator(output_dir='generated_images')
articles_with_images = generator.process_articles(articles)
```

**Features:**
- ✅ Gratuito (50 req/hora sin API key)
- ✅ Fallback a picsum.photos
- ✅ Imágenes 1200x600 profesionales
- ✅ Keywords automáticos desde título + categoría
- ✅ Sin autenticación requerida

#### 3. `generate-images-ai.py` (Actualizado)
**Generador IA (para cuando se reactive)**

- Corregido modelo: `blackboxai/black-forest-labs/flux-schnell`
- Nota documentada sobre balance agotado
- Listo para reactivarse cuando fal.ai esté disponible

---

## 🔄 Cambios en master_orchestrator.py

### Antes
```python
self.image_generator = AIImageGenerator()
```

### Ahora
```python
self.image_generator = UnifiedImageGenerator(prefer_ai=True)
```

**Beneficios:**
- Zero downtime por problemas de API externa
- Imágenes siempre generadas (IA o Unsplash)
- Transición transparente para el usuario

---

## 🧪 Testing

### Test 1: Verificar Unsplash
```bash
cd /home/sebastianvernis/news-prototype/Tecnología
python scripts/generate-images-unsplash.py
```

**Resultado esperado:**
```
🖼️  Generando imágenes desde Unsplash para N artículos
[1/N] Breaking News...
    🔍 Buscando: technology Breaking News
    📥 Descargando... ✅
```

### Test 2: Verificar Unified
```bash
python scripts/generate-images-unified.py
```

**Resultado esperado:**
```
🔍 Verificando disponibilidad de IA...
⚠️  IA no disponible: Balance agotado en fal.ai
✅ Modo: Unsplash (Free Stock Images)
```

### Test 3: Flujo completo
```bash
python scripts/master_orchestrator.py --usar-cache
```

---

## 📊 Comparativa de Soluciones

| Característica | IA (Flux) | Unsplash | PIL (Local) |
|----------------|-----------|----------|-------------|
| **Costo** | $0.003/img | Gratis | Gratis |
| **Calidad** | Alta (IA) | Alta (fotos) | Media (generado) |
| **Velocidad** | 5-10s | 2-3s | <1s |
| **Disponibilidad** | ❌ (balance agotado) | ✅ 99.9% | ✅ 100% |
| **API Key** | Requerida | Opcional | No |
| **Realismo** | Muy alto | Muy alto | Bajo |
| **Personalización** | Total | Media | Total |
| **Límites** | Balance | 50/hora | Ninguno |

---

## 🚀 Reactivar IA Cuando Esté Disponible

### Opción 1: Agregar balance a fal.ai
1. Ir a https://fal.ai/dashboard/billing
2. Agregar créditos
3. El sistema automáticamente usará IA de nuevo

### Opción 2: Cambiar a otro proveedor
```python
# En generate-images-ai.py, línea 86
payload = {
    # Probar otro proveedor si fal.ai sigue sin balance
    "model": "otro-proveedor/otro-modelo",
    ...
}
```

### Opción 3: Solo Unsplash (sin IA)
```python
# En master_orchestrator.py
self.image_generator = UnsplashImageGenerator()  # Directo sin unified
```

---

## 📝 Ventajas de la Solución

### 1. **Resiliencia**
- Sistema nunca falla por problemas externos
- Múltiples niveles de fallback

### 2. **Flexibilidad**
- Fácil cambiar entre IA/Unsplash/Local
- Un solo cambio de línea en código

### 3. **Transparencia**
- Logs claros del modo usado
- Usuario siempre informado

### 4. **Mantenibilidad**
- 3 módulos independientes
- Cada uno funcional por separado
- Fácil testear individualmente

---

## 🐛 Troubleshooting

### Problema: Unsplash devuelve 401
**Solución**: Usa modo demo (automático), fallback a picsum.photos

### Problema: Imágenes genéricas de picsum
**Solución**: Agregar UNSPLASH_ACCESS_KEY al .env
```bash
# .env
UNSPLASH_ACCESS_KEY="tu_api_key_de_unsplash"
```

### Problema: Quiero solo IA (sin fallback)
**Solución**: Usar directamente AIImageGenerator
```python
from generate_images_ai import AIImageGenerator
self.image_generator = AIImageGenerator()
```

---

## 📚 Referencias

### APIs Usadas
- **Blackbox AI**: https://docs.blackbox.ai/api-reference/models/image-models
- **Unsplash API**: https://unsplash.com/documentation
- **Picsum Photos**: https://picsum.photos (sin API key)

### Archivos Modificados
- `scripts/generate-images-ai.py` - Corregido modelo
- `scripts/generate-images-unsplash.py` - Nuevo
- `scripts/generate-images-unified.py` - Nuevo orquestador
- `scripts/master_orchestrator.py` - Usa unified generator

### Archivos sin Cambios
- `scripts/generate-images.py` - Generador local PIL (independiente)

---

## 🎯 Próximos Pasos (Opcional)

### Mejoras Futuras
1. **Cache de imágenes**: Evitar re-generar imágenes para mismo contenido
2. **Múltiples fuentes**: Agregar Pexels, Pixabay como alternativas
3. **Optimización**: Comprimir imágenes automáticamente
4. **Watermark**: Agregar atribución si requerido por Unsplash TOS

### Alternativas de IA
- **DALL-E 3**: Requiere OpenAI API key
- **Stability AI**: stable-diffusion-3.5 (cuando balance se reactive)
- **Midjourney**: Via API (próximamente)

---

**Estado**: ✅ Implementado y funcional  
**Prioridad**: Alta (sistema crítico)  
**Mantenedor**: Sistema automático con logs
