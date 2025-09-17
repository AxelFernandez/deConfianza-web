# DE CONFIANZA

Plataforma web para conectar prestadores de servicios profesionales y oficios con clientes potenciales.

## Características principales

- Búsqueda de servicios por ubicación, rubro, oficio y profesión
- Perfiles detallados para prestadores de servicios
- Sistema de suscripción con diferentes niveles de beneficios
- Reseñas y valoraciones de usuarios
- Interfaz intuitiva y fácil de usar

## Tecnologías utilizadas

### Backend
- Django
- Django REST Framework
- PostgreSQL

### Frontend
- Vue.js
- Bootstrap

### Infraestructura
- Docker
- Docker Compose
- Nginx Proxy Manager

## Requisitos previos

- Docker
- Docker Compose

## Entornos disponibles

El proyecto está configurado para funcionar en tres entornos diferentes:

1. **Desarrollo (dev)**: Entorno local para desarrollo con recarga en caliente
   - Backend: http://localhost:8001
   - Frontend: http://localhost:5174
   - Base de datos: PostgreSQL en puerto 5433

2. **Pruebas (test)**: Entorno de staging para pruebas
   - URL: https://test.deconfianza.com.ar
   - Backend: http://localhost:8002 (local)
   - Frontend: http://localhost:5175 (local)
   - Base de datos: PostgreSQL en puerto 5434

3. **Producción (prod)**: Entorno de producción
   - URL: https://deconfianza.com.ar
   - Base de datos: PostgreSQL en puerto 5432

## Configuración de variables de entorno

El proyecto utiliza archivos de variables de entorno para configurar los diferentes entornos:

1. Copia el archivo de plantilla para cada entorno:

```bash
# Para desarrollo
cp env-example env-dev

# Para pruebas
cp env-example env-test

# Para producción
cp env-example env-prod
```

2. Edita cada archivo según las necesidades de tu entorno:
   - `env-dev`: Configuración para desarrollo local
   - `env-test`: Configuración para entorno de pruebas
   - `env-prod`: Configuración para entorno de producción

Los scripts de inicio se encargarán de utilizar el archivo correcto según el entorno seleccionado.

## Iniciar y detener entornos

### Iniciar entornos individuales

Puedes iniciar cada entorno por separado usando los scripts proporcionados:

```bash
# Iniciar entorno de desarrollo
./start-dev.sh

# Iniciar entorno de pruebas
./start-test.sh

# Iniciar entorno de producción
./start-prod.sh

# Iniciar Nginx Proxy Manager
./start-nginx-proxy.sh
```

### Iniciar todos los entornos

También puedes iniciar todos los entornos a la vez:

```bash
./start-all.sh
```

### Detener entornos

Para detener los entornos:

```bash
./stop-all.sh
```

## Estructura del proyecto

```
deConfianza-web/
├── backend/                       # Aplicación Django
│   ├── apps/                      # Aplicaciones Django
│   │   ├── servicios/             # App para gestión de servicios
│   │   └── usuarios/              # App para gestión de usuarios
│   ├── deconfianza/               # Configuración principal de Django
│   │   ├── settings/              # Configuraciones por entorno
│   │       ├── base.py           # Configuración base compartida
│   │       ├── dev.py            # Configuración para desarrollo
│   │       ├── test.py           # Configuración para pruebas
│   │       └── prod.py           # Configuración para producción
│   ├── Dockerfile.dev            # Docker para desarrollo
│   ├── Dockerfile.test           # Docker para pruebas
│   ├── Dockerfile.prod           # Docker para producción
│   └── requirements.txt           # Dependencias de Python
├── frontend/                      # Aplicación Vue.js
│   ├── src/                       # Código fuente de Vue
│   ├── nginx/                     # Configuración de Nginx
│   ├── Dockerfile.dev            # Docker para desarrollo
│   ├── Dockerfile.test           # Docker para pruebas
│   ├── Dockerfile.prod           # Docker para producción
│   └── package.json               # Dependencias de Node.js
├── env-example                    # Plantilla para archivos de variables de entorno
├── env-dev                        # Variables de entorno para desarrollo
├── env-test                       # Variables de entorno para pruebas
├── env-prod                       # Variables de entorno para producción
├── docker-compose.yml             # Nginx Proxy Manager
├── docker-compose.dev.yml         # Configuración de Docker Compose para desarrollo
├── docker-compose.test.yml        # Configuración de Docker Compose para pruebas
├── docker-compose.prod.yml        # Configuración de Docker Compose para producción
├── start-dev.sh                   # Script para iniciar entorno de desarrollo
├── start-test.sh                  # Script para iniciar entorno de pruebas
├── start-prod.sh                  # Script para iniciar entorno de producción
├── start-nginx-proxy.sh           # Script para iniciar Nginx Proxy Manager
├── start-all.sh                   # Script para iniciar todos los entornos
├── stop-all.sh                    # Script para detener todos los entornos
└── README.md                      # Este archivo
```

## Nginx Proxy Manager

Para configurar los subdominios y dominios, sigue estos pasos:

1. Inicia Nginx Proxy Manager:
   ```bash
   ./start-nginx-proxy.sh
   ```

2. Accede al panel de administración:
   - URL: http://localhost:81
   - Usuario predeterminado: admin@example.com
   - Contraseña predeterminada: changeme

3. Configura los hosts proxy para cada entorno:
   - Desarrollo: localhost:5174 (frontend) y localhost:8001 (backend)
   - Pruebas: test.deconfianza.com.ar -> localhost:5175 (frontend) y localhost:8002 (backend/api)
   - Producción: deconfianza.com.ar -> backend-prod:8000 (backend/api) y frontend-prod:80 (frontend)

## Desarrollo

- Los cambios en el código del backend y frontend se recargan automáticamente en desarrollo
- Para crear un superusuario de Django:

```bash
# Entorno de desarrollo
docker-compose -f docker-compose.dev.yml exec backend-dev python manage.py createsuperuser

# Entorno de pruebas
docker-compose -f docker-compose.test.yml exec backend-test python manage.py createsuperuser

# Entorno de producción
docker-compose -f docker-compose.prod.yml exec backend-prod python manage.py createsuperuser
```

## Niveles de suscripción

1. **Rango 1 (Gratuito)**
   - Registro básico con nombre y dirección

2. **Rango 2 (Básico)**
   - Incluye teléfono, redes sociales, imágenes y videos

3. **Rango 3 (Premium)**
   - Todo lo anterior + reseñas de usuarios, asesoría empresarial y reportes

4. **Rango 4 (Destacado)**
   - Todo lo anterior + posicionamiento destacado en búsquedas y tarifario online