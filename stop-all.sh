#!/bin/bash

# Script para detener todos los entornos

echo "Deteniendo todos los entornos de DeConfianza"
echo "=============================================="

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar que Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Seleccionar entornos a detener
echo ""
echo "¿Qué entornos deseas detener?"
echo "1) Desarrollo"
echo "2) Pruebas"
echo "3) Producción"
echo "4) Nginx Proxy Manager"
echo "5) Todos los entornos"
echo "6) Cancelar"
echo ""
read -p "Selecciona una opción (1-6): " opcion

case $opcion in
    1)
        echo "Deteniendo entorno de desarrollo..."
        docker-compose -f docker-compose.dev.yml down
        ;;
    2)
        echo "Deteniendo entorno de pruebas..."
        docker-compose -f docker-compose.test.yml down
        ;;
    3)
        echo "Deteniendo entorno de producción..."
        docker-compose -f docker-compose.prod.yml down
        ;;
    4)
        echo "Deteniendo Nginx Proxy Manager..."
        docker-compose down
        ;;
    5)
        echo "Deteniendo todos los entornos..."
        docker-compose -f docker-compose.dev.yml down
        docker-compose -f docker-compose.test.yml down
        docker-compose -f docker-compose.prod.yml down
        docker-compose down
        ;;
    6)
        echo "Operación cancelada."
        exit 0
        ;;
    *)
        echo "Opción inválida."
        exit 1
        ;;
esac

echo ""
echo "Operación completada."
echo "=============================================="
