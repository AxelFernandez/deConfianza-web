<template>
  <div class="min-h-screen bg-neutral-50">
    <!-- Header con breadcrumb -->
    <header class="bg-white shadow-sm border-b border-neutral-200">
      <div class="container-custom py-6">
        <div class="flex items-center space-x-2 text-sm text-neutral-600 mb-2">
          <router-link to="/prestador/dashboard" class="hover:text-primary-600">Dashboard</router-link>
          <span>/</span>
          <span class="text-neutral-900">Mi perfil</span>
        </div>
        <h1 class="text-2xl font-bold text-neutral-900">Mi perfil</h1>
        <p class="text-neutral-600 mt-1">Gestiona tu información personal y configuración de perfil</p>
      </div>
    </header>
    
    <!-- Contenido principal -->
    <div class="container-custom py-8">
      <div class="grid md:grid-cols-4 gap-6">
        <!-- Menú lateral -->
        <div class="md:col-span-1">
          <DashboardNavigation />
        </div>
        
        <!-- Contenido -->
        <div class="md:col-span-3">
          <!-- Loading state -->
          <div v-if="loading" class="bg-white rounded-lg shadow-sm border border-neutral-100 p-8">
            <div class="flex items-center justify-center">
              <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin mr-3" />
              <span class="text-neutral-600">Cargando perfil...</span>
            </div>
          </div>

          <!-- Información del plan actual -->
          <div v-else-if="userProfile?.plan_info" class="bg-white rounded-lg shadow-sm border border-neutral-100 p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-neutral-900">Tu plan actual</h2>
              <router-link 
                to="/prestador/dashboard" 
                class="text-sm text-primary-600 hover:text-primary-800 font-medium"
              >
                Ver dashboard
              </router-link>
            </div>
            
            <div class="flex items-center bg-primary-50 border border-primary-200 rounded-lg p-4">
              <div class="mr-4">
                <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
                  <font-awesome-icon :icon="['fas', 'crown']" />
                </div>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-neutral-900">{{ userProfile.plan_info.name }}</h3>
                <p class="text-sm text-neutral-600 mb-2">
                  {{ userProfile.plan_info.fields_enabled?.length || 0 }} campos habilitados, 
                  {{ userProfile.plan_info.max_images }} imágenes, 
                  {{ userProfile.plan_info.max_videos }} videos
                </p>
                
                <!-- Permisos del plan -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                  <div class="flex items-center">
                    <font-awesome-icon 
                      :icon="['fas', userProfile.plan_info.puede_crear_servicios ? 'check' : 'times']" 
                      :class="userProfile.plan_info.puede_crear_servicios ? 'text-green-500' : 'text-red-500'"
                      class="mr-1"
                    />
                    Servicios
                  </div>
                  <div class="flex items-center">
                    <font-awesome-icon 
                      :icon="['fas', userProfile.plan_info.puede_recibir_resenas ? 'check' : 'times']" 
                      :class="userProfile.plan_info.puede_recibir_resenas ? 'text-green-500' : 'text-red-500'"
                      class="mr-1"
                    />
                    Reseñas
                  </div>
                  <div class="flex items-center">
                    <font-awesome-icon 
                      :icon="['fas', userProfile.plan_info.puede_subir_media ? 'check' : 'times']" 
                      :class="userProfile.plan_info.puede_subir_media ? 'text-green-500' : 'text-red-500'"
                      class="mr-1"
                    />
                    Media
                  </div>
                  <div class="flex items-center">
                    <font-awesome-icon 
                      :icon="['fas', userProfile.plan_info.puede_ver_estadisticas ? 'check' : 'times']" 
                      :class="userProfile.plan_info.puede_ver_estadisticas ? 'text-green-500' : 'text-red-500'"
                      class="mr-1"
                    />
                    Estadísticas
                  </div>
                </div>
              </div>
              <div class="text-right">
                <p class="font-semibold text-neutral-900">{{ userProfile.plan_info.price_text }}</p>
                <p class="text-xs text-neutral-500" v-if="userProfile.plan_info.precio_mensual > 0">Mensual</p>
              </div>
            </div>
          </div>

          <!-- Formulario de edición de perfil -->
          <div v-if="!loading" class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
            <!-- Header del formulario -->
            <div class="bg-gradient-to-r from-primary-50 to-blue-50 border-b border-primary-100 p-6">
              <div class="flex justify-between items-center">
                <div>
                  <h2 class="text-xl font-semibold text-neutral-900 mb-1">Información personal</h2>
                  <p class="text-sm text-neutral-600">Gestiona tu información de contacto y ubicación</p>
                </div>
                <div class="flex space-x-2">
                  <button 
                    v-if="isEditing"
                    @click="cancelEdit"
                    class="text-sm text-neutral-600 hover:text-neutral-800 px-4 py-2 border border-neutral-300 rounded-lg transition-colors hover:bg-neutral-50"
                  >
                    Cancelar
                  </button>
                  <button 
                    v-if="!isEditing"
                    @click="startEdit"
                    class="text-sm text-primary-600 hover:text-primary-800 font-medium px-4 py-2 border border-primary-300 rounded-lg transition-colors hover:bg-primary-50"
                  >
                    <font-awesome-icon :icon="['fas', 'edit']" class="mr-2" />
                    Editar perfil
                  </button>
                  <button 
                    v-else
                    @click="saveProfile"
                    :disabled="saving"
                    class="text-sm bg-primary-600 hover:bg-primary-700 text-white font-medium px-5 py-2 rounded-lg transition-colors disabled:bg-neutral-400"
                  >
                    <font-awesome-icon v-if="saving" :icon="['fas', 'spinner']" class="animate-spin mr-2" />
                    {{ saving ? 'Guardando...' : 'Guardar cambios' }}
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Contenido del formulario -->
            <div class="p-6">

            <form @submit.prevent="saveProfile" class="space-y-8">
              
              <!-- Información de cuenta (siempre visible) -->
              <div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
                  <font-awesome-icon :icon="['fas', 'user-circle']" class="mr-3 text-primary-600" />
                  Información de cuenta
                </h3>
                <div class="grid md:grid-cols-2 gap-4">
                  <!-- Nombre -->
                  <div class="bg-neutral-50 rounded-lg p-4 border border-neutral-200">
                    <div class="flex items-center">
                      <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mr-4">
                        <font-awesome-icon :icon="['fas', 'user']" class="text-primary-600" />
                      </div>
                      <div class="flex-1">
                        <h4 class="font-medium text-neutral-900">Nombre de usuario</h4>
                        <p class="text-sm text-neutral-600 mt-1">
                          {{ authStore.fullName || authStore.user?.email || 'Sin nombre' }}
                        </p>
                        <p class="text-xs text-neutral-500 mt-1">Nombre que verán tus clientes</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Email -->
                  <div class="bg-neutral-50 rounded-lg p-4 border border-neutral-200">
                    <div class="flex items-center">
                      <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                        <font-awesome-icon :icon="['fas', 'envelope']" class="text-blue-600" />
                      </div>
                      <div class="flex-1">
                        <h4 class="font-medium text-neutral-900">Email</h4>
                        <p class="text-sm text-neutral-600 mt-1">{{ authStore.user?.email || 'Sin email' }}</p>
                        <p class="text-xs text-neutral-500 mt-1">Email de la cuenta</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Información de contacto -->
              <div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
                  <font-awesome-icon :icon="['fas', 'phone']" class="mr-3 text-primary-600" />
                  Información de contacto
                </h3>
                
                <!-- Teléfono -->
                <PermissionWrapper 
                  :has-permission="isFieldEnabled('telefono')"
                  title="Teléfono no disponible"
                  message="La visualización de teléfono no está incluida en tu plan actual"
                  icon="phone"
                  @upgrade="handleUpgrade"
                >
                  <div class="bg-white rounded-lg border border-neutral-200 p-4 mb-4">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                          <font-awesome-icon :icon="['fas', 'phone']" class="text-green-600" />
                        </div>
                        <div>
                          <h4 class="font-medium text-neutral-900">Teléfono de contacto</h4>
                          <p v-if="!isEditing" class="text-sm text-neutral-600 mt-1">
                            {{ formData.telefono || 'No especificado' }}
                          </p>
                          <input 
                            v-else
                            v-model="formData.telefono"
                            type="tel"
                            class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent mt-2"
                            placeholder="+54 11 1234-5678"
                          />
                        </div>
                      </div>
                      <div class="text-right">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          <font-awesome-icon :icon="['fas', 'eye']" class="mr-1" />
                          Visible para clientes
                        </span>
                      </div>
                    </div>
                  </div>
                </PermissionWrapper>
              </div>

              <!-- Información de ubicación -->
              <div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-3 text-primary-600" />
                  Ubicación del negocio
                </h3>
                <div class="grid md:grid-cols-2 gap-4">
                  
                  <!-- Dirección -->
                  <PermissionWrapper 
                    :has-permission="isFieldEnabled('direccion')"
                    title="Dirección no disponible"
                    message="La visualización de dirección no está incluida en tu plan actual"
                    icon="map-marker-alt"
                    @upgrade="handleUpgrade"
                  >
                    <div class="bg-white rounded-lg border border-neutral-200 p-4">
                      <div class="flex items-start">
                        <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
                          <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="text-red-600" />
                        </div>
                        <div class="flex-1">
                          <h4 class="font-medium text-neutral-900 mb-2">Dirección</h4>
                          <p v-if="!isEditing" class="text-sm text-neutral-600">
                            {{ formData.direccion || 'No especificada' }}
                          </p>
                          <textarea 
                            v-else
                            v-model="formData.direccion"
                            rows="2"
                            class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Calle, número, piso, etc."
                          ></textarea>
                          <p class="text-xs text-neutral-500 mt-1">Dirección física del negocio</p>
                        </div>
                      </div>
                    </div>
                  </PermissionWrapper>
                  
                  <!-- Ciudad -->
                  <PermissionWrapper 
                    :has-permission="isFieldEnabled('ciudad')"
                    title="Ciudad no disponible"
                    message="La visualización de ciudad no está incluida en tu plan actual"
                    icon="city"
                    @upgrade="handleUpgrade"
                  >
                    <div class="bg-white rounded-lg border border-neutral-200 p-4">
                      <div class="flex items-center">
                        <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4">
                          <font-awesome-icon :icon="['fas', 'city']" class="text-indigo-600" />
                        </div>
                        <div class="flex-1">
                          <h4 class="font-medium text-neutral-900 mb-2">Ciudad</h4>
                          <p v-if="!isEditing" class="text-sm text-neutral-600">
                            {{ formData.ciudad || 'No especificada' }}
                          </p>
                          <input 
                            v-else
                            v-model="formData.ciudad"
                            type="text"
                            class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Ciudad"
                          />
                          <p class="text-xs text-neutral-500 mt-1">Ciudad donde operas</p>
                        </div>
                      </div>
                    </div>
                  </PermissionWrapper>
                  
                  <!-- Provincia -->
                  <PermissionWrapper 
                    :has-permission="isFieldEnabled('provincia')"
                    title="Provincia no disponible"
                    message="La visualización de provincia no está incluida en tu plan actual"
                    icon="map"
                    @upgrade="handleUpgrade"
                  >
                    <div class="bg-white rounded-lg border border-neutral-200 p-4">
                      <div class="flex items-center">
                        <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mr-4">
                          <font-awesome-icon :icon="['fas', 'map']" class="text-yellow-600" />
                        </div>
                        <div class="flex-1">
                          <h4 class="font-medium text-neutral-900 mb-2">Provincia</h4>
                          <p v-if="!isEditing" class="text-sm text-neutral-600">
                            {{ formData.provincia || 'No especificada' }}
                          </p>
                          <input 
                            v-else
                            v-model="formData.provincia"
                            type="text"
                            class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Provincia"
                          />
                          <p class="text-xs text-neutral-500 mt-1">Provincia</p>
                        </div>
                      </div>
                    </div>
                  </PermissionWrapper>
                  
                  <!-- Sitio web -->
                  <PermissionWrapper 
                    :has-permission="isFieldEnabled('sitio_web')"
                    title="Sitio web no disponible"
                    message="La visualización de sitio web no está incluida en tu plan actual"
                    icon="globe"
                    @upgrade="handleUpgrade"
                  >
                    <div class="bg-white rounded-lg border border-neutral-200 p-4">
                      <div class="flex items-center">
                        <div class="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center mr-4">
                          <font-awesome-icon :icon="['fas', 'globe']" class="text-teal-600" />
                        </div>
                        <div class="flex-1">
                          <h4 class="font-medium text-neutral-900 mb-2">Sitio web</h4>
                          <div v-if="!isEditing">
                            <a 
                              v-if="formData.sitio_web"
                              :href="formData.sitio_web" 
                              target="_blank" 
                              class="text-sm text-primary-600 hover:text-primary-800"
                            >
                              {{ formData.sitio_web }}
                            </a>
                            <p v-else class="text-sm text-neutral-600">No especificado</p>
                          </div>
                          <input 
                            v-else
                            v-model="formData.sitio_web"
                            type="url"
                            class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="https://mi-sitio-web.com"
                          />
                          <p class="text-xs text-neutral-500 mt-1">Sitio web del negocio</p>
                        </div>
                      </div>
                    </div>
                  </PermissionWrapper>
                </div>
              </div>

              <!-- Descripción -->
              <PermissionWrapper 
                :has-permission="isFieldEnabled('descripcion')"
                title="Descripción no disponible"
                message="La visualización de descripción no está incluida en tu plan actual"
                icon="file-text"
                @upgrade="handleUpgrade"
              >
                <div class="bg-white rounded-lg border border-neutral-200 p-4">
                  <div class="flex items-start">
                    <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'file-text']" class="text-gray-600" />
                    </div>
                    <div class="flex-1">
                      <h4 class="font-medium text-neutral-900 mb-2">Descripción del negocio</h4>
                      <p v-if="!isEditing" class="text-sm text-neutral-600 leading-relaxed">
                        {{ formData.descripcion || 'Sin descripción' }}
                      </p>
                      <textarea 
                        v-else
                        v-model="formData.descripcion"
                        rows="4"
                        class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        placeholder="Describe tu negocio, servicios y experiencia..."
                      ></textarea>
                      <p class="text-xs text-neutral-500 mt-1">Describe tu negocio y servicios</p>
                    </div>
                  </div>
                </div>
              </PermissionWrapper>

              <!-- Categorías y rubros -->
              <div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
                  <font-awesome-icon :icon="['fas', 'tags']" class="mr-3 text-primary-600" />
                  Categorización
                </h3>
                <div class="grid md:grid-cols-2 gap-4">
                  
                  <!-- Categoría -->
                  <div class="bg-white rounded-lg border border-neutral-200 p-4">
                    <div class="flex items-center">
                      <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mr-4">
                        <font-awesome-icon :icon="['fas', 'tag']" class="text-purple-600" />
                      </div>
                      <div class="flex-1">
                        <h4 class="font-medium text-neutral-900 mb-2">Categoría</h4>
                        <p v-if="!isEditing" class="text-sm text-neutral-600">
                          {{ userProfile?.categoria_nombre || 'No especificada' }}
                        </p>
                        <select 
                          v-else
                          v-model="formData.categoria"
                          @change="onCategoriaChange"
                          class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        >
                          <option value="">Selecciona una categoría</option>
                          <option 
                            v-for="categoria in categorias" 
                            :key="categoria.id" 
                            :value="categoria.id"
                          >
                            {{ categoria.nombre }}
                          </option>
                        </select>
                        <p class="text-xs text-neutral-500 mt-1">Categoría del servicio</p>
                      </div>
                    </div>
                  </div>

                  <!-- Rubro -->
                  <div class="bg-white rounded-lg border border-neutral-200 p-4">
                    <div class="flex items-center">
                      <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mr-4">
                        <font-awesome-icon :icon="['fas', 'briefcase']" class="text-orange-600" />
                      </div>
                      <div class="flex-1">
                        <h4 class="font-medium text-neutral-900 mb-2">Rubro</h4>
                        <p v-if="!isEditing" class="text-sm text-neutral-600">
                          {{ userProfile?.rubro_nombre || 'No especificado' }}
                        </p>
                        <select 
                          v-else
                          v-model="formData.rubro"
                          class="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                          :disabled="!formData.categoria"
                        >
                          <option value="">
                            {{ !formData.categoria ? 'Primero selecciona una categoría' : 'Selecciona un rubro' }}
                          </option>
                          <option 
                            v-for="rubro in rubrosFiltered" 
                            :key="rubro.id" 
                            :value="rubro.id"
                          >
                            {{ rubro.nombre }}
                          </option>
                        </select>
                        <p class="text-xs text-neutral-500 mt-1">Rubro específico</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import apiClient from '../../services/api';
