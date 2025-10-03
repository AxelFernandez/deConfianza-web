<template>
  <!-- Contenido desbloqueado -->
  <div v-if="hasPermission">
    <slot />
  </div>

  <!-- Contenido bloqueado -->
  <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <!-- Header con gradiente -->
    <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-bold text-gray-900">{{ title }}</h2>
          <p class="text-sm text-gray-600 mt-1">
            <font-awesome-icon :icon="['fas', 'lock']" class="mr-1 text-orange-500" />
            Función no disponible en tu plan
          </p>
        </div>
      </div>
    </div>

    <!-- Contenido bloqueado -->
    <div class="p-8">
      <div class="text-center max-w-md mx-auto">
        <!-- Icono grande -->
        <div class="w-20 h-20 bg-gradient-to-br from-orange-100 to-orange-200 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
          <font-awesome-icon :icon="['fas', icon]" class="text-orange-500 text-3xl" />
        </div>

        <!-- Mensaje -->
        <h3 class="text-xl font-bold text-gray-900 mb-3">{{ blockedTitle || title }}</h3>
        <p class="text-gray-600 mb-6 leading-relaxed">{{ message }}</p>

        <!-- Features preview (opcional) -->
        <div v-if="features && features.length" class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 mb-6 border border-blue-100">
          <p class="text-sm font-semibold text-gray-700 mb-4">Desbloquea:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-left">
            <div v-for="(feature, index) in features" :key="index" class="flex items-center text-gray-700">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-blue-500 mr-2 flex-shrink-0" />
              <span>{{ feature }}</span>
            </div>
          </div>
        </div>

        <!-- CTA Button -->
        <router-link
          to="/planes"
          class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
        >
          <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
          Mejorar Plan
        </router-link>

        <!-- Link alternativo -->
        <p class="text-sm text-gray-500 mt-4">
          <router-link to="/planes" class="text-blue-600 hover:text-blue-700 font-medium">
            Ver todos los planes disponibles →
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  hasPermission: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  blockedTitle: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: 'Esta función no está incluida en tu plan actual. Actualiza para desbloquear todas las características.'
  },
  icon: {
    type: String,
    default: 'lock'
  },
  features: {
    type: Array,
    default: () => []
  }
});
</script>
