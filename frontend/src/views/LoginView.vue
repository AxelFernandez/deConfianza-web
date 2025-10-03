<template>
  <div class="min-h-[calc(100vh-200px)] flex items-center py-10">
    <div class="container-custom">
      <div class="flex justify-center">
        <div class="w-full max-w-md">
          <div class="bg-white rounded-2xl shadow-lg border border-neutral-100">
            <div class="p-6 md:p-8">
              <h1 class="text-2xl font-display font-bold text-center mb-6">Iniciar sesión</h1>
              
              <form @submit.prevent="login" class="space-y-5">
                <!-- Mensaje de error -->
                <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded">
                  <p>{{ errorMessage }}</p>
                </div>

                <div>
                  <label for="email" class="block text-sm font-medium text-neutral-700 mb-1">Correo electrónico</label>
                  <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-neutral-500">
                      <font-awesome-icon :icon="['fas', 'envelope']" />
                    </div>
                    <input 
                      type="email" 
                      class="w-full pl-10 pr-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="email" 
                      v-model="email" 
                      required
                      placeholder="correo@ejemplo.com"
                      :disabled="authStore.loading"
                    >
                  </div>
                </div>
                
                <div>
                  <label for="password" class="block text-sm font-medium text-neutral-700 mb-1">Contraseña</label>
                  <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-neutral-500">
                      <font-awesome-icon :icon="['fas', 'lock']" />
                    </div>
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="w-full pl-10 pr-10 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                      id="password" 
                      v-model="password" 
                      required
                      placeholder="Contraseña"
                      :disabled="authStore.loading"
                    >
                    <button 
                      class="absolute inset-y-0 right-0 flex items-center px-3 text-neutral-500 hover:text-neutral-700" 
                      type="button"
                      @click="showPassword = !showPassword"
                      :disabled="authStore.loading"
                    >
                      <font-awesome-icon :icon="showPassword ? ['fas', 'eye-slash'] : ['fas', 'eye']" />
                    </button>
                  </div>
                </div>
                
                <div class="flex justify-between items-center">
                  <div class="flex items-center">
                    <input 
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded" 
                      type="checkbox" 
                      id="remember" 
                      v-model="remember"
                      :disabled="authStore.loading"
                    >
                    <label class="ml-2 block text-sm text-neutral-700" for="remember">
                      Recordarme
                    </label>
                  </div>
                  <a href="#" class="text-sm text-primary-600 hover:text-primary-800">¿Olvidaste tu contraseña?</a>
                </div>
                
                <div>
                  <button 
                    type="submit" 
                    class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center"
                    :disabled="authStore.loading"
                  >
                    <span v-if="authStore.loading" class="mr-2">
                      <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin" />
                    </span>
                    <font-awesome-icon v-else :icon="['fas', 'sign-in-alt']" class="mr-2" />
                    {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
                  </button>
                </div>
              </form>
              
              <div class="mt-6 text-center">
                <p class="text-sm text-neutral-600">¿No tienes una cuenta? <router-link to="/registrar" class="text-primary-600 hover:text-primary-800 font-medium">Regístrate</router-link></p>
              </div>
              
              <div class="relative flex items-center justify-center my-6">
                <div class="absolute inset-0 flex items-center">
                  <div class="w-full border-t border-neutral-300"></div>
                </div>
                <div class="relative bg-white px-4 text-sm text-neutral-500">O inicia sesión con</div>
              </div>
              
              <div class="grid grid-cols-1 gap-3">
                <button 
                  type="button"
                  @click="loginWithGoogle"
                  class="flex items-center justify-center py-2 px-4 border border-neutral-300 rounded-lg hover:bg-neutral-50 transition-colors"
                  :disabled="authStore.loading"
                >
                  <font-awesome-icon :icon="['fab', 'google']" class="mr-2 text-red-500" />
                  <span class="text-sm font-medium">Continuar con Google</span>
                </button>
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

const email = ref('');
const password = ref('');
const remember = ref(false);
const showPassword = ref(false);
const errorMessage = ref('');

async function login() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor ingresa tu correo y contraseña';
    return;
  }
  
  errorMessage.value = '';
  
  const credentials = {
    username: email.value, // El backend espera username para el login
    email: email.value,
    password: password.value
  };
  
  const success = await authStore.login(credentials);
  
  if (success) {
    // Verificar si el usuario ha completado el onboarding
    if (authStore.user?.perfil?.onboarding_completed) {
      // Si ya completó el onboarding, redirigir a la página solicitada o al dashboard
      const redirectTo = router.currentRoute.value.query.redirect || '/';
      router.push(redirectTo);
    } else {
      // Si no ha completado el onboarding, redirigir a la página de onboarding
      router.push('/onboarding');
    }
  } else {
    // Si hubo error, mostrar mensaje
    errorMessage.value = authStore.error || 'Error al iniciar sesión';
  }
}

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
      // Verificar si el usuario ha completado el onboarding
      if (authStore.user?.perfil?.onboarding_completed) {
        // Si ya completó el onboarding, redirigir a la página solicitada o al dashboard
        const redirectTo = router.currentRoute.value.query.redirect || '/';
        router.push(redirectTo);
      } else {
        // Si no ha completado el onboarding, redirigir a la página de onboarding
        router.push('/onboarding');
      }
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
