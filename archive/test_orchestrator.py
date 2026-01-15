#!/usr/bin/env python3
"""
Test Orchestrator - Versión de test con solo 2 noticias
"""

import sys
from pathlib import Path

# Agregar directorio parent al path
sys.path.insert(0, str(Path(__file__).parent))

from master_orchestrator import MasterOrchestrator


def main():
    """Ejecuta test con 2 noticias"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Orchestrator - Generación con 2 noticias")
    parser.add_argument('--verificar-dominios', action='store_true', help='Verificar disponibilidad de dominios')
    parser.add_argument('--output-dir', type=str, default=None, help='Directorio de salida')
    
    args = parser.parse_args()
    
    # Crear orquestador
    orchestrator = MasterOrchestrator(output_base_dir=args.output_dir)
    
    # Ejecutar flujo completo
    print("\n🧪 MODO TEST: Generando sitio con 2 noticias\n")
    
    try:
        # Paso 1: Descargar noticias (solo 2)
        noticias = orchestrator.paso_1_descargar_noticias(num_noticias=2)
        if not noticias:
            raise Exception("No hay noticias disponibles")
        
        # Paso 2: Parafrasear noticias
        noticias_parafraseadas = orchestrator.paso_2_parafrasear_noticias(noticias)
        
        # Paso 3: Generar imágenes
        imagenes = orchestrator.paso_3_generar_imagenes(noticias_parafraseadas, 1)
        
        # Paso 4: Crear metadata del sitio
        sites_metadata = orchestrator.paso_4_crear_metadata_sitios(1, args.verificar_dominios)
        
        # Paso 5: Generar logo
        logos = orchestrator.paso_5_generar_logos(sites_metadata)
        
        # Paso 6: Generar template CSS
        templates_metadata = orchestrator.paso_6_generar_templates_css(1)
        
        # Paso 7: Generar sitio HTML
        sitios_generados = orchestrator.paso_7_generar_sitios_html(
            sites_metadata, noticias_parafraseadas, imagenes,
            logos, templates_metadata
        )
        
        # Calcular estadísticas finales
        import time
        tiempo_total = time.time() - orchestrator.stats["tiempo_inicio"]
        
        resultado = {
            "success": True,
            "run_id": orchestrator.run_id,
            "sitios_generados": sitios_generados,
            "stats": {
                **orchestrator.stats,
                "tiempo_total_segundos": tiempo_total,
                "tiempo_total_minutos": tiempo_total / 60
            },
            "output_dir": str(orchestrator.output_base_dir)
        }
        
        # Guardar resumen
        orchestrator._guardar_resumen(resultado)
        
        orchestrator.log("=" * 70)
        orchestrator.log("🎉 TEST COMPLETADO EXITOSAMENTE", "SUCCESS")
        orchestrator.log("=" * 70)
        orchestrator.log(f"Sitio creado: {orchestrator.stats['sitios_creados']}")
        orchestrator.log(f"Noticias procesadas: {orchestrator.stats['noticias_parafraseadas']}")
        orchestrator.log(f"Imágenes generadas: {orchestrator.stats['imagenes_generadas']}")
        orchestrator.log(f"Tiempo total: {tiempo_total/60:.2f} minutos")
        orchestrator.log(f"Directorio de salida: {orchestrator.output_base_dir}")
        
        sys.exit(0)
        
    except Exception as e:
        orchestrator.log(f"Error en el flujo: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
