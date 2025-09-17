#!/bin/bash

# Script para iniciar el entorno de desarrollo

echo "Iniciando entorno de desarrollo de DeConfianza"
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

# Detener servicios existentes de desarrollo si están corriendo
echo "Deteniendo servicios existentes de desarrollo..."
docker-compose -f docker-compose.dev.yml down

# Iniciar servicios de desarrollo
echo "Iniciando servicios de desarrollo..."
docker-compose -f docker-compose.dev.yml up -d

# Mostrar información
echo ""
echo "Entorno de desarrollo iniciado correctamente"
echo "=============================================="
echo "Frontend: http://localhost:$(grep FRONTEND_PORT .env | cut -d '=' -f2)"
echo "Backend API: http://localhost:$(grep BACKEND_PORT .env | cut -d '=' -f2)/api/"
echo "Backend Admin: http://localhost:$(grep BACKEND_PORT .env | cut -d '=' -f2)/admin/"
echo "Base de datos: PostgreSQL en localhost:$(grep DB_PORT .env | cut -d '=' -f2)"
echo ""
echo "Para detener el entorno, ejecuta: ./stop-all.sh"
echo ""