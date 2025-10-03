<template>
  <section class="py-20 bg-gradient-to-br from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Planes que se adaptan a tu negocio
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Elige el plan perfecto para hacer crecer tu negocio y llegar a más clientes
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-12">
        <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-3xl animate-spin" />
        <p class="mt-4 text-gray-600">Cargando planes...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12">
        <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="text-red-500 text-3xl mb-4" />
        <p class="text-red-600">Error al cargar los planes. Inténtalo de nuevo.</p>
        <button @click="loadPlanes" class="mt-4 text-blue-600 hover:text-blue-700 underline">
          Reintentar
        </button>
      </div>

      <!-- Plans grid -->
      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div 
          v-for="plan in planes" 
          :key="plan.id"
          :class="[
            'relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 hover:shadow-xl',
            plan.is_popular ? 'border-blue-500 transform hover:scale-105' : 'border-gray-200 hover:border-blue-300'
          ]"
        >
          <!-- Popular badge -->
          <div v-if="plan.is_popular" class="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <span class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
              Más Popular
            </span>
          </div>

          <div class="p-8">
            <!-- Plan header -->
            <div class="text-center mb-8">
              <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ plan.name }}</h3>
              <p class="text-gray-600 text-sm mb-4">{{ plan.description }}</p>
              
              <div class="mb-6">
                <div v-if="plan.is_free" class="text-4xl font-bold text-green-600">
                  Gratis
                </div>
                <div v-else class="flex items-baseline justify-center">
                  <span class="text-4xl font-bold text-gray-900">${{ plan.price_text }}</span>
                  <span class="text-gray-600 ml-2">/mes</span>
                </div>
              </div>
            </div>

            <!-- Features -->
            <div class="mb-8">
              <h4 class="font-semibold text-gray-900 mb-4">Características incluidas:</h4>
              <ul class="space-y-3">
                <li 
                  v-for="feature in plan.features" 
                  :key="feature"
                  class="flex items-start"
                >
                  <font-awesome-icon 
                    :icon="['fas', 'check']" 
                    class="text-green-500 mt-1 mr-3 flex-shrink-0" 
                  />
                  <span class="text-gray-700 text-sm">{{ feature }}</span>
                </li>
              </ul>
            </div>

            <!-- CTA Button -->
            <button
              @click="selectPlan(plan)"
              :class="[
                'w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105',
                plan.is_popular 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg'
                  : plan.is_free
                    ? 'bg-green-500 hover:bg-green-600 text-white shadow-lg'
                    : 'bg-gray-900 hover:bg-gray-800 text-white shadow-lg'
              ]"
            >
              {{ plan.button_text }}
            </button>

            <!-- Additional info for paid plans -->
            <div v-if="!plan.is_free" class="mt-4 text-center">
              <p class="text-xs text-gray-500">
                Sin permanencia • Cancela cuando quieras
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Additional info -->
      <div class="mt-16 text-center">
        <div class="bg-blue-50 rounded-2xl p-8 max-w-4xl mx-auto">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">
            ¿Necesitas algo personalizado?
          </h3>
          <p class="text-gray-600 mb-6">
            Contáctanos para planes empresariales con características especiales
          </p>
          <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-semibold transition-colors">
            Contactar ventas
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

// Estado reactivo
const planes = ref([])
const loading = ref(true)
const error = ref(false)

// Función para cargar planes
const loadPlanes = async () => {
  try {
    loading.value = true
    error.value = false
    
    const response = await api.get('/usuarios/planes-publicos/')
    planes.value = response.data
    
    console.log('Planes cargados:', response.data)
  } catch (err) {
    console.error('Error cargando planes:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// Función para seleccionar un plan
const selectPlan = (plan) => {
  console.log('Plan seleccionado:', plan)
  
  // Redirigir directamente al login sin guardar nada
  router.push('/login')
}

// Cargar planes al montar el componente
onMounted(() => {
  loadPlanes()
})
</script>

<style scoped>
/* Animaciones adicionales */
.transform {
  transition: transform 0.3s ease;
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Gradientes personalizados */
.bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}
</style>
