#!/bin/bash

# Script para iniciar todos los entornos

echo "Iniciando todos los entornos de DeConfianza"
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

# Iniciar Nginx Proxy Manager
echo "Iniciando Nginx Proxy Manager..."
./start-nginx-proxy.sh

# Seleccionar entornos a iniciar
echo ""
echo "¿Qué entornos deseas iniciar?"
echo "1) Desarrollo"
echo "2) Pruebas"
echo "3) Producción"
echo "4) Todos los entornos"
echo "5) Cancelar"
echo ""
read -p "Selecciona una opción (1-5): " opcion

case $opcion in
    1)
        ./start-dev.sh
        ;;
    2)
        ./start-test.sh
        ;;
    3)
        ./start-prod.sh
        ;;
    4)
        ./start-dev.sh
        ./start-test.sh
        ./start-prod.sh
        ;;
    5)
        echo "Operación cancelada."
        exit 0
        ;;
    *)
        echo "Opción inválida."
        exit 1
        ;;
esac

echo ""
echo "Todos los servicios seleccionados han sido iniciados."
echo "=============================================="
