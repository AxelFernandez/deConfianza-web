<template>
  <PrestadorLayout 
    title="Dashboard" 
    :subtitle="`Bienvenido, ${authStore.user?.first_name || authStore.user?.username}`"
    :plan-name="dashboardData?.plan?.name"
    :dashboard-data="dashboardData"
    @logout="authStore.logout"
  >
    <div class="space-y-6">
          <!-- Plan móvil -->
          <router-link 
            to="/planes"
            class="sm:hidden block bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-4 text-white shadow-lg"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <font-awesome-icon :icon="['fas', 'crown']" class="text-2xl mr-3" />
                <div>
                  <p class="text-sm opacity-90">Tu Plan</p>
                  <p class="font-bold text-lg">{{ dashboardData?.plan?.name || 'Cargando...' }}</p>
                </div>
              </div>
              <font-awesome-icon :icon="['fas', 'chevron-right']" />
            </div>
          </router-link>

          <!-- Stats -->
          <div v-if="canViewStats" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between mb-4">
                <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'eye']" class="text-blue-600 text-xl" />
                </div>
                <span class="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-full">Este mes</span>
              </div>
              <p class="text-3xl font-bold text-gray-900 mb-1">
                {{ loadingDashboard ? '...' : (dashboardData?.estadisticas?.total_visualizaciones || 0) }}
              </p>
              <p class="text-sm text-gray-600">Visualizaciones</p>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between mb-4">
                <div class="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'star']" class="text-yellow-600 text-xl" />
                </div>
                <span class="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-full">Promedio</span>
              </div>
              <p class="text-3xl font-bold text-gray-900 mb-1">
                {{ loadingDashboard ? '...' : (dashboardData?.estadisticas?.promedio_calificacion || '0.0') }}
              </p>
              <p class="text-sm text-gray-600">Calificación</p>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between mb-4">
                <div class="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'comments']" class="text-purple-600 text-xl" />
                </div>
                <span class="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-full">Total</span>
              </div>
              <p class="text-3xl font-bold text-gray-900 mb-1">
                {{ loadingDashboard ? '...' : (dashboardData?.estadisticas?.total_resenas || 0) }}
              </p>
              <p class="text-sm text-gray-600">Reseñas</p>
            </div>
          </div>

          <!-- Stats bloqueadas -->
          <div v-else class="bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl p-8 text-center border-2 border-dashed border-gray-300">
            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
              <font-awesome-icon :icon="['fas', 'lock']" class="text-gray-400 text-2xl" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Estadísticas Premium</h3>
            <p class="text-gray-600 mb-4">Actualiza tu plan para ver estadísticas detalladas</p>
            <router-link to="/planes" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
              <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
              Mejorar Plan
            </router-link>
          </div>

          <!-- Servicios -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Mis Servicios</h2>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ dashboardData?.estadisticas?.total_servicios || 0 }} de {{ dashboardData?.limitaciones?.max_servicios || '∞' }} publicados
                  </p>
                </div>
                <router-link v-if="canCreateServices" to="/prestador/servicios" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                  Gestionar
                </router-link>
                <router-link v-else to="/planes" class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors">
                  Desbloquear
                </router-link>
              </div>
            </div>

            <div v-if="canCreateServices" class="p-6">
              <div v-if="loading" class="text-center py-12">
                <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-3xl animate-spin" />
              </div>

              <div v-else-if="misServicios.length" class="space-y-4">
                <div v-for="servicio in misServicios.slice(0, 3)" :key="servicio.id" class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-all">
                  <div class="flex-1">
                    <div class="flex items-center mb-2">
                      <h3 class="font-semibold text-gray-900">{{ servicio.nombre }}</h3>
                      <span class="ml-3 px-2 py-1 text-xs font-medium rounded-full" :class="servicio.activo ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                        {{ servicio.activo ? 'Activo' : 'Inactivo' }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-600">{{ servicio.descripcion }}</p>
                  </div>
                  <div class="ml-4 flex space-x-2">
                    <button @click="editService(servicio)" class="w-9 h-9 flex items-center justify-center rounded-lg text-gray-600 hover:bg-blue-50 hover:text-blue-600">
                      <font-awesome-icon :icon="['fas', 'edit']" />
                    </button>
                    <button @click="deleteService(servicio.id)" class="w-9 h-9 flex items-center justify-center rounded-lg text-gray-600 hover:bg-red-50 hover:text-red-600">
                      <font-awesome-icon :icon="['fas', 'trash']" />
                    </button>
                  </div>
                </div>
                <router-link v-if="misServicios.length > 3" to="/prestador/servicios" class="block text-center py-3 text-blue-600 hover:bg-blue-50 rounded-lg font-medium">
                  Ver todos ({{ misServicios.length }})
                </router-link>
              </div>

              <div v-else class="text-center py-12">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <font-awesome-icon :icon="['fas', 'briefcase']" class="text-gray-400 text-2xl" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">No tienes servicios</h3>
                <p class="text-gray-600 mb-4">Publica tus servicios para que los clientes te encuentren</p>
                <router-link to="/prestador/servicios" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Crear servicio
                </router-link>
              </div>
            </div>

            <div v-else class="p-6">
              <div class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
                <font-awesome-icon :icon="['fas', 'lock']" class="text-gray-400 text-3xl mb-4" />
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Servicios bloqueados</h3>
                <p class="text-gray-600 mb-4">No disponible en tu plan actual</p>
                <router-link to="/planes" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Mejorar Plan
                </router-link>
              </div>
            </div>
          </div>

          <!-- Reseñas -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Últimas Reseñas</h2>
                  <p class="text-sm text-gray-600 mt-1">{{ dashboardData?.estadisticas?.total_resenas || 0 }} reseñas</p>
                </div>
                <router-link v-if="canReceiveReviews" to="/prestador/resenas" class="text-blue-600 hover:text-blue-700 font-medium text-sm">
                  Ver todas →
                </router-link>
              </div>
            </div>

            <div v-if="canReceiveReviews" class="p-6">
              <div v-if="loadingDashboard" class="text-center py-12">
                <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-3xl animate-spin" />
              </div>

              <div v-else-if="dashboardData?.ultimas_resenas?.length" class="space-y-4">
                <div v-for="resena in dashboardData.ultimas_resenas" :key="resena.id" class="p-4 border border-gray-200 rounded-lg">
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                        {{ resena.nombre.charAt(0).toUpperCase() }}
                      </div>
                      <div>
                        <h4 class="font-semibold text-gray-900">{{ resena.nombre }}</h4>
                        <div class="flex text-yellow-400 text-sm">
                          <font-awesome-icon :icon="['fas', 'star']" v-for="i in 5" :key="i" :class="i <= resena.calificacion ? 'text-yellow-400' : 'text-gray-300'" />
                        </div>
                      </div>
                    </div>
                    <span class="text-xs text-gray-500">{{ resena.fecha }}</span>
                  </div>
                  <p class="text-sm text-gray-700">{{ resena.comentario }}</p>
                </div>
              </div>

              <div v-else class="text-center py-12">
                <font-awesome-icon :icon="['fas', 'comment-slash']" class="text-gray-400 text-3xl mb-4" />
                <p class="text-gray-600">Sin reseñas aún</p>
              </div>
            </div>

            <div v-else class="p-6">
              <div class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
                <font-awesome-icon :icon="['fas', 'lock']" class="text-gray-400 text-3xl mb-4" />
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Reseñas bloqueadas</h3>
                <p class="text-gray-600 mb-4">No disponible en tu plan actual</p>
                <router-link to="/planes" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Mejorar Plan
                </router-link>
              </div>
            </div>
          </div>
    </div>

    <ServiceModal :show="showAddServiceModal" :servicio="servicioEditando" @close="closeServiceModal" @saved="onServiceSaved" />
  </PrestadorLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';
