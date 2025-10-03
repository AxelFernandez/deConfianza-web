<template>
  <div class="space-y-4">
    <!-- Card de Plan -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="bg-gradient-to-r from-blue-600 to-blue-700 p-4">
        <div class="flex items-center text-white">
          <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center mr-3">
            <font-awesome-icon :icon="['fas', 'crown']" class="text-xl" />
          </div>
          <div class="flex-1">
            <p class="text-xs opacity-90">Tu Plan</p>
            <p class="font-bold text-lg">{{ dashboardData?.plan?.name || 'Cargando...' }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="dashboardData?.plan" class="p-4 space-y-3">
        <!-- Precio -->
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600">Precio</span>
          <span class="font-semibold text-gray-900">
            {{ dashboardData.plan.price_text === 'Gratis' ? 'Gratis' : `$${dashboardData.plan.price_text}/mes` }}
          </span>
        </div>

        <!-- Progreso de servicios -->
        <div v-if="dashboardData.limitaciones?.puede_crear_servicios" class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">Servicios</span>
            <span class="font-semibold text-gray-900">
              {{ dashboardData.estadisticas?.total_servicios || 0 }} / {{ dashboardData.limitaciones?.max_servicios || '∞' }}
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all"
              :class="serviciosPercentage < 80 ? 'bg-green-500' : serviciosPercentage < 100 ? 'bg-yellow-500' : 'bg-red-500'"
              :style="`width: ${serviciosPercentage}%`"
            ></div>
          </div>
        </div>

        <!-- Botón cambiar plan -->
        <router-link 
          to="/planes"
          class="block w-full text-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm font-medium"
        >
          <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
          Cambiar Plan
        </router-link>
      </div>
    </div>

    <!-- Navegación -->
    <nav class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="p-2">
        <router-link 
          to="/prestador/dashboard" 
          class="flex items-center px-4 py-3 rounded-lg transition-all group"
          :class="isActive('prestadorDashboard') ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transition-colors"
               :class="isActive('prestadorDashboard') ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 group-hover:bg-gray-200'">
            <font-awesome-icon :icon="['fas', 'tachometer-alt']" />
          </div>
          <span>Dashboard</span>
        </router-link>

        <router-link 
          to="/prestador/perfil" 
          class="flex items-center px-4 py-3 rounded-lg transition-all group mt-1"
          :class="isActive('prestadorPerfil') ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transition-colors"
               :class="isActive('prestadorPerfil') ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 group-hover:bg-gray-200'">
            <font-awesome-icon :icon="['fas', 'user']" />
          </div>
          <span>Mi Perfil</span>
        </router-link>

        <router-link 
          to="/prestador/servicios" 
          class="flex items-center px-4 py-3 rounded-lg transition-all group mt-1"
          :class="isActive('prestadorServicios') ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transition-colors"
               :class="isActive('prestadorServicios') ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 group-hover:bg-gray-200'">
            <font-awesome-icon :icon="['fas', 'briefcase']" />
          </div>
          <div class="flex-1 flex items-center justify-between">
            <span>Servicios</span>
            <span v-if="dashboardData?.estadisticas?.total_servicios" 
                  class="px-2 py-1 text-xs font-semibold rounded-full"
                  :class="isActive('prestadorServicios') ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'">
              {{ dashboardData.estadisticas.total_servicios }}
            </span>
          </div>
        </router-link>

        <router-link 
          to="/prestador/resenas" 
          class="flex items-center px-4 py-3 rounded-lg transition-all group mt-1"
          :class="isActive('prestadorResenas') ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transition-colors"
               :class="isActive('prestadorResenas') ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 group-hover:bg-gray-200'">
            <font-awesome-icon :icon="['fas', 'star']" />
          </div>
          <div class="flex-1 flex items-center justify-between">
            <span>Reseñas</span>
            <span v-if="dashboardData?.estadisticas?.total_resenas" 
                  class="px-2 py-1 text-xs font-semibold rounded-full"
                  :class="isActive('prestadorResenas') ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'">
              {{ dashboardData.estadisticas.total_resenas }}
            </span>
          </div>
        </router-link>

        <router-link 
          to="/prestador/configuracion" 
          class="flex items-center px-4 py-3 rounded-lg transition-all group mt-1"
          :class="isActive('prestadorConfiguracion') ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transition-colors"
               :class="isActive('prestadorConfiguracion') ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 group-hover:bg-gray-200'">
            <font-awesome-icon :icon="['fas', 'cog']" />
          </div>
          <span>Configuración</span>
        </router-link>
      </div>
    </nav>

    <!-- Links rápidos -->
    <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-100">
      <h3 class="text-sm font-semibold text-gray-900 mb-3">Enlaces Rápidos</h3>
      <div class="space-y-2">
        <router-link 
          to="/buscar" 
          class="flex items-center text-sm text-gray-700 hover:text-blue-600 transition-colors"
        >
          <font-awesome-icon :icon="['fas', 'search']" class="mr-2 text-xs" />
          Buscar Servicios
        </router-link>
        <router-link 
          to="/planes" 
          class="flex items-center text-sm text-gray-700 hover:text-blue-600 transition-colors"
        >
          <font-awesome-icon :icon="['fas', 'crown']" class="mr-2 text-xs" />
          Ver Planes
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  dashboardData: {
    type: Object,
    default: null
  }
});

const route = useRoute();

const isActive = (routeName) => {
  return route.name === routeName;
};

const serviciosPercentage = computed(() => {
  if (!props.dashboardData?.limitaciones?.puede_crear_servicios) return 0;
  const total = props.dashboardData?.estadisticas?.total_servicios || 0;
  const max = props.dashboardData?.limitaciones?.max_servicios || 1;
  return Math.min((total / max) * 100, 100);
});
</script>