<template>
  <div class="min-h-screen bg-neutral-50">
    <!-- Cabecera -->
    <header class="bg-white shadow-sm">
      <div class="container-custom py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-semibold text-neutral-900">Mis servicios</h1>
            <p class="text-sm text-neutral-600 mt-1">Gestiona los servicios que ofreces</p>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-neutral-600">{{ authStore.fullName }}</span>
            <button 
              @click="authStore.logout"
              class="text-sm text-neutral-600 hover:text-neutral-900 transition-colors"
            >
              <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-1" />
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Contenido principal -->
    <div class="container-custom py-8">
      <div class="grid md:grid-cols-4 gap-6">
        <!-- Menú lateral -->
        <div class="md:col-span-1">
          <DashboardNavigation />
        </div>
        
        <!-- Contenido -->
        <div class="md:col-span-3">
          <!-- Información del plan y límites -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Límites de tu plan</h2>
              <button class="text-sm text-primary-600 hover:text-primary-800 font-medium">
                Cambiar plan
              </button>
            </div>
            
            <div v-if="loadingDashboard" class="text-center py-8">
              <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
            </div>
            
            <div v-else-if="dashboardData?.plan" class="flex items-center bg-primary-50 border border-primary-200 rounded-lg p-4">
              <div class="mr-4">
                <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
                  <font-awesome-icon :icon="['fas', 'crown']" />
                </div>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-neutral-900">{{ dashboardData.plan.name }}</h3>
                <p class="text-sm text-neutral-600 mb-2">
                  {{ dashboardData.plan.fields_enabled?.length || 0 }} campos habilitados, 
                  {{ dashboardData.plan.max_images }} imágenes, 
                  {{ dashboardData.plan.max_videos }} videos
                </p>
                <!-- Barra de progreso de servicios -->
                <div class="text-xs text-neutral-500 mb-1">
                  Servicios: {{ dashboardData.estadisticas?.total_servicios || 0 }} / {{ dashboardData.limitaciones?.max_servicios || 0 }}
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="canAddService ? 'bg-green-500' : 'bg-red-500'"
                    :style="`width: ${Math.min((dashboardData.estadisticas?.total_servicios || 0) / (dashboardData.limitaciones?.max_servicios || 1) * 100, 100)}%`"
                  ></div>
                </div>
              </div>
              <div class="text-right">
                <p class="font-semibold text-neutral-900">{{ dashboardData.plan.price_text }}</p>
                <p class="text-xs text-neutral-500" v-if="dashboardData.plan.precio_mensual > 0">Mensual</p>
              </div>
            </div>
            
            <div v-else class="flex items-center bg-neutral-50 border border-neutral-200 rounded-lg p-4">
              <div class="mr-4">
                <div class="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center text-neutral-600">
                  <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
                </div>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-neutral-900">Sin plan asignado</h3>
                <p class="text-sm text-neutral-600">Contacta al administrador para asignar un plan</p>
              </div>
            </div>
          </div>
          
          <!-- Mis servicios -->
          <PermissionWrapper 
            :has-permission="canCreateServices" 
            title="Servicios no disponibles"
            message="Creación de servicios no incluida en tu plan actual"
            icon="briefcase"
            @upgrade="handleUpgrade"
          >
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg font-semibold text-neutral-900">Mis servicios</h2>
                <button 
                  @click="showAddServiceModal = true"
                  :disabled="!canAddService"
                  :class="canAddService 
                    ? 'bg-primary-600 hover:bg-primary-700 text-white' 
                    : 'bg-neutral-300 text-neutral-500 cursor-not-allowed'"
                  class="text-sm px-4 py-2 rounded-lg transition-colors"
                  :title="!canAddService ? `Límite alcanzado: ${dashboardData?.limitaciones?.max_servicios || 0} servicios máximo` : ''"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Agregar servicio
                </button>
              </div>
            
              <div v-if="loading" class="text-center py-8">
                <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
              </div>
              
              <div v-else-if="misServicios.length" class="space-y-4">
                <div v-for="servicio in misServicios" :key="servicio.id" class="border border-neutral-200 rounded-lg p-4">
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <h3 class="font-medium text-neutral-900">{{ servicio.nombre }}</h3>
                      <p class="text-sm text-neutral-600 mt-1">{{ servicio.descripcion }}</p>
                      <div class="flex items-center mt-2 text-sm text-neutral-500">
                        <span v-if="servicio.precio_base" class="mr-4">
                          <font-awesome-icon :icon="['fas', 'dollar-sign']" class="mr-1" />
                          ${{ servicio.precio_base }}
                        </span>
                        <span class="mr-4">
                          <font-awesome-icon :icon="['fas', 'tag']" class="mr-1" />
                          {{ servicio.categoria_nombre }} - {{ servicio.rubro_nombre }}
                        </span>
                        <span :class="servicio.activo ? 'text-green-600' : 'text-red-600'">
                          <font-awesome-icon :icon="['fas', servicio.activo ? 'check-circle' : 'times-circle']" class="mr-1" />
                          {{ servicio.activo ? 'Activo' : 'Inactivo' }}
                        </span>
                      </div>
                      <div class="text-xs text-neutral-400 mt-2">
                        Creado: {{ formatDate(servicio.fecha_creacion) }}
                      </div>
                    </div>
                    <div class="flex space-x-2">
                      <button 
                        @click="editService(servicio)"
                        class="text-neutral-600 hover:text-primary-600 transition-colors p-2"
                        title="Editar servicio"
                      >
                        <font-awesome-icon :icon="['fas', 'edit']" />
                      </button>
                      <button 
                        @click="deleteService(servicio.id)"
                        class="text-neutral-600 hover:text-red-600 transition-colors p-2"
                        title="Eliminar servicio"
                      >
                        <font-awesome-icon :icon="['fas', 'trash']" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-12 text-neutral-500">
                <font-awesome-icon :icon="['fas', 'briefcase']" class="text-4xl mb-4" />
                <h3 class="text-lg font-medium mb-2">Aún no tienes servicios publicados</h3>
                <p class="mb-6">Comienza agregando tu primer servicio para que los clientes puedan encontrarte</p>
                <button 
                  @click="showAddServiceModal = true"
                  :disabled="!canAddService"
                  :class="canAddService 
                    ? 'bg-primary-600 hover:bg-primary-700 text-white' 
                    : 'bg-neutral-300 text-neutral-500 cursor-not-allowed'"
                  class="px-6 py-3 rounded-lg transition-colors"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Agregar mi primer servicio
                </button>
              </div>
            </div>
          </PermissionWrapper>
        </div>
      </div>
    </div>
    
    <!-- Modal de servicios -->
    <ServiceModal 
      :show="showAddServiceModal"
      :servicio="servicioEditando"
      @close="closeServiceModal"
      @saved="onServiceSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';
