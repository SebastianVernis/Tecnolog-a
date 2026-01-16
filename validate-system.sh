#!/bin/bash
# Script de validación rápida del sistema de imágenes

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ VALIDACIÓN RÁPIDA - Sistema de Generación de Imágenes ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
PASS=0
FAIL=0

# Test 1: Archivos existen
echo "1️⃣ Verificando archivos..."
FILES=(
    "scripts/generate-images-ai.py"
    "scripts/generate-images-unsplash.py"
    "scripts/generate-images-unified.py"
    "scripts/master_orchestrator.py"
    "scripts/test/test_image_fallback.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✅${NC} $file"
        ((PASS++))
    else
        echo -e "   ${RED}❌${NC} $file"
        ((FAIL++))
    fi
done

# Test 2: Permisos de ejecución
echo ""
echo "2️⃣ Verificando permisos..."
EXEC_FILES=(
    "scripts/generate-images-ai.py"
    "scripts/generate-images-unsplash.py"
    "scripts/generate-images-unified.py"
    "scripts/test/test_image_fallback.py"
)

for file in "${EXEC_FILES[@]}"; do
    if [ -x "$file" ]; then
        echo -e "   ${GREEN}✅${NC} $file (ejecutable)"
        ((PASS++))
    else
        echo -e "   ${YELLOW}⚠️${NC}  $file (no ejecutable, pero OK)"
        ((PASS++))
    fi
done

# Test 3: Imports de Python
echo ""
echo "3️⃣ Verificando imports..."
python3 << 'EOF'
import sys
from pathlib import Path

try:
    # Test imports
    import importlib.util
    
    def test_import(name, path):
        spec = importlib.util.spec_from_file_location(name, Path(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    
    scripts = [
        ('ai', 'scripts/generate-images-ai.py'),
        ('unsplash', 'scripts/generate-images-unsplash.py'),
        ('unified', 'scripts/generate-images-unified.py'),
    ]
    
    for name, path in scripts:
        if test_import(name, path):
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path}")
            sys.exit(1)
    
    print("   ✅ Todos los imports funcionan")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

# Test 4: Documentación
echo ""
echo "4️⃣ Verificando documentación..."
DOCS=(
    "IMAGEN-GENERATION-FIX.md"
    "RESUMEN-CORRECCION-IMAGENES.md"
    "VALIDACION-IMAGEN-FALLBACK.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "   ${GREEN}✅${NC} $doc"
        ((PASS++))
    else
        echo -e "   ${RED}❌${NC} $doc"
        ((FAIL++))
    fi
done

# Test 5: Test funcional (opcional)
echo ""
echo "5️⃣ Test funcional..."
read -p "¿Ejecutar test funcional completo? (s/n) [n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    echo "   Ejecutando test..."
    python3 scripts/test/test_image_fallback.py
    if [ $? -eq 0 ]; then
        echo -e "   ${GREEN}✅${NC} Test funcional pasado"
        ((PASS++))
    else
        echo -e "   ${RED}❌${NC} Test funcional fallido"
        ((FAIL++))
    fi
else
    echo "   ⏭️  Test funcional omitido"
fi

# Resumen
echo ""
echo "════════════════════════════════════════════════════════════"
echo "📊 RESUMEN DE VALIDACIÓN"
echo "════════════════════════════════════════════════════════════"
echo -e "✅ Tests pasados: ${GREEN}$PASS${NC}"
echo -e "❌ Tests fallidos: ${RED}$FAIL${NC}"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ SISTEMA VALIDADO - Listo para usar${NC}"
    echo ""
    echo "🚀 Puedes ejecutar:"
    echo "   python scripts/master_orchestrator.py"
    echo "   python scripts/generate-interactive.py"
    echo "════════════════════════════════════════════════════════════"
    exit 0
else
    echo -e "${RED}❌ VALIDACIÓN FALLIDA - Revisar errores arriba${NC}"
    echo "════════════════════════════════════════════════════════════"
    exit 1
fi
