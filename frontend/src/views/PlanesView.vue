<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-white">
    <!-- Hero Section -->
    <section class="py-16 bg-gradient-to-r from-blue-600 to-purple-600">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
          Planes para Prestadores de Servicios
        </h1>
        <p class="text-xl text-blue-100 max-w-3xl mx-auto">
          Elige el plan perfecto para hacer crecer tu negocio
        </p>
      </div>
    </section>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-20">
      <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-4xl animate-spin" />
      <p class="mt-4 text-gray-600">Cargando información...</p>
    </div>

    <!-- Usuario Cliente: No mostrar planes -->
    <div v-else-if="isCliente" class="max-w-4xl mx-auto px-4 py-20 text-center">
      <div class="bg-white rounded-2xl shadow-lg p-12 border border-gray-200">
        <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <font-awesome-icon :icon="['fas', 'user-check']" class="text-blue-600 text-3xl" />
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-4">
          Ya eres parte de DeConfianza
        </h2>
        <p class="text-lg text-gray-600 mb-8">
          Como cliente, puedes buscar y contratar prestadores de servicios sin necesidad de suscripción.
        </p>
        <router-link 
          to="/buscar"
          class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold transition-colors"
        >
          <font-awesome-icon :icon="['fas', 'search']" class="mr-2" />
          Buscar Servicios
        </router-link>
      </div>
    </div>

    <!-- Usuario Prestador: Mostrar plan actual -->
    <div v-else-if="isPrestador" class="max-w-6xl mx-auto px-4 py-20">
      <!-- Alerta de cambio programado -->
      <div v-if="cambioProgramado" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8 rounded-r-lg">
        <div class="flex">
          <div class="flex-shrink-0">
            <font-awesome-icon :icon="['fas', 'clock']" class="text-yellow-400 text-xl" />
          </div>
          <div class="ml-3 flex-1">
            <h3 class="text-sm font-medium text-yellow-800">
              Cambio de Plan Programado
            </h3>
            <div class="mt-2 text-sm text-yellow-700">
              <p>Tu plan cambiará a <strong>{{ cambioProgramado.plan_nuevo.name }}</strong> el {{ formatDate(cambioProgramado.fecha_programada) }}</p>
              <p class="mt-1">Quedan {{ cambioProgramado.dias_hasta_cambio }} días.</p>
            </div>
            <div class="mt-4">
              <button
                @click="cancelarCambioProgramado"
                class="text-sm bg-yellow-100 hover:bg-yellow-200 text-yellow-800 px-4 py-2 rounded-lg transition-colors"
              >
                Cancelar Cambio
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-8 mb-12 border border-gray-200">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Tu Plan Actual</h2>
            <p class="text-gray-600">Gestiona tu suscripción y beneficios</p>
          </div>
          <div class="text-right">
            <div class="inline-flex items-center px-6 py-3 bg-blue-100 rounded-full">
              <font-awesome-icon :icon="['fas', 'crown']" class="text-blue-600 mr-2" />
              <span class="text-xl font-bold text-blue-900">{{ currentPlan?.name || 'Plan Básico' }}</span>
            </div>
          </div>
        </div>

        <!-- Info del plan actual -->
        <div class="grid md:grid-cols-4 gap-6 mb-8">
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="text-gray-600 mb-2">Precio Mensual</div>
            <div class="text-3xl font-bold text-gray-900">
              {{ currentPlan?.is_free ? 'Gratis' : `$${currentPlan?.price_text}` }}
            </div>
          </div>
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="text-gray-600 mb-2">Estado</div>
            <div class="flex items-center">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-green-100 text-green-800">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2" />
                Activo
              </span>
            </div>
          </div>
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="text-gray-600 mb-2">Próximo Cobro</div>
            <div class="text-sm font-medium text-gray-900">
              {{ formatDate(infoSuscripcion?.suscripcion?.proximo_cobro) || 'No disponible' }}
            </div>
            <div v-if="infoSuscripcion?.suscripcion?.dias_restantes" class="text-xs text-gray-500 mt-1">
              {{ infoSuscripcion.suscripcion.dias_restantes }} días
            </div>
          </div>
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="text-gray-600 mb-2">Servicios Creados</div>
            <div class="text-3xl font-bold text-gray-900">
              {{ userProfile?.servicios_count || 0 }} / {{ currentPlan?.max_servicios || '∞' }}
            </div>
          </div>
        </div>

        <!-- Características del plan actual -->
        <div class="mb-8">
          <h3 class="font-semibold text-gray-900 mb-4 text-lg">Características incluidas:</h3>
          <div class="grid md:grid-cols-2 gap-3">
            <div v-for="feature in currentPlan?.features" :key="feature" class="flex items-start">
              <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
              <span class="text-gray-700">{{ feature }}</span>
            </div>
          </div>
        </div>

        <!-- Botón de dashboard -->
        <div class="flex gap-4">
          <router-link 
            to="/prestador/dashboard"
            class="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
          >
            Ir al Dashboard
          </router-link>
          <button
            @click="showUpgradeOptions = !showUpgradeOptions"
            class="flex-1 text-center bg-gray-100 hover:bg-gray-200 text-gray-900 px-6 py-3 rounded-xl font-semibold transition-colors"
          >
            {{ showUpgradeOptions ? 'Ocultar Planes' : 'Ver Otros Planes' }}
          </button>
        </div>
      </div>

      <!-- Otros planes disponibles (solo si showUpgradeOptions) -->
      <div v-if="showUpgradeOptions" class="mt-12">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">
          Otros Planes Disponibles
        </h2>
        <PricingPlans 
          :planes="planesDisponibles" 
          :loading="loadingPlanes"
          :currentPlanCode="currentPlan?.code"
          @select="handlePlanSelect"
        />
      </div>
    </div>

    <!-- Usuario No Autenticado: Mostrar todos los planes -->
    <div v-else class="py-16">
      <PricingPlans 
        :planes="planesDisponibles" 
        :loading="loadingPlanes"
        @select="handlePlanSelect"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import PricingPlans from '../components/PricingPlans.vue'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

