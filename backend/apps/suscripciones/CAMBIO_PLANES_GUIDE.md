# 📋 Guía Completa: Sistema de Cambio de Planes

## 🎯 Estrategia Implementada: **Híbrido Inteligente**

### **Upgrade (Mejora de Plan)**
- ✅ **Inmediato** con prorrateo
- Usuario paga la diferencia de inmediato
- Obtiene beneficios instantáneamente

### **Downgrade (Reducción de Plan)**
- ✅ **Programado** al fin del ciclo
- Usuario mantiene beneficios hasta el próximo cobro
- No pierde días pagados

---

## 🏗️ **Arquitectura del Sistema**

### **1. Modelo: `CambioPlanProgramado`**

```python
class CambioPlanProgramado(models.Model):
    usuario = models.ForeignKey(User)
    plan_actual = models.ForeignKey(Plan, related_name='cambios_desde')
    plan_nuevo = models.ForeignKey(Plan, related_name='cambios_hacia')
    suscripcion_actual = models.ForeignKey(Suscripcion)
    
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField()
    fecha_procesado = models.DateTimeField(null=True)
    
    estado = models.CharField(max_length=20)  # pending, processed, cancelled
    es_upgrade = models.BooleanField(default=False)
    notas = models.TextField(blank=True)
```

### **2. Comando de Django: `procesar_cambios_plan`**

Procesa cambios programados automáticamente.

**Uso:**
```bash
# Modo normal
python manage.py procesar_cambios_plan

# Modo dry-run (solo muestra qué haría)
python manage.py procesar_cambios_plan --dry-run
```

### **3. Cron Job**

Ejecuta el comando diariamente para procesar cambios pendientes.

---

## ⚙️ **Configuración del Cron Job**

### **Opción 1: Crontab (Linux/Mac)**

```bash
# Editar crontab
crontab -e

# Agregar línea (ejecutar diariamente a las 2 AM)
0 2 * * * cd /ruta/proyecto && docker-compose exec -T backend-dev python manage.py procesar_cambios_plan >> /var/log/cambios_plan.log 2>&1
```

### **Opción 2: Django-Crontab** (Recomendado)

1. **Instalar:**
```bash
pip install django-crontab
```

2. **Configurar en `settings.py`:**
```python
INSTALLED_APPS = [
    ...
    'django_crontab',
]

CRONJOBS = [
    # Procesar cambios de plan diariamente a las 2 AM
    ('0 2 * * *', 'django.core.management.call_command', ['procesar_cambios_plan']),
    
    # Verificar suscripciones vencidas cada 6 horas
    ('0 */6 * * *', 'django.core.management.call_command', ['procesar_cambios_plan']),
]
```

3. **Activar:**
```bash
python manage.py crontab add
python manage.py crontab show  # Ver crons activos
```

### **Opción 3: Celery Beat** (Producción)

1. **Instalar:**
```bash
pip install celery redis
```

2. **Crear tarea en `tasks.py`:**
```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def procesar_cambios_plan_task():
    call_command('procesar_cambios_plan')
```

3. **Configurar en `settings.py`:**
```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'procesar-cambios-plan': {
        'task': 'apps.suscripciones.tasks.procesar_cambios_plan_task',
        'schedule': crontab(hour=2, minute=0),  # 2 AM diariamente
    },
}
```

### **Opción 4: Docker Compose Service**

Crear un servicio dedicado en `docker-compose.yml`:

```yaml
services:
  cron-worker:
    build: ./backend
    command: >
      sh -c "
        while true; do
          python manage.py procesar_cambios_plan
          sleep 86400  # 24 horas
        done
      "
    environment:
      - DJANGO_SETTINGS_MODULE=deconfianza.settings.prod
    depends_on:
      - db
      - backend
```

---

## 📊 **Flujo Completo del Sistema**

### **Caso 1: Upgrade (Basic → Full)**

