#!/usr/bin/env python3
"""
Script de prueba para el Master Orchestrator
Ejecuta una generación completa con 1 sitio para validar el flujo
"""

import sys
import os

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from master_orchestrator import MasterOrchestrator


def main():
    """Ejecuta prueba del orquestador"""
    print("🧪 Prueba del Master Orchestrator")
    print("=" * 70)
    print("Configuración: 1 sitio, sin verificación de dominios")
    print("=" * 70)
    print()
    
    # Confirmar
    response = input("¿Continuar con la prueba? (s/n): ").lower()
    if response != 's':
        print("❌ Prueba cancelada")
        return
    
    print()
    
    # Crear orquestador
    orchestrator = MasterOrchestrator(output_base_dir="../test_output")
    
    # Ejecutar flujo con 1 sitio
    resultado = orchestrator.ejecutar_flujo_completo(
        num_sitios=1,
        verificar_dominios=False
    )
    
    # Mostrar resultados
    print()
    print("=" * 70)
    print("📊 RESULTADOS DE LA PRUEBA")
    print("=" * 70)
    
    if resultado["success"]:
        print("✅ Prueba exitosa")
        print(f"\nEstadísticas:")
        for key, value in resultado["stats"].items():
            if not key.startswith("tiempo"):
                print(f"  {key}: {value}")
        
        print(f"\nTiempo total: {resultado['stats']['tiempo_total_minutos']:.2f} minutos")
        print(f"Directorio de salida: {resultado['output_dir']}")
        
        if resultado.get("sitios_generados"):
            print(f"\nSitios generados:")
            for sitio in resultado["sitios_generados"]:
                print(f"  - {sitio}")
    else:
        print("❌ Prueba fallida")
        print(f"Error: {resultado.get('error', 'Desconocido')}")
    
    print()


if __name__ == "__main__":
    main()
