import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { searchService } from '../services/api';

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
    { id: '', nombre: 'Todas las categorías' },
    { id: '1', nombre: 'Oficios' },
    { id: '2', nombre: 'Profesiones' }
  ]);
  
  const servicios = ref([
    { id: '', nombre: 'Todos los servicios', categoria_id: '' },
    { id: '1', nombre: 'Plomería', categoria_id: '1' },
    { id: '2', nombre: 'Electricidad', categoria_id: '1' },
    { id: '3', nombre: 'Carpintería', categoria_id: '1' },
    { id: '4', nombre: 'Jardinería', categoria_id: '1' },
    { id: '5', nombre: 'Abogacía', categoria_id: '2' },
    { id: '6', nombre: 'Contabilidad', categoria_id: '2' },
    { id: '7', nombre: 'Psicología', categoria_id: '2' }
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
        pagina: paginacion.value.pagina
      });
      
      resultados.value = response.data.resultados;
      paginacion.value = {
        pagina: response.data.pagina,
        totalPaginas: response.data.total_paginas,
        totalResultados: response.data.total_resultados
      };
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
    limpiarFiltros
  };
});
