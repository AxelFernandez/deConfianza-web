<template>
  <div>
    <section class="bg-primary-600 text-white py-10">
      <div class="container-custom">
        <h1 class="text-2xl md:text-3xl font-display font-bold mb-6">Buscar servicios</h1>
        <form @submit.prevent="realizarBusqueda" class="bg-white p-5 rounded-xl shadow-lg">
          <div class="grid md:grid-cols-4 gap-4">
            <div>
              <label for="location" class="block text-sm font-medium text-neutral-700 mb-1">Ubicación</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
                </div>
                <input 
                  type="text" 
                  class="w-full pl-10 pr-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                  id="location" 
                  v-model="filtros.ubicacion"
                  placeholder="Ciudad, provincia..."
                >
              </div>
            </div>
            <div>
              <label for="category" class="block text-sm font-medium text-neutral-700 mb-1">Categoría</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'th-large']" />
                </div>
                <select 
                  class="w-full pl-10 pr-8 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors appearance-none" 
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
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </div>
              </div>
            </div>
            <div>
              <label for="service" class="block text-sm font-medium text-neutral-700 mb-1">Servicio</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'tools']" />
                </div>
                <select 
                  class="w-full pl-10 pr-8 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors appearance-none" 
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
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </div>
              </div>
            </div>
            <div class="flex items-end">
              <button 
                type="submit" 
                class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center"
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
    </section>

    <section class="py-10">
      <div class="container-custom">
        <!-- Estado de error -->
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
          <p>{{ error }}</p>
          <button 
            @click="buscar"
            class="mt-3 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors text-sm"
          >
            Intentar nuevamente
          </button>
        </div>

        <!-- Estado de carga -->
        <div v-else-if="loading" class="py-20 text-center">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <p class="mt-3 text-neutral-600">Buscando servicios...</p>
        </div>

        <!-- Resultados -->
        <template v-else>
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
            <h2 class="text-2xl font-display font-bold text-neutral-900 mb-4 md:mb-0">
              {{ resultados.length ? `${paginacion.totalResultados} resultados encontrados` : 'No se encontraron resultados' }}
            </h2>
            <div v-if="resultados.length">
              <div class="relative">
                <select 
                  v-model="filtros.ordenar"
                  class="pl-3 pr-8 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors appearance-none text-sm" 
                >
                  <option value="relevance">Relevancia</option>
                  <option value="rating">Mejor calificación</option>
                  <option value="newest">Más recientes</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none text-neutral-500">
                  <font-awesome-icon :icon="['fas', 'chevron-down']" />
                </div>
              </div>
            </div>
          </div>

          <!-- Sin resultados -->
          <div v-if="!resultados.length && !loading" class="text-center py-10">
            <div class="text-neutral-400 mb-4">
              <font-awesome-icon :icon="['fas', 'search']" class="text-5xl" />
            </div>
            <h3 class="text-xl font-medium text-neutral-700 mb-2">No se encontraron resultados</h3>
            <p class="text-neutral-500 mb-4">Prueba con otros términos de búsqueda o filtros diferentes.</p>
          </div>

          <!-- Lista de resultados -->
          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="prestador in resultados" :key="prestador.id" class="group">
              <div class="bg-white rounded-xl border border-neutral-200 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 h-full p-5">
                <h3 class="text-lg font-semibold text-neutral-900 mb-2">{{ prestador.nombre }}</h3>
                <p class="flex items-center text-neutral-600 mb-2">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2 text-primary-500" />
                  {{ prestador.ubicacion || 'Sin ubicación especificada' }}
                </p>
                <p class="mb-4">
                  <span 
                    v-for="(servicio, index) in prestador.servicios?.slice(0, 2)" 
                    :key="index"
                    class="inline-block px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-700 mr-2 mb-1"
                  >
                    {{ servicio.nombre }}
                  </span>
                  <span 
                    v-if="prestador.servicios?.length > 2" 
                    class="inline-block px-2 py-1 rounded-full text-xs font-medium bg-neutral-100 text-neutral-700"
                  >
                    +{{ prestador.servicios.length - 2 }} más
                  </span>
                </p>
                <div class="flex justify-between items-center">
                  <div class="flex">
                    <template v-for="n in 5" :key="n">
                      <font-awesome-icon 
                        :icon="['fas', 'star']" 
                        :class="n <= Math.round(prestador.puntuacion || 0) ? 'text-yellow-500' : 'text-neutral-300'" 
                      />
                    </template>
                  </div>
                  <router-link 
                    :to="`/prestador/${prestador.id}`" 
                    class="px-3 py-1 border border-primary-600 text-primary-600 hover:bg-primary-50 rounded-lg text-sm font-medium transition-colors"
                  >
                    Ver detalles
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Paginación -->
        <nav v-if="resultados.length && paginacion.totalPaginas > 1" class="mt-10">
          <ul class="flex justify-center">
            <li>
              <button 
                @click="irAPagina(paginacion.pagina - 1)"
                class="flex items-center justify-center w-10 h-10 rounded-l-lg border border-neutral-300 bg-white" 
                :class="paginacion.pagina <= 1 ? 'text-neutral-400 cursor-not-allowed' : 'text-neutral-700 hover:bg-neutral-50'"
                :disabled="paginacion.pagina <= 1"
                type="button"
              >
                <font-awesome-icon :icon="['fas', 'chevron-left']" />
              </button>
            </li>
            
            <!-- Primera página -->
            <li v-if="paginacion.pagina > 3">
              <button 
                @click="irAPagina(1)"
                class="flex items-center justify-center w-10 h-10 border-t border-b border-neutral-300 bg-white hover:bg-neutral-50 text-neutral-700"
                type="button"
              >1</button>
            </li>
            
            <!-- Ellipsis al inicio -->
            <li v-if="paginacion.pagina > 4">
              <span class="flex items-center justify-center w-10 h-10 border-t border-b border-neutral-300 bg-white text-neutral-400">
                ...
              </span>
            </li>
            
            <!-- Páginas cercanas a la actual -->
            <template v-for="n in paginacion.totalPaginas" :key="n">
              <li v-if="n >= Math.max(1, paginacion.pagina - 2) && n <= Math.min(paginacion.totalPaginas, paginacion.pagina + 2)">
                <button 
                  @click="irAPagina(n)"
                  class="flex items-center justify-center w-10 h-10 border-t border-b border-neutral-300" 
                  :class="n === paginacion.pagina ? 'bg-primary-600 text-white' : 'bg-white hover:bg-neutral-50 text-neutral-700'"
                  type="button"
                >{{ n }}</button>
              </li>
            </template>
            
            <!-- Ellipsis al final -->
            <li v-if="paginacion.pagina < paginacion.totalPaginas - 3">
              <span class="flex items-center justify-center w-10 h-10 border-t border-b border-neutral-300 bg-white text-neutral-400">
                ...
              </span>
            </li>
            
            <!-- Última página -->
            <li v-if="paginacion.pagina < paginacion.totalPaginas - 2">
              <button 
                @click="irAPagina(paginacion.totalPaginas)"
                class="flex items-center justify-center w-10 h-10 border-t border-b border-neutral-300 bg-white hover:bg-neutral-50 text-neutral-700"
                type="button"
              >{{ paginacion.totalPaginas }}</button>
            </li>
            
            <li>
              <button 
                @click="irAPagina(paginacion.pagina + 1)"
                class="flex items-center justify-center w-10 h-10 rounded-r-lg border border-neutral-300 bg-white" 
                :class="paginacion.pagina >= paginacion.totalPaginas ? 'text-neutral-400 cursor-not-allowed' : 'text-neutral-700 hover:bg-neutral-50'"
                :disabled="paginacion.pagina >= paginacion.totalPaginas"
                type="button"
              >
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
              </button>
            </li>
          </ul>
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
  cambiarPagina 
} = searchStore;

// Manejar la búsqueda inicial y cambios en la URL
onMounted(() => {
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
/* Todos los estilos ahora están en las clases de Tailwind */
</style>
