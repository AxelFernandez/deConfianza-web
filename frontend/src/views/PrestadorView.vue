<template>
  <div>
    <!-- Estado de carga -->
    <div v-if="loading" class="py-20 text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      <p class="mt-3 text-neutral-600">Cargando información...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="py-20 text-center">
      <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 max-w-lg mx-auto">
        <p>{{ error }}</p>
        <button 
          @click="cargarDatos"
          class="mt-3 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors"
        >
          Intentar nuevamente
        </button>
      </div>
    </div>

    <!-- Contenido principal -->
    <template v-else-if="prestador">
      <section class="bg-primary-600 text-white py-8">
        <div class="container-custom">
          <div class="flex flex-col md:flex-row md:items-center">
            <div class="md:w-2/3">
              <h1 class="text-2xl md:text-3xl font-display font-bold mb-2">{{ prestador.nombre }}</h1>
              <div class="flex items-center mb-3">
                <div class="flex mr-2">
                  <template v-for="n in 5" :key="n">
                    <font-awesome-icon 
                      :icon="['fas', n <= Math.round(promedioPuntuacion) ? 'star' : 'star']" 
                      :class="n <= Math.round(promedioPuntuacion) ? 'text-yellow-400' : 'text-yellow-400/30'" 
                    />
                  </template>
                </div>
                <span>({{ cantidadResenas }} reseñas)</span>
              </div>
              <p class="flex items-center">
                <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2" />
                {{ prestador.ubicacion || 'Sin ubicación especificada' }}
              </p>
            </div>
            <div class="md:w-1/3 flex justify-start md:justify-end mt-4 md:mt-0 space-x-3">
              <button 
                v-if="prestador.telefono"
                @click="window.location.href = `tel:${prestador.telefono}`" 
                class="bg-white hover:bg-neutral-100 text-primary-600 font-medium py-2 px-4 rounded-lg transition-colors flex items-center"
              >
                <font-awesome-icon :icon="['fas', 'phone']" class="mr-2" />
                Contactar
              </button>
              <button class="border border-white hover:bg-white/10 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center">
                <font-awesome-icon :icon="['far', 'bookmark']" class="mr-2" />
                Guardar
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="py-10">
        <div class="container-custom">
          <div class="grid lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
              <!-- Galería de imágenes -->
              <div v-if="tieneImagenes" class="bg-white rounded-xl border border-neutral-200 shadow-sm mb-6 p-6">
                <h2 class="text-xl font-semibold text-neutral-900 mb-4">Galería</h2>
                <div class="grid grid-cols-3 gap-3">
                  <div 
                    v-for="(imagen, index) in prestador.imagenes" 
                    :key="index" 
                    class="aspect-square overflow-hidden rounded-lg"
                  >
                    <img 
                      :src="imagen.url" 
                      :alt="imagen.descripcion || `Imagen ${index + 1}`" 
                      class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                    >
                  </div>
                </div>
              </div>
              
              <!-- Descripción -->
              <div class="bg-white rounded-xl border border-neutral-200 shadow-sm mb-6 p-6">
                <h2 class="text-xl font-semibold text-neutral-900 mb-4">Acerca de</h2>
                <p v-if="prestador.descripcion" class="text-neutral-700">
                  {{ prestador.descripcion }}
                </p>
                <p v-else class="text-neutral-500 italic">
                  Este prestador aún no ha agregado una descripción.
                </p>
              </div>
              
              <!-- Servicios ofrecidos -->
              <div v-if="prestador.servicios && prestador.servicios.length" class="bg-white rounded-xl border border-neutral-200 shadow-sm mb-6 p-6">
                <h2 class="text-xl font-semibold text-neutral-900 mb-4">Servicios ofrecidos</h2>
                <div class="grid md:grid-cols-2 gap-4">
                  <ul v-for="(columna, colIndex) in serviciosAgrupados" :key="colIndex" class="space-y-3">
                    <li v-for="(servicio, index) in columna" :key="index" class="flex items-start">
                      <span class="mt-1 text-primary-500 mr-2">
                        <font-awesome-icon :icon="['fas', 'check']" />
                      </span>
                      <span class="text-neutral-700">{{ servicio.nombre }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              
              <!-- Reseñas -->
              <div class="bg-white rounded-xl border border-neutral-200 shadow-sm p-6">
                <div class="flex justify-between items-center mb-6">
                  <h2 class="text-xl font-semibold text-neutral-900">Reseñas ({{ cantidadResenas }})</h2>
                  <button 
                    @click="mostrarFormularioResena = !mostrarFormularioResena"
                    class="bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {{ mostrarFormularioResena ? 'Cancelar' : 'Dejar reseña' }}
                  </button>
                </div>
                
                <!-- Formulario de reseña -->
                <div v-if="mostrarFormularioResena" class="mb-6 p-4 bg-neutral-50 rounded-lg border border-neutral-200">
                  <h3 class="text-lg font-medium mb-3">Tu opinión</h3>
                  <form @submit.prevent="enviarResena">
                    <div class="mb-4">
                      <label class="block text-sm font-medium text-neutral-700 mb-1">Puntuación</label>
                      <div class="flex">
                        <button 
                          v-for="n in 5" 
                          :key="n"
                          type="button"
                          @click="nuevaResena.puntuacion = n"
                          class="text-xl mr-1"
                        >
                          <font-awesome-icon 
                            :icon="['fas', 'star']" 
                            :class="n <= nuevaResena.puntuacion ? 'text-yellow-500' : 'text-neutral-300'" 
                          />
                        </button>
                      </div>
                    </div>
                    <div class="mb-4">
                      <label for="comentario" class="block text-sm font-medium text-neutral-700 mb-1">Comentario</label>
                      <textarea 
                        id="comentario"
                        v-model="nuevaResena.comentario"
                        rows="3"
                        class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors"
                        required
                      ></textarea>
                    </div>
                    <div class="flex items-center mb-4">
                      <input 
                        id="anonimo"
                        type="checkbox"
                        v-model="nuevaResena.anonimo"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded"
                      >
                      <label for="anonimo" class="ml-2 text-sm text-neutral-700">Publicar como anónimo</label>
                    </div>
                    <div class="flex justify-end">
                      <button 
                        type="submit"
                        :disabled="loading"
                        class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <span v-if="loading" class="mr-2">
                          <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin" />
                        </span>
                        Enviar reseña
                      </button>
                    </div>
                  </form>
                </div>
                
                <!-- Reseñas individuales -->
                <div v-if="resenas.length" class="space-y-5">
                  <div 
                    v-for="(resena, index) in resenas.slice(0, 3)" 
                    :key="resena.id" 
                    class="pb-4" 
                    :class="{ 'border-b border-neutral-200': index < 2 }"
                  >
                    <div class="flex items-center justify-between mb-2">
                      <div class="flex items-center">
                        <span class="font-medium text-neutral-900 mr-3">
                          {{ resena.anonimo ? 'Usuario anónimo' : resena.usuario.nombre }}
                        </span>
                        <div class="flex">
                          <template v-for="n in 5" :key="n">
                            <font-awesome-icon 
                              :icon="['fas', 'star']" 
                              :class="n <= resena.puntuacion ? 'text-yellow-500' : 'text-neutral-300'" 
                            />
                          </template>
                        </div>
                      </div>
                      <span class="text-sm text-neutral-500">
                        {{ new Date(resena.fecha_creacion).toLocaleDateString() }}
                      </span>
                    </div>
                    <p class="text-neutral-700">
                      {{ resena.comentario }}
                    </p>
                  </div>
                </div>
                
                <div v-else class="text-center py-6 text-neutral-500">
                  <p>Aún no hay reseñas para este prestador.</p>
                  <p class="mt-2 text-sm">¡Sé el primero en dejar tu opinión!</p>
                </div>
                
                <a 
                  v-if="resenas.length > 3" 
                  href="#" 
                  class="block text-center text-primary-600 hover:text-primary-700 font-medium mt-4"
                >
                  Ver todas las reseñas
                </a>
              </div>
            </div>
            
            <div>
              <!-- Tarjeta de información de contacto -->
              <div class="bg-white rounded-xl border border-neutral-200 shadow-sm p-6 sticky top-6">
                <h3 class="text-lg font-semibold text-neutral-900 mb-4">Información de contacto</h3>
                <ul class="space-y-4">
                  <li v-if="prestador.telefono" class="flex items-center">
                    <span class="text-primary-500 mr-3 w-5 flex justify-center">
                      <font-awesome-icon :icon="['fas', 'phone']" />
                    </span>
                    <span class="text-neutral-700">{{ prestador.telefono }}</span>
                  </li>
                  <li v-if="prestador.email" class="flex items-center">
                    <span class="text-primary-500 mr-3 w-5 flex justify-center">
                      <font-awesome-icon :icon="['fas', 'envelope']" />
                    </span>
                    <span class="text-neutral-700">{{ prestador.email }}</span>
                  </li>
                  <li v-if="prestador.ubicacion" class="flex items-center">
                    <span class="text-primary-500 mr-3 w-5 flex justify-center">
                      <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
                    </span>
                    <span class="text-neutral-700">{{ prestador.ubicacion }}</span>
                  </li>
                  <li v-if="prestador.horario" class="flex items-center">
                    <span class="text-primary-500 mr-3 w-5 flex justify-center">
                      <font-awesome-icon :icon="['fas', 'clock']" />
                    </span>
                    <span class="text-neutral-700">{{ prestador.horario }}</span>
                  </li>
                </ul>
                
                <div v-if="prestador.redes_sociales && prestador.redes_sociales.length" class="flex space-x-4 mt-5">
                  <a 
                    v-for="(red, index) in prestador.redes_sociales" 
                    :key="index"
                    :href="red.url" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="text-primary-600 hover:text-primary-800 transition-colors"
                  >
                    <font-awesome-icon :icon="['fab', red.tipo.toLowerCase()]" size="lg" />
                  </a>
                </div>
                
                <div class="mt-6 space-y-3">
                  <button 
                    v-if="prestador.telefono"
                    @click="window.location.href = `tel:${prestador.telefono}`" 
                    class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <font-awesome-icon :icon="['fas', 'phone']" class="mr-2" />
                    Contactar ahora
                  </button>
                  <button 
                    @click="navigator.share({ title: prestador.nombre, url: window.location.href })"
                    class="w-full border border-primary-600 text-primary-600 hover:bg-primary-50 font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <font-awesome-icon :icon="['fas', 'share-alt']" class="mr-2" />
                    Compartir
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
    
    <!-- Prestador no encontrado -->
    <div v-else class="py-20 text-center">
      <h2 class="text-2xl font-bold text-neutral-900 mb-3">Prestador no encontrado</h2>
      <p class="text-neutral-600 mb-6">No pudimos encontrar la información del prestador solicitado.</p>
      <router-link to="/buscar" class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors inline-block">
        Volver a búsqueda
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import { usePrestadorStore } from '../stores/prestadorStore';

const route = useRoute();
const prestadorStore = usePrestadorStore();
const { 
  prestador, 
  resenas, 
  loading, 
  error, 
  promedioPuntuacion, 
  cantidadResenas, 
  tieneImagenes,
  serviciosAgrupados 
} = prestadorStore;

// Estado local para componentes UI
const mostrarFormularioResena = ref(false);
const nuevaResena = ref({
  puntuacion: 5,
  comentario: '',
  anonimo: false
});

// Cargar datos del prestador cuando cambie el ID en la ruta
watch(() => route.params.id, cargarDatos, { immediate: true });

async function cargarDatos() {
  if (route.params.id) {
    prestadorStore.resetState();
    await prestadorStore.fetchPrestador(route.params.id);
    await prestadorStore.fetchResenas(route.params.id);
  }
}

async function enviarResena() {
  try {
    await prestadorStore.enviarResena(route.params.id, nuevaResena.value);
    // Resetear formulario
    nuevaResena.value = {
      puntuacion: 5,
      comentario: '',
      anonimo: false
    };
    mostrarFormularioResena.value = false;
  } catch (error) {
    // El error ya se maneja en el store
  }
}

// Limpiar estado al desmontar el componente
onMounted(() => {
  return () => prestadorStore.resetState();
});
</script>

<style scoped>
/* Todos los estilos ahora están en las clases de Tailwind */
</style>
