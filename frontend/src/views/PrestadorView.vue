<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Estado de carga -->
    <div v-if="loading" class="py-20 text-center">
      <div class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600"></div>
      <p class="mt-4 text-gray-600 text-lg">Cargando información del prestador...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="py-20 text-center">
      <div class="bg-red-50 border-l-4 border-red-500 text-red-700 p-6 max-w-lg mx-auto rounded-r-xl">
        <div class="flex items-center">
          <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="text-red-500 mr-3" />
          <div>
            <h3 class="font-semibold">Error al cargar el prestador</h3>
            <p class="mt-1">{{ error }}</p>
          </div>
        </div>
        <button 
          @click="cargarDatos"
          class="mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors font-medium"
        >
          Intentar nuevamente
        </button>
      </div>
    </div>

    <!-- Contenido principal -->
    <template v-else-if="prestador">
      <!-- Hero Section -->
      <section class="relative bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white">
        <div class="absolute inset-0 bg-black/20"></div>
        <div class="container-custom relative z-10 py-16">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <!-- Información principal -->
            <div class="lg:w-2/3 mb-8 lg:mb-0">
              <div class="flex items-center mb-4">
                <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mr-6">
                  <font-awesome-icon :icon="['fas', 'user']" class="text-3xl text-white" />
                </div>
                <div>
                  <h1 class="text-3xl md:text-4xl font-display font-bold mb-2">
                    {{ prestador.nombre_comercial }}
                  </h1>
                  <div class="flex items-center mb-3">
                    <div class="flex mr-3">
                      <template v-for="n in 5" :key="n">
                        <font-awesome-icon 
                          :icon="['fas', 'star']" 
                          :class="n <= Math.round(promedioPuntuacion) ? 'text-yellow-400' : 'text-yellow-400/30'" 
                          class="text-lg"
                        />
                      </template>
                    </div>
                    <span class="text-blue-100">
                      {{ promedioPuntuacion }} ({{ cantidadResenas }} reseñas)
                    </span>
                  </div>
                  <div class="flex items-center text-blue-100">
                    <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2" />
                    <span>{{ prestador.ciudad }}, {{ prestador.provincia }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Plan badge -->
              <div class="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full">
                <span class="text-sm font-medium">{{ prestador.plan_info?.name || 'Plan Gratuito' }}</span>
              </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="lg:w-1/3 flex flex-col sm:flex-row lg:flex-col gap-3">
              <button 
                v-if="prestador.telefono"
                @click="window.location.href = `tel:${prestador.telefono}`" 
                class="bg-white hover:bg-gray-100 text-blue-600 font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <font-awesome-icon :icon="['fas', 'phone']" class="mr-2" />
                Contactar ahora
              </button>
              <button 
                @click="compartirPerfil"
                class="border-2 border-white hover:bg-white/10 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center backdrop-blur-sm"
              >
                <font-awesome-icon :icon="['fas', 'share-alt']" class="mr-2" />
                Compartir
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Contenido principal -->
      <section class="py-12">
        <div class="container-custom">
          <div class="grid lg:grid-cols-3 gap-8">
            <!-- Columna principal -->
            <div class="lg:col-span-2 space-y-8">
              <!-- Galería de medios -->
              <div v-if="tieneMedia" class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-2xl font-bold text-gray-900 flex items-center">
                    <font-awesome-icon :icon="['fas', 'images']" class="mr-3 text-blue-600" />
                    Galería
                  </h2>
                </div>
                <div class="p-6">
                  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div 
                      v-for="(media, index) in prestador.media" 
                      :key="index" 
                      class="aspect-square overflow-hidden rounded-xl bg-gray-100 group cursor-pointer"
                      @click="abrirModalMedia(media, index)"
                    >
                      <img 
                        v-if="media.tipo === 'imagen'"
                        :src="media.archivo" 
                        :alt="media.descripcion || `Imagen ${index + 1}`" 
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      >
                      <div 
                        v-else
                        class="w-full h-full flex items-center justify-center bg-gray-200"
                      >
                        <font-awesome-icon :icon="['fas', 'play']" class="text-3xl text-gray-500" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Descripción -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-2xl font-bold text-gray-900 flex items-center">
                    <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-3 text-blue-600" />
                    Acerca de
                  </h2>
                </div>
                <div class="p-6">
                  <p v-if="prestador.descripcion" class="text-gray-700 leading-relaxed text-lg">
                    {{ prestador.descripcion }}
                  </p>
                  <div v-else class="text-center py-8">
                    <font-awesome-icon :icon="['fas', 'edit']" class="text-4xl text-gray-300 mb-4" />
                    <p class="text-gray-500 text-lg">Este prestador aún no ha agregado una descripción.</p>
                  </div>
                </div>
              </div>
              
              <!-- Servicios ofrecidos -->
              <div v-if="prestador.servicios && prestador.servicios.length" class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-2xl font-bold text-gray-900 flex items-center">
                    <font-awesome-icon :icon="['fas', 'tools']" class="mr-3 text-blue-600" />
                    Servicios ofrecidos
                  </h2>
                </div>
                <div class="p-6">
                  <div class="grid md:grid-cols-2 gap-6">
                    <div v-for="(servicio, index) in prestador.servicios" :key="index" class="flex items-start">
                      <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-blue-600 text-sm" />
                      </div>
                      <div>
                        <h3 class="font-semibold text-gray-900 mb-1">{{ servicio.nombre }}</h3>
                        <p v-if="servicio.descripcion" class="text-gray-600 text-sm">{{ servicio.descripcion }}</p>
                        <div v-if="servicio.precio_base" class="mt-2">
                          <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                            Desde ${{ servicio.precio_base }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Reseñas -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                  <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-bold text-gray-900 flex items-center">
                      <font-awesome-icon :icon="['fas', 'star']" class="mr-3 text-blue-600" />
                      Reseñas ({{ cantidadResenas }})
                    </h2>
                    <button 
                      @click="mostrarFormularioResena = !mostrarFormularioResena"
                      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-xl transition-colors flex items-center"
                    >
                      <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                      {{ mostrarFormularioResena ? 'Cancelar' : 'Dejar reseña' }}
                    </button>
                  </div>
                </div>
                
                <div class="p-6">
                  <!-- Formulario de reseña -->
                  <div v-if="mostrarFormularioResena" class="mb-8 p-6 bg-gray-50 rounded-xl border border-gray-200">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">Tu opinión cuenta</h3>
                    <form @submit.prevent="enviarResena">
                      <div class="mb-6">
                        <label class="block text-sm font-semibold text-gray-700 mb-3">Puntuación</label>
                        <div class="flex space-x-2">
                          <button 
                            v-for="n in 5" 
                            :key="n"
                            type="button"
                            @click="nuevaResena.puntuacion = n"
                            class="text-3xl transition-colors"
                          >
                            <font-awesome-icon 
                              :icon="['fas', 'star']" 
                              :class="n <= nuevaResena.puntuacion ? 'text-yellow-500' : 'text-gray-300'" 
                            />
                          </button>
                        </div>
                      </div>
                      <div class="mb-6">
                        <label for="comentario" class="block text-sm font-semibold text-gray-700 mb-2">Comentario</label>
                        <textarea 
                          id="comentario"
                          v-model="nuevaResena.comentario"
                          rows="4"
                          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200"
                          placeholder="Comparte tu experiencia con este prestador..."
                          required
                        ></textarea>
                      </div>
                      <div class="flex items-center mb-6">
                        <input 
                          id="anonimo"
                          type="checkbox"
                          v-model="nuevaResena.anonimo"
                          class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        >
                        <label for="anonimo" class="ml-3 text-sm text-gray-700">Publicar como anónimo</label>
                      </div>
                      <div class="flex justify-end">
                        <button 
                          type="submit"
                          :disabled="loading"
                          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <span v-if="loading" class="mr-2">
                            <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin" />
                          </span>
                          Enviar reseña
                        </button>
                      </div>
                    </form>
                  </div>
                  
                  <!-- Lista de reseñas -->
                  <div v-if="resenas.length" class="space-y-6">
                    <div 
                      v-for="(resena, index) in resenas.slice(0, 5)" 
                      :key="resena.id" 
                      class="border-b border-gray-200 pb-6 last:border-b-0 last:pb-0"
                    >
                      <div class="flex items-start justify-between mb-3">
                        <div class="flex items-center">
                          <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                            <font-awesome-icon :icon="['fas', 'user']" class="text-blue-600" />
                          </div>
                          <div>
                            <h4 class="font-semibold text-gray-900">
                              {{ resena.nombre || 'Usuario anónimo' }}
                            </h4>
                            <div class="flex items-center mt-1">
                              <div class="flex mr-2">
                                <template v-for="n in 5" :key="n">
                                  <font-awesome-icon 
                                    :icon="['fas', 'star']" 
                                    :class="n <= resena.calificacion ? 'text-yellow-400' : 'text-gray-300'" 
                                    class="text-sm"
                                  />
                                </template>
                              </div>
                              <span class="text-sm text-gray-500">
                                {{ new Date(resena.fecha).toLocaleDateString('es-ES', { 
                                  year: 'numeric', 
                                  month: 'long', 
                                  day: 'numeric' 
                                }) }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <p class="text-gray-700 leading-relaxed">{{ resena.comentario }}</p>
                    </div>
                  </div>
                  
                  <div v-else class="text-center py-12">
                    <font-awesome-icon :icon="['fas', 'star']" class="text-5xl text-gray-300 mb-4" />
                    <h3 class="text-xl font-semibold text-gray-700 mb-2">Aún no hay reseñas</h3>
                    <p class="text-gray-500 mb-6">¡Sé el primero en compartir tu experiencia!</p>
                  </div>
                  
                  <div v-if="resenas.length > 5" class="text-center mt-6">
                    <button class="text-blue-600 hover:text-blue-700 font-semibold">
                      Ver todas las reseñas ({{ resenas.length }})
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Sidebar -->
            <div class="space-y-6">
              <!-- Tarjeta de contacto -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden sticky top-6">
                <div class="p-6 border-b border-gray-200">
                  <h3 class="text-xl font-bold text-gray-900 flex items-center">
                    <font-awesome-icon :icon="['fas', 'phone']" class="mr-3 text-blue-600" />
                    Contacto
                  </h3>
                </div>
                <div class="p-6 space-y-4">
                  <div v-if="prestador.telefono" class="flex items-center">
                    <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'phone']" class="text-blue-600" />
                    </div>
                    <div>
                      <p class="text-sm text-gray-500">Teléfono</p>
                      <p class="font-semibold text-gray-900">{{ prestador.telefono }}</p>
                    </div>
                  </div>
                  
                  <div v-if="prestador.sitio_web" class="flex items-center">
                    <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'globe']" class="text-green-600" />
                    </div>
                    <div>
                      <p class="text-sm text-gray-500">Sitio web</p>
                      <a :href="prestador.sitio_web" target="_blank" class="font-semibold text-blue-600 hover:text-blue-700">
                        Visitar sitio
                      </a>
                    </div>
                  </div>
                  
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="text-purple-600" />
                    </div>
                    <div>
                      <p class="text-sm text-gray-500">Ubicación</p>
                      <p class="font-semibold text-gray-900">{{ prestador.ciudad }}, {{ prestador.provincia }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="p-6 bg-gray-50 border-t border-gray-200 space-y-3">
                  <button 
                    v-if="prestador.telefono"
                    @click="window.location.href = `tel:${prestador.telefono}`" 
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-xl transition-colors flex items-center justify-center"
                  >
                    <font-awesome-icon :icon="['fas', 'phone']" class="mr-2" />
                    Llamar ahora
                  </button>
                  <button 
                    @click="compartirPerfil"
                    class="w-full border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold py-3 px-4 rounded-xl transition-colors flex items-center justify-center"
                  >
                    <font-awesome-icon :icon="['fas', 'share-alt']" class="mr-2" />
                    Compartir perfil
                  </button>
                </div>
              </div>
              
              <!-- Estadísticas -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                  <h3 class="text-xl font-bold text-gray-900 flex items-center">
                    <font-awesome-icon :icon="['fas', 'chart-bar']" class="mr-3 text-blue-600" />
                    Estadísticas
                  </h3>
                </div>
                <div class="p-6 space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600">Calificación promedio</span>
                    <div class="flex items-center">
                      <span class="font-semibold text-gray-900 mr-2">{{ promedioPuntuacion }}</span>
                      <div class="flex">
                        <template v-for="n in 5" :key="n">
                          <font-awesome-icon 
                            :icon="['fas', 'star']" 
                            :class="n <= Math.round(promedioPuntuacion) ? 'text-yellow-400' : 'text-gray-300'" 
                            class="text-sm"
                          />
                        </template>
                      </div>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600">Total de reseñas</span>
                    <span class="font-semibold text-gray-900">{{ cantidadResenas }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600">Servicios ofrecidos</span>
                    <span class="font-semibold text-gray-900">{{ prestador.servicios?.length || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600">Miembro desde</span>
                    <span class="font-semibold text-gray-900">
                      {{ new Date(prestador.fecha_creacion).toLocaleDateString('es-ES', { 
                        year: 'numeric', 
                        month: 'short' 
                      }) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
    
    <!-- Prestador no encontrado -->
    <div v-else class="py-20 text-center">
      <div class="max-w-md mx-auto">
        <font-awesome-icon :icon="['fas', 'user-slash']" class="text-6xl text-gray-300 mb-6" />
        <h2 class="text-3xl font-bold text-gray-900 mb-4">Prestador no encontrado</h2>
        <p class="text-gray-600 mb-8">No pudimos encontrar la información del prestador solicitado.</p>
        <router-link 
          to="/buscar" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors inline-flex items-center"
        >
          <font-awesome-icon :icon="['fas', 'search']" class="mr-2" />
          Volver a búsqueda
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import { usePrestadorStore } from '../stores/prestadorStore';
import { prestadorService } from '../services/api';

const route = useRoute();
const prestadorStore = usePrestadorStore();
const { 
  prestador, 
  resenas, 
  loading, 
  error, 
  promedioPuntuacion, 
  cantidadResenas, 
  tieneMedia,
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
    
    // Registrar visualización del perfil
    try {
      await prestadorService.registrarVisualizacion(route.params.id);
    } catch (error) {
      // No mostrar error al usuario, solo log en consola
      console.log('No se pudo registrar la visualización:', error);
    }
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

function compartirPerfil() {
  if (navigator.share) {
    navigator.share({
      title: prestador.value?.nombre_comercial,
      text: `Mira el perfil de ${prestador.value?.nombre_comercial} en deConfianza`,
      url: window.location.href
    });
  } else {
    // Fallback: copiar URL al portapapeles
    navigator.clipboard.writeText(window.location.href);
    // Aquí podrías mostrar un toast de confirmación
  }
}

function abrirModalMedia(media, index) {
  // Implementar modal para ver medios en tamaño completo
  console.log('Abrir modal para:', media, index);
}

// Limpiar estado al desmontar el componente
onMounted(() => {
  return () => prestadorStore.resetState();
});
</script>

<style scoped>
.container-custom {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
}
</style>