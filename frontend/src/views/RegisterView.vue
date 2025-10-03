<template>
  <div class="py-10">
    <div class="container-custom">
      <div class="flex justify-center">
        <div class="w-full max-w-2xl">
          <div class="bg-white rounded-2xl shadow-lg border border-neutral-100">
            <div class="p-6 md:p-8">
              <h1 class="text-2xl font-display font-bold text-center mb-6">Crear una cuenta</h1>
              
              <!-- Mensaje de error -->
              <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded mb-4">
                <p>{{ errorMessage }}</p>
              </div>
              
              <!-- Formulario de registro unificado -->
              <form @submit.prevent="register" class="space-y-5">
                <div class="grid md:grid-cols-2 gap-4">
                  <div>
                    <label for="firstName" class="block text-sm font-medium text-neutral-700 mb-1">Nombre</label>
                    <input 
                      type="text" 
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="firstName" 
                      v-model="firstName" 
                      required
                    >
                  </div>
                  <div>
                    <label for="lastName" class="block text-sm font-medium text-neutral-700 mb-1">Apellido</label>
                    <input 
                      type="text" 
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="lastName" 
                      v-model="lastName" 
                      required
                    >
                  </div>
                </div>
                
                <div>
                  <label for="email" class="block text-sm font-medium text-neutral-700 mb-1">Correo electrónico</label>
                  <input 
                    type="email" 
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                    id="email" 
                    v-model="email" 
                    required
                  >
                </div>
                
                <div class="grid md:grid-cols-2 gap-4">
                  <div>
                    <label for="password" class="block text-sm font-medium text-neutral-700 mb-1">Contraseña</label>
                    <input 
                      type="password" 
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="password" 
                      v-model="password" 
                      required
                    >
                  </div>
                  <div>
                    <label for="confirmPassword" class="block text-sm font-medium text-neutral-700 mb-1">Confirmar contraseña</label>
                    <input 
                      type="password" 
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="confirmPassword" 
                      v-model="confirmPassword" 
                      required
                    >
                  </div>
                </div>
                
                <div class="flex items-start">
                  <div class="flex items-center h-5">
                    <input 
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded" 
                      type="checkbox" 
                      id="termsCheck" 
                      v-model="termsAccepted" 
                      required
                    >
                  </div>
                  <label class="ml-2 block text-sm text-neutral-700" for="termsCheck">
                    Acepto los <a href="#" class="text-primary-600 hover:text-primary-800">Términos y condiciones</a> y la <a href="#" class="text-primary-600 hover:text-primary-800">Política de privacidad</a>
                  </label>
                </div>
                
                <div>
                  <button 
                    type="submit" 
                    class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
                    :disabled="authStore.loading"
                  >
                    <span v-if="authStore.loading" class="mr-2">
                      <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin" />
                    </span>
                    <font-awesome-icon v-else :icon="['fas', 'user-plus']" class="mr-2" />
                    {{ authStore.loading ? 'Registrando...' : 'Crear cuenta' }}
                  </button>
                </div>
              </form>

              <!-- Separador -->
              <div class="my-6 flex items-center">
                <div class="flex-grow border-t border-neutral-200"></div>
                <span class="px-4 text-neutral-500 text-sm">o</span>
                <div class="flex-grow border-t border-neutral-200"></div>
              </div>

              <!-- Botón de Google -->
              <div>
                <button 
                  type="button"
                  @click="loginWithGoogle"
                  class="w-full flex items-center justify-center py-2 px-4 border border-neutral-300 rounded-lg hover:bg-neutral-50 transition-colors"
                  :disabled="authStore.loading"
                >
                  <font-awesome-icon :icon="['fab', 'google']" class="mr-2 text-red-500" />
                  <span class="text-sm font-medium">Continuar con Google</span>
                </button>
              </div>

              <!-- Enlace a login -->
              <div class="mt-6 text-center">
                <p class="text-neutral-600">
                  ¿Ya tienes una cuenta? 
                  <router-link to="/login" class="text-primary-600 hover:text-primary-800 font-medium">
                    Iniciar sesión
                  </router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();
const app = getCurrentInstance();

// Campos del formulario
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const termsAccepted = ref(false);
const errorMessage = ref('');

// Validar contraseñas
const validatePasswords = () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden';
    return false;
  }
  
  if (password.value.length < 8) {
    errorMessage.value = 'La contraseña debe tener al menos 8 caracteres';
    return false;
  }
  
  return true;
};

// Registrar usuario
async function register() {
  if (!validatePasswords()) return;
  
  errorMessage.value = '';
  
  try {
    const userData = {
      username: email.value,
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      perfil: {
        es_prestador: false
      }
    };
    
    const success = await authStore.register(userData);
    
    if (success) {
      router.push('/onboarding');
    } else {
      errorMessage.value = authStore.error || 'Error al registrarse';
    }
  } catch (error) {
    console.error('Error en registro:', error);
    errorMessage.value = 'Error al procesar el registro';
  }
}

// Login con Google
async function loginWithGoogle() {
  try {
    // Usar la API expuesta por el plugin para obtener el credential (ID token)
    const googleAuth = app?.appContext?.config?.globalProperties?.$googleAuth;
    if (!googleAuth || !googleAuth.getIdCredential) {
      errorMessage.value = 'Error al inicializar Google Auth';
      return;
    }
    // Pedir credential
    const resp = await googleAuth.getIdCredential();
    const credential = resp?.credential;
    if (!credential) {
      errorMessage.value = 'No se obtuvo respuesta de Google';
      return;
    }
    // Enviar credential al backend para intercambiarlo por JWT
    const ok = await authStore.loginWithGoogle(credential);
    
    if (ok) {
      // Siempre redirigir al onboarding después del registro con Google
      router.push('/onboarding');
    } else {
      errorMessage.value = authStore.error || 'Error al iniciar sesión con Google';
    }
  } catch (error) {
    console.error('Error en login con Google:', error);
    errorMessage.value = 'Error al iniciar sesión con Google';
  }
}
</script>

<style scoped>
/* Todos los estilos ahora están en las clases de Tailwind */
</style>