import DashboardNavigation from '../../components/DashboardNavigation.vue';
import PermissionWrapper from '../../components/PermissionWrapper.vue';

const authStore = useAuthStore();

// Estado del componente
const loading = ref(true);
const isEditing = ref(false);
const saving = ref(false);

// Datos
const userProfile = ref(null);
const categorias = ref([]);
const rubros = ref([]);

// Datos del formulario
const formData = ref({
  telefono: '',
  direccion: '',
  ciudad: '',
  provincia: '',
  sitio_web: '',
  descripcion: '',
  categoria: '',
  rubro: ''
});

// Datos originales para cancelar edición
const originalData = ref({});

// Computed para rubros filtrados por categoría
const rubrosFiltered = computed(() => {
  if (!formData.value.categoria) return [];
  return rubros.value.filter(rubro => rubro.categoria === parseInt(formData.value.categoria));
});

// Función para verificar si un campo está habilitado en el plan
const isFieldEnabled = (fieldName) => {
  if (!userProfile.value?.plan_info?.fields_enabled) return false;
  return userProfile.value.plan_info.fields_enabled.includes(fieldName);
};

// Cargar datos del perfil
const loadProfile = async () => {
  try {
    loading.value = true;
    await authStore.fetchUserProfile();
    userProfile.value = authStore.user?.perfil;
    
    if (userProfile.value) {
      formData.value = {
        telefono: userProfile.value.telefono || '',
        direccion: userProfile.value.direccion || '',
        ciudad: userProfile.value.ciudad || '',
        provincia: userProfile.value.provincia || '',
        sitio_web: userProfile.value.sitio_web || '',
        descripcion: userProfile.value.descripcion || '',
        categoria: userProfile.value.categoria || '',
        rubro: userProfile.value.rubro || ''
      };
      
      // Guardar datos originales
      originalData.value = { ...formData.value };
    }
  } catch (error) {
    console.error('Error cargando perfil:', error);
  } finally {
    loading.value = false;
  }
};