// Estado
const loading = ref(true)
const loadingPlanes = ref(false)
const planesDisponibles = ref([])
const showUpgradeOptions = ref(false)
const cambioProgramado = ref(null)
const infoSuscripcion = ref(null)

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userProfile = computed(() => authStore.user?.perfil)
const isPrestador = computed(() => isAuthenticated.value && userProfile.value?.es_prestador)
const isCliente = computed(() => isAuthenticated.value && !userProfile.value?.es_prestador)
const currentPlan = computed(() => userProfile.value?.plan_info)

// Funciones
const loadPlanes = async () => {
  try {
    loadingPlanes.value = true
    const response = await api.get('/usuarios/planes-publicos/')
    planesDisponibles.value = response.data
  } catch (err) {
    console.error('Error cargando planes:', err)
  } finally {
    loadingPlanes.value = false
  }
}

const handlePlanSelect = async (plan) => {
  console.log('Plan seleccionado:', plan)
  
  if (!isAuthenticated.value) {
    // Usuario no autenticado: redirigir a login sin preselección
    router.push('/login')
  } else if (isPrestador.value) {
    // Prestador: solicitar cambio de plan
    await solicitarCambioPlan(plan)
  }
}

const solicitarCambioPlan = async (plan) => {
  try {
    loading.value = true
    
    const response = await api.post('/suscripciones/solicitar-cambio-plan/', {
      plan_code: plan.code
    })
    
    const data = response.data
    
    if (data.tipo === 'upgrade') {
      if (data.cambio_inmediato) {
        // Upgrade sin costo
        alert(data.mensaje)
        await authStore.fetchUserProfile() // Recargar perfil
        await loadPlanes()
      } else {
        // Upgrade con prorrateo - redirigir a MercadoPago
        if (data.init_point) {
          // Mostrar modal con detalles del prorrateo
          if (confirm(`${data.calculo.detalle}\n\n¿Deseas continuar con el pago?`)) {
            window.location.href = data.init_point
          }
        }
      }
    } else if (data.tipo === 'downgrade') {
      // Downgrade programado
      alert(`${data.mensaje}\n\n${data.detalle}`)
      await authStore.fetchUserProfile() // Recargar perfil
      showUpgradeOptions.value = false // Ocultar otros planes
    }
    
  } catch (error) {
    console.error('Error solicitando cambio de plan:', error)
    const errorMsg = error.response?.data?.error || 'Error al solicitar cambio de plan'
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const cancelarCambioProgramado = async () => {
  if (!confirm('¿Estás seguro de que deseas cancelar el cambio de plan programado?')) {
    return
  }
  
  try {
    loading.value = true
    await api.post('/suscripciones/cancelar-cambio-programado/')
    
    alert('Cambio de plan cancelado exitosamente')
    cambioProgramado.value = null
    
  } catch (error) {
    console.error('Error cancelando cambio:', error)
    alert('Error al cancelar el cambio')
  } finally {
    loading.value = false
  }
}

const loadInfoSuscripcion = async () => {
  if (!isPrestador.value) return
  
  try {
    const response = await api.get('/suscripciones/info-suscripcion/')
    
    if (response.data.tiene_suscripcion) {
      infoSuscripcion.value = response.data
      cambioProgramado.value = response.data.cambio_programado
    }
  } catch (error) {
    console.error('Error cargando info de suscripción:', error)
  }
}

// Lifecycle
onMounted(async () => {
  loading.value = true
  
  // Si está autenticado, cargar perfil
  if (isAuthenticated.value && !authStore.user) {
    try {
      await authStore.fetchUserProfile()
    } catch (error) {
      console.error('Error cargando perfil:', error)
    }
  }
  
  // Cargar planes
  await loadPlanes()
  
  // Si es prestador, cargar info de suscripción
  if (isPrestador.value) {
    await loadInfoSuscripcion()
  }
  
  loading.value = false
})
</script>

<style scoped>
/* Animaciones */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
