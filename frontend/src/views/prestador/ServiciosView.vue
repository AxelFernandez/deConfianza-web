<template>
  <PrestadorLayout 
    title="Mis Servicios" 
    subtitle="Gestiona los servicios que ofreces"
    breadcrumb="Servicios"
    :plan-name="dashboardData?.plan?.name"
    :dashboard-data="dashboardData"
    @logout="authStore.logout"
  >
    <FeatureCard
      :has-permission="canCreateServices"
      title="Servicios"
      blocked-title="Crea y Gestiona tus Servicios"
      message="La creación de servicios no está disponible en tu plan actual. Actualiza para publicar tus servicios y conectar con clientes."
      icon="briefcase"
      :features="['Publicar servicios ilimitados', 'Editar información en tiempo real', 'Gestionar disponibilidad', 'Recibir solicitudes de clientes']"
    >
      <div class="space-y-6">
        <!-- Header con botón agregar -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-gray-900">Tus Servicios</h2>
              <p class="text-sm text-gray-600 mt-1">
                {{ servicios.length }} de {{ dashboardData?.limitaciones?.max_servicios || '∞' }} servicios publicados
              </p>
            </div>
            <button
              @click="showModal = true"
              :disabled="!canAddService"
              class="flex items-center px-6 py-3 rounded-xl font-semibold transition-all shadow-sm"
              :class="canAddService 
                ? 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md transform hover:scale-105' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'"
              :title="!canAddService ? `Límite alcanzado: ${dashboardData?.limitaciones?.max_servicios || 0} servicios máximo` : ''"
            >
              <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
              Nuevo Servicio
            </button>
          </div>

          <!-- Progreso -->
          <div v-if="dashboardData?.limitaciones" class="mt-4">
            <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>Uso de servicios</span>
              <span class="font-semibold">{{ serviciosPercentage }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div 
                class="h-3 rounded-full transition-all duration-500"
                :class="serviciosPercentage < 80 ? 'bg-green-500' : serviciosPercentage < 100 ? 'bg-yellow-500' : 'bg-red-500'"
                :style="`width: ${serviciosPercentage}%`"
              ></div>
            </div>
          </div>
        </div>

        <!-- Lista de servicios -->
        <div v-if="loading" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12">
          <div class="text-center">
            <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-4xl animate-spin mb-4" />
            <p class="text-gray-600">Cargando servicios...</p>
          </div>
        </div>

        <div v-else-if="servicios.length" class="grid gap-4">
          <div 
            v-for="servicio in servicios" 
            :key="servicio.id" 
            class="bg-white rounded-xl shadow-sm border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all overflow-hidden group"
          >
            <div class="p-6">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <!-- Header del servicio -->
                  <div class="flex items-center mb-3">
                    <div class="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg flex items-center justify-center mr-4 group-hover:from-blue-200 group-hover:to-blue-300 transition-all">
                      <font-awesome-icon :icon="['fas', 'briefcase']" class="text-blue-600 text-xl" />
                    </div>
                    <div class="flex-1">
                      <h3 class="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {{ servicio.nombre }}
                      </h3>
                      <div class="flex items-center mt-1 space-x-3">
                        <span 
                          class="px-3 py-1 text-xs font-semibold rounded-full"
                          :class="servicio.activo ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                        >
                          {{ servicio.activo ? '● Activo' : '● Inactivo' }}
                        </span>
                        <span v-if="servicio.precio_base" class="text-sm text-gray-600 font-medium">
                          ${{ servicio.precio_base }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Descripción -->
                  <p class="text-gray-700 leading-relaxed mb-4">{{ servicio.descripcion }}</p>

                  <!-- Metadata -->
                  <div class="flex items-center space-x-4 text-sm text-gray-500">
                    <span v-if="servicio.categoria_nombre" class="flex items-center">
                      <font-awesome-icon :icon="['fas', 'tag']" class="mr-1 text-xs" />
                      {{ servicio.categoria_nombre }}
                    </span>
                    <span v-if="servicio.rubro_nombre" class="flex items-center">
                      <font-awesome-icon :icon="['fas', 'folder']" class="mr-1 text-xs" />
                      {{ servicio.rubro_nombre }}
                    </span>
                  </div>
                </div>

                <!-- Actions -->
                <div class="ml-4 flex flex-col space-y-2">
                  <button 
                    @click="editService(servicio)"
                    class="w-10 h-10 flex items-center justify-center rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
                    title="Editar servicio"
                  >
                    <font-awesome-icon :icon="['fas', 'edit']" />
                  </button>
                  <button 
                    @click="deleteService(servicio.id)"
                    class="w-10 h-10 flex items-center justify-center rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition-colors"
                    title="Eliminar servicio"
                  >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="bg-white rounded-xl shadow-sm border-2 border-dashed border-gray-300 p-12">
          <div class="text-center max-w-md mx-auto">
            <div class="w-20 h-20 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <font-awesome-icon :icon="['fas', 'briefcase']" class="text-blue-600 text-3xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">No tienes servicios aún</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Comienza a publicar tus servicios para que los clientes puedan encontrarte y contactarte fácilmente.
            </p>
            <button
              @click="showModal = true"
              class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
              Crear mi primer servicio
            </button>
          </div>
        </div>
      </div>
    </FeatureCard>

    <!-- Modal -->
    <ServiceModal 
      :show="showModal"
      :servicio="servicioEditando"
      @close="closeModal"
      @saved="onServiceSaved"
    />
  </PrestadorLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';
import PrestadorLayout from '../../components/PrestadorLayout.vue';
import FeatureCard from '../../components/FeatureCard.vue';
import ServiceModal from '../../components/ServiceModal.vue';

const authStore = useAuthStore();

const servicios = ref([]);
const dashboardData = ref(null);
const loading = ref(false);
const loadingDashboard = ref(false);
const showModal = ref(false);
const servicioEditando = ref(null);

const canCreateServices = computed(() => dashboardData.value?.limitaciones?.puede_crear_servicios ?? true);

const canAddService = computed(() => {
  if (!canCreateServices.value) return false;
  if (!dashboardData.value?.limitaciones) return true;
  const total = dashboardData.value.estadisticas?.total_servicios || 0;
  const max = dashboardData.value.limitaciones.max_servicios;
  return total < max;
});

const serviciosPercentage = computed(() => {
  if (!dashboardData.value?.limitaciones) return 0;
  const total = dashboardData.value.estadisticas?.total_servicios || 0;
  const max = dashboardData.value.limitaciones.max_servicios || 1;
  return Math.min(Math.round((total / max) * 100), 100);
});

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
    servicios.value = response.data.servicios || response.data;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loading.value = false;
  }
}

function editService(servicio) {
  servicioEditando.value = servicio;
  showModal.value = true;
}

async function deleteService(id) {
  if (confirm('¿Estás seguro de eliminar este servicio?')) {
    try {
      await misServiciosService.deleteServicio(id);
      await loadServicios();
      await loadDashboard();
    } catch (error) {
      alert('Error al eliminar el servicio');
    }
  }
}

function closeModal() {
  showModal.value = false;
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