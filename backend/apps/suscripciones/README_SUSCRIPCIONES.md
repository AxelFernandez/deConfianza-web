# Sistema de Suscripciones - MercadoPago

## 📋 Opciones Disponibles

### 1. **Pagos Únicos** (Sistema Actual)
- ❌ **Sin renovación automática**
- ✅ Más simple de implementar
- ❌ Usuario debe renovar manualmente cada mes
- ❌ Mayor tasa de churn (usuarios que olvidan renovar)

**API:** `POST /api/suscripciones/crear-preferencia/`

### 2. **Suscripciones Automáticas** (Nuevo)
- ✅ **Renovación 100% automática**
- ✅ Mejor experiencia de usuario
- ✅ Menor tasa de churn
- ⚡ Requiere configuración adicional

**API:** `POST /api/suscripciones/crear-suscripcion/`

---

## 🔄 Flujo de Suscripciones Automáticas

### Paso 1: Crear Suscripción
```bash
POST /api/suscripciones/crear-suscripcion/
{
    "plan": "full"
}
```

**Respuesta:**
```json
{
    "preapproval_id": "2c938084726fca480172750000000000",
    "init_point": "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_id=2c938084726fca480172750000000000",
    "external_reference": "sub_123_full_1634567890",
    "auto_recurring": true,
    "plan": "Full",
    "amount": 2900.0,
    "frequency": "monthly"
}
```

### Paso 2: Usuario Autoriza Débito
- Usuario va a `init_point`
- Autoriza débito automático mensual
- MercadoPago envía webhook `preapproval`

### Paso 3: Cobro Automático Mensual
- MercadoPago cobra automáticamente cada mes
- Envía webhook `authorized_payment`
- Sistema extiende automáticamente la suscripción

### Paso 4: Cancelación (Opcional)
```bash
POST /api/suscripciones/cancelar-suscripcion/
```

---

## 🎯 Configuración de Webhooks

### Webhook de Suscripciones
**URL:** `https://tu-dominio.com/api/suscripciones/webhook/suscripciones/`

**Eventos a configurar en MercadoPago:**
```json
{
    "events": [
        "preapproval",
        "authorized_payment"
    ]
}
```

### Tipos de Eventos

#### `preapproval`
- **pending**: Suscripción creada, esperando autorización
- **authorized**: Usuario autorizó débito automático
- **paused**: Suscripción pausada
- **cancelled**: Suscripción cancelada

#### `authorized_payment`
- **approved**: Pago mensual exitoso
- **rejected**: Pago rechazado (tarjeta sin fondos, etc.)

---

## 🔧 Configuración en MercadoPago

### 1. Crear Aplicación
1. Ir a https://www.mercadopago.com.ar/developers
2. Crear nueva aplicación
3. Obtener `ACCESS_TOKEN` y `PUBLIC_KEY`

### 2. Configurar Webhooks
```bash
curl -X POST \
    -H 'accept: application/json' \
    -H 'content-type: application/json' \
    -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
    'https://api.mercadopago.com/v1/webhooks' \
    -d '{
        "url": "https://tu-dominio.com/api/suscripciones/webhook/suscripciones/",
        "events": [
            {"resource": "preapproval", "topic": "preapproval"},
            {"resource": "authorized_payment", "topic": "authorized_payment"}
        ]
    }'
```

### 3. Variables de Entorno
```env
MERCADOPAGO_ACCESS_TOKEN=your_access_token
MERCADOPAGO_PUBLIC_KEY=your_public_key
```

---

## 📊 Comparación de Sistemas

| Característica | Pagos Únicos | Suscripciones Automáticas |
|----------------|---------------|---------------------------|
| Renovación automática | ❌ | ✅ |
| Experiencia de usuario | Regular | Excelente |
| Tasa de retención | Baja | Alta |
| Complejidad técnica | Baja | Media |
| Gestión de vencimientos | Manual | Automática |
| Webhooks requeridos | 1 | 2 |
| Cancelación | Inmediata | Configurable |

---

## 🚀 Migración Gradual

### Opción 1: Ambos Sistemas en Paralelo
- Mantener pagos únicos para usuarios existentes
- Ofrecer suscripciones automáticas para nuevos usuarios
- Permitir migración opcional

### Opción 2: Migración Completa
- Migrar todos los usuarios a suscripciones automáticas
- Deprecar sistema de pagos únicos
- Mejor experiencia unificada

---

## 💡 Recomendación

**Implementar suscripciones automáticas** para:
- ✅ Mejor experiencia de usuario
- ✅ Mayor retención de clientes
- ✅ Menos trabajo manual de renovaciones
- ✅ Flujo de caja más predecible

**Mantener ambos sistemas** durante período de transición.
