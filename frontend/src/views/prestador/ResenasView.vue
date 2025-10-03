<template>
  <PrestadorLayout 
    title="Reseñas" 
    subtitle="Gestiona las valoraciones de tus clientes"
    breadcrumb="Reseñas"
    :plan-name="dashboardData?.plan?.name"
    :dashboard-data="dashboardData"
    @logout="authStore.logout"
  >
    <FeatureCard
      :has-permission="canReceiveReviews"
      title="Reseñas"
      blocked-title="Recibe Valoraciones de tus Clientes"
      message="La función de reseñas no está disponible en tu plan actual. Actualiza para recibir valoraciones y construir confianza con futuros clientes."
      icon="star"
      :features="['Recibir reseñas ilimitadas', 'Mostrar calificación promedio', 'Responder a clientes', 'Aumentar tu credibilidad']"
    >
      <div class="space-y-6">
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'star']" class="text-yellow-600 text-xl" />
              </div>
            </div>
            <p class="text-3xl font-bold text-gray-900 mb-1">
              {{ loadingDashboard ? '...' : (dashboardData?.estadisticas?.promedio_calificacion || '0.0') }}
            </p>
            <p class="text-sm text-gray-600">Calificación Promedio</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'comments']" class="text-purple-600 text-xl" />
              </div>
            </div>
            <p class="text-3xl font-bold text-gray-900 mb-1">
              {{ loadingDashboard ? '...' : (dashboardData?.estadisticas?.total_resenas || 0) }}
            </p>
            <p class="text-sm text-gray-600">Total de Reseñas</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'thumbs-up']" class="text-green-600 text-xl" />
              </div>
            </div>
            <p class="text-3xl font-bold text-gray-900 mb-1">
              {{ loadingDashboard ? '...' : '100%' }}
            </p>
            <p class="text-sm text-gray-600">Satisfacción</p>
          </div>
        </div>

        <!-- Lista de reseñas -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
            <h2 class="text-xl font-bold text-gray-900">Todas las Reseñas</h2>
            <p class="text-sm text-gray-600 mt-1">Valoraciones recibidas de tus clientes</p>
          </div>

          <div v-if="loading" class="p-12 text-center">
            <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-4xl animate-spin mb-4" />
            <p class="text-gray-600">Cargando reseñas...</p>
          </div>

          <div v-else-if="resenas.length" class="divide-y divide-gray-200">
            <div 
              v-for="resena in resenas" 
              :key="resena.id" 
              class="p-6 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                    {{ resena.nombre?.charAt(0).toUpperCase() || 'U' }}
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900 text-lg">{{ resena.nombre || 'Usuario' }}</h3>
                    <div class="flex items-center mt-1">
                      <div class="flex text-yellow-400 mr-3">
                        <font-awesome-icon 
                          :icon="['fas', 'star']" 
                          v-for="i in 5" 
                          :key="i"
                          :class="i <= (resena.calificacion || 0) ? 'text-yellow-400' : 'text-gray-300'"
                          class="text-sm"
                        />
                      </div>
                      <span class="text-sm text-gray-500">{{ resena.fecha || 'Fecha no disponible' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <p class="text-gray-700 leading-relaxed">{{ resena.comentario || 'Sin comentario' }}</p>
            </div>
          </div>

          <div v-else class="p-12">
            <div class="text-center max-w-md mx-auto">
              <div class="w-20 h-20 bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <font-awesome-icon :icon="['fas', 'star']" class="text-yellow-600 text-3xl" />
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">Aún no tienes reseñas</h3>
              <p class="text-gray-600 leading-relaxed">
                Las valoraciones de tus clientes aparecerán aquí. Ofrece un excelente servicio para recibir buenas reseñas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </FeatureCard>
  </PrestadorLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { misServiciosService } from '../../services/api';
import PrestadorLayout from '../../components/PrestadorLayout.vue';
import FeatureCard from '../../components/FeatureCard.vue';

const authStore = useAuthStore();

const resenas = ref([]);
const dashboardData = ref(null);
const loading = ref(false);
const loadingDashboard = ref(false);

const canReceiveReviews = computed(() => dashboardData.value?.limitaciones?.puede_recibir_resenas ?? true);

async function loadDashboard() {
  loadingDashboard.value = true;
  try {
    const response = await misServiciosService.getDashboard();
    dashboardData.value = response.data;
    resenas.value = response.data.ultimas_resenas || [];
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