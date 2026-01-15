#!/usr/bin/env python3
"""
Generador de Layouts Dinámicos para Sitios de Noticias
Crea estructuras HTML variadas con diferentes disposiciones y estilos
"""

import random
from typing import Dict, List, Optional
from header_generator import HeaderGenerator
from footer_generator import FooterGenerator


class LayoutGenerator:
    """Generador de layouts dinámicos para sitios de noticias"""
    
    # Tipos de layouts disponibles
    LAYOUT_TYPES = [
        "classic",           # Layout clásico de periódico
        "magazine",          # Estilo revista con grid
        "modern_cards",      # Tarjetas modernas
        "masonry",           # Layout tipo Pinterest
        "featured_sidebar",  # Destacado con sidebar
        "grid_equal",        # Grid de tamaños iguales
        "timeline",          # Línea de tiempo vertical
        "asymmetric",        # Asimétrico moderno
        "minimalist",        # Minimalista con mucho espacio blanco
        "full_width",        # Ancho completo sin márgenes
        "boxed",             # Contenedor en caja centrada
        "overlay",           # Con overlays de imágenes
        "split_screen",      # Pantalla dividida
        "newspaper_classic", # Periódico clásico multi-columna
        "blog_style",        # Estilo blog personal
        "editorial",         # Editorial de revista premium
        "portfolio",         # Estilo portafolio con galería
        "grid_mosaic",       # Mosaico dinámico
        "horizontal_scroll", # Scroll horizontal
        "vertical_list"      # Lista vertical simple
    ]
    
    # Posiciones de sidebar
    SIDEBAR_POSITIONS = ["left", "right", "none"]
    
    # Estilos de header
    HEADER_STYLES = [
        "centered",          # Logo centrado
        "left_aligned",      # Logo a la izquierda
        "split",             # Logo izq, menú der
        "minimal",           # Minimalista
        "bold",              # Audaz con mucho espacio
        "stacked",           # Logo y menú apilados
        "floating",          # Header flotante transparente
        "compact",           # Header compacto
        "magazine_style",    # Estilo revista elegante
        "newspaper_banner",  # Banner de periódico tradicional
        "modern_thin",       # Moderno y delgado
        "boxed_header"       # Header en caja contenida
    ]
    
    # Estilos de navegación
    NAV_STYLES = [
        "horizontal",        # Menú horizontal clásico
        "horizontal_center", # Menú horizontal centrado
        "hamburger",         # Menú hamburguesa
        "sidebar_nav",       # Navegación lateral
        "mega_menu",         # Mega menú con categorías
        "dropdown",          # Menú con dropdowns
        "tabs",              # Estilo pestañas
        "pills",             # Menú estilo pills/botones
        "vertical_stack",    # Menú vertical apilado
        "icon_menu",         # Menú con iconos
        "sticky_nav",        # Navegación pegajosa al scroll
        "offcanvas"          # Menú offcanvas lateral
    ]
    
    # Disposiciones de noticias destacadas
    FEATURED_LAYOUTS = [
        "hero_full",         # Hero a ancho completo
        "hero_split",        # Hero dividido 60/40
        "carousel",          # Carrusel de noticias
        "grid_featured",     # Grid de destacadas
        "stacked",           # Apiladas verticalmente
        "hero_slider",       # Slider de héroes
        "featured_3col",     # 3 columnas destacadas
        "big_small_grid",    # Una grande + varias pequeñas
        "overlay_cards",     # Tarjetas con overlay
        "video_hero",        # Hero con video de fondo
        "parallax",          # Efecto parallax
        "diagonal_split",    # División diagonal
        "magazine_spread",   # Diseño de revista doble página
        "minimal_hero",      # Hero minimalista
        "full_height_hero"   # Hero de altura completa
    ]
    
    def __init__(self):
        """Inicializa el generador"""
        self.used_combinations = set()
        self.header_gen = HeaderGenerator()
        self.footer_gen = FooterGenerator()
    
    def generar_configuracion_layout(self) -> Dict:
        """
        Genera una configuración completa de layout aleatoria
        
        Returns:
            dict: Configuración del layout
        """
        # Generar configuraciones de header y footer usando los nuevos generadores
        header_config = self.header_gen.generar_configuracion_aleatoria()
        footer_config = self.footer_gen.generar_configuracion_aleatoria()
        
        config = {
            "layout_type": random.choice(self.LAYOUT_TYPES),
            "sidebar_position": random.choice(self.SIDEBAR_POSITIONS),
            "header_style": header_config["header_style"],
            "nav_style": header_config["nav_style"],
            "header_elementos_extra": header_config.get("elementos_extra", []),
            "featured_layout": random.choice(self.FEATURED_LAYOUTS),
            "show_images": random.choice([True, True, True, False]),  # 75% probabilidad
            "news_per_row": random.choice([1, 2, 3, 4]),
            "show_sidebar_widgets": random.choice([True, False]),
            "footer_style": footer_config["footer_style"],
            "footer_columns": footer_config["num_columns"],
            "footer_include_social": footer_config["include_social"],
            "footer_include_newsletter": footer_config["include_newsletter"],
            "use_breadcrumbs": random.choice([True, False]),
            "sticky_header": header_config.get("sticky", False),
        }
        
        return config
    
    def randomizar_categorias(self, categorias: List[str]) -> List[str]:
        """
        Randomiza el orden de las categorías
        
        Args:
            categorias: Lista de categorías
            
        Returns:
            list: Categorías en orden aleatorio
        """
        # Mantener "Inicio" siempre primero
        if "Inicio" in categorias:
            otras = [c for c in categorias if c != "Inicio"]
            random.shuffle(otras)
            return ["Inicio"] + otras
        else:
            categorias_copy = categorias.copy()
            random.shuffle(categorias_copy)
            return categorias_copy
    
    def generar_distribucion_noticias(self, total_noticias: int) -> Dict:
        """
        Genera distribución de noticias en secciones
        
        Args:
            total_noticias: Cantidad total de noticias disponibles
            
        Returns:
            dict: Distribución de noticias
        """
        # Asegurar mínimos
        min_featured = 1
        min_main = 3
        min_sidebar = 2
        
        # Distribuir el resto
        featured = random.randint(min_featured, min(3, total_noticias))
        remaining = total_noticias - featured
        
        main = random.randint(min_main, min(12, remaining))
        remaining -= main
        
        sidebar = min(random.randint(min_sidebar, 5), remaining)
        
        return {
            "featured": featured,
            "main": main,
            "sidebar": sidebar,
            "layout_pattern": random.choice([
                "featured_top",      # Destacadas arriba
                "featured_mixed",    # Destacadas mezcladas
                "grid_uniform",      # Grid uniforme
                "masonry_style"      # Estilo masonry
            ])
        }
    
    def generar_estilos_widget_sidebar(self) -> List[Dict]:
        """
        Genera configuración de widgets para sidebar
        
        Returns:
            list: Lista de widgets configurados
        """
        widgets_disponibles = [
            {"tipo": "newsletter", "titulo": "Suscríbete", "prioridad": 1},
            {"tipo": "trending", "titulo": "Tendencias", "prioridad": 2},
            {"tipo": "categories", "titulo": "Categorías", "prioridad": 3},
            {"tipo": "social", "titulo": "Síguenos", "prioridad": 4},
            {"tipo": "recent", "titulo": "Recientes", "prioridad": 5},
            {"tipo": "tags", "titulo": "Etiquetas", "prioridad": 6},
        ]
        
        # Seleccionar 2-4 widgets aleatorios
        num_widgets = random.randint(2, 4)
        widgets_seleccionados = random.sample(widgets_disponibles, num_widgets)
        
        # Randomizar orden
        random.shuffle(widgets_seleccionados)
        
        return widgets_seleccionados
    
    def generar_clases_css_dinamicas(self, config: Dict) -> Dict[str, str]:
        """
        Genera clases CSS basadas en la configuración
        
        Args:
            config: Configuración del layout
            
        Returns:
            dict: Clases CSS para diferentes elementos
        """
        return {
            "container": f"container layout-{config['layout_type']}",
            "header": f"header header-{config['header_style']} {'sticky' if config.get('sticky_header') else ''}",
            "nav": f"nav nav-{config['nav_style']}",
            "main": f"main-content sidebar-{config['sidebar_position']}",
            "featured": f"featured-section layout-{config['featured_layout']}",
            "news_grid": f"news-grid cols-{config['news_per_row']}",
            "sidebar": f"sidebar position-{config['sidebar_position']}",
            "footer": f"footer cols-{config['footer_columns']}"
        }


