#!/usr/bin/env python3
"""
Master Orchestrator - Flujo Completo de Generación de Sitios
Orquesta todo el proceso desde descarga de noticias hasta sitios completos
"""

import os
import json
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Importar módulos del proyecto
try:
    import importlib.util
    
    def import_module_from_file(module_name, file_path):
        """Importa un módulo desde un archivo con guiones en el nombre"""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        raise ImportError(f"No se pudo importar {module_name} desde {file_path}")
    
    # Obtener directorio actual
    current_dir = Path(__file__).parent
    
    # Importar módulos con guiones
    article_expander_module = import_module_from_file(
        'article_expander',
        current_dir / 'article-expander.py'
    )
    ArticleExpander = article_expander_module.ArticleExpander
    
    # Usar generador unificado (IA + fallback Unsplash)
    generate_images_unified_module = import_module_from_file(
        'generate_images_unified',
        current_dir / 'generate-images-unified.py'
    )
    UnifiedImageGenerator = generate_images_unified_module.UnifiedImageGenerator
    
    # Importar módulos con guiones bajos normalmente
    from paraphrase import NewsParaphraser
    from site_name_generator import SiteNameGenerator
    from domain_verifier import DomainVerifier
    from site_pre_creation import SitePreCreation
    from legal_pages_generator import LegalPagesGenerator
    from template_combiner import TemplateCombiner
    from layout_generator import LayoutGenerator, HTMLLayoutBuilder
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print(f"Directorio actual: {Path(__file__).parent}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

load_dotenv()


class MasterOrchestrator:
    """Orquestador principal del flujo completo de generación"""
    
    def __init__(self, output_base_dir: str = None):
        """
        Inicializa el orquestador
        
        Args:
            output_base_dir: Directorio base para sitios generados
        """
        # Usar rutas absolutas basadas en la ubicación del script
        script_dir = Path(__file__).parent
        base_dir = script_dir.parent
        
        if output_base_dir is None:
            self.output_base_dir = base_dir / "generated_sites"
        else:
            self.output_base_dir = Path(output_base_dir)
        
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Directorios de trabajo con rutas absolutas
        self.data_dir = base_dir / "data"
        self.templates_dir = base_dir / "templates"
        
        # Inicializar componentes
        self.paraphraser = NewsParaphraser()
        self.article_expander = ArticleExpander()
        self.name_generator = SiteNameGenerator()
        self.domain_verifier = DomainVerifier()
        self.template_combiner = TemplateCombiner()
        # Usar generador unificado (NewsAPI Original primero, luego fallbacks)
        self.image_generator = UnifiedImageGenerator(prefer_ai=False)
        self.layout_generator = LayoutGenerator()
        self.legal_generator = LegalPagesGenerator()
        
        # Timestamp para esta ejecución
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Estadísticas
        self.stats = {
            "noticias_descargadas": 0,
            "noticias_parafraseadas": 0,
            "imagenes_generadas": 0,
            "sitios_creados": 0,
            "tiempo_inicio": time.time()
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "PROGRESS": "🔄"
        }.get(level, "📝")
        
        print(f"[{timestamp}] {prefix} {message}", flush=True)
    
    def paso_1_descargar_noticias(self, num_noticias: int = 50, force_download: bool = False) -> List[Dict]:
        """
        Paso 1: Descarga noticias desde APIs
        
        Args:
            num_noticias: Número de noticias a descargar
            force_download: Forzar descarga en vivo incluso si hay archivos
            
        Returns:
            Lista de noticias descargadas
        """
        self.log("=" * 70)
        self.log("PASO 1: Descargando Noticias", "PROGRESS")
        self.log("=" * 70)
        
        # Si no se fuerza descarga, intentar usar archivo existente
        if not force_download:
            noticias_files = list(self.data_dir.glob("noticias_newsapi_*.json"))
            if noticias_files:
                latest_file = max(noticias_files, key=lambda p: p.stat().st_mtime)
                self.log(f"Usando archivo existente: {latest_file.name}")
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    noticias = json.load(f)
                
                self.stats["noticias_descargadas"] = len(noticias)
                self.log(f"Cargadas {len(noticias)} noticias originales", "SUCCESS")
                return noticias[:num_noticias]
        
        # Descargar noticias en vivo desde NewsAPI
        self.log("Descargando noticias en vivo desde NewsAPI...", "PROGRESS")
        
        try:
            # Importar el módulo de NewsAPI
            import sys
            from pathlib import Path
            api_dir = Path(__file__).parent / "api"
            if str(api_dir) not in sys.path:
                sys.path.insert(0, str(api_dir))
            
            from newsapi import fetch_newsapi
            
            # Descargar noticias
            noticias = fetch_newsapi(
                query='tecnología',
                language='es',
                page_size=num_noticias,
                enrich=True,
                silent=False
            )
            
            self.stats["noticias_descargadas"] = len(noticias)
            self.log(f"Descargadas {len(noticias)} noticias desde NewsAPI", "SUCCESS")
            return noticias
            
        except Exception as e:
            self.log(f"Error descargando noticias: {e}", "ERROR")
            return []
    
    def paso_2_parafrasear_noticias(self, noticias: List[Dict]) -> List[Dict]:
        """
        Paso 2: Parafrasea cada noticia 1 vez
        
        Args:
            noticias: Lista de noticias originales
            
        Returns:
            Lista de noticias parafraseadas
        """
        self.log("=" * 70)
        self.log("PASO 2: Parafraseando Noticias y Generando Artículos Completos", "PROGRESS")
        self.log("=" * 70)
        
        noticias_parafraseadas = []
        
        for noticia_idx, noticia in enumerate(noticias, 1):
            self.log(f"Procesando noticia {noticia_idx}/{len(noticias)}: {noticia.get('title', '')[:60]}...")
            
            try:
                # Parafrasear con estilo aleatorio
                style_idx = noticia_idx % len(self.paraphraser.styles)
                style = self.paraphraser.styles[style_idx]
                
                self.log(f"  [{noticia_idx}/{len(noticias)}] Estilo: {style}", "PROGRESS")
                
                # Parafrasear título y descripción
                paraphrased = self.paraphraser.paraphrase_article(noticia, style=style)
                
                # Expandir a artículo completo
                structure_idx = noticia_idx % len(self.article_expander.structures)
                structure = self.article_expander.structures[structure_idx]
                
                full_article = self.article_expander.expand_article(
                    paraphrased,
                    target_words=800,
                    structure=structure
                )
                
                # Combinar datos con autor aleatorio
                article_data = {
                    **paraphrased,
                    "full_article": full_article,
                    "original_id": noticia.get('id', noticia_idx),
                    "style": style,
                    "structure": structure,
                    "author": self.legal_generator.generar_autor_aleatorio()
                }
                
                noticias_parafraseadas.append(article_data)
                self.stats["noticias_parafraseadas"] += 1
                
            except Exception as e:
                self.log(f"Error parafraseando noticia {noticia_idx}: {e}", "ERROR")
                # Usar original como fallback con autor aleatorio
                noticias_parafraseadas.append({
                    **noticia,
                    "full_article": noticia.get('content', noticia.get('description', '')),
                    "original_id": noticia.get('id', noticia_idx),
                    "author": self.legal_generator.generar_autor_aleatorio()
                })
            
            # Rate limiting
            time.sleep(0.5)
        
        self.log(f"Parafraseado completado: {self.stats['noticias_parafraseadas']} artículos generados", "SUCCESS")
        return noticias_parafraseadas
    
    def paso_3_generar_imagenes(self, noticias: List[Dict], site_num: int) -> Dict[str, str]:
        """
        Paso 3: Genera 1 imagen por noticia
        
        Args:
            noticias: Lista de noticias parafraseadas
            site_num: Número del sitio
            
        Returns:
            Dict[article_id -> image_path]
        """
        self.log("=" * 70)
        self.log("PASO 3: Generando Imágenes de Noticias", "PROGRESS")
        self.log("=" * 70)
        
        site_images_dir = self.output_base_dir / f"site_{site_num}" / "images"
        site_images_dir.mkdir(parents=True, exist_ok=True)
        
        imagenes = {}
        
        for idx, noticia in enumerate(noticias, 1):
            try:
                # Preparar datos del artículo para generación de imagen
                title = noticia.get('title', '')
                description = noticia.get('description', '')
                category = noticia.get('category', 'tecnología')
                
                # Crear prompt (usado solo si IA está disponible)
                prompt = f"""Professional news image for technology article: {title}. 
{description}. 
Style: Modern, clean, tech-focused. Category: {category}. 
High quality, photojournalistic, relevant to the specific topic. 
No text, no watermarks."""
                
                self.log(f"  [{idx}/{len(noticias)}] Descargando imagen: {title[:50]}...", "PROGRESS")
                
                # Generar/descargar imagen (NewsAPI primero, luego fallbacks)
                article_id = f"article_{idx}"
                image_path = self.image_generator.generate_image(prompt, article_id, idx, article=noticia)
                
                # Mover a directorio del sitio
                if image_path and Path(image_path).exists():
                    dest_path = site_images_dir / f"news_{idx}.jpg"
                    shutil.copy2(image_path, dest_path)
                    imagenes[article_id] = str(dest_path)
                    self.stats["imagenes_generadas"] += 1
                
            except Exception as e:
                self.log(f"Error generando imagen {idx}: {e}", "WARNING")
            
            # Rate limiting
            time.sleep(1)
        
        self.log(f"Generación de imágenes completada: {self.stats['imagenes_generadas']} imágenes", "SUCCESS")
        return imagenes
    
    def paso_4_crear_metadata_sitios(self, num_sitios: int, verificar_dominios: bool = False) -> List[Dict]:
        """
        Paso 4: Genera nombre de sitio + verifica dominios + crea logo
        
        Args:
            num_sitios: Número de sitios a crear
            verificar_dominios: Si True, verifica disponibilidad de dominios
            
        Returns:
            Lista de metadatos de sitios
        """
        self.log("=" * 70)
        self.log("PASO 4: Creando Metadata de Sitios", "PROGRESS")
        self.log("=" * 70)
        
        protocolo = SitePreCreation(output_dir=str(self.data_dir / "sites_metadata"))
        
        sites_metadata = protocolo.crear_batch_sitios(
            cantidad=num_sitios,
            verificar_dominios=verificar_dominios,
            guardar_archivo=True
        )
        
        self.log(f"Metadata de {len(sites_metadata)} sitios creada", "SUCCESS")
        return sites_metadata
    
    def paso_5_generar_logos(self, sites_metadata: List[Dict]) -> Dict[int, str]:
        """
        Paso 5: Genera logos para cada sitio (prompts ultra específicos)
        
        Args:
            sites_metadata: Metadata de los sitios
            
        Returns:
            Dict[site_id -> logo_path]
        """
        self.log("=" * 70)
        self.log("PASO 5: Generando Logos de Sitios", "PROGRESS")
        self.log("=" * 70)
        
        logos = {}
        
        for idx, metadata in enumerate(sites_metadata, 1):
            try:
                site_name = metadata['nombre']
                tagline = metadata['tagline']
                domain = metadata['dominio']
                
                # Prompt ultra específico para logo
                prompt = f"""Professional minimalist logo for news website "{site_name}". 
Tagline: {tagline}. 
Style: Modern, clean, trustworthy, media company aesthetic. 
Simple icon or lettermark, tech-focused, credible news brand. 
Suitable for website header. No complex details. 
Colors: professional blue, black or modern gradient. 
Vector style, flat design, high contrast."""
                
                self.log(f"  [{idx}/{len(sites_metadata)}] Generando logo: {site_name}", "PROGRESS")
                
                # Generar logo
                logo_path = self.image_generator.generate_image(
                    prompt,
                    f"logo_site_{idx}",
                    1
                )
                
                # Mover a directorio del sitio
                if logo_path and Path(logo_path).exists():
                    site_dir = self.output_base_dir / f"site_{idx}"
                    site_dir.mkdir(parents=True, exist_ok=True)
                    dest_path = site_dir / "logo.jpg"
                    shutil.copy2(logo_path, dest_path)
                    logos[idx] = str(dest_path)
                
            except Exception as e:
                self.log(f"Error generando logo para sitio {idx}: {e}", "WARNING")
            
            time.sleep(1)
        
        self.log(f"Generación de logos completada: {len(logos)} logos", "SUCCESS")
        return logos
    
    def paso_6_generar_templates_css(self, num_sitios: int) -> List[Dict]:
        """
        Paso 6: Genera paleta + tipografía + layout y combina módulos
        
        Args:
            num_sitios: Número de templates a generar
            
        Returns:
            Lista de metadata de templates
        """
        self.log("=" * 70)
        self.log("PASO 6: Generando Templates CSS Modulares", "PROGRESS")
        self.log("=" * 70)
        
        # Generar templates únicos
        templates_metadata = self.template_combiner.generar_multiples_templates(
            num_templates=num_sitios,
            output_dir=str(self.templates_dir / "css"),
            aleatorio=True
        )
        
        self.log(f"Templates CSS generados: {len(templates_metadata)}", "SUCCESS")
        return templates_metadata
    
    def paso_7_generar_sitios_html(self, 
                                   sites_metadata: List[Dict],
                                   noticias: List[Dict],
                                   imagenes: Dict[str, str],
                                   logos: Dict[int, str],
                                   templates_metadata: List[Dict]) -> List[str]:
        """
        Paso 7: Genera sitio HTML completo
        
        Args:
            sites_metadata: Metadata del sitio
            noticias: Lista de noticias parafraseadas
            imagenes: Imágenes generadas
            logos: Logos generados
            templates_metadata: Metadata de templates CSS
            
        Returns:
            Lista de paths de sitios generados
        """
        self.log("=" * 70)
        self.log("PASO 7: Generando Sitio HTML", "PROGRESS")
        self.log("=" * 70)
        
        sitios_generados = []
        metadata = sites_metadata[0]
        idx = 1
        
        try:
            site_dir = self.output_base_dir / f"site_{idx}"
            site_dir.mkdir(parents=True, exist_ok=True)
            
            template_info = templates_metadata[0]
            logo_path = logos.get(idx)
            
            self.log(f"Generando: {metadata['nombre']}", "PROGRESS")
            
            # Generar HTML del sitio (index.html)
            index_html = self._generar_index_html(
                metadata, noticias, template_info, idx, logo_path
            )
            
            index_path = site_dir / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            # Generar páginas de artículos individuales
            self._generar_paginas_articulos(site_dir, noticias, metadata, template_info, idx, logo_path)
            
            # Generar páginas legales
            self._generar_paginas_legales(site_dir, metadata)
            
            # Copiar CSS
            self._copiar_css(site_dir, idx)
            
            sitios_generados.append(str(index_path))
            self.stats["sitios_creados"] += 1
            
        except Exception as e:
            self.log(f"Error generando sitio: {e}", "ERROR")
        
        self.log(f"Sitio HTML generado", "SUCCESS")
        return sitios_generados
    
    def _generar_index_html(self, metadata: Dict, noticias: List[Dict], 
                           template_info: Dict, site_num: int, logo_path: str = None) -> str:
        """Genera el HTML del index del sitio usando generadores modulares"""
        
        # Generar configuración de layout
        layout_config = self.layout_generator.generar_configuracion_layout()
        
        # Crear builder con la configuración
        builder = HTMLLayoutBuilder(layout_config)
        
        # Configuración del sitio
        site_config = {
            "title": metadata['nombre'],
            "tagline": metadata['tagline']
        }
        
        # Obtener categorías de las noticias
        categorias_set = set()
        for noticia in noticias:
            cat = noticia.get('category', 'General')
            if cat:
                categorias_set.add(cat.capitalize())
        categorias = ["Inicio"] + sorted(list(categorias_set))[:6]  # Limitar a 7 categorías
        
        # Generar componentes usando los nuevos generadores
        header_html = builder.build_header(site_config, categorias, logo_path)
        
        # Obtener información del layout para el footer
        layout_info = layout_config.get('layout_type', 'default')
        footer_html = builder.build_footer(site_config, layout_info, site_num)
        
        # Generar sección de noticias
        clases_css = self.layout_generator.generar_clases_css_dinamicas(layout_config)
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['nombre']} - {metadata['tagline']}</title>
    <link rel="stylesheet" href="style.css">
    <meta name="description" content="{metadata['tagline']}">
    <meta name="layout" content="{layout_info}">
