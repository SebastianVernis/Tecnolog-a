# Sistema de Generación de Headers y Footers

Sistema modular para generar componentes de header y footer con múltiples variaciones para sitios de noticias.

## 📁 Archivos Creados

### Generadores
- **`scripts/header_generator.py`** - Generador modular de headers con 12 estilos diferentes
- **`scripts/footer_generator.py`** - Generador modular de footers con 10 estilos diferentes

### Estilos
- **`templates/css/header_footer_base.css`** - CSS base para todos los estilos de headers y footers

### Testing
- **`scripts/test_headers_footers.py`** - Script de prueba para validar la integración

## 🎨 Estilos de Header Disponibles

El `HeaderGenerator` ofrece 12 estilos distintos:

1. **centered** - Logo y tagline centrados, navegación debajo
2. **left_aligned** - Logo a la izquierda, navegación a la derecha
3. **split** - Logo izquierda, menú derecha, espacio entre ambos
4. **minimal** - Diseño minimalista con elementos esenciales
5. **bold** - Header grande y llamativo con tipografía bold
6. **stacked** - Logo, tagline y navegación apilados verticalmente
7. **floating** - Header transparente flotante sobre contenido
8. **compact** - Header delgado y compacto
9. **magazine_style** - Elegante estilo editorial de revista
10. **newspaper_banner** - Estilo banner de periódico tradicional
11. **modern_thin** - Header moderno ultra delgado
12. **boxed_header** - Header contenido en una caja con borde

## 🧭 Estilos de Navegación Disponibles

12 variaciones de navegación:

1. **horizontal** - Menú horizontal clásico
2. **horizontal_center** - Menú horizontal centrado
3. **hamburger** - Menú hamburguesa colapsable (mobile-friendly)
4. **sidebar_nav** - Navegación en sidebar
5. **mega_menu** - Mega menú con categorías expandidas
6. **dropdown** - Menú con submenús dropdown
7. **tabs** - Estilo pestañas
8. **pills** - Menú estilo botones pills
9. **vertical_stack** - Menú vertical apilado
10. **icon_menu** - Menú con iconos y texto
11. **sticky_nav** - Navegación que se mantiene visible al scroll
12. **offcanvas** - Menú lateral offcanvas (mobile-friendly)

## 🦶 Estilos de Footer Disponibles

El `FooterGenerator` ofrece 10 estilos:

1. **classic_4col** - Footer tradicional con 4 columnas
2. **modern_3col** - Footer moderno con 3 columnas balanceadas
3. **minimal_2col** - Footer minimalista con 2 columnas
4. **centered** - Footer con contenido centrado
5. **mega_footer** - Footer extenso con múltiples secciones (5 columnas)
6. **newsletter_focus** - Footer destacando suscripción a newsletter
7. **social_focus** - Footer destacando redes sociales
8. **compact** - Footer compacto de una sola línea
9. **split** - Footer dividido en secciones visuales
10. **boxed** - Footer contenido en una caja

## 🧩 Elementos Adicionales

### Header Elements
Los headers pueden incluir elementos adicionales:
- `search_bar` - Barra de búsqueda
- `social_links` - Enlaces a redes sociales
- `subscribe_button` - Botón de suscripción
- `date_time` - Fecha y hora actual
- `weather` - Widget de clima
- `language_selector` - Selector de idioma
- `user_menu` - Menú de usuario/login
- `breaking_news` - Ticker de noticias de última hora
- `ad_banner` - Banner publicitario

### Footer Sections
Los footers pueden incluir secciones:
- `about` - Acerca de nosotros con redes sociales
- `sections` - Enlaces a secciones del sitio
- `legal` - Términos, privacidad, etc.
- `contact` - Información de contacto
- `newsletter` - Formulario de suscripción
- `recent_posts` - Artículos recientes
- `categories` - Categorías del sitio
- `services` - Servicios ofrecidos
- `apps` - Enlaces a aplicaciones móviles

## 💻 Uso

### Uso Básico

```python
from header_generator import HeaderGenerator
from footer_generator import FooterGenerator

# Crear generadores
header_gen = HeaderGenerator()
footer_gen = FooterGenerator()

# Generar header
header_html = header_gen.generar_header(
    site_name="Mi Sitio de Noticias",
    tagline="Noticias confiables",
    categorias=["Inicio", "Nacional", "Internacional", "Deportes"],
    header_style="modern_thin",
    nav_style="horizontal_center",
    elementos_extra=["search_bar", "social_links"],
    sticky=True
)

# Generar footer
footer_html = footer_gen.generar_footer(
    site_name="Mi Sitio de Noticias",
    tagline="Noticias confiables",
    footer_style="modern_3col",
    include_social=True,
    include_newsletter=True
)
```

