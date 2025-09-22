import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { prestadorService } from '../services/api';

export const usePrestadorStore = defineStore('prestador', () => {
  // Estado
  const prestador = ref(null);
  const resenas = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  // Getters
  const promedioPuntuacion = computed(() => {
    if (!resenas.value.length) return 0;
    
    const suma = resenas.value.reduce((acc, resena) => acc + resena.puntuacion, 0);
    return (suma / resenas.value.length).toFixed(1);
  });
  
  const cantidadResenas = computed(() => resenas.value.length);
  
  const tieneMedia = computed(() => 
    prestador.value && prestador.value.media && prestador.value.media.length > 0
  );
  
  const serviciosAgrupados = computed(() => {
    if (!prestador.value || !prestador.value.servicios) return [];
    
    // Divide los servicios en dos columnas para la UI
    const servicios = [...prestador.value.servicios];
    const mitad = Math.ceil(servicios.length / 2);
    
    return [
      servicios.slice(0, mitad),
      servicios.slice(mitad)
    ];
  });
  
  // Acciones
  async function fetchPrestador(id) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await prestadorService.getPrestador(id);
      prestador.value = response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar los datos del prestador';
      console.error('Error al cargar prestador:', err);
    } finally {
      loading.value = false;
    }
  }
  
  async function fetchResenas(id) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await prestadorService.getResenasPrestador(id);
      resenas.value = response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar las reseñas';
      console.error('Error al cargar reseñas:', err);
    } finally {
      loading.value = false;
    }
  }
  
  async function enviarResena(prestadorId, resenaData) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await prestadorService.crearResena(prestadorId, resenaData);
      // Actualizar la lista de reseñas con la nueva
      resenas.value.unshift(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al enviar la reseña';
      console.error('Error al enviar reseña:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }
  
  // Reset del estado
  function resetState() {
    prestador.value = null;
    resenas.value = [];
    error.value = null;
  }
  
  return {
    // Estado
    prestador,
    resenas,
    loading,
    error,
    
    // Getters
    promedioPuntuacion,
    cantidadResenas,
    tieneMedia,
    serviciosAgrupados,
    
    // Acciones
    fetchPrestador,
    fetchResenas,
    enviarResena,
    resetState
  };
});
