import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { searchService, catalogService } from '../services/api';

export const useSearchStore = defineStore('search', () => {
  // Estado
  const resultados = ref([]);
  const filtros = ref({
    ubicacion: '',
    categoria: '',
    servicio: '',
    ordenar: 'relevance'
  });
  const paginacion = ref({
    pagina: 1,
    totalPaginas: 1,
    totalResultados: 0
  });
  const loading = ref(false);
  const error = ref(null);
  
  // Getters
  const hayResultados = computed(() => resultados.value.length > 0);
  const categorias = ref([
    { id: '', nombre: 'Todas las categorías' }
  ]);
  
  const servicios = ref([
    { id: '', nombre: 'Todos los servicios', categoria_id: '' }
  ]);
  
  const serviciosFiltrados = computed(() => {
    if (!filtros.value.categoria) {
      return servicios.value;
    }
    return servicios.value.filter(s => 
      s.categoria_id === '' || s.categoria_id === filtros.value.categoria
    );
  });
  
  // Acciones
  async function cargarCategorias() {
    try {
      const response = await catalogService.getCategorias();
      categorias.value = [
        { id: '', nombre: 'Todas las categorías' },
        ...response.data
      ];
    } catch (err) {
      console.error('Error cargando categorías:', err);
    }
  }
  
  async function cargarServicios() {
    try {
      const response = await catalogService.getServicios();
      servicios.value = [
        { id: '', nombre: 'Todos los servicios', categoria_id: '' },
        ...response.data
      ];
    } catch (err) {
      console.error('Error cargando servicios:', err);
    }
  }
  
  async function buscar(params = {}) {
    loading.value = true;
    error.value = null;
    
    // Actualizar filtros con los parámetros proporcionados
    if (params.ubicacion !== undefined) filtros.value.ubicacion = params.ubicacion;
    if (params.categoria !== undefined) filtros.value.categoria = params.categoria;
    if (params.servicio !== undefined) filtros.value.servicio = params.servicio;
    if (params.ordenar !== undefined) filtros.value.ordenar = params.ordenar;
    if (params.pagina !== undefined) paginacion.value.pagina = params.pagina;
    
    try {
      const response = await searchService.buscar({
        ...filtros.value,
        page: paginacion.value.pagina
      });
      
      // El PrestadorViewSet devuelve los datos directamente en response.data
      resultados.value = response.data.results || response.data;
      
      // Manejar paginación si está disponible
      if (response.data.count !== undefined) {
        paginacion.value = {
          pagina: paginacion.value.pagina,
          totalPaginas: Math.ceil(response.data.count / 20), // 20 por página según configuración del backend
          totalResultados: response.data.count
        };
      } else {
        // Si no hay paginación, asumir que todos los resultados están en la primera página
        paginacion.value = {
          pagina: 1,
          totalPaginas: 1,
          totalResultados: resultados.value.length
        };
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al realizar la búsqueda';
      console.error('Error al buscar:', err);
    } finally {
      loading.value = false;
    }
  }
  
  function cambiarPagina(pagina) {
    if (pagina >= 1 && pagina <= paginacion.value.totalPaginas) {
      buscar({ pagina });
    }
  }
  
  function limpiarFiltros() {
    filtros.value = {
      ubicacion: '',
      categoria: '',
      servicio: '',
      ordenar: 'relevance'
    };
    paginacion.value.pagina = 1;
    buscar(); // Realizar búsqueda con filtros limpios
  }
  
  return {
    // Estado
    resultados,
    filtros,
    paginacion,
    loading,
    error,
    categorias,
    servicios,
    
    // Getters
    hayResultados,
    serviciosFiltrados,
    
    // Acciones
    buscar,
    cambiarPagina,
    limpiarFiltros,
    cargarCategorias,
    cargarServicios
  };
});
