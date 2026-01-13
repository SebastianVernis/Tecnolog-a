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
    
    generate_images_module = import_module_from_file(
        'generate_images_ai',
        current_dir / 'generate-images-ai.py'
    )
    AIImageGenerator = generate_images_module.AIImageGenerator
    
    # Importar módulos con guiones bajos normalmente
    from paraphrase import NewsParaphraser
    from site_name_generator import SiteNameGenerator
    from domain_verifier import DomainVerifier
    from site_pre_creation import SitePreCreation
    from template_combiner import TemplateCombiner
    from layout_generator import LayoutGenerator
    
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
        self.image_generator = AIImageGenerator()
        self.layout_generator = LayoutGenerator()
        
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
        
        print(f"[{timestamp}] {prefix} {message}")
    
    def paso_1_descargar_noticias(self, num_noticias: int = 50) -> List[Dict]:
        """
        Paso 1: Descarga noticias desde APIs
        
        Args:
            num_noticias: Número de noticias a descargar
            
        Returns:
            Lista de noticias descargadas
        """
        self.log("=" * 70)
        self.log("PASO 1: Descargando Noticias", "PROGRESS")
        self.log("=" * 70)
        
        # Buscar archivo de noticias más reciente
        noticias_files = list(self.data_dir.glob("noticias_final_*.json"))
        if noticias_files:
            latest_file = max(noticias_files, key=lambda p: p.stat().st_mtime)
            self.log(f"Usando archivo existente: {latest_file.name}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                noticias = json.load(f)
            
            self.stats["noticias_descargadas"] = len(noticias)
            self.log(f"Cargadas {len(noticias)} noticias", "SUCCESS")
            return noticias[:num_noticias]
        else:
            self.log("No hay noticias disponibles. Ejecuta el scraper primero.", "ERROR")
            return []
    
    def paso_2_parafrasear_noticias(self, noticias: List[Dict], num_sitios: int) -> Dict[int, List[Dict]]:
        """
        Paso 2: Parafrasea cada noticia N veces (1 por sitio)
        
        Args:
            noticias: Lista de noticias originales
            num_sitios: Número de sitios a crear (variaciones por noticia)
            
        Returns:
            Dict[site_id -> List[noticias_parafraseadas]]
        """
        self.log("=" * 70)
        self.log("PASO 2: Parafraseando Noticias y Generando Artículos Completos", "PROGRESS")
        self.log("=" * 70)
        
        # Estructura: {site_id: [noticias_parafraseadas]}
        noticias_por_sitio = {i: [] for i in range(1, num_sitios + 1)}
        
        total_operaciones = len(noticias) * num_sitios
        contador = 0
        
        for noticia_idx, noticia in enumerate(noticias, 1):
            self.log(f"Procesando noticia {noticia_idx}/{len(noticias)}: {noticia.get('title', '')[:60]}...")
            
            for site_id in range(1, num_sitios + 1):
                contador += 1
                
                try:
                    # Parafrasear con estilo único
                    style_idx = (site_id - 1) % len(self.paraphraser.styles)
                    style = self.paraphraser.styles[style_idx]
                    
                    self.log(f"  [{contador}/{total_operaciones}] Sitio {site_id} - Estilo: {style}", "PROGRESS")
                    
                    # Parafrasear título y descripción
                    paraphrased = self.paraphraser.paraphrase_article(noticia, style=style)
                    
                    # Expandir a artículo completo
                    structure_idx = (site_id - 1) % len(self.article_expander.structures)
                    structure = self.article_expander.structures[structure_idx]
                    
                    full_article = self.article_expander.expand_article(
                        paraphrased,
                        target_words=800,
                        structure=structure
                    )
                    
                    # Combinar datos
                    article_data = {
                        **paraphrased,
                        "full_article": full_article,
                        "original_id": noticia.get('id', noticia_idx),
                        "site_id": site_id,
                        "style": style,
                        "structure": structure
                    }
                    
                    noticias_por_sitio[site_id].append(article_data)
                    self.stats["noticias_parafraseadas"] += 1
                    
                except Exception as e:
                    self.log(f"Error parafraseando para sitio {site_id}: {e}", "ERROR")
                    # Usar original como fallback
                    noticias_por_sitio[site_id].append({
                        **noticia,
                        "full_article": noticia.get('content', noticia.get('description', '')),
                        "original_id": noticia.get('id', noticia_idx),
                        "site_id": site_id
                    })
                
                # Rate limiting
                time.sleep(0.5)
        
        self.log(f"Parafraseado completado: {self.stats['noticias_parafraseadas']} variaciones generadas", "SUCCESS")
        return noticias_por_sitio
    
    def paso_3_generar_imagenes(self, noticias_por_sitio: Dict[int, List[Dict]]) -> Dict[int, Dict[str, str]]:
        """
        Paso 3: Genera 1 imagen por noticia parafraseada (ultra específica)
        
        Args:
            noticias_por_sitio: Noticias organizadas por sitio
            
        Returns:
            Dict[site_id -> Dict[article_id -> image_path]]
        """
        self.log("=" * 70)
        self.log("PASO 3: Generando Imágenes de Noticias", "PROGRESS")
        self.log("=" * 70)
        
        imagenes_por_sitio = {}
        
        for site_id, noticias in noticias_por_sitio.items():
            self.log(f"Generando imágenes para Sitio {site_id}...")
            
            site_images_dir = self.output_base_dir / f"site_{site_id}" / "images"
            site_images_dir.mkdir(parents=True, exist_ok=True)
            
            imagenes_por_sitio[site_id] = {}
            
            for idx, noticia in enumerate(noticias, 1):
                try:
                    # Crear prompt ultra específico
                    title = noticia.get('title', '')
                    description = noticia.get('description', '')
                    category = noticia.get('category', 'tecnología')
                    
                    prompt = f"""Professional news image for technology article: {title}. 
{description}. 
Style: Modern, clean, tech-focused. Category: {category}. 
High quality, photojournalistic, relevant to the specific topic. 
No text, no watermarks."""
                    
                    self.log(f"  [{idx}/{len(noticias)}] Generando imagen: {title[:50]}...", "PROGRESS")
                    
                    # Generar imagen
                    article_id = f"article_{site_id}_{idx}"
                    image_path = self.image_generator.generate_image(prompt, article_id, idx)
                    
                    # Mover a directorio del sitio
                    if image_path and Path(image_path).exists():
                        dest_path = site_images_dir / f"news_{idx}.jpg"
                        shutil.copy2(image_path, dest_path)
                        imagenes_por_sitio[site_id][article_id] = str(dest_path)
                        self.stats["imagenes_generadas"] += 1
                    
                except Exception as e:
                    self.log(f"Error generando imagen {idx}: {e}", "WARNING")
                
                # Rate limiting
                time.sleep(1)
        
        self.log(f"Generación de imágenes completada: {self.stats['imagenes_generadas']} imágenes", "SUCCESS")
        return imagenes_por_sitio
    
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
                                   noticias_por_sitio: Dict[int, List[Dict]],
                                   imagenes_por_sitio: Dict[int, Dict[str, str]],
                                   logos: Dict[int, str],
                                   templates_metadata: List[Dict]) -> List[str]:
        """
        Paso 7: Genera sitios HTML completos
        
        Args:
            sites_metadata: Metadata de sitios
            noticias_por_sitio: Noticias por sitio
            imagenes_por_sitio: Imágenes por sitio
            logos: Logos por sitio
            templates_metadata: Metadata de templates CSS
            
        Returns:
            Lista de paths de sitios generados
        """
        self.log("=" * 70)
        self.log("PASO 7: Generando Sitios HTML", "PROGRESS")
        self.log("=" * 70)
        
        sitios_generados = []
        
        for idx, metadata in enumerate(sites_metadata, 1):
            try:
                site_dir = self.output_base_dir / f"site_{idx}"
                site_dir.mkdir(parents=True, exist_ok=True)
                
                # Obtener datos
                noticias = noticias_por_sitio.get(idx, [])
                template_info = templates_metadata[idx - 1] if idx <= len(templates_metadata) else None
                
                self.log(f"  [{idx}/{len(sites_metadata)}] Generando: {metadata['nombre']}", "PROGRESS")
                
                # Generar HTML del sitio (index.html)
                index_html = self._generar_index_html(
                    metadata, noticias, template_info, idx
                )
                
                index_path = site_dir / "index.html"
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(index_html)
                
                # Generar páginas de artículos individuales
                self._generar_paginas_articulos(site_dir, noticias, metadata, template_info, idx)
                
                # Copiar CSS
                self._copiar_css(site_dir, idx)
                
                sitios_generados.append(str(index_path))
                self.stats["sitios_creados"] += 1
                
            except Exception as e:
                self.log(f"Error generando sitio {idx}: {e}", "ERROR")
        
        self.log(f"Sitios HTML generados: {len(sitios_generados)}", "SUCCESS")
        return sitios_generados
    
    def _generar_index_html(self, metadata: Dict, noticias: List[Dict], 
                           template_info: Dict, site_num: int) -> str:
        """Genera el HTML del index del sitio"""
        # Implementación simplificada - integrar con generate-sites.py
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['nombre']} - {metadata['tagline']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo-section">
                <img src="logo.jpg" alt="{metadata['nombre']}" class="logo-img">
                <div>
                    <h1 class="logo">{metadata['nombre']}</h1>
                    <p class="tagline">{metadata['tagline']}</p>
                </div>
            </div>
        </div>
    </header>
    
    <main class="main">
        <div class="container">
            <section class="news-grid">
"""
        
        for idx, noticia in enumerate(noticias[:12], 1):
            html += f"""                <article class="news-card">
                    <img src="images/news_{idx}.jpg" alt="{noticia.get('category', 'Noticia')}" class="card-image">
                    <div class="card-content">
                        <span class="category">{noticia.get('category', 'General').capitalize()}</span>
                        <h3 class="card-title"><a href="article_{idx}.html">{noticia.get('title', 'Título')}</a></h3>
                        <p class="card-excerpt">{noticia.get('description', '')[:150]}...</p>
                    </div>
                </article>
"""
        
        html += """            </section>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 {}</p>
        </div>
    </footer>
</body>
</html>""".format(metadata['nombre'])
        
        return html
    
    def _generar_paginas_articulos(self, site_dir: Path, noticias: List[Dict],
                                   metadata: Dict, template_info: Dict, site_num: int):
        """Genera páginas HTML individuales para cada artículo"""
        for idx, noticia in enumerate(noticias, 1):
            article_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{noticia.get('title', 'Artículo')} - {metadata['nombre']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo"><a href="index.html">{metadata['nombre']}</a></h1>
        </div>
    </header>
    
    <main class="main">
        <article class="article-full">
            <div class="container">
                <h1 class="article-title">{noticia.get('title', '')}</h1>
                <div class="article-meta">
                    <span class="category">{noticia.get('category', 'General')}</span>
                    <span class="author">Por {noticia.get('author', 'Redacción')}</span>
                    <span class="date">{noticia.get('published_at', '')}</span>
                </div>
                <img src="images/news_{idx}.jpg" alt="{noticia.get('title', '')}" class="article-image">
                <div class="article-content">
                    {noticia.get('full_article', noticia.get('content', noticia.get('description', '')))}
                </div>
            </div>
        </article>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; 2025 {metadata['nombre']}</p>
        </div>
    </footer>
</body>
</html>"""
            
            article_path = site_dir / f"article_{idx}.html"
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(article_html)
    
    def _copiar_css(self, site_dir: Path, site_num: int):
        """Copia el CSS del template al directorio del sitio"""
        css_source = self.templates_dir / "css" / f"template{site_num}.css"
        css_dest = site_dir / "style.css"
        
        if css_source.exists():
            shutil.copy2(css_source, css_dest)
    
    def ejecutar_flujo_completo(self, num_sitios: int = 5, 
                                verificar_dominios: bool = False) -> Dict:
        """
        Ejecuta el flujo completo de generación
        
        Args:
            num_sitios: Número de sitios a generar
            verificar_dominios: Si True, verifica disponibilidad de dominios
            
        Returns:
            Diccionario con resultados y estadísticas
        """
        self.log("=" * 70)
        self.log("🚀 INICIANDO FLUJO COMPLETO DE GENERACIÓN DE SITIOS")
        self.log("=" * 70)
        self.log(f"Run ID: {self.run_id}")
        self.log(f"Sitios a generar: {num_sitios}")
        self.log(f"Verificar dominios: {verificar_dominios}")
        
        try:
            # Paso 1: Descargar noticias
            noticias = self.paso_1_descargar_noticias(num_noticias=20)
            if not noticias:
                raise Exception("No hay noticias disponibles")
            
            # Paso 2: Parafrasear noticias (1 variación por sitio)
            noticias_por_sitio = self.paso_2_parafrasear_noticias(noticias, num_sitios)
            
            # Paso 3: Generar imágenes
            imagenes_por_sitio = self.paso_3_generar_imagenes(noticias_por_sitio)
            
            # Paso 4: Crear metadata de sitios
            sites_metadata = self.paso_4_crear_metadata_sitios(num_sitios, verificar_dominios)
            
            # Paso 5: Generar logos
            logos = self.paso_5_generar_logos(sites_metadata)
            
            # Paso 6: Generar templates CSS
            templates_metadata = self.paso_6_generar_templates_css(num_sitios)
            
            # Paso 7: Generar sitios HTML
            sitios_generados = self.paso_7_generar_sitios_html(
                sites_metadata, noticias_por_sitio, imagenes_por_sitio,
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
            self.log(f"Sitios creados: {self.stats['sitios_creados']}")
            self.log(f"Noticias parafraseadas: {self.stats['noticias_parafraseadas']}")
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
    
    parser = argparse.ArgumentParser(description="Master Orchestrator - Generación Completa de Sitios")
    parser.add_argument('--sitios', type=int, default=5, help='Número de sitios a generar')
    parser.add_argument('--verificar-dominios', action='store_true', help='Verificar disponibilidad de dominios')
    parser.add_argument('--output-dir', type=str, default='../generated_sites', help='Directorio de salida')
    
    args = parser.parse_args()
    
    # Crear orquestador
    orchestrator = MasterOrchestrator(output_base_dir=args.output_dir)
    
    # Ejecutar flujo
    resultado = orchestrator.ejecutar_flujo_completo(
        num_sitios=args.sitios,
        verificar_dominios=args.verificar_dominios
    )
    
    # Retornar código de salida
    sys.exit(0 if resultado["success"] else 1)


if __name__ == "__main__":
    main()
