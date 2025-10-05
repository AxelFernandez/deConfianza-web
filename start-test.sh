#!/bin/bash

# Script para iniciar el entorno de pruebas

echo "Iniciando entorno de pruebas de DeConfianza"
echo "=============================================="

# Verificar si se pasó el flag --no-cache
NO_CACHE_FLAG=""
if [ "$1" == "--no-cache" ]; then
    echo "Modo: Rebuild completo sin caché"
    NO_CACHE_FLAG="--no-cache"
else
    echo "Modo: Build normal (usa caché si está disponible)"
    echo "Usa './start-test.sh --no-cache' para forzar rebuild completo"
fi
echo ""

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

# Detener servicios existentes de pruebas si están corriendo
echo "Deteniendo servicios existentes de pruebas..."

# Desconectar Nginx Proxy Manager de la red de test si está conectado
NPM_CONTAINER=$(docker ps -q -f name=nginx-proxy-manager)
if [ ! -z "$NPM_CONTAINER" ]; then
    echo "Desconectando Nginx Proxy Manager de la red de test..."
    docker network disconnect deconfianza-test_deconfianza_test_network $NPM_CONTAINER 2>/dev/null || true
fi

docker-compose -f docker-compose.test.yml down

# Iniciar servicios de pruebas
echo "Iniciando servicios de pruebas..."
if [ ! -z "$NO_CACHE_FLAG" ]; then
    docker-compose -f docker-compose.test.yml build $NO_CACHE_FLAG
    docker-compose -f docker-compose.test.yml up -d
else
    docker-compose -f docker-compose.test.yml up -d --build
fi

# Reconectar Nginx Proxy Manager a la red de test
if [ ! -z "$NPM_CONTAINER" ]; then
    echo "Reconectando Nginx Proxy Manager a la red de test..."
    docker network connect deconfianza-test_deconfianza_test_network $NPM_CONTAINER 2>/dev/null || true
fi

# Mostrar información
echo ""
echo "Entorno de pruebas iniciado correctamente"
echo "=============================================="
echo "Frontend: http://localhost:$(grep FRONTEND_PORT .env | cut -d '=' -f2)"
echo "Backend API: http://localhost:$(grep BACKEND_PORT .env | cut -d '=' -f2)/api/"
echo "Backend Admin: http://localhost:$(grep BACKEND_PORT .env | cut -d '=' -f2)/admin/"
echo "Base de datos: PostgreSQL en localhost:$(grep DB_PORT .env | cut -d '=' -f2)"
echo ""
echo "Para detener el entorno, ejecuta: ./stop-all.sh"
echo ""