class HTMLLayoutBuilder:
    """Constructor de HTML con layouts dinámicos"""
    
    def __init__(self, layout_config: Dict):
        """
        Inicializa el constructor
        
        Args:
            layout_config: Configuración del layout
        """
        self.config = layout_config
        self.generator = LayoutGenerator()
        self.header_gen = HeaderGenerator()
        self.footer_gen = FooterGenerator()
    
    def build_header(self, site_config: Dict, categorias: List[str], logo_path: str = None) -> str:
        """
        Construye el header según el estilo configurado usando HeaderGenerator
        
        Args:
            site_config: Configuración del sitio
            categorias: Lista de categorías
            logo_path: Ruta al archivo de logo (opcional)
            
        Returns:
            str: HTML del header
        """
        # Usar el generador modular de headers
        return self.header_gen.generar_header(
            site_name=site_config["title"],
            tagline=site_config["tagline"],
            categorias=categorias,
            header_style=self.config.get('header_style'),
            nav_style=self.config.get('nav_style'),
            elementos_extra=self.config.get('header_elementos_extra', []),
            sticky=self.config.get('sticky_header', False),
            logo_path=logo_path
        )
    
    def _build_nav(self, categorias: List[str], style: str, wrapper: bool = True, minimal: bool = False) -> str:
        """Construye la navegación según el estilo"""
        nav_class = f"nav nav-{style}"
        if minimal:
            nav_class += " nav-minimal"
        
        html = ""
        if wrapper:
            html += f'            <nav class="{nav_class}">\n'
        else:
            html += f'                <nav class="{nav_class}">\n'
        
        indent = "                " if wrapper else "                    "
        
        for categoria in categorias:
            html += f'{indent}<a href="#{categoria.lower()}" class="nav-link">{categoria}</a>\n'
        
        if wrapper:
            html += '            </nav>\n'
        else:
            html += '                </nav>\n'
        
        return html
    
    def build_featured_section(self, noticias: List[Dict]) -> str:
        """
        Construye sección de noticias destacadas
        
        Args:
            noticias: Lista de noticias destacadas
            
        Returns:
            str: HTML de la sección
        """
        layout = self.config['featured_layout']
        html = f'    <section class="featured-section layout-{layout}">\n'
        
        if layout == "hero_full":
            html += self._build_hero_full(noticias[0] if noticias else {})
        
        elif layout == "hero_split":
            html += self._build_hero_split(noticias)
        
        elif layout == "carousel":
            html += self._build_carousel(noticias)
        
        elif layout == "grid_featured":
            html += self._build_grid_featured(noticias)
        
        elif layout == "stacked":
            html += self._build_stacked(noticias)
        
        html += '    </section>\n\n'
        return html
    
    def _build_hero_full(self, noticia: Dict) -> str:
        """Hero a ancho completo"""
        if not noticia:
            return ""
        
        image = noticia.get('ai_image_path') or 'https://via.placeholder.com/1600x800'
        if image and not image.startswith('http'):
            image = f"../{image}"
        
        return f'''        <article class="hero-full">
            <div class="hero-image" style="background-image: url('{image}')"></div>
            <div class="hero-content">
                <span class="hero-category">{noticia.get('category', 'Destacado')}</span>
                <h2 class="hero-title">{noticia.get('title', '')}</h2>
                <p class="hero-excerpt">{noticia.get('description', '')[:200]}...</p>
                <div class="hero-meta">
                    <span>{noticia.get('author', 'Redacción')}</span>
                    <span>{noticia.get('published_at', '')}</span>
                </div>
            </div>
        </article>\n'''
    
    def _build_hero_split(self, noticias: List[Dict]) -> str:
        """Hero dividido 60/40"""
        html = '        <div class="hero-split-container">\n'
        
        if noticias:
            # Principal (60%)
            main = noticias[0]
            image = main.get('ai_image_path', 'https://via.placeholder.com/800x600')
            if image and not image.startswith('http'):
                image = f"../{image}"
            
            html += f'''            <article class="hero-main">
                <img src="{image}" alt="Destacado" style="max-height: 400px; width: 100%; object-fit: cover;">
                <div class="content">
                    <span class="category">{main.get('category', 'Destacado')}</span>
                    <h2>{main.get('title', '')}</h2>
                    <p>{main.get('description', '')[:150]}...</p>
                </div>
            </article>\n'''
        
        if len(noticias) > 1:
            # Secundarias (40%)
            html += '            <div class="hero-secondary">\n'
            for noticia in noticias[1:3]:
                image = noticia.get('ai_image_path') or 'https://via.placeholder.com/400x300'
                if image and not image.startswith('http'):
                    image = f"../{image}"
                
                html += f'''                <article class="hero-item">
                    <img src="{image}" alt="{noticia.get('category', '')}" style="max-height: 200px; width: 100%; object-fit: cover;">
                    <h3>{noticia.get('title', '')}</h3>
                </article>\n'''
            html += '            </div>\n'
        
        html += '        </div>\n'
        return html
    
    def _build_carousel(self, noticias: List[Dict]) -> str:
        """Carrusel de noticias"""
        html = '        <div class="carousel-container">\n'
        html += '            <div class="carousel-slides">\n'
        
        for noticia in noticias[:5]:
            image = noticia.get('ai_image_path') or 'https://via.placeholder.com/1200x600'
            if image and not image.startswith('http'):
                image = f"../{image}"
            
            html += f'''                <div class="carousel-slide">
                    <img src="{image}" alt="Slide" style="max-height: 450px; width: 100%; object-fit: cover;">
                    <div class="carousel-caption">
                        <h3>{noticia.get('title', '')}</h3>
                        <p>{noticia.get('description', '')[:100]}...</p>
                    </div>
                </div>\n'''
        
        html += '            </div>\n'
        html += '            <button class="carousel-prev">‹</button>\n'
        html += '            <button class="carousel-next">›</button>\n'
        html += '        </div>\n'
        return html
    
    def _build_grid_featured(self, noticias: List[Dict]) -> str:
        """Grid de noticias destacadas"""
        html = '        <div class="featured-grid">\n'
        
        for noticia in noticias[:4]:
            image = noticia.get('ai_image_path') or 'https://via.placeholder.com/600x400'
            if image and not image.startswith('http'):
                image = f"../{image}"
            
            html += f'''            <article class="featured-card">
                <img src="{image}" alt="{noticia.get('category', '')}" style="max-height: 250px; width: 100%; object-fit: cover;">
                <div class="card-content">
                    <span class="category">{noticia.get('category', 'General')}</span>
                    <h3>{noticia.get('title', '')}</h3>
                    <p>{noticia.get('description', '')[:120]}...</p>
                </div>
            </article>\n'''
        
        html += '        </div>\n'
        return html
    
    def _build_stacked(self, noticias: List[Dict]) -> str:
        """Noticias apiladas verticalmente"""
        html = '        <div class="stacked-featured">\n'
        
        for noticia in noticias[:3]:
            image = noticia.get('ai_image_path') or 'https://via.placeholder.com/1000x400'
            if image and not image.startswith('http'):
                image = f"../{image}"
            
            html += f'''            <article class="stacked-item">
                <img src="{image}" alt="{noticia.get('category', '')}" style="max-height: 300px; width: 100%; object-fit: cover;">
                <div class="stacked-content">
                    <span class="category">{noticia.get('category', 'General')}</span>
                    <h3>{noticia.get('title', '')}</h3>
                    <p>{noticia.get('description', '')}</p>
                    <span class="author">{noticia.get('author', 'Redacción')}</span>
                </div>
            </article>\n'''
        
        html += '        </div>\n'
        return html
    
    def build_news_grid(self, noticias: List[Dict], distribucion: Dict) -> str:
        """
        Construye grid de noticias principal
        
        Args:
            noticias: Lista de noticias
            distribucion: Configuración de distribución
            
        Returns:
            str: HTML del grid
        """
        layout_type = self.config['layout_type']
        cols = self.config['news_per_row']
        
        html = f'    <section class="news-section layout-{layout_type}">\n'
        html += '        <div class="container">\n'
        html += f'            <div class="news-grid cols-{cols}">\n'
        
        for noticia in noticias:
            html += self._build_news_card(noticia, layout_type)
        
        html += '            </div>\n'
        html += '        </div>\n'
        html += '    </section>\n\n'
        
        return html
    
    def _build_news_card(self, noticia: Dict, layout_type: str) -> str:
        """Construye una tarjeta de noticia"""
        image = noticia.get('ai_image_path') or 'https://via.placeholder.com/600x400'
        if image and not image.startswith('http'):
            image = f"../{image}"
        elif not image:
            image = 'https://via.placeholder.com/600x400'
        
        card_class = f"news-card layout-{layout_type}"
        
        if layout_type in ["magazine", "masonry"]:
            # Tarjetas con imagen arriba
            return f'''                <article class="{card_class}">
                    <img src="{image}" alt="{noticia.get('category', '')}" class="card-image" style="max-height: 220px; width: 100%; object-fit: cover;">
                    <div class="card-body">
                        <span class="card-category">{noticia.get('category', 'General')}</span>
                        <h3 class="card-title">{noticia.get('title', '')}</h3>
                        <p class="card-excerpt">{noticia.get('description', '')[:150]}...</p>
                        <div class="card-meta">
                            <span>{noticia.get('author', 'Redacción')}</span>
                            <span>{noticia.get('published_at', '')}</span>
                        </div>
                    </div>
                </article>\n'''
        
        elif layout_type == "timeline":
            # Layout línea de tiempo
            return f'''                <article class="{card_class}">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <span class="timeline-time">{noticia.get('published_at', '')}</span>
                        <h3>{noticia.get('title', '')}</h3>
                        <img src="{image}" alt="{noticia.get('category', '')}" style="max-height: 200px; width: 100%; object-fit: cover;">
                        <p>{noticia.get('description', '')[:120]}...</p>
                    </div>
                </article>\n'''
        
        else:
            # Tarjetas clásicas
            return f'''                <article class="{card_class}">
                    <div class="card-image-wrapper">
                        <img src="{image}" alt="{noticia.get('category', '')}" style="max-height: 240px; width: 100%; object-fit: cover;">
                        <span class="card-category-badge">{noticia.get('category', 'General')}</span>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">{noticia.get('title', '')}</h3>
                        <p class="card-text">{noticia.get('description', '')[:130]}...</p>
                        <div class="card-footer">
                            <span class="author">{noticia.get('author', 'Redacción')}</span>
                            <span class="date">{noticia.get('published_at', '')}</span>
                        </div>
                    </div>
                </article>\n'''
    
    def build_sidebar(self, noticias_sidebar: List[Dict], widgets: List[Dict]) -> str:
        """
        Construye sidebar con widgets
        
        Args:
            noticias_sidebar: Noticias para sidebar
            widgets: Configuración de widgets
            
        Returns:
            str: HTML del sidebar
        """
        if self.config['sidebar_position'] == 'none':
            return ""
        
        position = self.config['sidebar_position']
        html = f'    <aside class="sidebar sidebar-{position}">\n'
        
        for widget in widgets:
            html += self._build_widget(widget, noticias_sidebar)
        
        html += '    </aside>\n\n'
        return html
    
    def _build_widget(self, widget: Dict, noticias: List[Dict]) -> str:
        """Construye un widget específico"""
        tipo = widget['tipo']
        titulo = widget['titulo']
        
        html = f'        <div class="widget widget-{tipo}">\n'
        html += f'            <h3 class="widget-title">{titulo}</h3>\n'
        html += '            <div class="widget-content">\n'
        
        if tipo == "newsletter":
            html += '''                <p>Recibe las mejores noticias</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="Tu email" required>
                    <button type="submit">Suscribirse</button>
                </form>\n'''
        
        elif tipo == "trending":
            html += '                <ul class="trending-list">\n'
            for i, noticia in enumerate(noticias[:5], 1):
                html += f'                    <li><span class="rank">{i}</span> {noticia.get("title", "")[:60]}...</li>\n'
            html += '                </ul>\n'
        
        elif tipo == "recent":
            html += '                <ul class="recent-list">\n'
            for noticia in noticias[:4]:
                image = noticia.get('ai_image_path') or 'https://via.placeholder.com/100x75'
                if image and not image.startswith('http'):
                    image = f"../{image}"
                html += f'''                    <li>
                        <img src="{image}" alt="Reciente" style="max-width: 80px; max-height: 60px; object-fit: cover;">
                        <div>
                            <h4>{noticia.get("title", "")[:50]}...</h4>
                            <span>{noticia.get("published_at", "")}</span>
                        </div>
                    </li>\n'''
            html += '                </ul>\n'
        
        elif tipo == "social":
            html += '''                <div class="social-links">
                    <a href="#" class="social-link facebook">Facebook</a>
                    <a href="#" class="social-link twitter">Twitter</a>
                    <a href="#" class="social-link instagram">Instagram</a>
                    <a href="#" class="social-link youtube">YouTube</a>
                </div>\n'''
        
        elif tipo == "categories":
            categorias = ["Nacional", "Internacional", "Política", "Economía", "Tecnología", "Deportes"]
            html += '                <ul class="category-list">\n'
            for cat in categorias:
                html += f'                    <li><a href="#{cat.lower()}">{cat}</a></li>\n'
            html += '                </ul>\n'
        
        elif tipo == "tags":
            tags = ["Actualidad", "Análisis", "Opinión", "Reportaje", "Entrevista", "Internacional"]
            html += '                <div class="tags-cloud">\n'
            for tag in tags:
                html += f'                    <a href="#{tag.lower()}" class="tag">{tag}</a>\n'
            html += '                </div>\n'
        
        html += '            </div>\n'
        html += '        </div>\n\n'
        
        return html
    
    def build_footer(self, site_config: Dict, layout_info: Optional[str] = None, 
                    template_num: Optional[int] = None) -> str:
        """
        Construye el footer usando FooterGenerator
        
        Args:
            site_config: Configuración del sitio
            layout_info: Información del layout usado
            template_num: Número de template
            
        Returns:
            str: HTML del footer
        """
        # Usar el generador modular de footers
        return self.footer_gen.generar_footer(
            site_name=site_config["title"],
            tagline=site_config["tagline"],
            footer_style=self.config.get('footer_style'),
            include_social=self.config.get('footer_include_social', True),
            include_newsletter=self.config.get('footer_include_newsletter', False),
            layout_info=layout_info,
            template_num=template_num
        )


