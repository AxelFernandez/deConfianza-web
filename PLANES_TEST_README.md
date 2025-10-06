# Planes de Suscripción para Test

Este documento describe los planes de suscripción configurados para el entorno de test y cómo crearlos.

## Planes Configurados

### 🆓 Plan Gratis
- **Código:** `free`
- **Precio:** Gratis
- **Características:**
  - ✅ Puede cargar dirección
  - ❌ No puede cargar teléfono
  - ❌ Sin imágenes ni videos
  - ❌ Sin reseñas
  - ❌ Sin estadísticas
  - **Servicios:** Hasta 1 servicio

### 📦 Plan Estándar
- **Código:** `standard`
- **Precio:** $2.999/mes
- **Características:**
  - ✅ Puede cargar dirección
  - ✅ Puede cargar teléfono
  - ✅ Hasta 3 imágenes
  - ❌ Sin videos
  - ❌ Sin reseñas
  - ❌ Sin estadísticas
  - **Servicios:** Hasta 3 servicios

### 💎 Plan Premium
- **Código:** `premium`
- **Precio:** $9.999/mes
- **Características:**
  - ✅ Puede cargar dirección, teléfono, ciudad, provincia
  - ✅ Puede cargar sitio web y descripción
  - ✅ Hasta 10 imágenes
  - ✅ Hasta 2 videos
  - ✅ Puede recibir reseñas
  - ✅ Tiene acceso a estadísticas
  - **Servicios:** Hasta 10 servicios

## Cómo Crear los Planes

### Opción 1: Usando el script (Recomendado)

```bash
# En tu servidor de test
cd ~/deconfianza-test
./crear-planes-test.sh
```

### Opción 2: Comando de Django directo

```bash
# Ejecutar el comando dentro del contenedor
docker exec deconfianza-test_backend-test_1 python manage.py crear_planes_test
```

### Opción 3: Desde el shell de Django

```bash
# Acceder al shell de Django
docker exec -it deconfianza-test_backend-test_1 python manage.py shell

# Ejecutar:
from django.core.management import call_command
call_command('crear_planes_test')
```

## Verificar los Planes

Puedes verificar que los planes se crearon correctamente de varias formas:

### 1. Desde el Admin de Django

```
https://test.deconfianza.com.ar/admin/usuarios/plan/
```

### 2. Desde el Shell de Django

```bash
docker exec -it deconfianza-test_backend-test_1 python manage.py shell
```

```python
from apps.usuarios.models import Plan

# Ver todos los planes
for plan in Plan.objects.all():
    print(f"{plan.name}: ${plan.precio_mensual} - {plan.code}")
```

### 3. Desde la API

```bash
curl https://test.deconfianza.com.ar/api/usuarios/planes/
```

## Actualizar los Planes

El comando `crear_planes_test` usa `update_or_create`, por lo que:
- Si el plan no existe, lo crea
- Si el plan ya existe (mismo `code`), lo actualiza

Puedes ejecutar el comando múltiples veces sin problemas.

## Campos Habilitados por Plan

Los campos que cada plan puede editar en el perfil del prestador:

- **Gratis:** `direccion`
- **Estándar:** `direccion`, `telefono`
- **Premium:** `direccion`, `telefono`, `ciudad`, `provincia`, `sitio_web`, `descripcion`

## Notas Importantes

1. El plan **Gratis** se asigna automáticamente a todos los usuarios que no tienen suscripción activa.
2. Los precios están en pesos argentinos (ARS).
3. Los planes están configurados para usar MercadoPago Sandbox en test.
4. Para cambiar de plan, el usuario debe ir a `/planes` en el frontend.

## Solución de Problemas

### Error: "No module named 'apps.usuarios.management'"

Asegúrate de que existan los archivos `__init__.py` en:
- `backend/apps/usuarios/management/__init__.py`
- `backend/apps/usuarios/management/commands/__init__.py`

### Los planes no se ven en el frontend

Verifica que el endpoint `/api/usuarios/planes/` esté funcionando:

```bash
curl https://test.deconfianza.com.ar/api/usuarios/planes/
```

Si no funciona, revisa la configuración de Nginx Proxy Manager para que proxy las peticiones `/api/` al backend.