```
Usuario en Plan Basic ($0/mes)
    ↓
Solicita cambiar a Full ($2900/mes)
    ↓
Sistema detecta: es_upgrade = True
    ↓
Calcula prorrateo:
  - Días restantes del ciclo: 15 días
  - Costo proporcional: $2900 * (15/30) = $1450
    ↓
Crea preferencia de pago en MercadoPago por $1450
    ↓
Usuario paga
    ↓
Sistema ejecuta INMEDIATAMENTE:
  - Desactiva suscripción Basic
  - Crea nueva suscripción Full (válida 30 días)
  - Usuario obtiene beneficios al instante
```

### **Caso 2: Downgrade (Full → Basic)**

```
Usuario en Plan Full ($2900/mes)
    ↓
Solicita cambiar a Basic ($0/mes)
    ↓
Sistema detecta: es_upgrade = False
    ↓
Crea CambioPlanProgramado:
  - estado: 'pending'
  - fecha_programada: fecha_fin de suscripción actual (ej: 15 días)
  - es_upgrade: False
    ↓
Usuario ve mensaje:
  "Tu plan cambiará a Basic el 15 de Octubre.
   Seguirás disfrutando de Full hasta entonces."
    ↓
[Pasan 15 días]
    ↓
Cron job ejecuta: python manage.py procesar_cambios_plan
    ↓
Sistema procesa automáticamente:
  - Desactiva suscripción Full
  - Crea nueva suscripción Basic
  - Usuario ahora tiene plan Basic
```

---

## 💰 **Cálculo de Prorrateo (Upgrades)**

### **Fórmula:**

```python
def calcular_prorrateo(suscripcion_actual, plan_nuevo):
    # Días restantes en el ciclo actual
    dias_restantes = (suscripcion_actual.fecha_fin - timezone.now()).days
    
    # Costo diario del plan nuevo
    costo_diario_nuevo = plan_nuevo.precio_mensual / 30
    
    # Costo proporcional a pagar
    monto_prorrateo = costo_diario_nuevo * dias_restantes
    
    # También considerar crédito del plan actual
    costo_diario_actual = suscripcion_actual.plan.precio_mensual / 30
    credito_plan_actual = costo_diario_actual * dias_restantes
    
    # Monto final a cobrar
    monto_final = monto_prorrateo - credito_plan_actual
    
    return max(monto_final, 0)  # Nunca negativo
```

### **Ejemplo:**

```
Plan Actual: Full ($2900/mes)
Plan Nuevo: Premium ($5000/mes)
Días restantes: 15

Cálculo:
  Costo diario Full: $2900 / 30 = $96.67/día
  Costo diario Premium: $5000 / 30 = $166.67/día
  
  Crédito Full: $96.67 * 15 = $1450.05
  Costo Premium: $166.67 * 15 = $2500.05
  
  A pagar: $2500.05 - $1450.05 = $1050.00
```

---

## 🔔 **Notificaciones al Usuario**

### **Notificación de Downgrade Programado**

```python
# En la API de cambio de plan
def notificar_downgrade_programado(cambio):
    send_mail(
        subject='Tu plan cambiará próximamente',
        message=f'''
        Hola {cambio.usuario.first_name},
        
        Tu plan cambiará de {cambio.plan_actual.name} a {cambio.plan_nuevo.name}
        el {cambio.fecha_programada.strftime("%d de %B")}.
        
        Seguirás disfrutando de los beneficios de {cambio.plan_actual.name}
        hasta entonces.
        
        Si deseas cancelar este cambio, puedes hacerlo desde tu panel de control.
        ''',
        from_email='no-reply@deconfianza.com',
        recipient_list=[cambio.usuario.email],
    )
```

### **Notificación Pre-Ejecución (3 días antes)**

```python
# En el comando procesar_cambios_plan
cambios_proximos = CambioPlanProgramado.objects.filter(
    estado='pending',
    fecha_programada__gte=timezone.now(),
    fecha_programada__lte=timezone.now() + timedelta(days=3)
)

for cambio in cambios_proximos:
    notificar_cambio_proximo(cambio)
```

