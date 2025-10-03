<template>
  <PrestadorLayout 
    title="Configuración" 
    subtitle="Ajusta las preferencias de tu cuenta"
    breadcrumb="Configuración"
    :plan-name="dashboardData?.plan?.name"
    :dashboard-data="dashboardData"
    @logout="authStore.logout"
  >
    <div class="space-y-6">
      <!-- Información de la cuenta -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">Información de la Cuenta</h2>
          <p class="text-sm text-gray-600 mt-1">Datos básicos de tu perfil</p>
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-center justify-between py-3 border-b border-gray-100">
            <div>
              <p class="text-sm text-gray-600">Nombre de usuario</p>
              <p class="font-semibold text-gray-900">{{ authStore.user?.username }}</p>
            </div>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-gray-100">
            <div>
              <p class="text-sm text-gray-600">Email</p>
              <p class="font-semibold text-gray-900">{{ authStore.user?.email }}</p>
            </div>
          </div>
          <div class="flex items-center justify-between py-3">
            <div>
              <p class="text-sm text-gray-600">Nombre completo</p>
              <p class="font-semibold text-gray-900">
                {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Plan actual -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 border-b border-blue-100">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-gray-900">Tu Plan</h2>
              <p class="text-sm text-gray-600 mt-1">Gestiona tu suscripción</p>
            </div>
            <router-link 
              to="/planes"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Ver Planes
            </router-link>
          </div>
        </div>
        <div class="p-6">
          <div v-if="loadingDashboard" class="text-center py-8">
            <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-3xl animate-spin" />
          </div>
          <div v-else-if="dashboardData?.plan" class="flex items-center bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-6 text-white">
            <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center mr-6">
              <font-awesome-icon :icon="['fas', 'crown']" class="text-3xl" />
            </div>
            <div class="flex-1">
              <h3 class="text-2xl font-bold mb-2">{{ dashboardData.plan.name }}</h3>
              <div class="grid grid-cols-2 gap-4 text-sm opacity-90">
                <div>
                  <p class="mb-1">✓ {{ dashboardData.plan.max_servicios }} servicios</p>
                  <p>✓ {{ dashboardData.plan.max_images }} imágenes</p>
                </div>
                <div>
                  <p class="mb-1">✓ {{ dashboardData.plan.max_videos }} videos</p>
                  <p>✓ {{ dashboardData.plan.fields_enabled?.length || 0 }} campos</p>
                </div>
              </div>
            </div>
            <div class="text-right">
              <p class="text-3xl font-bold">{{ dashboardData.plan.price_text }}</p>
              <p class="text-sm opacity-90" v-if="dashboardData.plan.precio_mensual > 0">/mes</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Preferencias -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">Preferencias</h2>
          <p class="text-sm text-gray-600 mt-1">Ajusta la configuración de tu perfil</p>
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-center justify-between py-3 border-b border-gray-100">
            <div>
              <p class="font-semibold text-gray-900">Notificaciones por email</p>
              <p class="text-sm text-gray-600">Recibe actualizaciones en tu correo</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" class="sr-only peer" checked>
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-gray-100">
            <div>
              <p class="font-semibold text-gray-900">Perfil público</p>
              <p class="text-sm text-gray-600">Mostrar tu perfil en búsquedas</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" class="sr-only peer" checked>
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Zona de peligro -->
      <div class="bg-white rounded-xl shadow-sm border-2 border-red-200 overflow-hidden">
        <div class="bg-gradient-to-r from-red-50 to-pink-50 p-6 border-b border-red-200">
          <h2 class="text-xl font-bold text-red-900">Zona de Peligro</h2>
          <p class="text-sm text-red-700 mt-1">Acciones irreversibles</p>
        </div>
        <div class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-semibold text-gray-900">Eliminar cuenta</p>
              <p class="text-sm text-gray-600">Esta acción no se puede deshacer</p>
            </div>
            <button class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium">
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Sesión -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">Sesión</h2>
          <p class="text-sm text-gray-600 mt-1">Gestiona tu sesión actual</p>
        </div>
        <div class="p-6">
          <button 
            @click="authStore.logout"
            class="w-full flex items-center justify-center px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors font-medium"
          >
            <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-2" />
            Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  </PrestadorLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';
import PrestadorLayout from '../../components/PrestadorLayout.vue';

const authStore = useAuthStore();

const dashboardData = ref(null);
const loadingDashboard = ref(false);

async function loadDashboard() {
  loadingDashboard.value = true;
  try {
    const response = await misServiciosService.getDashboard();
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loadingDashboard.value = false;
  }
}

onMounted(() => {
  loadDashboard();
});
</script>