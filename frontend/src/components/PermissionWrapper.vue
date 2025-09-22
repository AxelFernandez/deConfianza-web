<template>
  <div class="relative">
    <!-- Contenido principal -->
    <div 
      :class="{ 
        'blur-sm pointer-events-none': !hasPermission,
        'transition-all duration-300': true 
      }"
    >
      <slot />
    </div>
    
    <!-- Overlay cuando no tiene permisos -->
    <div 
      v-if="!hasPermission" 
      class="absolute inset-0 bg-white/90 backdrop-blur-sm flex items-center justify-center rounded-lg border-2 border-dashed border-neutral-300 z-10 overflow-hidden"
    >
      <div class="text-center p-4 max-w-full mx-2">
        <div class="w-12 h-12 mx-auto mb-3 bg-neutral-100 rounded-full flex items-center justify-center">
          <font-awesome-icon :icon="['fas', icon]" class="text-xl text-neutral-400" />
        </div>
        <h3 class="text-base font-semibold text-neutral-700 mb-2 leading-tight">{{ title }}</h3>
        <p class="text-xs text-neutral-600 mb-3 leading-relaxed">{{ message }}</p>
        <button 
          v-if="showUpgradeButton"
          class="bg-primary-600 hover:bg-primary-700 text-white px-3 py-1.5 rounded-md text-xs font-medium transition-colors"
          @click="$emit('upgrade')"
        >
          <font-awesome-icon :icon="['fas', 'crown']" class="mr-1" />
          Mejorar plan
        </button>
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
    default: 'Funcionalidad no disponible'
  },
  message: {
    type: String,
    default: 'Esta función no está incluida en tu plan actual'
  },
  icon: {
    type: String,
    default: 'lock'
  },
  showUpgradeButton: {
    type: Boolean,
    default: true
  }
});

defineEmits(['upgrade']);
</script>

<style scoped>
/* Los estilos están en las clases de Tailwind */
</style>
