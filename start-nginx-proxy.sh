#!/bin/bash

# Script para iniciar el Nginx Proxy Manager

echo "Iniciando Nginx Proxy Manager"
echo "============================"

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

# Crear directorios necesarios si no existen
mkdir -p ./data/nginx/config
mkdir -p ./data/nginx/letsencrypt
mkdir -p ./data/mysql

# Crear las redes si no existen
docker network create deconfianza_dev_network 2>/dev/null || true
docker network create deconfianza_test_network 2>/dev/null || true
docker network create deconfianza_prod_network 2>/dev/null || true

# Iniciar Nginx Proxy Manager
echo "Iniciando Nginx Proxy Manager..."
docker-compose up -d

echo ""
echo "Nginx Proxy Manager iniciado correctamente"
echo "========================================"
echo "Panel de administración: http://localhost:81"
echo "Usuario predeterminado: admin@example.com"
echo "Contraseña predeterminada: changeme"
echo ""
echo "Recuerda cambiar las credenciales predeterminadas al iniciar sesión por primera vez."
echo ""
echo "Para detener el servicio, ejecuta: docker-compose down"
echo ""