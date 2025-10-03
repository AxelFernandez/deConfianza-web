# Test del Flujo de Pricing

## 🎯 Objetivo
Validar que el flujo completo de selección de plan desde pricing funcione correctamente.

## 📋 Pasos a probar

### 1. **Página Principal (Home)**
- ✅ Verificar que aparezca la sección de pricing
- ✅ Confirmar que se carguen los planes desde la API
- ✅ Validar que los botones de suscripción funcionen

### 2. **Selección de Plan**
- ✅ Hacer clic en "Suscribirse por $2900" (plan Full)
- ✅ Verificar que se guarde en localStorage:
  ```javascript
  localStorage.getItem('selectedPlan')
  // Debería contener: { id, code: 'full', name: 'Full', price_text: '2900', is_free: false, timestamp }
  ```
- ✅ Confirmar redirección a `/login?plan=full&redirect=onboarding`

### 3. **Login/Registro**
- ✅ Completar login con Google o registro
- ✅ Verificar redirección automática a onboarding

### 4. **Onboarding con Plan Pre-seleccionado**
- ✅ Confirmar que `userType` se establezca como 'prestador'
- ✅ Verificar que `selectedPlan` sea 'full'
- ✅ Validar que salte al paso 2 (selección de plan)
- ✅ Comprobar que el plan Full esté pre-seleccionado
- ✅ Continuar el onboarding normalmente

### 5. **Completar Onboarding**
- ✅ Finalizar el proceso de onboarding
- ✅ Verificar que se limpie el localStorage:
  ```javascript
  localStorage.getItem('selectedPlan') === null
  ```
- ✅ Confirmar redirección al dashboard

## 🧪 Test Manual

### Comando para limpiar localStorage:
```javascript
localStorage.removeItem('selectedPlan')
```

### Comando para simular plan pre-seleccionado:
```javascript
localStorage.setItem('selectedPlan', JSON.stringify({
  id: 2,
  code: 'full',
  name: 'Full', 
  price_text: '2900',
  is_free: false,
  timestamp: new Date().getTime()
}))
```

### Verificar plan guardado:
```javascript
console.log('Plan guardado:', JSON.parse(localStorage.getItem('selectedPlan') || 'null'))
```

## 🔍 Puntos de Verificación

1. **API funcional**: `GET /api/usuarios/planes-publicos/`
2. **LocalStorage**: Plan se guarda y recupera correctamente
3. **Redirección**: Login → Onboarding con parámetros
4. **Pre-selección**: Plan aparece seleccionado en onboarding
5. **Limpieza**: LocalStorage se limpia al completar

## 🚨 Posibles Problemas

- **Expiración**: Plan en localStorage expira después de 30 minutos
- **Plan inexistente**: Validación si el plan ya no está disponible
- **Navegación directa**: ¿Qué pasa si alguien va directo al onboarding?
- **Usuario ya registrado**: ¿Funciona el flujo para usuarios existentes?

## ✅ Checklist Final

- [ ] Sección de pricing visible en home
- [ ] API devuelve planes correctamente
- [ ] Plan se guarda en localStorage al hacer clic
- [ ] Redirección a login con parámetros correctos
- [ ] Onboarding detecta plan pre-seleccionado
- [ ] Plan aparece seleccionado en UI
- [ ] Flujo completo funciona end-to-end
- [ ] LocalStorage se limpia al finalizar