def main():
    """Función de prueba"""
    print("🎨 Generador de Layouts Dinámicos")
    print("=" * 60)
    
    generator = LayoutGenerator()
    
    # Generar 5 configuraciones diferentes
    print("\n📋 Generando 5 configuraciones de layout:\n")
    
    for i in range(1, 6):
        config = generator.generar_configuracion_layout()
        print(f"Layout {i}:")
        print(f"  Tipo: {config['layout_type']}")
        print(f"  Header: {config['header_style']}")
        print(f"  Navegación: {config['nav_style']}")
        print(f"  Destacados: {config['featured_layout']}")
        print(f"  Sidebar: {config['sidebar_position']}")
        print(f"  Noticias por fila: {config['news_per_row']}")
        print(f"  Columnas footer: {config['footer_columns']}")
        print()
    
    # Test de randomización de categorías
    categorias = ["Inicio", "Nacional", "Internacional", "Política", "Economía"]
    print("📂 Randomización de categorías:")
    print(f"Original: {categorias}")
    print(f"Random 1: {generator.randomizar_categorias(categorias.copy())}")
    print(f"Random 2: {generator.randomizar_categorias(categorias.copy())}")
    print(f"Random 3: {generator.randomizar_categorias(categorias.copy())}")


if __name__ == "__main__":
    main()