---

## 🧪 **Testing Manual**

### **1. Test de Upgrade**

```bash
# En Django shell
docker-compose exec backend-dev python manage.py shell

# Código Python
from django.contrib.auth.models import User
from apps.usuarios.models import Plan
from apps.suscripciones.models import Suscripcion
from django.utils import timezone
from datetime import timedelta

user = User.objects.get(username='test_user')
plan_basic = Plan.objects.get(code='basic')
plan_full = Plan.objects.get(code='full')

# Crear suscripción Basic
suscripcion = Suscripcion.objects.create(
    usuario=user,
    plan=plan_basic,
    estado='approved',
    monto=0,
    activa=True,
    fecha_inicio=timezone.now(),
    fecha_fin=timezone.now() + timedelta(days=30)
)

# Simular upgrade a Full
# (Esto se haría desde la API, pero aquí lo hacemos manual)
print(f"Días restantes: {suscripcion.dias_restantes}")
print(f"Fecha fin: {suscripcion.fecha_fin}")
```

### **2. Test de Downgrade**

```python
# Crear cambio programado
from apps.suscripciones.models import CambioPlanProgramado

cambio = CambioPlanProgramado.objects.create(
    usuario=user,
    plan_actual=plan_full,
    plan_nuevo=plan_basic,
    suscripcion_actual=suscripcion,
    fecha_programada=timezone.now() + timedelta(days=15),
    es_upgrade=False
)

print(f"Cambio creado: {cambio}")
print(f"Se ejecutará el: {cambio.fecha_programada}")
```

### **3. Test del Comando Cron**

```bash
# Dry-run
python manage.py procesar_cambios_plan --dry-run

# Ejecutar realmente
python manage.py procesar_cambios_plan
```

---

## 🚨 **Casos Edge a Considerar**

### **1. Usuario cancela durante cambio programado**
```python
# En el view de cancelar cambio
cambio = CambioPlanProgramado.objects.get(id=cambio_id, usuario=request.user)
if cambio.estado == 'pending':
    cambio.cancelar_cambio()
    # Notificar al usuario
```

### **2. Usuario hace múltiples cambios**
```python
# Cancelar cambios pendientes anteriores
cambios_anteriores = CambioPlanProgramado.objects.filter(
    usuario=request.user,
    estado='pending'
)
cambios_anteriores.update(estado='cancelled')

# Crear nuevo cambio
nuevo_cambio = CambioPlanProgramado.objects.create(...)
```

### **3. Fallo en procesamiento**
```python
# En procesar_cambio()
try:
    # Lógica de cambio
    ...
except Exception as e:
    cambio.notas += f"\nError: {str(e)}"
    cambio.save()
    # Enviar alerta a admin
    send_admin_alert(f"Fallo procesando cambio {cambio.id}")
```

---

## ✅ **Checklist de Implementación**

- [x] Modelo `CambioPlanProgramado` creado
- [x] Migraciones aplicadas
- [x] Admin configurado con badges
- [x] Comando `procesar_cambios_plan` creado
- [ ] API endpoints para cambiar plan (próximo paso)
- [ ] Frontend para solicitar cambios (próximo paso)
- [ ] Cálculo de prorrateo implementado (próximo paso)
- [ ] Integración con MercadoPago para upgrades (próximo paso)
- [ ] Notificaciones por email (próximo paso)
- [ ] Cron job configurado en producción
- [ ] Tests automatizados
- [ ] Logging y monitoreo

---

## 🔮 **Próximos Pasos**

1. Crear API endpoint `/api/suscripciones/cambiar-plan/`
2. Implementar cálculo de prorrateo
3. Integrar con MercadoPago para upgrades
4. Crear UI en frontend
5. Implementar notificaciones
6. Configurar cron en producción

**Sistema listo para continuar desarrollo.** 🚀
