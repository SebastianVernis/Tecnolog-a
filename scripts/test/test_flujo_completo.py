#!/usr/bin/env python3
"""
Test del flujo completo con solo 2 artículos
Prueba rápida end-to-end del master orchestrator
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Agregar directorio padre al path
current_dir = Path(__file__).parent
scripts_dir = current_dir.parent
sys.path.insert(0, str(scripts_dir))

load_dotenv()

def test_flujo_completo():
    """
    Ejecuta el flujo completo con:
    - 2 artículos
    - 1 sitio
    - Sin verificación de dominios (más rápido)
    - Usa cache de noticias si existe
    """
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🧪 TEST DE FLUJO COMPLETO - 2 ARTÍCULOS                         ║
║  Master Orchestrator End-to-End Test                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar API keys necesarias
    print("🔑 Verificando API keys...")
    required_keys = {
        'NEWSAPI_KEY': os.getenv('NEWSAPI_KEY'),
        'BLACKBOX_API_KEY': os.getenv('BLACKBOX_API_KEY')
    }
    
    missing_keys = []
    for key_name, key_value in required_keys.items():
        if not key_value:
            missing_keys.append(key_name)
            print(f"   ❌ {key_name}: NO ENCONTRADA")
        else:
            print(f"   ✅ {key_name}: Configurada")
    
    if missing_keys:
        print(f"\n❌ Error: Faltan API keys: {', '.join(missing_keys)}")
        print("   Configura las variables en el archivo .env")
        return False
    
    # Importar master orchestrator
    try:
        from master_orchestrator import MasterOrchestrator
        print("\n✅ Master Orchestrator importado correctamente")
    except Exception as e:
        print(f"\n❌ Error importando Master Orchestrator: {e}")
        return False
    
    # Crear directorio de salida para tests
    test_output_dir = scripts_dir.parent / "generated_sites_test"
    test_output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Directorio de salida: {test_output_dir}")
    print("\n" + "="*70)
    print("🚀 INICIANDO FLUJO COMPLETO")
    print("="*70)
    print("Configuración:")
    print("  - Artículos: 2")
    print("  - Sitios: 1")
    print("  - Verificar dominios: No")
    print("  - Usar cache: Sí (si existe)")
    print("="*70)
    
    try:
        # Crear orquestador
        orchestrator = MasterOrchestrator(output_base_dir=str(test_output_dir))
        
        # Modificar paso 1 para usar solo 2 noticias
        original_paso_1 = orchestrator.paso_1_descargar_noticias
        
        def paso_1_limitado(num_noticias=2, force_download=False):
            noticias = original_paso_1(num_noticias=num_noticias, force_download=force_download)
            return noticias[:2]  # Asegurar máximo 2
        
        orchestrator.paso_1_descargar_noticias = paso_1_limitado
        
        # Modificar paso 2 para procesar solo 2
        original_paso_2 = orchestrator.paso_2_parafrasear_noticias
        
        def paso_2_limitado(noticias):
            noticias_limitadas = noticias[:2]
            return original_paso_2(noticias_limitadas)
        
        orchestrator.paso_2_parafrasear_noticias = paso_2_limitado
        
        # Modificar paso 3 para generar solo 2 imágenes
        original_paso_3 = orchestrator.paso_3_generar_imagenes
        
        def paso_3_limitado(noticias, site_num):
            noticias_limitadas = noticias[:2]
            return original_paso_3(noticias_limitadas, site_num)
        
        orchestrator.paso_3_generar_imagenes = paso_3_limitado
        
        # Modificar paso 7 para generar solo 2 artículos
        original_paso_7 = orchestrator.paso_7_generar_sitios_html
        
        def paso_7_limitado(sites_metadata, noticias, imagenes, logos, templates_metadata):
            noticias_limitadas = noticias[:2]
            return original_paso_7(sites_metadata, noticias_limitadas, imagenes, logos, templates_metadata)
        
        orchestrator.paso_7_generar_sitios_html = paso_7_limitado
        
        # Ejecutar flujo (usa cache por defecto)
        inicio = time.time()
        resultado = orchestrator.ejecutar_flujo_completo(
            verificar_dominios=False,
            force_download=False  # Usar cache si existe
        )
        tiempo_total = time.time() - inicio
        
        # Verificar resultado
        if resultado.get('success'):
            print("\n" + "="*70)
            print("✅ FLUJO COMPLETADO EXITOSAMENTE")
            print("="*70)
            
            stats = resultado.get('stats', {})
            print(f"\n📊 Estadísticas:")
            print(f"   - Noticias procesadas: {stats.get('noticias_parafraseadas', 0)}")
            print(f"   - Imágenes generadas: {stats.get('imagenes_generadas', 0)}")
            print(f"   - Sitios creados: {stats.get('sitios_creados', 0)}")
            print(f"   - Tiempo total: {tiempo_total:.2f}s ({tiempo_total/60:.2f} min)")
            
            # Verificar archivos generados
            site_dir = test_output_dir / "site_1"
            if site_dir.exists():
                print(f"\n📁 Archivos generados en: {site_dir}")
                
                archivos_esperados = [
                    'index.html',
                    'style.css',
                    'article_1.html',
                    'article_2.html',
                    'terminos.html',
                    'privacidad.html',
                    'faqs.html',
                    'acerca.html',
                    'logo.jpg',
                    'images/news_1.jpg',
                    'images/news_2.jpg'
                ]
                
                print("\n✓ Verificando archivos:")
                for archivo in archivos_esperados:
                    file_path = site_dir / archivo
                    existe = file_path.exists()
                    icono = "✅" if existe else "❌"
                    print(f"   {icono} {archivo}")
                
                print(f"\n🌐 Para ver el sitio:")
                print(f"   cd {site_dir}")
                print(f"   python -m http.server 8001")
                print(f"   Abrir: http://localhost:8001")
            
            # Guardar resumen de test
            test_summary = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'success': True,
                'config': {
                    'articulos': 2,
                    'sitios': 1,
                    'verificar_dominios': False,
                    'usar_cache': True
                },
                'stats': stats,
                'tiempo_total_segundos': tiempo_total,
                'output_dir': str(test_output_dir)
            }
            
            summary_path = current_dir / 'test_flujo_completo_resultado.json'
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(test_summary, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Resumen guardado en: {summary_path}")
            
            return True
        else:
            print("\n" + "="*70)
            print("❌ FLUJO FALLÓ")
            print("="*70)
            error = resultado.get('error', 'Error desconocido')
            print(f"\nError: {error}")
            
            # Guardar error
            error_summary = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'success': False,
                'error': error,
                'stats': resultado.get('stats', {})
            }
            
            error_path = current_dir / 'test_flujo_completo_error.json'
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(error_summary, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Error guardado en: {error_path}")
            
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    success = test_flujo_completo()
    
    print("\n" + "="*70)
    if success:
        print("🎉 TEST COMPLETADO EXITOSAMENTE")
    else:
        print("❌ TEST FALLÓ")
    print("="*70)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
