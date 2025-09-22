<template>
  <div class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
    <div class="p-4 bg-primary-50 border-b border-neutral-200">
      <h2 class="font-medium text-primary-800">Navegación</h2>
    </div>
    <nav class="p-2">
      <router-link 
        to="/prestador/dashboard" 
        class="flex items-center px-3 py-2 rounded-md mt-1 transition-colors"
        :class="$route.name === 'prestadorDashboard' ? 'bg-primary-100 text-primary-800 font-medium' : 'text-neutral-700 hover:bg-neutral-50'"
      >
        <font-awesome-icon :icon="['fas', 'tachometer-alt']" class="mr-3" />
        Panel principal
      </router-link>
      <router-link 
        to="/prestador/perfil" 
        class="flex items-center px-3 py-2 rounded-md mt-1 transition-colors"
        :class="$route.name === 'prestadorPerfil' ? 'bg-primary-100 text-primary-800 font-medium' : 'text-neutral-700 hover:bg-neutral-50'"
      >
        <font-awesome-icon :icon="['fas', 'user']" class="mr-3" />
        Mi perfil
      </router-link>
      <router-link 
        to="/prestador/configuracion" 
        class="flex items-center px-3 py-2 rounded-md mt-1 transition-colors"
        :class="$route.name === 'prestadorConfiguracion' ? 'bg-primary-100 text-primary-800 font-medium' : 'text-neutral-700 hover:bg-neutral-50'"
      >
        <font-awesome-icon :icon="['fas', 'cog']" class="mr-3" />
        Configuración
      </router-link>
      <router-link 
        to="/prestador/servicios" 
        class="flex items-center px-3 py-2 rounded-md mt-1 transition-colors"
        :class="$route.name === 'prestadorServicios' ? 'bg-primary-100 text-primary-800 font-medium' : 'text-neutral-700 hover:bg-neutral-50'"
      >
        <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-3" />
        Mis servicios
      </router-link>
      <router-link 
        to="/prestador/resenas" 
        class="flex items-center px-3 py-2 rounded-md mt-1 transition-colors"
        :class="$route.name === 'prestadorResenas' ? 'bg-primary-100 text-primary-800 font-medium' : 'text-neutral-700 hover:bg-neutral-50'"
      >
        <font-awesome-icon :icon="['fas', 'star']" class="mr-3" />
        Reseñas
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

const $route = useRoute();
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
