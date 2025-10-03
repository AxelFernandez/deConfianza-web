# 🧪 Instrucciones para Probar el Sistema de Cambio de Planes

## 📋 **Pre-requisitos**

1. Sistema en ejecución: `docker-compose up` o `./start-dev.sh`
2. Backend: http://localhost:8000
3. Frontend: http://localhost:5173
4. Admin: http://localhost:8000/admin

---

## 🎯 **Escenarios de Prueba**

### **Escenario 1: Upgrade Inmediato (Basic → Full)**

#### **Objetivo:** Probar upgrade con prorrateo y pago en MercadoPago

**Pasos:**

1. **Crear usuario prestador con plan Basic:**
   ```bash
   # Opción A: Desde Django Admin
   - Ir a http://localhost:8000/admin
   - Crear User y Perfil con es_prestador=True
   - Crear Suscripción activa con plan Basic
   
   # Opción B: Desde el frontend
   - Registrarse y completar onboarding como prestador
   - Seleccionar plan Basic (gratis)
   ```

2. **Verificar suscripción activa:**
   ```bash
   docker exec deconfianza-web-backend-dev-1 python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   from apps.suscripciones.models import Suscripcion
   
   user = User.objects.get(email='tu_email@test.com')
   suscripcion = Suscripcion.objects.filter(usuario=user, activa=True).first()
   print(f"Plan: {suscripcion.plan.name}")
   print(f"Días restantes: {suscripcion.dias_restantes}")
   print(f"Fecha fin: {suscripcion.fecha_fin}")
   ```

3. **Probar cambio de plan:**
   - Login como prestador
   - Ir a http://localhost:5173/planes
   - Verificar que muestra el plan actual (Basic)
   - Click en "Ver Otros Planes"
   - Click en plan "Full"
   - Verificar modal con cálculo de prorrateo
   - Ver detalles: monto, días, crédito
   - Click en "Confirmar"
   - Redirige a MercadoPago (sandbox)

4. **Simular pago en MercadoPago:**
   - Usar tarjeta de prueba: 5031 7557 3453 0604
   - CVV: 123
   - Fecha: cualquier futura
   - Nombre: APRO (para aprobar)
   - Completar pago

5. **Verificar cambio aplicado:**
   - Redirige a /suscripcion/exito
   - Ir a /planes
   - Verificar que ahora muestra plan "Full"
   - Verificar próximo cobro actualizado

6. **Verificar en backend:**
   ```python
   suscripcion_nueva = Suscripcion.objects.filter(usuario=user, activa=True).first()
   print(f"Plan nuevo: {suscripcion_nueva.plan.name}")
   print(f"Monto pagado: ${suscripcion_nueva.monto}")
   ```

**✅ Resultado Esperado:**
- Modal muestra cálculo correcto
- Redirige a MercadoPago
- Pago procesa correctamente
- Plan actualiza inmediatamente
- Suscripción anterior desactivada
- Nueva suscripción con días restantes del ciclo

---

### **Escenario 2: Downgrade Programado (Full → Basic)**

#### **Objetivo:** Probar downgrade con cambio programado al fin de ciclo

**Pasos:**

1. **Crear usuario con plan Full:**
   ```python
   # En Django shell
   from django.contrib.auth.models import User
   from apps.usuarios.models import Plan
   from apps.suscripciones.models import Suscripcion
   from django.utils import timezone
   from datetime import timedelta
   
   user = User.objects.create_user(
       username='testfull',
       email='testfull@test.com',
       password='test123',
       first_name='Test',
       last_name='Full'
   )
   
   plan_full = Plan.objects.get(code='full')
   
   # Crear suscripción activa con 15 días restantes
   Suscripcion.objects.create(
       usuario=user,
       plan=plan_full,
       estado='approved',
       monto=plan_full.precio_mensual,
       activa=True,
       fecha_inicio=timezone.now() - timedelta(days=15),
       fecha_fin=timezone.now() + timedelta(days=15),
       fecha_pago=timezone.now() - timedelta(days=15)
   )
   ```

2. **Solicitar downgrade:**
   - Login como usuario Full
   - Ir a /planes
   - Click en "Ver Otros Planes"
   - Click en plan "Basic" (gratis)
   - Verificar mensaje: "Tu plan cambiará a Basic el [fecha]"

3. **Verificar alerta programada:**
   - Debe aparecer alerta amarilla en /planes
   - Muestra: "Cambio de Plan Programado"
   - Muestra: "Tu plan cambiará a Basic el..."
   - Muestra: "Quedan X días"
   - Botón "Cancelar Cambio" visible

4. **Verificar en admin:**
   - Ir a http://localhost:8000/admin/suscripciones/cambioplanerogramado/
   - Ver cambio programado con badge "Downgrade"
   - Estado: "Pendiente"
   - Fecha programada: fecha_fin de suscripción actual

5. **Probar cancelar cambio:**
   - En /planes, click "Cancelar Cambio"
   - Confirmar
   - Alerta desaparece
   - En admin, estado cambia a "Cancelado"

6. **Recrear cambio y probar cron:**
   ```bash
   # Cambiar fecha_programada a hoy en admin
   
   # Ejecutar comando
   docker exec deconfianza-web-backend-dev-1 python manage.py procesar_cambios_plan
   ```

7. **Verificar procesamiento:**
   - Ver output del comando
   - En admin: estado "Procesado"
   - Usuario ahora tiene plan Basic
   - Suscripción Full desactivada

