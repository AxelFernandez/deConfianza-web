<template>
  <div class="min-h-screen bg-neutral-50">
    <!-- Header con breadcrumb -->
    <header class="bg-white shadow-sm border-b border-neutral-200">
      <div class="container-custom py-6">
        <div class="flex items-center space-x-2 text-sm text-neutral-600 mb-2">
          <router-link to="/prestador/dashboard" class="hover:text-primary-600">Dashboard</router-link>
          <span>/</span>
          <span class="text-neutral-900">Configuración</span>
        </div>
        <h1 class="text-2xl font-bold text-neutral-900">Configuración</h1>
        <p class="text-neutral-600 mt-1">Gestiona la configuración de tu cuenta y preferencias</p>
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
              <span class="text-neutral-600">Cargando configuración...</span>
            </div>
          </div>

          <!-- Contenido principal -->
          <div v-else class="space-y-6">
            
            <!-- Sección de seguridad -->
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
              <div class="bg-gradient-to-r from-red-50 to-orange-50 border-b border-red-100 p-6">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
                    <font-awesome-icon :icon="['fas', 'shield-alt']" class="text-red-600" />
                  </div>
                  <div>
                    <h2 class="text-xl font-semibold text-neutral-900">Seguridad de la cuenta</h2>
                    <p class="text-sm text-neutral-600">Gestiona la seguridad y acceso a tu cuenta</p>
                  </div>
                </div>
              </div>
              
              <div class="p-6">
                <!-- Información de la cuenta -->
                <div class="mb-6">
                  <h3 class="text-lg font-medium text-neutral-900 mb-4">Información de la cuenta</h3>
                  <div class="grid md:grid-cols-2 gap-4">
                    
                    <!-- Tipo de cuenta -->
                    <div class="bg-neutral-50 rounded-lg p-4 border border-neutral-200">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <font-awesome-icon :icon="['fas', isGoogleAccount ? 'google' : 'user']" class="text-blue-600" />
                        </div>
                        <div>
                          <h4 class="font-medium text-neutral-900">Tipo de cuenta</h4>
                          <p class="text-sm text-neutral-600 mt-1">
                            {{ isGoogleAccount ? 'Cuenta vinculada a Google' : 'Cuenta local' }}
                          </p>
                          <span 
                            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium mt-2"
                            :class="isGoogleAccount ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'"
                          >
                            <font-awesome-icon :icon="['fas', isGoogleAccount ? 'check-circle' : 'user-circle']" class="mr-1" />
                            {{ isGoogleAccount ? 'Google' : 'Local' }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Email -->
                    <div class="bg-neutral-50 rounded-lg p-4 border border-neutral-200">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
                          <font-awesome-icon :icon="['fas', 'envelope']" class="text-green-600" />
                        </div>
                        <div>
                          <h4 class="font-medium text-neutral-900">Email</h4>
                          <p class="text-sm text-neutral-600 mt-1">{{ authStore.user?.email || 'No especificado' }}</p>
                          <p class="text-xs text-neutral-500 mt-1">
                            {{ isGoogleAccount ? 'Verificado por Google' : 'Verificar email' }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Cambio de contraseña -->
                <div v-if="!isGoogleAccount">
                  <h3 class="text-lg font-medium text-neutral-900 mb-4">Cambiar contraseña</h3>
                  <div class="bg-white border border-neutral-200 rounded-lg p-6">
                    <form @submit.prevent="changePassword" class="space-y-4">
                      <!-- Contraseña actual -->
                      <div>
                        <label class="block text-sm font-medium text-neutral-700 mb-1">
                          Contraseña actual
                        </label>
                        <div class="relative">
                          <input 
                            v-model="passwordForm.currentPassword"
                            :type="showCurrentPassword ? 'text' : 'password'"
                            class="w-full px-3 py-2 pr-10 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Ingresa tu contraseña actual"
                            required
                          />
                          <button 
                            type="button"
                            @click="showCurrentPassword = !showCurrentPassword"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                          >
                            <font-awesome-icon 
                              :icon="['fas', showCurrentPassword ? 'eye-slash' : 'eye']" 
                              class="text-neutral-400 hover:text-neutral-600"
                            />
                          </button>
                        </div>
                      </div>

                      <!-- Nueva contraseña -->
                      <div>
                        <label class="block text-sm font-medium text-neutral-700 mb-1">
                          Nueva contraseña
                        </label>
                        <div class="relative">
                          <input 
                            v-model="passwordForm.newPassword"
                            :type="showNewPassword ? 'text' : 'password'"
                            class="w-full px-3 py-2 pr-10 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Ingresa tu nueva contraseña"
                            required
                            minlength="8"
                          />
                          <button 
                            type="button"
                            @click="showNewPassword = !showNewPassword"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                          >
                            <font-awesome-icon 
                              :icon="['fas', showNewPassword ? 'eye-slash' : 'eye']" 
                              class="text-neutral-400 hover:text-neutral-600"
                            />
                          </button>
                        </div>
                        <p class="text-xs text-neutral-500 mt-1">Mínimo 8 caracteres</p>
                      </div>

                      <!-- Confirmar contraseña -->
                      <div>
                        <label class="block text-sm font-medium text-neutral-700 mb-1">
                          Confirmar nueva contraseña
                        </label>
                        <div class="relative">
                          <input 
                            v-model="passwordForm.confirmPassword"
                            :type="showConfirmPassword ? 'text' : 'password'"
                            class="w-full px-3 py-2 pr-10 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Confirma tu nueva contraseña"
                            required
                            minlength="8"
                          />
                          <button 
                            type="button"
                            @click="showConfirmPassword = !showConfirmPassword"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                          >
                            <font-awesome-icon 
                              :icon="['fas', showConfirmPassword ? 'eye-slash' : 'eye']" 
                              class="text-neutral-400 hover:text-neutral-600"
                            />
                          </button>
                        </div>
                        <p 
                          v-if="passwordForm.newPassword && passwordForm.confirmPassword"
                          class="text-xs mt-1"
                          :class="passwordsMatch ? 'text-green-600' : 'text-red-600'"
                        >
                          <font-awesome-icon 
                            :icon="['fas', passwordsMatch ? 'check' : 'times']" 
                            class="mr-1"
                          />
                          {{ passwordsMatch ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden' }}
                        </p>
                      </div>

                      <!-- Botones -->
                      <div class="flex justify-end space-x-3 pt-4">
                        <button 
                          type="button"
                          @click="resetPasswordForm"
                          class="px-4 py-2 text-sm text-neutral-600 hover:text-neutral-800 border border-neutral-300 rounded-md hover:bg-neutral-50 transition-colors"
                        >
                          Cancelar
                        </button>
                        <button 
                          type="submit"
                          :disabled="!canSubmitPassword || changingPassword"
                          class="px-4 py-2 text-sm bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors disabled:bg-neutral-400 disabled:cursor-not-allowed"
                        >
                          <font-awesome-icon 
                            v-if="changingPassword" 
                            :icon="['fas', 'spinner']" 
                            class="animate-spin mr-2" 
                          />
                          {{ changingPassword ? 'Cambiando...' : 'Cambiar contraseña' }}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>

                <!-- Mensaje para cuentas de Google -->
                <div v-else class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <div class="flex items-start">
                    <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                      <font-awesome-icon :icon="['fab', 'google']" class="text-blue-600" />
                    </div>
                    <div>
                      <h4 class="font-medium text-blue-900 mb-2">Cuenta vinculada a Google</h4>
                      <p class="text-sm text-blue-700 mb-3">
                        Tu cuenta está vinculada a Google. Para cambiar tu contraseña, debes hacerlo desde tu cuenta de Google.
                      </p>
                      <div class="flex space-x-3">
                        <a 
                          href="https://myaccount.google.com/security"
                          target="_blank"
                          class="inline-flex items-center px-3 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
                        >
                          <font-awesome-icon :icon="['fab', 'google']" class="mr-2" />
                          Ir a Google Account
                        </a>
                        <button 
                          @click="showGoogleInfo = !showGoogleInfo"
                          class="inline-flex items-center px-3 py-2 text-sm text-blue-600 hover:text-blue-800 border border-blue-300 rounded-md hover:bg-blue-50 transition-colors"
                        >
                          <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-2" />
                          Más información
                        </button>
                      </div>
                      
                      <!-- Información adicional -->
                      <div v-if="showGoogleInfo" class="mt-4 p-3 bg-blue-100 rounded-md">
                        <h5 class="font-medium text-blue-900 mb-2">¿Por qué no puedo cambiar mi contraseña aquí?</h5>
                        <ul class="text-xs text-blue-700 space-y-1">
                          <li>• Tu cuenta está vinculada a Google para mayor seguridad</li>
                          <li>• Google maneja la autenticación y seguridad de tu cuenta</li>
                          <li>• Puedes gestionar tu contraseña desde tu cuenta de Google</li>
                          <li>• Esto te permite usar la misma contraseña en otros servicios de Google</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sección de notificaciones (placeholder) -->
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
              <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100 p-6">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                    <font-awesome-icon :icon="['fas', 'bell']" class="text-blue-600" />
                  </div>
                  <div>
                    <h2 class="text-xl font-semibold text-neutral-900">Notificaciones</h2>
                    <p class="text-sm text-neutral-600">Configura cómo y cuándo recibir notificaciones</p>
                  </div>
                </div>
              </div>
              
              <div class="p-6">
                <div class="text-center py-8">
                  <font-awesome-icon :icon="['fas', 'bell-slash']" class="text-4xl text-neutral-400 mb-4" />
                  <h3 class="text-lg font-medium text-neutral-900 mb-2">Configuración de notificaciones</h3>
                  <p class="text-neutral-600">Esta funcionalidad estará disponible próximamente.</p>
                </div>
              </div>
            </div>

            <!-- Sección de privacidad (placeholder) -->
            <div class="bg-white rounded-lg shadow-sm border border-neutral-100 overflow-hidden">
              <div class="bg-gradient-to-r from-green-50 to-emerald-50 border-b border-green-100 p-6">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                    <font-awesome-icon :icon="['fas', 'user-shield']" class="text-green-600" />
                  </div>
                  <div>
                    <h2 class="text-xl font-semibold text-neutral-900">Privacidad</h2>
                    <p class="text-sm text-neutral-600">Gestiona tu privacidad y datos personales</p>
                  </div>
                </div>
              </div>
              
              <div class="p-6">
                <div class="text-center py-8">
                  <font-awesome-icon :icon="['fas', 'user-shield']" class="text-4xl text-neutral-400 mb-4" />
                  <h3 class="text-lg font-medium text-neutral-900 mb-2">Configuración de privacidad</h3>
                  <p class="text-neutral-600">Esta funcionalidad estará disponible próximamente.</p>
                </div>
              </div>
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
import DashboardNavigation from '../../components/DashboardNavigation.vue';

const authStore = useAuthStore();

// Estado del componente
const loading = ref(true);
const changingPassword = ref(false);
const showGoogleInfo = ref(false);

// Estados para mostrar/ocultar contraseñas
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

// Formulario de cambio de contraseña
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// Computed para verificar si es cuenta de Google
const isGoogleAccount = computed(() => {
  // Verificar si el usuario se registró con Google
  return authStore.user?.perfil?.is_google_user || false;
});

// Computed para verificar si las contraseñas coinciden
const passwordsMatch = computed(() => {
  return passwordForm.value.newPassword === passwordForm.value.confirmPassword && 
         passwordForm.value.newPassword.length >= 8;
});

// Computed para verificar si se puede enviar el formulario
const canSubmitPassword = computed(() => {
  return passwordForm.value.currentPassword &&
         passwordForm.value.newPassword &&
         passwordForm.value.confirmPassword &&
         passwordsMatch.value &&
         passwordForm.value.newPassword.length >= 8;
});

// Función para resetear el formulario de contraseña
const resetPasswordForm = () => {
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
  showCurrentPassword.value = false;
  showNewPassword.value = false;
  showConfirmPassword.value = false;
};

// Función para cambiar contraseña
const changePassword = async () => {
  if (!canSubmitPassword.value) return;
  
  try {
    changingPassword.value = true;
    
    const { authService } = await import('../../services/api');
    
    await authService.changePassword({
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword,
      confirm_password: passwordForm.value.confirmPassword
    });
    
    // Mostrar mensaje de éxito
    alert('Contraseña cambiada exitosamente');
    
    // Resetear formulario
    resetPasswordForm();
    
  } catch (error) {
    console.error('Error cambiando contraseña:', error);
    
    if (error.response?.data) {
      const errorData = error.response.data;
      if (errorData.current_password) {
        alert('Contraseña actual incorrecta');
      } else if (errorData.new_password) {
        alert('Nueva contraseña inválida: ' + errorData.new_password.join(', '));
      } else {
        alert('Error al cambiar contraseña: ' + JSON.stringify(errorData));
      }
    } else {
      alert('Error al cambiar la contraseña. Inténtalo de nuevo.');
    }
  } finally {
    changingPassword.value = false;
  }
};

// Cargar datos iniciales
const loadData = async () => {
  try {
    loading.value = true;
    // Aquí podrías cargar configuraciones adicionales si las hay
    await new Promise(resolve => setTimeout(resolve, 500)); // Simular carga
  } catch (error) {
    console.error('Error cargando configuración:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