### Configuración Aleatoria

```python
# Generar configuración aleatoria
header_config = header_gen.generar_configuracion_aleatoria()
footer_config = footer_gen.generar_configuracion_aleatoria()

# Usar configuración
header_html = header_gen.generar_header(
    site_name="Mi Sitio",
    tagline="Tagline",
    categorias=["Cat1", "Cat2"],
    **header_config
)
```

### Integración con LayoutGenerator

El sistema está totalmente integrado con `layout_generator.py`:

```python
from layout_generator import LayoutGenerator, HTMLLayoutBuilder

# Generar configuración completa
generator = LayoutGenerator()
config = generator.generar_configuracion_layout()

# Construir HTML
builder = HTMLLayoutBuilder(config)
site_config = {"title": "Mi Sitio", "tagline": "Tagline"}
categorias = ["Cat1", "Cat2", "Cat3"]

header = builder.build_header(site_config, categorias)
footer = builder.build_footer(site_config, "modern_grid", 1)
```

## 🔧 Integración Completa

El sistema se integra automáticamente en el flujo de generación:

1. **LayoutGenerator** genera configuraciones que incluyen estilos de header/footer
2. **HTMLLayoutBuilder** utiliza los generadores modulares
3. **master_orchestrator.py** usa el builder para generar sitios completos

### Flujo de Generación

```
master_orchestrator.py
    ↓
layout_generator.generar_configuracion_layout()
    ↓ (incluye header_config, footer_config)
HTMLLayoutBuilder
    ↓
header_generator.generar_header()
footer_generator.generar_footer()
    ↓
HTML completo con header y footer personalizados
```

## 🎯 Características

### Headers
- ✅ 12 estilos de header
- ✅ 12 estilos de navegación
- ✅ 9 elementos adicionales opcionales
- ✅ Soporte para sticky headers
- ✅ Responsive design integrado
- ✅ Hamburger menu para móviles

### Footers
- ✅ 10 estilos de footer
- ✅ 1-5 columnas configurables
- ✅ 9 tipos de secciones
- ✅ Formularios de newsletter
- ✅ Enlaces sociales
- ✅ Información de layout/template
- ✅ Responsive design integrado

## 📱 Responsive

Todos los componentes son completamente responsive:

- **Desktop** (>768px): Layouts completos con todas las columnas
- **Tablet** (768px): Navegación colapsada, footers adaptados
- **Mobile** (<480px): Headers compactos, footers en columna única

## 🧪 Testing

Ejecutar pruebas de integración:

```bash
cd scripts
python3 test_headers_footers.py
```

Esto genera un archivo HTML de ejemplo con header y footer completos.

## 📦 CSS

Para usar los estilos, incluir el CSS base en los templates:

```html
<link rel="stylesheet" href="../templates/css/header_footer_base.css">
```

El CSS base define:
- Variables CSS customizables
- Estilos base para todos los componentes
- Variaciones de estilos
- Media queries responsive
- Transiciones y animaciones

## 🔄 Variables CSS Customizables

```css
:root {
    --header-height: 80px;
    --header-bg: #ffffff;
    --header-text: #333333;
    --nav-link-hover: #e74c3c;
    --footer-bg: #2c3e50;
    --footer-text: rgba(255, 255, 255, 0.8);
}
```

## 📊 Estadísticas

- **Headers**: 12 estilos × 12 nav styles = **144 combinaciones**
- **Footers**: 10 estilos × 5 configuraciones de columnas = **50 variaciones**
- **Total**: **7,200 combinaciones únicas** de header + footer

## 🚀 Próximas Mejoras

- [ ] Mega menus interactivos con JavaScript
- [ ] Animaciones de transición
- [ ] Dark mode automático
- [ ] A/B testing de layouts
- [ ] Analytics de engagement por estilo
- [ ] Personalización por usuario

## 📝 Notas

- Los generadores son **stateless** - cada llamada es independiente
- La configuración se puede serializar/deserializar para consistencia
- Los estilos CSS son modulares y no conflictivos
- Compatibilidad con todos los navegadores modernos

## 🤝 Contribuir

Para agregar nuevos estilos:

1. Agregar estilo al diccionario `HEADER_STYLES` o `FOOTER_STYLES`
2. Implementar lógica de generación HTML
3. Agregar estilos CSS correspondientes
4. Actualizar documentación

---

**Versión**: 1.0  
**Fecha**: Enero 2026  
**Autor**: Sistema de Generación Automática de Sitios
