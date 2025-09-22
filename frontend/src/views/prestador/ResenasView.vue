<template>
  <div class="min-h-screen bg-neutral-50">
    <!-- Cabecera -->
    <header class="bg-white shadow-sm">
      <div class="container-custom py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-semibold text-neutral-900">Mis reseñas</h1>
            <p class="text-sm text-neutral-600 mt-1">Gestiona las reseñas de tus clientes</p>
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
          <!-- Estadísticas de reseñas -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Estadísticas de reseñas</h2>
              <button class="text-sm text-primary-600 hover:text-primary-800 font-medium">
                Compartir perfil
              </button>
            </div>
            
            <div v-if="loadingDashboard" class="text-center py-8">
              <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
            </div>
            
            <div v-else-if="dashboardData?.estadisticas" class="grid md:grid-cols-3 gap-6">
              <!-- Calificación promedio -->
              <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mx-auto mb-3">
                  <span class="text-2xl font-bold text-yellow-600">
                    {{ dashboardData.estadisticas.promedio_calificacion || 0 }}
                  </span>
                </div>
                <h3 class="font-medium text-neutral-900">Calificación promedio</h3>
                <div class="flex justify-center mt-2">
                  <div class="flex text-yellow-400">
                    <font-awesome-icon 
                      v-for="i in 5" 
                      :key="i" 
                      :icon="['fas', i <= Math.round(dashboardData.estadisticas.promedio_calificacion || 0) ? 'star' : 'star']"
                      :class="i <= Math.round(dashboardData.estadisticas.promedio_calificacion || 0) ? 'text-yellow-400' : 'text-neutral-300'"
                      class="text-sm"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Total de reseñas -->
              <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                  <font-awesome-icon :icon="['fas', 'comments']" class="text-2xl text-blue-600" />
                </div>
                <h3 class="font-medium text-neutral-900">Total de reseñas</h3>
                <p class="text-2xl font-bold text-neutral-900 mt-1">
                  {{ dashboardData.estadisticas.total_resenas || 0 }}
                </p>
              </div>
              
              <!-- Visualizaciones del mes -->
              <div class="text-center">
                <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-3">
                  <font-awesome-icon :icon="['fas', 'eye']" class="text-2xl text-green-600" />
                </div>
                <h3 class="font-medium text-neutral-900">Visualizaciones</h3>
                <p class="text-2xl font-bold text-neutral-900 mt-1">
                  {{ dashboardData.estadisticas.visualizaciones_mes || 0 }}
                </p>
                <p class="text-xs text-neutral-500">este mes</p>
              </div>
            </div>
          </div>
          
          <!-- Distribución de calificaciones -->
          <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <h2 class="text-lg font-semibold text-neutral-900 mb-4">Distribución de calificaciones</h2>
            
            <div v-if="loadingResenas" class="text-center py-8">
              <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
            </div>
            
            <div v-else-if="distribucionCalificaciones.length" class="space-y-3">
              <div v-for="item in distribucionCalificaciones" :key="item.estrellas" class="flex items-center">
                <div class="flex items-center w-20">
                  <span class="text-sm font-medium text-neutral-700 mr-2">{{ item.estrellas }}</span>
                  <font-awesome-icon :icon="['fas', 'star']" class="text-yellow-400 text-sm" />
                </div>
                <div class="flex-1 mx-4">
                  <div class="w-full bg-neutral-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full bg-yellow-400 transition-all duration-300"
                      :style="`width: ${item.porcentaje}%`"
                    ></div>
                  </div>
                </div>
                <div class="w-12 text-right">
                  <span class="text-sm text-neutral-600">{{ item.cantidad }}</span>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-8 text-neutral-500">
              <font-awesome-icon :icon="['fas', 'chart-bar']" class="text-3xl mb-2" />
              <p>No hay suficientes reseñas para mostrar la distribución</p>
            </div>
          </div>
          
          <!-- Lista de reseñas -->
          <PermissionWrapper 
            :has-permission="canReceiveReviews" 
            title="Reseñas no disponibles"
            message="Función de reseñas no incluida en tu plan actual"
            icon="star"
            @upgrade="handleUpgrade"
          >
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg font-semibold text-neutral-900">Todas las reseñas</h2>
                <div class="flex items-center space-x-2">
                  <select 
                    v-model="filtroCalificacion" 
                    @change="filtrarResenas"
                    class="text-sm border border-neutral-300 rounded-lg px-3 py-1 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="">Todas las calificaciones</option>
                    <option value="5">5 estrellas</option>
                    <option value="4">4 estrellas</option>
                    <option value="3">3 estrellas</option>
                    <option value="2">2 estrellas</option>
                    <option value="1">1 estrella</option>
                  </select>
                  <select 
                    v-model="ordenResenas" 
                    @change="filtrarResenas"
                    class="text-sm border border-neutral-300 rounded-lg px-3 py-1 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="-fecha">Más recientes</option>
                    <option value="fecha">Más antiguas</option>
                    <option value="-calificacion">Mejor calificadas</option>
                    <option value="calificacion">Peor calificadas</option>
                  </select>
                </div>
              </div>
            
              <div v-if="loadingResenas" class="text-center py-8">
                <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
              </div>
              
              <div v-else-if="resenasFiltradas.length" class="space-y-4">
                <div v-for="resena in resenasFiltradas" :key="resena.id" class="border border-neutral-200 rounded-lg p-4">
                  <div class="flex justify-between items-start mb-3">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                        <span class="text-primary-600 font-medium text-sm">
                          {{ resena.nombre.charAt(0).toUpperCase() }}
                        </span>
                      </div>
                      <div>
                        <h4 class="font-medium text-neutral-900">{{ resena.nombre }}</h4>
                        <div class="flex text-yellow-400">
                          <font-awesome-icon 
                            v-for="i in 5" 
                            :key="i" 
                            :icon="['fas', 'star']"
                            :class="i <= resena.calificacion ? 'text-yellow-400' : 'text-neutral-300'"
                            class="text-sm"
                          />
                        </div>
                      </div>
                    </div>
                    <span class="text-xs text-neutral-500">{{ formatDate(resena.fecha) }}</span>
                  </div>
                  <p class="text-neutral-700 leading-relaxed">{{ resena.comentario }}</p>
                  
                  <!-- Acciones (solo para reseñas recientes o si es necesario) -->
                  <div class="flex justify-end mt-3 pt-3 border-t border-neutral-100">
                    <button 
                      @click="responderResena(resena)"
                      class="text-sm text-primary-600 hover:text-primary-800 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'reply']" class="mr-1" />
                      Responder
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-12 text-neutral-500">
                <font-awesome-icon :icon="['fas', 'comment-slash']" class="text-4xl mb-4" />
                <h3 class="text-lg font-medium mb-2">Aún no tienes reseñas</h3>
                <p class="mb-6">Cuando los clientes dejen reseñas sobre tus servicios, aparecerán aquí</p>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
                  <h4 class="font-medium text-blue-900 mb-2">💡 Consejos para recibir reseñas:</h4>
                  <ul class="text-sm text-blue-800 text-left space-y-1">
                    <li>• Proporciona un excelente servicio</li>
                    <li>• Comunica claramente con tus clientes</li>
                    <li>• Cumple con los tiempos acordados</li>
                    <li>• Solicita feedback al finalizar el trabajo</li>
                  </ul>
                </div>
              </div>
            </div>
          </PermissionWrapper>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService, prestadorService } from '../../services/api';
