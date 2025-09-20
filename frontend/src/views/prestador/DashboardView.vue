<template>
  <div class="min-h-screen bg-neutral-50">
    <!-- Cabecera -->
    <header class="bg-white shadow-sm">
      <div class="container-custom py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-xl font-semibold text-neutral-900">Panel de prestador</h1>
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
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
            <div class="p-4 bg-primary-50 border-b border-neutral-200">
              <h2 class="font-medium text-primary-800">Navegación</h2>
            </div>
            <nav class="p-2">
              <a href="#" class="flex items-center px-3 py-2 rounded-md bg-primary-100 text-primary-800 font-medium">
                <font-awesome-icon :icon="['fas', 'tachometer-alt']" class="mr-3" />
                Panel principal
              </a>
              <a href="#" class="flex items-center px-3 py-2 rounded-md text-neutral-700 hover:bg-neutral-50 mt-1">
                <font-awesome-icon :icon="['fas', 'user']" class="mr-3" />
                Mi perfil
              </a>
              <a href="#" class="flex items-center px-3 py-2 rounded-md text-neutral-700 hover:bg-neutral-50 mt-1">
                <font-awesome-icon :icon="['fas', 'cog']" class="mr-3" />
                Configuración
              </a>
              <a href="#" class="flex items-center px-3 py-2 rounded-md text-neutral-700 hover:bg-neutral-50 mt-1">
                <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-3" />
                Mis servicios
              </a>
              <a href="#" class="flex items-center px-3 py-2 rounded-md text-neutral-700 hover:bg-neutral-50 mt-1">
                <font-awesome-icon :icon="['fas', 'star']" class="mr-3" />
                Reseñas
              </a>
            </nav>
          </div>
        </div>
        
        <!-- Contenido -->
        <div class="md:col-span-3">
          <!-- Tarjetas de resumen -->
          <div class="grid md:grid-cols-3 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-4">
              <div class="flex items-center">
                <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
                  <font-awesome-icon :icon="['fas', 'eye']" />
                </div>
                <div>
                  <h3 class="text-sm text-neutral-500 font-medium">Visualizaciones</h3>
                  <p class="text-2xl font-semibold text-neutral-900">128</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-4">
              <div class="flex items-center">
                <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-4">
                  <font-awesome-icon :icon="['fas', 'star']" />
                </div>
                <div>
                  <h3 class="text-sm text-neutral-500 font-medium">Calificación</h3>
                  <p class="text-2xl font-semibold text-neutral-900">4.8</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-4">
              <div class="flex items-center">
                <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 mr-4">
                  <font-awesome-icon :icon="['fas', 'comments']" />
                </div>
                <div>
                  <h3 class="text-sm text-neutral-500 font-medium">Reseñas</h3>
                  <p class="text-2xl font-semibold text-neutral-900">12</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Información del plan -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Tu plan actual</h2>
              <button class="text-sm text-primary-600 hover:text-primary-800 font-medium">
                Cambiar plan
              </button>
            </div>
            
            <div class="flex items-center bg-primary-50 border border-primary-200 rounded-lg p-4">
              <div class="mr-4">
                <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
                  <font-awesome-icon :icon="['fas', 'crown']" />
                </div>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-neutral-900">Plan Premium</h3>
                <p class="text-sm text-neutral-600">Incluye reseñas, asesoría y reportes mensuales</p>
              </div>
              <div class="text-right">
                <p class="font-semibold text-neutral-900">$25/mes</p>
                <p class="text-xs text-neutral-500">Próximo pago: 15/10/2025</p>
              </div>
            </div>
          </div>
          
          <!-- Mis servicios -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Mis servicios</h2>
              <button 
                @click="showAddServiceModal = true"
                class="bg-primary-600 hover:bg-primary-700 text-white text-sm px-4 py-2 rounded-lg transition-colors"
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
                      <span :class="servicio.activo ? 'text-green-600' : 'text-red-600'">
                        <font-awesome-icon :icon="['fas', servicio.activo ? 'check-circle' : 'times-circle']" class="mr-1" />
                        {{ servicio.activo ? 'Activo' : 'Inactivo' }}
                      </span>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click="editService(servicio)"
                      class="text-neutral-600 hover:text-primary-600 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'edit']" />
                    </button>
                    <button 
                      @click="deleteService(servicio.id)"
                      class="text-neutral-600 hover:text-red-600 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'trash']" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-8 text-neutral-500">
              <font-awesome-icon :icon="['fas', 'briefcase']" class="text-3xl mb-2" />
              <p class="mb-4">Aún no tienes servicios publicados</p>
              <button 
                @click="showAddServiceModal = true"
                class="bg-primary-600 hover:bg-primary-700 text-white text-sm px-4 py-2 rounded-lg transition-colors"
              >
                Agregar mi primer servicio
              </button>
            </div>
          </div>
          
          <!-- Últimas reseñas -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Últimas reseñas</h2>
              <a href="#" class="text-sm text-primary-600 hover:text-primary-800 font-medium">
                Ver todas
              </a>
            </div>
            
            <div v-if="reseñas.length" class="space-y-4">
              <div v-for="(reseña, index) in reseñas" :key="index" class="border-b border-neutral-200 pb-4 last:border-0 last:pb-0">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-medium text-neutral-900">{{ reseña.nombre }}</h4>
                    <div class="flex text-yellow-400">
                      <font-awesome-icon :icon="['fas', 'star']" v-for="i in reseña.calificacion" :key="i" class="text-sm" />
                    </div>
                  </div>
                  <span class="text-xs text-neutral-500">{{ reseña.fecha }}</span>
                </div>
                <p class="text-sm text-neutral-600">{{ reseña.comentario }}</p>
              </div>
            </div>
            
            <div v-else class="text-center py-8 text-neutral-500">
              <font-awesome-icon :icon="['fas', 'comment-slash']" class="text-3xl mb-2" />
              <p>Aún no tienes reseñas</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';

const authStore = useAuthStore();

// Estado
const misServicios = ref([]);
const loading = ref(false);
const showAddServiceModal = ref(false);

// Cargar servicios
async function loadServicios() {
  loading.value = true;
  try {
    const response = await misServiciosService.getMisServicios();
    misServicios.value = response.data;
  } catch (error) {
    console.error('Error cargando servicios:', error);
  } finally {
    loading.value = false;
  }
}

// Acciones
function editService(servicio) {
  // TODO: Implementar modal de edición
  console.log('Editar servicio:', servicio);
}

async function deleteService(id) {
  if (confirm('¿Estás seguro de que quieres eliminar este servicio?')) {
    try {
      await misServiciosService.deleteServicio(id);
      await loadServicios();
    } catch (error) {
      console.error('Error eliminando servicio:', error);
    }
  }
}

onMounted(() => {
  loadServicios();
});

// Datos de ejemplo
const reseñas = [
  {
    nombre: 'María López',
    calificacion: 5,
    comentario: 'Excelente servicio, muy profesional y puntual. Recomendado al 100%.',
    fecha: 'Hace 2 días'
  },
  {
    nombre: 'Juan Pérez',
    calificacion: 4,
    comentario: 'Buen trabajo, aunque tardó un poco más de lo esperado.',
    fecha: 'Hace 1 semana'
  },
  {
    nombre: 'Ana García',
    calificacion: 5,
    comentario: 'Muy conforme con el trabajo realizado. Volveré a contratar sus servicios.',
    fecha: 'Hace 2 semanas'
  }
];
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
