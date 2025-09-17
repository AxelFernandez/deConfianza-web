#!/bin/bash

# Script para iniciar el entorno de producción

echo "Iniciando entorno de PRODUCCIÓN de DeConfianza"
echo "=============================================="
echo "ADVERTENCIA: Este script iniciará el entorno de producción."
echo "Asegúrate de que estás en un servidor de producción."
echo ""
read -p "¿Estás seguro de que quieres continuar? (s/N): " respuesta

if [[ "$respuesta" != "s" && "$respuesta" != "S" ]]; then
    echo "Operación cancelada."
    exit 0
fi

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

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "Error: No se encuentra el archivo .env."
    echo "Por favor, crea el archivo .env a partir del archivo env-example."
    exit 1
fi

echo "Usando variables de entorno desde .env (sin modificarlo)."

# Crear las redes si no existen
docker network create deconfianza_dev_network 2>/dev/null || true
docker network create deconfianza_test_network 2>/dev/null || true
docker network create deconfianza_prod_network 2>/dev/null || true

# Detener servicios existentes de producción si están corriendo
echo "Deteniendo servicios existentes de producción..."
docker-compose -f docker-compose.prod.yml down

# Iniciar servicios de producción
echo "Iniciando servicios de producción..."
docker-compose -f docker-compose.prod.yml up -d

# Mostrar información
echo ""
echo "Entorno de PRODUCCIÓN iniciado correctamente"
echo "=============================================="
echo "Frontend: $(grep FRONTEND_URL .env | cut -d '=' -f2)"
echo "Backend API: $(grep API_URL .env | cut -d '=' -f2)"
echo "Backend Admin: $(grep BACKEND_URL .env | cut -d '=' -f2)/admin/"
echo ""
echo "Para detener el entorno, ejecuta: ./stop-all.sh"
echo ""