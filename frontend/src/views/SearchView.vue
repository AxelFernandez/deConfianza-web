<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- Hero Section con búsqueda -->
    <section class="relative bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white py-16">
      <div class="absolute inset-0 bg-black/10"></div>
      <div class="container-custom relative z-10">
        <div class="text-center mb-12">
          <h1 class="text-4xl md:text-5xl font-display font-bold mb-4">
            Encuentra el profesional perfecto
          </h1>
          <p class="text-xl text-blue-100 max-w-2xl mx-auto">
            Conectamos clientes con prestadores de servicios confiables en tu zona
          </p>
        </div>
        
        <!-- Formulario de búsqueda mejorado -->
        <div class="max-w-4xl mx-auto">
          <form @submit.prevent="realizarBusqueda" class="bg-white/95 backdrop-blur-sm p-8 rounded-2xl shadow-2xl">
            <div class="grid md:grid-cols-4 gap-4">
              <!-- Ubicación -->
              <div class="space-y-2">
                <label for="location" class="block text-sm font-semibold text-gray-700">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2 text-blue-600" />
                  Ubicación
                </label>
                <input 
                  type="text" 
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 bg-white/80" 
                  id="location" 
                  v-model="filtros.ubicacion"
                  placeholder="Ciudad, provincia..."
                >
              </div>
              
              <!-- Categoría -->
              <div class="space-y-2">
                <label for="category" class="block text-sm font-semibold text-gray-700">
                  <font-awesome-icon :icon="['fas', 'th-large']" class="mr-2 text-blue-600" />
                  Categoría
                </label>
                <select 
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 bg-white/80 appearance-none" 
                  id="category"
                  v-model="filtros.categoria"
                >
                  <option 
                    v-for="categoria in categorias" 
                    :key="categoria.id" 
                    :value="categoria.id"
                  >
                    {{ categoria.nombre }}
                  </option>
                </select>
              </div>
              
              <!-- Servicio -->
              <div class="space-y-2">
                <label for="service" class="block text-sm font-semibold text-gray-700">
                  <font-awesome-icon :icon="['fas', 'tools']" class="mr-2 text-blue-600" />
                  Servicio
                </label>
                <select 
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 bg-white/80 appearance-none" 
                  id="service"
                  v-model="filtros.servicio"
                >
                  <option 
                    v-for="servicio in serviciosFiltrados" 
                    :key="servicio.id" 
                    :value="servicio.id"
                  >
                    {{ servicio.nombre }}
                  </option>
                </select>
              </div>
              
              <!-- Botón de búsqueda -->
              <div class="flex items-end">
                <button 
                  type="submit" 
                  class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  :disabled="loading"
                >
                  <span v-if="loading" class="mr-2">
                    <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin" />
                  </span>
                  <font-awesome-icon v-else :icon="['fas', 'search']" class="mr-2" />
                  {{ loading ? 'Buscando...' : 'Buscar' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>

    <!-- Contenido principal -->
    <section class="py-12">
      <div class="container-custom">
        <!-- Estado de error -->
        <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-6 mb-8 rounded-r-xl">
          <div class="flex items-center">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="text-red-500 mr-3" />
            <div>
              <h3 class="font-semibold">Error en la búsqueda</h3>
              <p class="mt-1">{{ error }}</p>
            </div>
          </div>
          <button 
            @click="buscar"
            class="mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors text-sm font-medium"
          >
            Intentar nuevamente
          </button>
        </div>

        <!-- Estado de carga -->
        <div v-else-if="loading" class="py-20 text-center">
          <div class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600"></div>
          <p class="mt-4 text-gray-600 text-lg">Buscando profesionales...</p>
        </div>

        <!-- Resultados -->
        <template v-else>
          <!-- Header de resultados -->
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
            <div>
              <h2 class="text-3xl font-display font-bold text-gray-900 mb-2">
                {{ resultados.length ? `${paginacion.totalResultados} profesionales encontrados` : 'No se encontraron resultados' }}
              </h2>
              <p v-if="resultados.length" class="text-gray-600">
                Encuentra el profesional perfecto para tu proyecto
              </p>
            </div>
            
            <!-- Filtros de ordenamiento -->
            <div v-if="resultados.length" class="mt-4 md:mt-0">
              <div class="relative">
                <select 
                  v-model="filtros.ordenar"
                  class="pl-4 pr-10 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 appearance-none bg-white shadow-sm" 
                >
                  <option value="relevance">Relevancia</option>
                  <option value="rating">Mejor calificación</option>
                  <option value="newest">Más recientes</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-500">
                  <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </div>
              </div>
            </div>
          </div>

          <!-- Sin resultados -->
          <div v-if="!resultados.length && !loading" class="text-center py-16">
            <div class="text-gray-300 mb-6">
              <font-awesome-icon :icon="['fas', 'search']" class="text-8xl" />
            </div>
            <h3 class="text-2xl font-semibold text-gray-700 mb-3">No se encontraron resultados</h3>
            <p class="text-gray-500 mb-6 max-w-md mx-auto">
              Prueba con otros términos de búsqueda o filtros diferentes. También puedes expandir tu búsqueda a áreas cercanas.
            </p>
            <button 
              @click="limpiarFiltros"
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-colors"
            >
              Limpiar filtros
            </button>
          </div>

          <!-- Grid de resultados -->
          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="prestador in resultados" :key="prestador.id" class="group">
              <div class="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 h-full overflow-hidden">
                <!-- Header de la tarjeta -->
                <div class="p-6 pb-4">
                  <div class="flex items-start justify-between mb-4">
                    <div class="flex-1">
                      <h3 class="text-xl font-bold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
                        {{ prestador.nombre_comercial }}
                      </h3>
                      <div class="flex items-center text-gray-600 mb-3">
                        <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2 text-blue-500 text-sm" />
                        <span class="text-sm">{{ prestador.ubicacion || 'Sin ubicación especificada' }}</span>
                      </div>
                    </div>
                    
                    <!-- Plan badge -->
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {{ prestador.plan_nombre }}
                    </span>
                  </div>
                  
                  <!-- Servicios -->
                  <div class="mb-4">
                    <div v-if="prestador.servicios && prestador.servicios.length > 0" class="flex flex-wrap gap-2">
                      <span 
                        v-for="(servicio, index) in prestador.servicios.slice(0, 3)" 
                        :key="index"
                        class="inline-block px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700"
                      >
                        {{ servicio.nombre }}
                      </span>
                      <span 
                        v-if="prestador.servicios.length > 3" 
                        class="inline-block px-3 py-1 rounded-full text-xs font-medium bg-gray-200 text-gray-600"
                      >
                        +{{ prestador.servicios.length - 3 }} más
                      </span>
                    </div>
                    <div v-else class="text-sm text-gray-500 italic">
                      Sin servicios registrados
                    </div>
                  </div>
                </div>
                
                <!-- Footer de la tarjeta -->
                <div class="px-6 py-4 bg-gray-50 border-t border-gray-100">
                  <div class="flex justify-between items-center">
                    <!-- Calificación -->
                    <div class="flex items-center">
                      <div class="flex mr-2">
                        <template v-for="n in 5" :key="n">
                          <font-awesome-icon 
                            :icon="['fas', 'star']" 
                            :class="n <= Math.round(prestador.puntuacion || 0) ? 'text-yellow-400' : 'text-gray-300'" 
                            class="text-sm"
                          />
                        </template>
                      </div>
                      <span class="text-sm text-gray-600">
                        {{ prestador.puntuacion > 0 ? prestador.puntuacion.toFixed(1) : 'Sin calificaciones' }}
                      </span>
                    </div>
                    
                    <!-- Botón de acción -->
                    <router-link 
                      :to="`/prestador/${prestador.id}`" 
                      class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center"
                    >
                      Ver perfil
                      <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2 text-xs" />
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Paginación mejorada -->
        <nav v-if="resultados.length && paginacion.totalPaginas > 1" class="mt-16">
          <div class="flex justify-center">
            <div class="flex items-center space-x-2 bg-white rounded-xl shadow-sm border border-gray-200 p-2">
              <!-- Botón anterior -->
              <button 
                @click="irAPagina(paginacion.pagina - 1)"
                class="flex items-center justify-center w-10 h-10 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 transition-colors" 
                :class="paginacion.pagina <= 1 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:border-blue-500'"
                :disabled="paginacion.pagina <= 1"
                type="button"
              >
                <font-awesome-icon :icon="['fas', 'chevron-left']" />
              </button>
              
              <!-- Páginas -->
              <template v-for="n in paginacion.totalPaginas" :key="n">
                <button 
                  v-if="n >= Math.max(1, paginacion.pagina - 2) && n <= Math.min(paginacion.totalPaginas, paginacion.pagina + 2)"
                  @click="irAPagina(n)"
                  class="flex items-center justify-center w-10 h-10 rounded-lg font-medium transition-colors" 
                  :class="n === paginacion.pagina ? 'bg-blue-600 text-white' : 'bg-white hover:bg-gray-50 text-gray-700 border border-gray-300'"
                  type="button"
                >{{ n }}</button>
              </template>
              
              <!-- Botón siguiente -->
              <button 
                @click="irAPagina(paginacion.pagina + 1)"
                class="flex items-center justify-center w-10 h-10 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 transition-colors" 
                :class="paginacion.pagina >= paginacion.totalPaginas ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:border-blue-500'"
                :disabled="paginacion.pagina >= paginacion.totalPaginas"
                type="button"
              >
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
              </button>
            </div>
          </div>
        </nav>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useSearchStore } from '../stores/searchStore';

const route = useRoute();
const router = useRouter();
const searchStore = useSearchStore();
const { 
  resultados, 
  filtros, 
  paginacion, 
  loading, 
  error, 
  categorias, 
  serviciosFiltrados,
  buscar, 
  cambiarPagina,
  cargarCategorias,
  cargarServicios,
  limpiarFiltros
} = searchStore;

// Manejar la búsqueda inicial y cambios en la URL
onMounted(async () => {
  // Cargar datos iniciales
  await Promise.all([
    cargarCategorias(),
    cargarServicios()
  ]);
  
  // Sincronizar filtros con parámetros de URL
  const params = route.query;
  
  if (params.ubicacion) filtros.value.ubicacion = params.ubicacion;
  if (params.categoria) filtros.value.categoria = params.categoria;
  if (params.servicio) filtros.value.servicio = params.servicio;
  if (params.ordenar) filtros.value.ordenar = params.ordenar;
  if (params.pagina) paginacion.value.pagina = parseInt(params.pagina) || 1;
  
  // Realizar búsqueda inicial
  buscar();
});

// Observar cambios en los filtros para actualizar URL y realizar búsqueda
watch(
  [
    () => filtros.value,
    () => paginacion.value && paginacion.value.pagina
  ],
  () => {
    const nextQuery = {};

    // Añadir filtros con valor no vacío
    Object.entries(filtros.value || {}).forEach(([key, value]) => {
      if (value !== '' && value !== undefined && value !== null) {
        nextQuery[key] = value;
      }
    });

    // Añadir página solo si es > 1
    const currentPage = paginacion.value && paginacion.value.pagina;
    if (typeof currentPage === 'number' && currentPage > 1) {
      nextQuery.pagina = currentPage;
    }

    // Reemplazar para evitar loops en el historial
    router.replace({ query: nextQuery });
  },
  { deep: true }
);

// Manejar envío del formulario de búsqueda
function realizarBusqueda() {
  paginacion.value.pagina = 1; // Resetear página al hacer nueva búsqueda
  buscar();
}

// Manejar cambio de página
function irAPagina(pagina) {
  if (pagina >= 1 && pagina <= paginacion.value.totalPaginas) {
    cambiarPagina(pagina);
  }
}
</script>

<style scoped>
/* Estilos adicionales si es necesario */
.container-custom {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
}
</style>