**✅ Resultado Esperado:**
- Cambio NO se aplica inmediatamente
- Se crea registro en CambioPlanProgramado
- Alerta amarilla en /planes
- Puede cancelar el cambio
- Cron procesa correctamente en fecha programada

---

### **Escenario 3: Upgrade sin Costo (Basic → Basic Paid)**

#### **Objetivo:** Probar upgrade cuando no hay diferencia de precio

**Pasos:**

1. Crear dos planes con mismo precio (ej: ambos $0)
2. Solicitar cambio
3. Verificar que se aplica inmediatamente sin pago

**✅ Resultado Esperado:**
- No redirige a MercadoPago
- Cambio instantáneo
- Mensaje: "Tu plan ha sido actualizado"

---

### **Escenario 4: Validaciones**

#### **Objetivo:** Probar validaciones del sistema

**Pruebas:**

1. **Intentar cambiar al mismo plan:**
   - Seleccionar plan actual
   - Verificar error: "Ya tienes este plan activo"

2. **Intentar cambiar con cambio pendiente:**
   - Tener un downgrade programado
   - Intentar otro cambio
   - Verificar error: "Ya tienes un cambio programado"

3. **Usuario sin suscripción:**
   - Usuario nuevo sin plan
   - Intentar cambio
   - Verificar error: "No tienes una suscripción activa"

**✅ Resultado Esperado:**
- Todos los errores se muestran correctamente
- No se permite cambio inválido

---

### **Escenario 5: Cálculo de Prorrateo**

#### **Objetivo:** Verificar cálculos correctos

**Test Manual:**

```python
# En Django shell
from apps.suscripciones.utils import calcular_prorrateo
from apps.suscripciones.models import Suscripcion

suscripcion = Suscripcion.objects.get(id=X)  # Tu suscripción
plan_nuevo = Plan.objects.get(code='full')

resultado = calcular_prorrateo(suscripcion, plan_nuevo)

print(f"Días restantes: {resultado['dias_restantes']}")
print(f"Crédito actual: ${resultado['credito_plan_actual']}")
print(f"Costo nuevo: ${resultado['costo_plan_nuevo']}")
print(f"A pagar: ${resultado['monto_a_pagar']}")
print(f"\n{resultado['detalle']}")
```

**Verificar manualmente:**
```
Ejemplo:
- Plan actual: Basic ($0/mes)
- Plan nuevo: Full ($2900/mes)
- Días restantes: 15

Cálculo esperado:
  Costo diario Full: $2900 / 30 = $96.67
  Costo por 15 días: $96.67 × 15 = $1450.05
  Crédito Basic: $0
  
  A pagar: $1450.05 ✅
```

---

### **Escenario 6: UI Completo**

#### **Objetivo:** Verificar todos los elementos de UI

**Checklist Frontend:**

- [ ] Página /planes carga correctamente
- [ ] Usuario no autenticado: muestra planes + redirect a login
- [ ] Cliente: muestra mensaje "Ya eres parte"
- [ ] Prestador: muestra card con plan actual
- [ ] Muestra precio mensual correcto
- [ ] Muestra estado "Activo" con badge verde
- [ ] Muestra próximo cobro con fecha
- [ ] Muestra días restantes
- [ ] Muestra servicios creados / límite
- [ ] Lista características del plan
- [ ] Botón "Ver Otros Planes" funciona
- [ ] Grid de otros planes excluye plan actual
- [ ] Plan actual tiene badge "Plan Actual" deshabilitado
- [ ] Si hay cambio programado: alerta amarilla visible
- [ ] Alerta muestra plan nuevo, fecha, días restantes
- [ ] Botón "Cancelar Cambio" funciona
- [ ] Modal de prorrateo muestra cálculo detallado
- [ ] Redirección a MercadoPago funciona

---

## 🐛 **Debugging**

### **Ver logs de backend:**
```bash
docker logs -f deconfianza-web-backend-dev-1
```

### **Ver logs de suscripciones:**
```python
from apps.suscripciones.models import LogWebhook
LogWebhook.objects.all().order_by('-fecha')[:10]
```

### **Ver cambios programados:**
```python
from apps.suscripciones.models import CambioPlanProgramado
CambioPlanProgramado.objects.all()
```

### **Forzar fecha para testing:**
```python
# Cambiar fecha_programada a ahora
cambio = CambioPlanProgramado.objects.get(id=X)
cambio.fecha_programada = timezone.now()
cambio.save()

# Ejecutar cron
# docker exec ... python manage.py procesar_cambios_plan
```

---

## ✅ **Checklist de Pruebas Completo**

- [ ] Escenario 1: Upgrade con prorrateo funciona
- [ ] Escenario 2: Downgrade programado funciona
- [ ] Escenario 3: Upgrade sin costo funciona
- [ ] Escenario 4: Validaciones funcionan
- [ ] Escenario 5: Cálculos son correctos
- [ ] Escenario 6: UI completo funciona
- [ ] Cron job procesa correctamente
- [ ] Admin muestra datos correctos
- [ ] Webhooks de MercadoPago funcionan
- [ ] Cancelar cambio funciona
- [ ] Próximo cobro se muestra correctamente

---

## 🚀 **Ready para Producción**

Una vez todos los escenarios pasen:
1. Configurar cron en servidor
2. Configurar MercadoPago en producción
3. Probar con datos reales
4. Monitorear logs primeros días

**¡Sistema completo y probado!** 🎉
