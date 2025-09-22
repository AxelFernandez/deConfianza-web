<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex justify-between items-center p-6 border-b border-neutral-200">
        <h2 class="text-xl font-semibold text-neutral-900">
          {{ isEditing ? 'Editar servicio' : 'Agregar nuevo servicio' }}
        </h2>
        <button 
          @click="closeModal"
          class="text-neutral-400 hover:text-neutral-600 transition-colors"
        >
          <font-awesome-icon :icon="['fas', 'times']" class="text-xl" />
        </button>
      </div>
      
      <!-- Form -->
      <form @submit.prevent="submitForm" class="p-6">
        <div class="space-y-6">
          <!-- Nombre del servicio -->
          <div>
            <label for="nombre" class="block text-sm font-medium text-neutral-700 mb-2">
              Nombre del servicio *
            </label>
            <input
              id="nombre"
              v-model="form.nombre"
              type="text"
              required
              class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Ej: Reparación de computadoras"
            />
          </div>
          
          <!-- Descripción -->
          <div>
            <label for="descripcion" class="block text-sm font-medium text-neutral-700 mb-2">
              Descripción *
            </label>
            <textarea
              id="descripcion"
              v-model="form.descripcion"
              required
              rows="4"
              class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Describe detalladamente tu servicio..."
            ></textarea>
          </div>
          
          <!-- Precio base -->
          <div>
            <label for="precio_base" class="block text-sm font-medium text-neutral-700 mb-2">
              Precio base (opcional)
            </label>
            <div class="relative">
              <span class="absolute left-3 top-2 text-neutral-500">$</span>
              <input
                id="precio_base"
                v-model="form.precio_base"
                type="number"
                step="0.01"
                min="0"
                class="w-full pl-8 pr-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="0.00"
              />
            </div>
            <p class="text-xs text-neutral-500 mt-1">Puedes dejar este campo vacío si prefieres cotizar por consulta</p>
          </div>
          
          <!-- Categoría -->
          <div>
            <label for="categoria" class="block text-sm font-medium text-neutral-700 mb-2">
              Categoría *
            </label>
            <select
              id="categoria"
              v-model="form.categoria"
              required
              @change="onCategoriaChange"
              class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Selecciona una categoría</option>
              <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
                {{ categoria.nombre }}
              </option>
            </select>
          </div>
          
          <!-- Rubro -->
          <div>
            <label for="rubro" class="block text-sm font-medium text-neutral-700 mb-2">
              Rubro *
            </label>
            <select
              id="rubro"
              v-model="form.rubro"
              required
              :disabled="!form.categoria"
              class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-neutral-100 disabled:cursor-not-allowed"
            >
              <option value="">Selecciona un rubro</option>
              <option v-for="rubro in rubros" :key="rubro.id" :value="rubro.id">
                {{ rubro.nombre }}
              </option>
            </select>
          </div>
          
          <!-- Estado -->
          <div>
            <label class="flex items-center">
              <input
                v-model="form.activo"
                type="checkbox"
                class="rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-neutral-700">Servicio activo</span>
            </label>
            <p class="text-xs text-neutral-500 mt-1">Los servicios inactivos no aparecerán en las búsquedas</p>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="flex justify-end space-x-3 mt-8 pt-6 border-t border-neutral-200">
          <button
            type="button"
            @click="closeModal"
            class="px-4 py-2 text-neutral-700 bg-neutral-100 hover:bg-neutral-200 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <font-awesome-icon v-if="loading" :icon="['fas', 'spinner']" class="animate-spin mr-2" />
            {{ isEditing ? 'Actualizar' : 'Crear' }} servicio
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { catalogService, misServiciosService } from '../services/api';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  servicio: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'saved']);

// Estado del formulario
const form = ref({
  nombre: '',
  descripcion: '',
  precio_base: '',
  categoria: '',
  rubro: '',
  activo: true
});

// Estado de la aplicación
const loading = ref(false);
const categorias = ref([]);
const rubros = ref([]);

// Computed
const isEditing = computed(() => !!props.servicio);

// Cargar categorías
async function loadCategorias() {
  try {
    const response = await catalogService.getCategorias();
    categorias.value = response.data;
  } catch (error) {
    console.error('Error cargando categorías:', error);
  }
}

// Cargar rubros por categoría
async function loadRubros(categoriaId) {
  if (!categoriaId) {
    rubros.value = [];
    return;
  }
  
  try {
    const response = await catalogService.getRubros({ categoria: categoriaId });
    rubros.value = response.data;
  } catch (error) {
    console.error('Error cargando rubros:', error);
  }
}

// Event handlers
function onCategoriaChange() {
  form.value.rubro = '';
  loadRubros(form.value.categoria);
}

function closeModal() {
  emit('close');
}

async function submitForm() {
  loading.value = true;
  
  try {
    const formData = {
      ...form.value,
      precio_base: form.value.precio_base ? parseFloat(form.value.precio_base) : null
    };
    
    if (isEditing.value) {
      await misServiciosService.updateServicio(props.servicio.id, formData);
    } else {
      await misServiciosService.createServicio(formData);
    }
    
    emit('saved');
    closeModal();
  } catch (error) {
    console.error('Error guardando servicio:', error);
    // TODO: Mostrar mensaje de error al usuario
    alert('Error al guardar el servicio. Por favor, intenta nuevamente.');
  } finally {
    loading.value = false;
  }
}

// Watchers
watch(() => props.show, (newValue) => {
  if (newValue) {
    // Resetear formulario
    form.value = {
      nombre: '',
      descripcion: '',
      precio_base: '',
      categoria: '',
      rubro: '',
      activo: true
    };
    
    // Si estamos editando, cargar datos del servicio
    if (props.servicio) {
      form.value = {
        nombre: props.servicio.nombre || '',
        descripcion: props.servicio.descripcion || '',
        precio_base: props.servicio.precio_base || '',
        categoria: props.servicio.categoria || '',
        rubro: props.servicio.rubro || '',
        activo: props.servicio.activo !== false
      };
      
      // Cargar rubros si ya hay una categoría seleccionada
      if (props.servicio.categoria) {
        loadRubros(props.servicio.categoria);
      }
    }
  }
});

onMounted(() => {
  loadCategorias();
});
</script>
