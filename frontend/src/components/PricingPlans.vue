<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-3xl animate-spin" />
      <p class="mt-4 text-gray-600">Cargando planes...</p>
    </div>

    <!-- Plans Grid -->
    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div 
        v-for="plan in planes" 
        :key="plan.id"
        :class="[
          'relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 hover:shadow-xl',
          plan.is_popular ? 'border-blue-500 transform hover:scale-105' : 'border-gray-200 hover:border-blue-300',
          currentPlanCode === plan.code ? 'ring-4 ring-green-500 ring-opacity-50' : ''
        ]"
      >
        <!-- Current Plan Badge -->
        <div v-if="currentPlanCode === plan.code" class="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <span class="bg-green-500 text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
            Plan Actual
          </span>
        </div>

        <!-- Popular Badge -->
        <div v-else-if="plan.is_popular" class="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <span class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
            Más Popular
          </span>
        </div>

        <div class="p-8">
          <!-- Plan Header -->
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
            <h4 class="font-semibold text-gray-900 mb-4">Incluye:</h4>
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
            v-if="currentPlanCode !== plan.code"
            @click="$emit('select', plan)"
            :class="[
              'w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105',
              plan.is_popular 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg'
                : plan.is_free
                  ? 'bg-green-500 hover:bg-green-600 text-white shadow-lg'
                  : 'bg-gray-900 hover:bg-gray-800 text-white shadow-lg'
            ]"
          >
            {{ plan.button_text || 'Seleccionar Plan' }}
          </button>

          <!-- Current Plan Button (disabled) -->
          <button
            v-else
            disabled
            class="w-full py-4 px-6 rounded-xl font-semibold text-lg bg-gray-100 text-gray-500 cursor-not-allowed"
          >
            Plan Actual
          </button>

          <!-- Additional Info -->
          <div v-if="!plan.is_free" class="mt-4 text-center">
            <p class="text-xs text-gray-500">
              Sin permanencia • Cancela cuando quieras
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  planes: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  currentPlanCode: {
    type: String,
    default: null
  }
})

defineEmits(['select'])
</script>

<style scoped>
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