// Cargar categorías y rubros
const loadCategoriasRubros = async () => {
  try {
    const { catalogService } = await import('../../services/api');
    const [categoriasResponse, rubrosResponse] = await Promise.all([
      catalogService.getCategorias(),
      catalogService.getRubros()
    ]);
    
    categorias.value = categoriasResponse.data.results || categoriasResponse.data;
    rubros.value = rubrosResponse.data.results || rubrosResponse.data;
  } catch (error) {
    console.error('Error cargando categorías y rubros:', error);
  }
};

// Manejar cambio de categoría
const onCategoriaChange = () => {
  formData.value.rubro = ''; // Limpiar rubro cuando cambia categoría
};

// Iniciar edición
const startEdit = () => {
  isEditing.value = true;
  originalData.value = { ...formData.value };
};

// Cancelar edición
const cancelEdit = () => {
  isEditing.value = false;
  formData.value = { ...originalData.value };
};

// Guardar perfil
const saveProfile = async () => {
  try {
    saving.value = true;
    
    const updateData = {
      perfil: {
        telefono: formData.value.telefono,
        direccion: formData.value.direccion,
        ciudad: formData.value.ciudad,
        provincia: formData.value.provincia,
        sitio_web: formData.value.sitio_web,
        descripcion: formData.value.descripcion,
        categoria: formData.value.categoria || null,
        rubro: formData.value.rubro || null
      }
    };
    
    const { authService } = await import('../../services/api');
    await authService.updateProfile(updateData);
    await authStore.fetchUserProfile(); // Recargar datos
    
    isEditing.value = false;
    userProfile.value = authStore.user?.perfil;
    
    // Mostrar mensaje de éxito
    alert('Perfil actualizado exitosamente');
    
  } catch (error) {
    console.error('Error guardando perfil:', error);
    if (error.response?.data) {
      alert('Error al guardar: ' + JSON.stringify(error.response.data));
    } else {
      alert('Error al guardar el perfil. Inténtalo de nuevo.');
    }
  } finally {
    saving.value = false;
  }
};

// Función para manejar upgrade de plan
const handleUpgrade = () => {
  alert('Funcionalidad de upgrade de plan próximamente disponible');
};

onMounted(() => {
  loadProfile();
  loadCategoriasRubros();
});
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
