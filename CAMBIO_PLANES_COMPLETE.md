# ✅ Sistema Completo de Cambio de Planes

## 🎯 **Implementación Finalizada**

Se ha implementado un sistema completo de cambio de planes con:
- ✅ Cálculo automático de prorrateo
- ✅ Integración con MercadoPago
- ✅ UI completa en frontend
- ✅ Cron job para cambios programados

---

## 🏗️ **Backend Implementado**

### **1. Modelos**

#### **`CambioPlanProgramado`** (`backend/apps/suscripciones/models.py`)
```python
class CambioPlanProgramado(models.Model):
    usuario = ForeignKey(User)
    plan_actual = ForeignKey(Plan)
    plan_nuevo = ForeignKey(Plan)
    suscripcion_actual = ForeignKey(Suscripcion)
    fecha_programada = DateTimeField()
    es_upgrade = BooleanField()
    estado = CharField()  # pending, processed, cancelled
```

### **2. Utilidades** (`backend/apps/suscripciones/utils.py`)

- **`calcular_prorrateo()`** - Calcula monto a pagar en upgrades
- **`determinar_tipo_cambio()`** - Identifica upgrade/downgrade
- **`puede_cambiar_plan()`** - Validaciones antes del cambio
- **`obtener_suscripcion_activa()`** - Obtiene suscripción vigente
- **`calcular_fecha_proximo_cobro()`** - Próxima fecha de renovación

### **3. API Endpoints** (`backend/apps/suscripciones/views.py`)

#### **POST `/api/suscripciones/solicitar-cambio-plan/`**
```json
Request:
{
  "plan_code": "full"
}

Response (Upgrade con pago):
{
  "tipo": "upgrade",
  "preference_id": "123456",
  "init_point": "https://mp.com/...",
  "calculo": {
    "monto_a_pagar": 1450.00,
    "dias_restantes": 15,
    "detalle": "..."
  }
}

Response (Downgrade programado):
{
  "tipo": "downgrade",
  "cambio_programado": true,
  "fecha_programada": "2025-10-15",
  "mensaje": "..."
}
```

#### **GET `/api/suscripciones/info-suscripcion/`**
```json
{
  "tiene_suscripcion": true,
  "suscripcion": {
    "plan": { "code": "full", "name": "Full", ... },
    "proximo_cobro": "2025-10-15",
    "dias_restantes": 15
  },
  "cambio_programado": {
    "plan_nuevo": { "code": "basic", ... },
    "fecha_programada": "2025-10-15",
    "dias_hasta_cambio": 15
  }
}
```

#### **POST `/api/suscripciones/cancelar-cambio-programado/`**
```json
{
  "mensaje": "Cambio de plan cancelado exitosamente"
}
```

### **4. Comando Cron** (`backend/apps/suscripciones/management/commands/procesar_cambios_plan.py`)

```bash
# Procesar cambios pendientes
python manage.py procesar_cambios_plan

# Modo dry-run (testing)
python manage.py procesar_cambios_plan --dry-run
```

**Configuración de Cron:**
```bash
# Ejecutar diariamente a las 2 AM
0 2 * * * cd /proyecto && docker-compose exec -T backend-dev python manage.py procesar_cambios_plan
```

### **5. Admin de Django**

- Vista completa con badges de colores
- Filtros por estado, tipo, fechas
- Acciones: procesar y cancelar cambios
- Contador de días hasta el cambio

---

## 🎨 **Frontend Implementado**

### **1. Página de Planes** (`frontend/src/views/PlanesView.vue`)

#### **Estados por Tipo de Usuario:**

**Usuario No Autenticado:**
- Muestra todos los planes
- Botón "Seleccionar" → redirige a `/login`

**Usuario Cliente:**
- Mensaje: "Ya eres parte de DeConfianza"
- No muestra planes (no los necesita)
- Botón: "Buscar Servicios"

**Usuario Prestador:**
- Muestra plan actual con detalles:
  - Precio mensual
  - Estado (Activo)
  - Próximo cobro + días restantes
  - Servicios creados / límite
  - Características incluidas
- Botón "Ver Otros Planes" (toggle)
- Si hay cambio programado → Alerta amarilla con info

#### **Funcionalidades:**

**Upgrade (Plan más caro):**
```javascript
1. Usuario hace click en plan
2. Frontend llama API solicitar-cambio-plan
3. Muestra modal con cálculo de prorrateo
4. Usuario confirma
5. Redirige a MercadoPago
6. Pago exitoso → Plan actualizado inmediatamente
```

**Downgrade (Plan más barato):**
```javascript
1. Usuario hace click en plan
2. Frontend llama API solicitar-cambio-plan
3. Sistema programa cambio para fin de ciclo
4. Muestra mensaje: "Cambiará el DD/MM/YYYY"
5. Alerta amarilla aparece con opción de cancelar
6. En fecha programada → Cron procesa automáticamente
```

### **2. Componente de Planes** (`frontend/src/components/PricingPlans.vue`)

