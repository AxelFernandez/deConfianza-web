#!/bin/bash

# Script para crear planes de test en el contenedor de backend-test

echo "🚀 Creando planes de test en el backend..."
echo "=============================================="
echo ""

# Verificar que el contenedor esté corriendo
if ! docker ps | grep -q "deconfianza-test_backend-test"; then
    echo "❌ Error: El contenedor backend-test no está corriendo."
    echo "   Por favor, inicia el entorno de test primero con: ./start-test.sh"
    exit 1
fi

# Ejecutar el comando de Django
docker exec deconfianza-test_backend-test_1 python manage.py crear_planes_test

echo ""
echo "✅ ¡Planes creados exitosamente!"
echo ""