import PrestadorLayout from '../../components/PrestadorLayout.vue';
import ServiceModal from '../../components/ServiceModal.vue';

const authStore = useAuthStore();

const misServicios = ref([]);
const dashboardData = ref(null);
const loading = ref(false);
const loadingDashboard = ref(false);
const showAddServiceModal = ref(false);
const servicioEditando = ref(null);

const canCreateServices = computed(() => dashboardData.value?.limitaciones?.puede_crear_servicios ?? true);
const canReceiveReviews = computed(() => dashboardData.value?.limitaciones?.puede_recibir_resenas ?? true);
const canViewStats = computed(() => dashboardData.value?.limitaciones?.puede_ver_estadisticas ?? true);

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

async function loadServicios() {
  loading.value = true;
  try {
    const response = await misServiciosService.getMisServicios();
    misServicios.value = response.data.servicios || response.data;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loading.value = false;
  }
}

function editService(servicio) {
  servicioEditando.value = servicio;
  showAddServiceModal.value = true;
}

async function deleteService(id) {
  if (confirm('¿Eliminar servicio?')) {
    try {
      await misServiciosService.deleteServicio(id);
      await loadServicios();
      await loadDashboard();
    } catch (error) {
      alert('Error al eliminar');
    }
  }
}

function closeServiceModal() {
  showAddServiceModal.value = false;
  servicioEditando.value = null;
}

async function onServiceSaved() {
  await loadServicios();
  await loadDashboard();
}

onMounted(() => {
  loadDashboard();
  loadServicios();
});
</script>