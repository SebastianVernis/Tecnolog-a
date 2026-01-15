#!/usr/bin/env python3
"""
Test de Verificación de Todos los Módulos
Verifica que el master_orchestrator use correctamente los 16 módulos del sistema
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Agregar directorio padre al path
current_dir = Path(__file__).parent
scripts_dir = current_dir.parent
sys.path.insert(0, str(scripts_dir))

load_dotenv()


def verificar_imports():
    """Verifica que todos los módulos se importen correctamente"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🧪 VERIFICACIÓN DE MÓDULOS                                       ║
║  Test de Integración de 16 Módulos                               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📦 Verificando imports de módulos...\n")
    
    modulos = {}
    errores = []
    
    # Módulo 1: Master Orchestrator
    try:
        from master_orchestrator import MasterOrchestrator
        modulos['master_orchestrator'] = MasterOrchestrator
        print("✅ 1. master_orchestrator.py → MasterOrchestrator")
    except Exception as e:
        errores.append(f"❌ 1. master_orchestrator.py: {e}")
        print(errores[-1])
    
    # Módulo 2: NewsAPI
    try:
        sys.path.insert(0, str(scripts_dir / 'api'))
        from newsapi import fetch_newsapi
        modulos['newsapi'] = fetch_newsapi
        print("✅ 2. api/newsapi.py → fetch_newsapi")
    except Exception as e:
        errores.append(f"❌ 2. api/newsapi.py: {e}")
        print(errores[-1])
    
    # Módulo 3: NewsParaphraser
    try:
        from paraphrase import NewsParaphraser
        modulos['paraphrase'] = NewsParaphraser
        print("✅ 3. paraphrase.py → NewsParaphraser")
    except Exception as e:
        errores.append(f"❌ 3. paraphrase.py: {e}")
        print(errores[-1])
    
    # Módulo 4: ArticleExpander
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'article_expander',
            scripts_dir / 'article-expander.py'
        )
        article_expander = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(article_expander)
        modulos['article_expander'] = article_expander.ArticleExpander
        print("✅ 4. article-expander.py → ArticleExpander")
    except Exception as e:
        errores.append(f"❌ 4. article-expander.py: {e}")
        print(errores[-1])
    
    # Módulo 5: AIImageGenerator
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'generate_images_ai',
            scripts_dir / 'generate-images-ai.py'
        )
        generate_images = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generate_images)
        modulos['generate_images_ai'] = generate_images.AIImageGenerator
        print("✅ 5. generate-images-ai.py → AIImageGenerator")
    except Exception as e:
        errores.append(f"❌ 5. generate-images-ai.py: {e}")
        print(errores[-1])
    
    # Módulo 6: SiteNameGenerator
    try:
        from site_name_generator import SiteNameGenerator
        modulos['site_name_generator'] = SiteNameGenerator
        print("✅ 6. site_name_generator.py → SiteNameGenerator")
    except Exception as e:
        errores.append(f"❌ 6. site_name_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 7: DomainVerifier
    try:
        from domain_verifier import DomainVerifier
        modulos['domain_verifier'] = DomainVerifier
        print("✅ 7. domain_verifier.py → DomainVerifier")
    except Exception as e:
        errores.append(f"❌ 7. domain_verifier.py: {e}")
        print(errores[-1])
    
    # Módulo 8: SitePreCreation
    try:
        from site_pre_creation import SitePreCreation
        modulos['site_pre_creation'] = SitePreCreation
        print("✅ 8. site_pre_creation.py → SitePreCreation")
    except Exception as e:
        errores.append(f"❌ 8. site_pre_creation.py: {e}")
        print(errores[-1])
    
    # Módulo 9: ColorPaletteGenerator
    try:
        from color_palette_generator import ColorPaletteGenerator
        modulos['color_palette_generator'] = ColorPaletteGenerator
        print("✅ 9. color_palette_generator.py → ColorPaletteGenerator")
    except Exception as e:
        errores.append(f"❌ 9. color_palette_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 10: FontFamilyGenerator
    try:
        from font_family_generator import FontFamilyGenerator
        modulos['font_family_generator'] = FontFamilyGenerator
        print("✅ 10. font_family_generator.py → FontFamilyGenerator")
    except Exception as e:
        errores.append(f"❌ 10. font_family_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 11: LayoutCSSGenerator
    try:
        from layout_css_generator import LayoutCSSGenerator
        modulos['layout_css_generator'] = LayoutCSSGenerator
        print("✅ 11. layout_css_generator.py → LayoutCSSGenerator")
    except Exception as e:
        errores.append(f"❌ 11. layout_css_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 12: TemplateCombiner
    try:
        from template_combiner import TemplateCombiner
        modulos['template_combiner'] = TemplateCombiner
        print("✅ 12. template_combiner.py → TemplateCombiner")
    except Exception as e:
        errores.append(f"❌ 12. template_combiner.py: {e}")
        print(errores[-1])
    
    # Módulo 13: LayoutGenerator
    try:
        from layout_generator import LayoutGenerator
        modulos['layout_generator'] = LayoutGenerator
        print("✅ 13. layout_generator.py → LayoutGenerator")
    except Exception as e:
        errores.append(f"❌ 13. layout_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 14: HeaderGenerator
    try:
        from header_generator import HeaderGenerator
        modulos['header_generator'] = HeaderGenerator
        print("✅ 14. header_generator.py → HeaderGenerator")
    except Exception as e:
        errores.append(f"❌ 14. header_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 15: FooterGenerator
    try:
        from footer_generator import FooterGenerator
        modulos['footer_generator'] = FooterGenerator
        print("✅ 15. footer_generator.py → FooterGenerator")
    except Exception as e:
        errores.append(f"❌ 15. footer_generator.py: {e}")
        print(errores[-1])
    
    # Módulo 16: LegalPagesGenerator
    try:
        from legal_pages_generator import LegalPagesGenerator
        modulos['legal_pages_generator'] = LegalPagesGenerator
        print("✅ 16. legal_pages_generator.py → LegalPagesGenerator")
    except Exception as e:
        errores.append(f"❌ 16. legal_pages_generator.py: {e}")
        print(errores[-1])
    
    return modulos, errores


def verificar_instancias_orchestrator():
    """Verifica que MasterOrchestrator instancie todos los módulos"""
    print("\n" + "="*70)
    print("🔍 Verificando instancias en MasterOrchestrator...")
    print("="*70 + "\n")
    
    try:
        from master_orchestrator import MasterOrchestrator
        
        # Crear orquestador
        test_dir = scripts_dir.parent / "test_output_modules"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        orchestrator = MasterOrchestrator(output_base_dir=str(test_dir))
        
        # Verificar atributos
        atributos_esperados = {
            'paraphraser': 'NewsParaphraser',
            'article_expander': 'ArticleExpander',
            'name_generator': 'SiteNameGenerator',
            'domain_verifier': 'DomainVerifier',
            'template_combiner': 'TemplateCombiner',
            'image_generator': 'AIImageGenerator',
            'layout_generator': 'LayoutGenerator',
            'legal_generator': 'LegalPagesGenerator'
        }
        
        verificados = 0
        faltantes = []
        
        for attr, clase in atributos_esperados.items():
            if hasattr(orchestrator, attr):
                obj = getattr(orchestrator, attr)
                print(f"✅ orchestrator.{attr} → {obj.__class__.__name__}")
                verificados += 1
            else:
                print(f"❌ orchestrator.{attr} → NO ENCONTRADO")
                faltantes.append(attr)
        
        print(f"\n📊 Resultado: {verificados}/{len(atributos_esperados)} instancias verificadas")
        
        if faltantes:
            print(f"❌ Faltantes: {', '.join(faltantes)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando instancias: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_uso_en_flujo():
    """Verifica que todos los módulos se usen en el flujo (directo o indirecto)"""
    print("\n" + "="*70)
    print("🔄 Verificando uso de módulos en el flujo...")
    print("="*70 + "\n")
    
    try:
        from master_orchestrator import MasterOrchestrator
        
        # Leer el código del master_orchestrator
        orchestrator_file = scripts_dir / 'master_orchestrator.py'
        with open(orchestrator_file, 'r', encoding='utf-8') as f:
            codigo_orchestrator = f.read()
        
        # Leer código de módulos intermedios
        template_combiner_file = scripts_dir / 'template_combiner.py'
        with open(template_combiner_file, 'r', encoding='utf-8') as f:
            codigo_template = f.read()
        
        layout_generator_file = scripts_dir / 'layout_generator.py'
        with open(layout_generator_file, 'r', encoding='utf-8') as f:
            codigo_layout = f.read()
        
        # Buscar uso directo en orchestrator
        print("📊 Uso DIRECTO en master_orchestrator:")
        usos_directos = {
            'paso_1_descargar_noticias': 'NewsAPI',
            'self.paraphraser': 'NewsParaphraser',
            'self.article_expander': 'ArticleExpander',
            'self.image_generator': 'AIImageGenerator',
            'SitePreCreation': 'SitePreCreation',
            'self.template_combiner': 'TemplateCombiner',
            'self.layout_generator': 'LayoutGenerator',
            'self.legal_generator': 'LegalPagesGenerator'
        }
        
        encontrados_directos = 0
        for busqueda, descripcion in usos_directos.items():
            if busqueda in codigo_orchestrator:
                print(f"  ✅ {descripcion}")
                encontrados_directos += 1
            else:
                print(f"  ❌ {descripcion}")
        
        # Verificar uso indirecto (composición)
        print("\n📊 Uso INDIRECTO (vía composición):")
        
        usos_indirectos = []
        
        # SiteNameGenerator y DomainVerifier vía SitePreCreation
        site_pre_file = scripts_dir / 'site_pre_creation.py'
        with open(site_pre_file, 'r', encoding='utf-8') as f:
            codigo_site_pre = f.read()
        
        if 'SiteNameGenerator' in codigo_site_pre:
            print(f"  ✅ SiteNameGenerator (vía SitePreCreation)")
            usos_indirectos.append('SiteNameGenerator')
        
        if 'DomainVerifier' in codigo_site_pre:
            print(f"  ✅ DomainVerifier (vía SitePreCreation)")
            usos_indirectos.append('DomainVerifier')
        
        # ColorPaletteGenerator, FontFamilyGenerator, LayoutCSSGenerator vía TemplateCombiner
        if 'ColorPaletteGenerator' in codigo_template:
            print(f"  ✅ ColorPaletteGenerator (vía TemplateCombiner)")
            usos_indirectos.append('ColorPaletteGenerator')
        
        if 'FontFamilyGenerator' in codigo_template:
            print(f"  ✅ FontFamilyGenerator (vía TemplateCombiner)")
            usos_indirectos.append('FontFamilyGenerator')
        
        if 'LayoutCSSGenerator' in codigo_template:
            print(f"  ✅ LayoutCSSGenerator (vía TemplateCombiner)")
            usos_indirectos.append('LayoutCSSGenerator')
        
        # HeaderGenerator y FooterGenerator vía LayoutGenerator
        if 'HeaderGenerator' in codigo_layout:
            print(f"  ✅ HeaderGenerator (vía LayoutGenerator)")
            usos_indirectos.append('HeaderGenerator')
        
        if 'FooterGenerator' in codigo_layout:
            print(f"  ✅ FooterGenerator (vía LayoutGenerator)")
            usos_indirectos.append('FooterGenerator')
        
        total_modulos = len(usos_directos) + len(usos_indirectos)
        print(f"\n📊 Resultado:")
        print(f"  Uso directo: {encontrados_directos}/{len(usos_directos)}")
        print(f"  Uso indirecto: {len(usos_indirectos)}/7")
        print(f"  TOTAL: {encontrados_directos + len(usos_indirectos)}/16 módulos")
        
        return (encontrados_directos == len(usos_directos)) and (len(usos_indirectos) == 7)
        
    except Exception as e:
        print(f"❌ Error verificando uso: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_metodos_flujo():
    """Verifica que todos los pasos del flujo estén implementados"""
    print("\n" + "="*70)
    print("📋 Verificando métodos de flujo...")
    print("="*70 + "\n")
    
    try:
        from master_orchestrator import MasterOrchestrator
        
        test_dir = scripts_dir.parent / "test_output_modules"
        orchestrator = MasterOrchestrator(output_base_dir=str(test_dir))
        
        metodos_flujo = [
            ('paso_1_descargar_noticias', 'Descarga de noticias (NewsAPI)'),
            ('paso_2_parafrasear_noticias', 'Parafraseo + Expansión'),
            ('paso_3_generar_imagenes', 'Generación de imágenes AI'),
            ('paso_4_crear_metadata_sitios', 'Creación de metadata'),
            ('paso_5_generar_logos', 'Generación de logos'),
            ('paso_6_generar_templates_css', 'Generación de templates CSS'),
            ('paso_7_generar_sitios_html', 'Generación de HTML'),
            ('ejecutar_flujo_completo', 'Ejecución del flujo completo')
        ]
        
        verificados = 0
        faltantes = []
        
        for metodo, descripcion in metodos_flujo:
            if hasattr(orchestrator, metodo):
                print(f"✅ {metodo}() → {descripcion}")
                verificados += 1
            else:
                print(f"❌ {metodo}() → NO ENCONTRADO")
                faltantes.append(metodo)
        
        print(f"\n📊 Resultado: {verificados}/{len(metodos_flujo)} métodos implementados")
        
        if faltantes:
            print(f"❌ Faltantes: {', '.join(faltantes)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando métodos: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print("\n🚀 Iniciando verificación de módulos...\n")
    
    resultados = {
        'imports': False,
        'instancias': False,
        'uso_flujo': False,
        'metodos': False
    }
    
    # Test 1: Imports
    modulos, errores = verificar_imports()
    resultados['imports'] = len(errores) == 0
    
    # Test 2: Instancias en orchestrator
    if resultados['imports']:
        resultados['instancias'] = verificar_instancias_orchestrator()
    
    # Test 3: Uso en el flujo
    if resultados['instancias']:
        resultados['uso_flujo'] = verificar_uso_en_flujo()
    
    # Test 4: Métodos del flujo
    if resultados['instancias']:
        resultados['metodos'] = verificar_metodos_flujo()
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70 + "\n")
    
    tests = [
        ('Imports de módulos', resultados['imports']),
        ('Instancias en orchestrator', resultados['instancias']),
        ('Uso en el flujo', resultados['uso_flujo']),
        ('Métodos del flujo', resultados['metodos'])
    ]
    
    for nombre, resultado in tests:
        icono = "✅" if resultado else "❌"
        print(f"{icono} {nombre}")
    
    todos_ok = all(resultados.values())
    
    print("\n" + "="*70)
    if todos_ok:
        print("🎉 TODOS LOS MÓDULOS VERIFICADOS CORRECTAMENTE")
        print("✅ El sistema usa correctamente los 16 módulos")
    else:
        print("❌ VERIFICACIÓN FALLÓ")
        print("⚠️ Revisar errores arriba")
    print("="*70 + "\n")
    
    sys.exit(0 if todos_ok else 1)


if __name__ == '__main__':
    main()