import PermissionWrapper from '../../components/PermissionWrapper.vue';
import DashboardNavigation from '../../components/DashboardNavigation.vue';

const authStore = useAuthStore();

// Estado
const resenas = ref([]);
const resenasFiltradas = ref([]);
const dashboardData = ref(null);
const loadingResenas = ref(false);
const loadingDashboard = ref(false);
const filtroCalificacion = ref('');
const ordenResenas = ref('-fecha');

// Computed para limitaciones por plan
const canReceiveReviews = computed(() => {
  return dashboardData.value?.limitaciones?.puede_recibir_resenas ?? true;
});

// Computed para distribución de calificaciones
const distribucionCalificaciones = computed(() => {
  if (!resenas.value.length) return [];
  
  const distribucion = {};
  for (let i = 1; i <= 5; i++) {
    distribucion[i] = 0;
  }
  
  resenas.value.forEach(resena => {
    distribucion[resena.calificacion]++;
  });
  
  const total = resenas.value.length;
  return Object.entries(distribucion).map(([estrellas, cantidad]) => ({
    estrellas: parseInt(estrellas),
    cantidad,
    porcentaje: total > 0 ? (cantidad / total) * 100 : 0
  })).reverse();
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

// Cargar reseñas
async function loadResenas() {
  loadingResenas.value = true;
  try {
    const response = await misServiciosService.getMisResenas();
    resenas.value = response.data.resenas || [];
    filtrarResenas();
  } catch (error) {
    console.error('Error cargando reseñas:', error);
  } finally {
    loadingResenas.value = false;
  }
}

// Filtrar reseñas
function filtrarResenas() {
  let filtradas = [...resenas.value];
  
  // Filtrar por calificación
  if (filtroCalificacion.value) {
    filtradas = filtradas.filter(resena => resena.calificacion === parseInt(filtroCalificacion.value));
  }
  
  // Ordenar
  filtradas.sort((a, b) => {
    const [campo, direccion] = ordenResenas.value.startsWith('-') 
      ? [ordenResenas.value.slice(1), 'desc'] 
      : [ordenResenas.value, 'asc'];
    
    if (campo === 'fecha') {
      const fechaA = new Date(a.fecha);
      const fechaB = new Date(b.fecha);
      return direccion === 'desc' ? fechaB - fechaA : fechaA - fechaB;
    } else if (campo === 'calificacion') {
      return direccion === 'desc' ? b.calificacion - a.calificacion : a.calificacion - b.calificacion;
    }
    return 0;
  });
  
  resenasFiltradas.value = filtradas;
}

// Acciones
function responderResena(resena) {
  // TODO: Implementar modal de respuesta a reseña
  console.log('Responder a reseña:', resena);
  alert('Funcionalidad de respuesta a reseñas próximamente disponible');
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

onMounted(async () => {
  await loadDashboard();
  await loadResenas();
});
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
