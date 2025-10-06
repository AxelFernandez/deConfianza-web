#!/bin/bash

# Script para inicializar todos los datos de test (planes, categorías y rubros)

echo "🚀 Inicializando datos de test..."
echo "=============================================="
echo ""

# Verificar que el contenedor esté corriendo
if ! docker ps | grep -q "deconfianza-test_backend-test"; then
    echo "❌ Error: El contenedor backend-test no está corriendo."
    echo "   Por favor, inicia el entorno de test primero con: ./start-test.sh"
    exit 1
fi

echo "📦 Creando planes de suscripción..."
echo "=============================================="
docker exec deconfianza-test_backend-test_1 python manage.py crear_planes_test

echo ""
echo "📂 Creando categorías y rubros..."
echo "=============================================="
docker exec deconfianza-test_backend-test_1 python manage.py crear_rubros_test

echo ""
echo "✅ ¡Datos de test creados exitosamente!"
echo ""
echo "Puedes verificar los datos en:"
echo "  • Admin Django: https://test.deconfianza.com.ar/admin/"
echo "  • Planes: https://test.deconfianza.com.ar/admin/usuarios/plan/"
echo "  • Categorías: https://test.deconfianza.com.ar/admin/servicios/categoria/"
echo "  • Rubros: https://test.deconfianza.com.ar/admin/servicios/rubro/"
echo ""