- Grid responsive de tarjetas
- Badge "Plan Actual" con ring verde
- Badge "Más Popular" en plan premium
- Deshabilitado para plan actual
- Características listadas con checks

---

## 💰 **Cálculo de Prorrateo**

### **Fórmula:**

```
Días restantes = fecha_fin - hoy
Costo diario actual = precio_actual / 30
Costo diario nuevo = precio_nuevo / 30
Crédito = costo_diario_actual × días_restantes
Costo nuevo = costo_diario_nuevo × días_restantes
A pagar = max(costo_nuevo - crédito, 0)
```

### **Ejemplo:**

```
Plan actual: Basic ($0)
Plan nuevo: Full ($2900)
Días restantes: 15

Cálculo:
  Crédito Basic: $0/día × 15 = $0
  Costo Full: $96.67/día × 15 = $1450.05
  
  A pagar: $1450.05
  
Nueva suscripción válida por 15 días, luego $2900/mes completo.
```

---

## 🔄 **Flujos Completos**

### **Flujo 1: Upgrade (Basic → Full)**

```
1. Usuario en /planes ve su plan Basic
2. Click en "Ver Otros Planes"
3. Click en plan Full
4. Sistema calcula: $1450 por 15 días restantes
5. Modal muestra detalle del prorrateo
6. Usuario confirma
7. Redirige a MercadoPago
8. Paga $1450
9. Webhook recibe pago
10. Sistema desactiva suscripción Basic
11. Crea nueva suscripción Full (15 días)
12. Usuario obtiene beneficios inmediatamente
13. En 15 días: se cobra $2900 completo
```

### **Flujo 2: Downgrade (Full → Basic)**

```
1. Usuario en /planes ve su plan Full
2. Click en "Ver Otros Planes"
3. Click en plan Basic
4. Sistema detecta downgrade
5. Programa cambio para: 15/Oct (fecha_fin)
6. Mensaje: "Cambiará a Basic el 15/Oct"
7. Aparece alerta amarilla con cuenta regresiva
8. Usuario sigue usando Full por 15 días
9. [15 días después]
10. Cron ejecuta a las 2 AM
11. Procesa cambio automáticamente
12. Desactiva suscripción Full
13. Crea suscripción Basic
14. Usuario ahora tiene plan Basic
```

---

## 🧪 **Testing**

### **1. Test de Upgrade**

```bash
# 1. Crear usuario con plan Basic
# 2. Ir a /planes
# 3. Click en "Ver Otros Planes"
# 4. Click en plan Full
# 5. Verificar modal de prorrateo
# 6. Confirmar y ver redirección a MP
```

### **2. Test de Downgrade**

```bash
# 1. Crear usuario con plan Full
# 2. Ir a /planes
# 3. Click en plan Basic
# 4. Verificar mensaje de cambio programado
# 5. Verificar alerta amarilla
# 6. Test cancelar cambio
```

### **3. Test de Cron**

```bash
# Ver cambios pendientes en admin
python manage.py procesar_cambios_plan --dry-run

# Procesar manualmente
python manage.py procesar_cambios_plan
```

---

## 📁 **Archivos Creados/Modificados**

### **Backend:**
1. `backend/apps/suscripciones/models.py` → `CambioPlanProgramado`
2. `backend/apps/suscripciones/utils.py` → Utilidades de cálculo
3. `backend/apps/suscripciones/views.py` → 3 nuevos endpoints
4. `backend/apps/suscripciones/urls.py` → 3 nuevas rutas
5. `backend/apps/suscripciones/admin.py` → Admin para cambios
6. `backend/apps/suscripciones/management/commands/procesar_cambios_plan.py` → Cron
7. `backend/apps/suscripciones/migrations/0004_*.py` → Migración aplicada

### **Frontend:**
1. `frontend/src/views/PlanesView.vue` → Actualizado con cambio de planes
2. `frontend/src/components/PricingPlans.vue` → Grid de planes

### **Documentación:**
1. `backend/apps/suscripciones/CAMBIO_PLANES_GUIDE.md` → Guía técnica
2. `CAMBIO_PLANES_COMPLETE.md` → Este archivo

---

## ✅ **Checklist Final**

- [x] Modelo `CambioPlanProgramado`
- [x] Migraciones aplicadas
- [x] Utilidades de cálculo de prorrateo
- [x] API endpoints (3)
- [x] Integración MercadoPago
- [x] Comando cron
- [x] Admin de Django
- [x] Frontend UI completo
- [x] Alerta de cambio programado
- [x] Cancelar cambio programado
- [x] Mostrar próximo cobro
- [x] Documentación completa

---

## 🚀 **Sistema Listo para Producción**

**Todo implementado y funcionando:**
- ✅ Backend con API completa
- ✅ Cálculo automático de prorrateo
- ✅ Integración MercadoPago
- ✅ Frontend UI completo
- ✅ Cron job para cambios programados
- ✅ Admin de Django
- ✅ Documentación técnica

**Próximo paso: Configurar cron en servidor de producción.** 🎉
