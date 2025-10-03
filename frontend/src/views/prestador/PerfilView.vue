<template>
  <PrestadorLayout 
    title="Mi Perfil" 
    subtitle="Gestiona tu información personal y profesional"
    breadcrumb="Perfil"
    :plan-name="dashboardData?.plan?.name"
    :dashboard-data="dashboardData"
    @logout="authStore.logout"
  >
    <div class="space-y-6">
      <!-- Loading -->
      <div v-if="loading" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <font-awesome-icon :icon="['fas', 'spinner']" class="text-blue-600 text-4xl animate-spin mb-4" />
        <p class="text-gray-600">Cargando perfil...</p>
      </div>

      <!-- Formulario -->
      <form v-else @submit.prevent="saveProfile" class="space-y-6">
        <!-- Info Personal -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold text-gray-900">Información Personal</h2>
                <p class="text-sm text-gray-600 mt-1">Datos básicos de tu perfil</p>
              </div>
              <button 
                v-if="!isEditing"
                type="button"
                @click="startEdit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                <font-awesome-icon :icon="['fas', 'edit']" class="mr-2" />
                Editar
              </button>
              <div v-else class="flex space-x-2">
                <button 
                  type="button"
                  @click="cancelEdit"
                  class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  type="submit"
                  :disabled="saving"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:bg-gray-400"
                >
                  <font-awesome-icon v-if="saving" :icon="['fas', 'spinner']" class="animate-spin mr-2" />
                  {{ saving ? 'Guardando...' : 'Guardar' }}
                </button>
              </div>
            </div>
          </div>

          <div class="p-6 space-y-6">
            <!-- Datos de cuenta -->
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <font-awesome-icon :icon="['fas', 'user']" class="text-blue-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Usuario</p>
                    <p class="font-semibold text-gray-900">{{ authStore.user?.username }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                    <font-awesome-icon :icon="['fas', 'envelope']" class="text-green-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Email</p>
                    <p class="font-semibold text-gray-900">{{ authStore.user?.email }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Campos editables -->
            <div class="grid md:grid-cols-2 gap-6">
              <!-- Teléfono -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Teléfono
                  <span v-if="!isFieldEnabled('telefono')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <input
                  v-model="formData.telefono"
                  type="tel"
                  :disabled="!isEditing || !isFieldEnabled('telefono')"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Ej: +54 261 1234567"
                />
              </div>

              <!-- Ciudad -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Ciudad
                  <span v-if="!isFieldEnabled('ciudad')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <input
                  v-model="formData.ciudad"
                  type="text"
                  :disabled="!isEditing || !isFieldEnabled('ciudad')"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Ej: Mendoza"
                />
              </div>

              <!-- Provincia -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Provincia
                  <span v-if="!isFieldEnabled('provincia')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <input
                  v-model="formData.provincia"
                  type="text"
                  :disabled="!isEditing || !isFieldEnabled('provincia')"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Ej: Mendoza"
                />
              </div>

              <!-- Dirección -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Dirección
                  <span v-if="!isFieldEnabled('direccion')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <input
                  v-model="formData.direccion"
                  type="text"
                  :disabled="!isEditing || !isFieldEnabled('direccion')"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Ej: Calle 123"
                />
              </div>

              <!-- Sitio web -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Sitio Web
                  <span v-if="!isFieldEnabled('sitio_web')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <input
                  v-model="formData.sitio_web"
                  type="url"
                  :disabled="!isEditing || !isFieldEnabled('sitio_web')"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="https://tusitio.com"
                />
              </div>

              <!-- Descripción -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Descripción
                  <span v-if="!isFieldEnabled('descripcion')" class="text-orange-600 ml-1">🔒</span>
                </label>
                <textarea
                  v-model="formData.descripcion"
                  :disabled="!isEditing || !isFieldEnabled('descripcion')"
                  rows="4"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Cuéntanos sobre tu negocio..."
                ></textarea>
              </div>
            </div>

            <!-- Categoría y Rubro -->
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Categoría</label>
                <select
                  v-model="formData.categoria"
                  :disabled="!isEditing"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                >
                  <option value="">Selecciona una categoría</option>
                  <option v-for="cat in categorias" v-if="cat && cat.id" :key="cat.id" :value="cat.id">
                    {{ cat.nombre }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Rubro</label>
                <select
                  v-model="formData.rubro"
                  :disabled="!isEditing || !formData.categoria"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                >
                  <option value="">Selecciona un rubro</option>
                  <option v-for="rub in rubros" v-if="rub && rub.id" :key="rub.id" :value="rub.id">
                    {{ rub.nombre }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Campos bloqueados -->
        <div v-if="blockedFields.length" class="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-xl p-6 border-2 border-dashed border-orange-300">
          <div class="flex items-start">
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'lock']" class="text-orange-600 text-xl" />
            </div>
            <div class="flex-1">
              <h3 class="font-bold text-gray-900 mb-2">Campos Bloqueados por tu Plan</h3>
              <p class="text-sm text-gray-700 mb-3">
                Los siguientes campos no están disponibles en tu plan actual:
              </p>
              <div class="flex flex-wrap gap-2 mb-4">
                <span v-for="field in blockedFields" :key="field" class="px-3 py-1 bg-white rounded-full text-sm font-medium text-gray-700 border border-orange-200">
                  🔒 {{ field }}
                </span>
              </div>
              <router-link 
                to="/planes"
                class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
                Mejorar Plan para Desbloquear
              </router-link>
            </div>
          </div>
        </div>
      </form>
    </div>
  </PrestadorLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { authService, catalogService, misServiciosService } from '../../services/api';
import PrestadorLayout from '../../components/PrestadorLayout.vue';

const authStore = useAuthStore();

const loading = ref(false);
const saving = ref(false);
const isEditing = ref(false);
const dashboardData = ref(null);
const categorias = ref([]);
const rubros = ref([]);

const formData = ref({
  telefono: '',
  direccion: '',
  ciudad: '',
  provincia: '',
  sitio_web: '',
  descripcion: '',
  categoria: null,
  rubro: null
});

const originalData = ref({});

const isFieldEnabled = (fieldName) => {
  const fieldsEnabled = dashboardData.value?.plan?.fields_enabled || [];
  return fieldsEnabled.includes(fieldName);
};

const blockedFields = computed(() => {
  const allFields = {
    telefono: 'Teléfono',
    direccion: 'Dirección',
    ciudad: 'Ciudad',
    provincia: 'Provincia',
    sitio_web: 'Sitio Web',
    descripcion: 'Descripción'
  };
  
  return Object.entries(allFields)
    .filter(([key]) => !isFieldEnabled(key))
    .map(([, value]) => value);
});

async function loadDashboard() {
  try {
    const response = await misServiciosService.getDashboard();
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

async function loadProfile() {
  loading.value = true;
  try {
    const response = await authService.getCurrentUser();
    const perfil = response.data.perfil || {};
    
    formData.value = {
      telefono: perfil.telefono || '',
      direccion: perfil.direccion || '',
      ciudad: perfil.ciudad || '',
      provincia: perfil.provincia || '',
      sitio_web: perfil.sitio_web || '',
      descripcion: perfil.descripcion || '',
      categoria: perfil.categoria || null,
      rubro: perfil.rubro || null
    };
    
    originalData.value = { ...formData.value };
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loading.value = false;
  }
}

async function loadCategorias() {
  try {
    const response = await catalogService.getCategorias();
    categorias.value = (response.data || []).filter(cat => cat && cat.id);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function loadRubros() {
  if (!formData.value.categoria) {
    rubros.value = [];
    return;
  }
  
  try {
    const response = await catalogService.getRubros(formData.value.categoria);
    rubros.value = (response.data || []).filter(rubro => rubro && rubro.id);
  } catch (error) {
    console.error('Error:', error);
  }
}

watch(() => formData.value.categoria, () => {
  formData.value.rubro = null;
  loadRubros();
});

function startEdit() {
  isEditing.value = true;
}

function cancelEdit() {
  formData.value = { ...originalData.value };
  isEditing.value = false;
}

async function saveProfile() {
  saving.value = true;
  try {
    await authService.updateProfile({
      perfil: formData.value
    });
    
    originalData.value = { ...formData.value };
    isEditing.value = false;
    await authStore.fetchUserProfile();
    
    alert('Perfil actualizado correctamente');
  } catch (error) {
    console.error('Error:', error);
    alert('Error al guardar el perfil');
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  loadDashboard();
  loadProfile();
  loadCategorias();
});
</script>