import PermissionWrapper from '../../components/PermissionWrapper.vue';
import DashboardNavigation from '../../components/DashboardNavigation.vue';
import ServiceModal from '../../components/ServiceModal.vue';

const authStore = useAuthStore();

// Estado
const misServicios = ref([]);
const dashboardData = ref(null);
const loading = ref(false);
const loadingDashboard = ref(false);
const showAddServiceModal = ref(false);
const servicioEditando = ref(null);

// Computed para limitaciones por plan
const canCreateServices = computed(() => {
  return dashboardData.value?.limitaciones?.puede_crear_servicios ?? true;
});

const canAddService = computed(() => {
  if (!canCreateServices.value) return false;
  if (!dashboardData.value?.limitaciones) return true;
  const totalServicios = dashboardData.value.estadisticas?.total_servicios || 0;
  const maxServicios = dashboardData.value.limitaciones.max_servicios;
  return totalServicios < maxServicios;
});

// Cargar datos del dashboard
async function loadDashboard() {
  loadingDashboard.value = true;
  try {
    const response = await misServiciosService.getDashboard();
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Error cargando dashboard:', error);
  } finally {
    loadingDashboard.value = false;
  }
}

// Cargar servicios
async function loadServicios() {
  loading.value = true;
  try {
    const response = await misServiciosService.getMisServicios();
    misServicios.value = response.data.servicios || response.data;
  } catch (error) {
    console.error('Error cargando servicios:', error);
  } finally {
    loading.value = false;
  }
}

// Acciones
function editService(servicio) {
  servicioEditando.value = servicio;
  showAddServiceModal.value = true;
}

async function deleteService(id) {
  if (confirm('¿Estás seguro de que quieres eliminar este servicio?')) {
    try {
      await misServiciosService.deleteServicio(id);
      await loadServicios();
      await loadDashboard(); // Recargar dashboard para actualizar contadores
    } catch (error) {
      console.error('Error eliminando servicio:', error);
      alert('Error al eliminar el servicio. Por favor, intenta nuevamente.');
    }
  }
}

function closeServiceModal() {
  showAddServiceModal.value = false;
  servicioEditando.value = null;
}

async function onServiceSaved() {
  await loadServicios();
  await loadDashboard(); // Recargar dashboard para actualizar contadores
}

// Función para manejar upgrade de plan
function handleUpgrade() {
  // TODO: Implementar redirección a página de planes o modal de upgrade
  console.log('Redirigir a upgrade de plan');
  alert('Funcionalidad de upgrade de plan próximamente disponible');
}

// Función para formatear fechas
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

onMounted(() => {
  loadDashboard();
  loadServicios();
});
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