</head>
<body class="{clases_css['container']}">

{header_html}

    <main class="{clases_css['main']}">
        <div class="content-wrapper">
    <section class="{clases_css['featured']}">
    </section>

    <section class="news-section {layout_info}">
        <div class="container">
            <div class="{clases_css['news_grid']}">
"""
        
        for idx, noticia in enumerate(noticias[:12], 1):
            image_path = f"images/news_{idx}.jpg"
            html += f"""                <article class="news-card {layout_info}">
                    <div class="card-image-wrapper">
                        <img src="{image_path}" alt="" style="max-height: 240px; width: 100%; object-fit: cover;">
                        <span class="card-category-badge">{noticia.get('category', 'General')}</span>
                    </div>
                    <div class="card-content">
                        <h3 class="card-title"><a href="article_{idx}.html">{noticia.get('title', '')}</a></h3>
                        <p class="card-text">{noticia.get('description', '')[:130]}...</p>
                        <div class="card-footer">
                            <span class="author">{noticia.get('author', 'Redacción')}</span>
                            <span class="date">{noticia.get('published_at', '')}</span>
                        </div>
                    </div>
                </article>
"""
        
        html += f"""            </div>
        </div>
    </section>

        </div>
    </main>

{footer_html}
</body>
</html>
"""
        
        return html
    
    def _generar_sidebar_articulos(self, otras_noticias: List[Dict], metadata: Dict) -> str:
        """
        Genera sidebar con miniaturas de otros artículos
        
        Args:
            otras_noticias: Lista de otras noticias con índices
            metadata: Metadata del sitio
            
        Returns:
            str: HTML del sidebar
        """
        items_html = []
        for i, noticia in enumerate(otras_noticias):
            # Usar el índice de la noticia original si existe
            article_idx = noticia.get('_display_index', i + 1)
            title = noticia.get('title', '')
            title_truncated = title if len(title) <= 80 else title[:80] + '...'
            
            items_html.append(f"""
                    <article class="sidebar-article">
                        <a href="article_{article_idx}.html" class="sidebar-article-link">
                            <div class="sidebar-article-image">
                                <img src="images/news_{article_idx}.jpg" alt="{title[:50]}">
                                <span class="sidebar-category">{noticia.get('category', 'General')}</span>
                            </div>
                            <div class="sidebar-article-content">
                                <h3 class="sidebar-article-title">{title_truncated}</h3>
                                <span class="sidebar-article-date">{noticia.get('published_at', '')[:10]}</span>
                            </div>
                        </a>
                    </article>""")
        
        sidebar_html = f"""
                <aside class="article-sidebar">
                    <div class="sidebar-section">
                        <h2 class="sidebar-title">Más Noticias</h2>
                        <div class="sidebar-articles">
{''.join(items_html)}
                        </div>
                    </div>
                    
                    <div class="sidebar-section sidebar-newsletter">
                        <h3>Suscríbete</h3>
                        <p>Recibe las últimas noticias en tu correo</p>
                        <form class="newsletter-form">
                            <input type="email" placeholder="Tu email" required>
                            <button type="submit">Suscribirse</button>
                        </form>
                    </div>
                </aside>"""
        
        return sidebar_html
    
    def _formatear_contenido_html(self, texto: str) -> str:
        """
        Convierte texto plano en HTML con estructura semántica y marcado
        """
        if not texto:
            return ""
        
        # Dividir por líneas vacías (doble salto de línea)
        parrafos = texto.strip().split('\n\n')
        
        # Envolver cada párrafo en tags <p> con clases semánticas
        html_parrafos = []
        for i, parrafo in enumerate(parrafos):
            parrafo = parrafo.strip()
            if parrafo:
                # Limpiar saltos de línea internos y espacios múltiples
                parrafo = ' '.join(parrafo.split())
                
                # Primer párrafo como lead/intro
                if i == 0:
                    html_parrafos.append(f'<p class="lead">{parrafo}</p>')
                else:
                    html_parrafos.append(f'<p>{parrafo}</p>')
        
        return '\n                    '.join(html_parrafos)
    
    def _generar_paginas_articulos(self, site_dir: Path, noticias: List[Dict],
                                   metadata: Dict, template_info: Dict, site_num: int, logo_path: str = None):
        """Genera páginas HTML individuales para cada artículo con sidebar"""
        for idx, noticia in enumerate(noticias, 1):
            # Generar sidebar con otros artículos (excluyendo el actual)
            otras_noticias = []
            for i, n in enumerate(noticias, 1):
                if i != idx:
                    n_copy = n.copy()
                    n_copy['_display_index'] = i
                    otras_noticias.append(n_copy)
            
            sidebar_html = self._generar_sidebar_articulos(otras_noticias[:6], metadata)
            
            article_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{noticia.get('title', 'Artículo')} - {metadata['nombre']}</title>
    <link rel="stylesheet" href="style.css">
    <meta name="description" content="{noticia.get('description', '')[:150]}">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-branding">
                {'<img src="logo.jpg" alt="' + metadata['nombre'] + '" class="logo-img">' if logo_path else ''}
                <h1 class="logo"><a href="index.html">{metadata['nombre']}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="main article-page">
        <div class="container">
            <div class="article-layout">
                <article class="article-full">
                    <header class="article-header">
                        <div class="article-category-badge">{noticia.get('category', 'General')}</div>
                        <h1 class="article-title">{noticia.get('title', '')}</h1>
                        <div class="article-meta">
                            <span class="author">Por {noticia.get('author', 'Redacción')}</span>
                            <span class="separator">•</span>
                            <time class="date">{noticia.get('published_at', '')}</time>
                        </div>
                    </header>
                    
                    <figure class="article-image-wrapper">
                        <img src="images/news_{idx}.jpg" alt="{noticia.get('title', '')}" class="article-image">
                    </figure>
                    
                    <div class="article-content">
                    {self._formatear_contenido_html(noticia.get('full_article', noticia.get('content', noticia.get('description', ''))))}
                    </div>
                    
                    <footer class="article-footer">
                        <div class="article-tags">
                            <span class="tag">{noticia.get('category', 'General')}</span>
                        </div>
                        <div class="article-share">
                            <span>Compartir:</span>
                            <a href="#" class="share-link">Facebook</a>
                            <a href="#" class="share-link">Twitter</a>
                            <a href="#" class="share-link">WhatsApp</a>
                        </div>
                    </footer>
                </article>
                
                {sidebar_html}
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; 2026 {metadata['nombre']}</p>
        </div>
    </footer>
</body>
</html>"""
            
            article_path = site_dir / f"article_{idx}.html"
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(article_html)
    
    def _generar_paginas_legales(self, site_dir: Path, metadata: Dict):
        """
        Genera páginas legales (Términos, Privacidad, FAQs, Acerca de)
        
        Args:
            site_dir: Directorio del sitio
            metadata: Metadata del sitio
        """
        site_name = metadata['nombre']
        domain = metadata['dominio']
        tagline = metadata['tagline']
        
        # Generar Términos y Condiciones
        terms_html = self.legal_generator.generar_terminos_condiciones(site_name, domain)
        terms_path = site_dir / "terminos.html"
        with open(terms_path, 'w', encoding='utf-8') as f:
            f.write(terms_html)
        
        # Generar Política de Privacidad
        privacy_html = self.legal_generator.generar_politica_privacidad(site_name, domain)
        privacy_path = site_dir / "privacidad.html"
        with open(privacy_path, 'w', encoding='utf-8') as f:
            f.write(privacy_html)
        
        # Generar FAQs
        faqs_html = self.legal_generator.generar_faqs(site_name)
        faqs_path = site_dir / "faqs.html"
        with open(faqs_path, 'w', encoding='utf-8') as f:
            f.write(faqs_html)
        
        # Generar Acerca de
        about_html = self.legal_generator.generar_acerca_de(site_name, tagline, domain)
        about_path = site_dir / "acerca.html"
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(about_html)
    
    def _copiar_css(self, site_dir: Path, site_num: int):
        """Copia el CSS del template al directorio del sitio"""
        css_source = self.templates_dir / "css" / f"template{site_num}.css"
        css_dest = site_dir / "style.css"
        
        if css_source.exists():
            shutil.copy2(css_source, css_dest)
    
    def ejecutar_flujo_completo(self, verificar_dominios: bool = False, force_download: bool = True) -> Dict:
        """
        Ejecuta el flujo completo de generación
        
        Args:
            verificar_dominios: Si True, verifica disponibilidad de dominios
            force_download: Si True, descarga noticias en vivo desde NewsAPI
            
        Returns:
            Diccionario con resultados y estadísticas
        """
        self.log("=" * 70)
        self.log("🚀 INICIANDO FLUJO COMPLETO DE GENERACIÓN DE SITIO")
        self.log("=" * 70)
        self.log(f"Run ID: {self.run_id}")
        self.log(f"Verificar dominios: {verificar_dominios}")
        self.log(f"Descarga en vivo: {force_download}")
        
        try:
            # Paso 1: Descargar noticias
            noticias = self.paso_1_descargar_noticias(num_noticias=20, force_download=force_download)
            if not noticias:
                raise Exception("No hay noticias disponibles")
            
            # Paso 2: Parafrasear noticias (1 vez cada una)
            noticias_parafraseadas = self.paso_2_parafrasear_noticias(noticias)
            
            # Paso 3: Generar imágenes
            imagenes = self.paso_3_generar_imagenes(noticias_parafraseadas, 1)
            
            # Paso 4: Crear metadata del sitio
            sites_metadata = self.paso_4_crear_metadata_sitios(1, verificar_dominios)
            
            # Paso 5: Generar logo
            logos = self.paso_5_generar_logos(sites_metadata)
            
            # Paso 6: Generar template CSS
            templates_metadata = self.paso_6_generar_templates_css(1)
            
            # Paso 7: Generar sitio HTML
            sitios_generados = self.paso_7_generar_sitios_html(
                sites_metadata, noticias_parafraseadas, imagenes,
                logos, templates_metadata
            )
            
            # Calcular estadísticas finales
            tiempo_total = time.time() - self.stats["tiempo_inicio"]
            
            resultado = {
                "success": True,
                "run_id": self.run_id,
                "sitios_generados": sitios_generados,
                "stats": {
                    **self.stats,
                    "tiempo_total_segundos": tiempo_total,
                    "tiempo_total_minutos": tiempo_total / 60
                },
                "output_dir": str(self.output_base_dir)
            }
            
            # Guardar resumen
            self._guardar_resumen(resultado)
            
            self.log("=" * 70)
            self.log("🎉 FLUJO COMPLETADO EXITOSAMENTE", "SUCCESS")
            self.log("=" * 70)
            self.log(f"Sitio creado: {self.stats['sitios_creados']}")
            self.log(f"Noticias procesadas: {self.stats['noticias_parafraseadas']}")
            self.log(f"Imágenes generadas: {self.stats['imagenes_generadas']}")
            self.log(f"Tiempo total: {tiempo_total/60:.2f} minutos")
            self.log(f"Directorio de salida: {self.output_base_dir}")
            
            return resultado
            
        except Exception as e:
            self.log(f"Error en el flujo: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "stats": self.stats
            }
    
    def _guardar_resumen(self, resultado: Dict):
        """Guarda un resumen de la ejecución"""
        resumen_path = self.output_base_dir / f"run_summary_{self.run_id}.json"
        with open(resumen_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Master Orchestrator - Generación Completa de Sitio")
    parser.add_argument('--verificar-dominios', action='store_true', help='Verificar disponibilidad de dominios')
    parser.add_argument('--output-dir', type=str, default=None, help='Directorio de salida')
    parser.add_argument('--usar-cache', action='store_true', help='Usar noticias en cache en lugar de descargar nuevas')
    
    args = parser.parse_args()
    
    # Crear orquestador
    orchestrator = MasterOrchestrator(output_base_dir=args.output_dir)
    
    # Ejecutar flujo (por defecto descarga en vivo)
    resultado = orchestrator.ejecutar_flujo_completo(
        verificar_dominios=args.verificar_dominios,
        force_download=not args.usar_cache
    )
    
    # Retornar código de salida
    sys.exit(0 if resultado["success"] else 1)


if __name__ == "__main__":
    main()
