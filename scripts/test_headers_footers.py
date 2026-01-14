#!/usr/bin/env python3
"""
Script de prueba para validar integración de headers y footers
"""

import sys
from pathlib import Path

# Asegurar que se pueden importar los módulos
sys.path.insert(0, str(Path(__file__).parent))

from layout_generator import LayoutGenerator, HTMLLayoutBuilder

def test_integration():
    """Prueba la integración completa"""
    print("🧪 Probando integración de Headers y Footers\n")
    print("=" * 70)
    
    # Crear generador
    generator = LayoutGenerator()
    
    # Generar configuración
    print("\n1️⃣ Generando configuración de layout...")
    config = generator.generar_configuracion_layout()
    
    print(f"   Layout Type: {config['layout_type']}")
    print(f"   Header Style: {config['header_style']}")
    print(f"   Nav Style: {config['nav_style']}")
    print(f"   Footer Style: {config['footer_style']}")
    print(f"   Footer Columns: {config['footer_columns']}")
    print(f"   Sticky Header: {config['sticky_header']}")
    
    # Crear builder
    print("\n2️⃣ Creando HTMLLayoutBuilder...")
    builder = HTMLLayoutBuilder(config)
    
    # Configuración del sitio
    site_config = {
        "title": "Noticias Tech MX",
        "tagline": "Tecnología e Innovación"
    }
    
    categorias = ["Inicio", "Tecnología", "Startups", "Hardware", "Software", "IA"]
    
    # Generar header
    print("\n3️⃣ Generando Header...")
    header_html = builder.build_header(site_config, categorias)
    print(f"   ✅ Header generado ({len(header_html)} caracteres)")
    print("   Primeras líneas:")
    print("   " + "\n   ".join(header_html.split('\n')[:5]))
    
    # Generar footer
    print("\n4️⃣ Generando Footer...")
    footer_html = builder.build_footer(site_config, "modern_grid", 1)
    print(f"   ✅ Footer generado ({len(footer_html)} caracteres)")
    print("   Primeras líneas:")
    print("   " + "\n   ".join(footer_html.split('\n')[:5]))
    
    # Generar HTML completo de ejemplo
    print("\n5️⃣ Generando HTML completo de ejemplo...")
    
    clases_css = generator.generar_clases_css_dinamicas(config)
    
    html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['title']} - {site_config['tagline']}</title>
    <link rel="stylesheet" href="../templates/css/template1.css">
</head>
<body class="{clases_css['container']}">

{header_html}

    <main class="{clases_css['main']}">
        <div class="content-wrapper">
            <section class="{clases_css['featured']}">
                <h2>Sección de Noticias</h2>
                <p>Aquí irían las noticias destacadas...</p>
            </section>
        </div>
    </main>

{footer_html}
</body>
</html>
"""
    
    # Guardar ejemplo
    output_file = Path(__file__).parent.parent / "test_header_footer_output.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_completo)
    
    print(f"   ✅ HTML completo guardado en: {output_file}")
    print(f"   Tamaño total: {len(html_completo)} caracteres")
    
    print("\n" + "=" * 70)
    print("✅ Integración completada exitosamente!")
    print("\nPuedes abrir el archivo HTML generado para ver el resultado.")
    
    return True

if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
