<template>
  <div class="py-10">
    <div class="container-custom">
      <div class="flex justify-center">
        <div class="w-full max-w-2xl">
          <div class="bg-white rounded-2xl shadow-lg border border-neutral-100">
            <div class="p-6 md:p-8">
              <h1 class="text-2xl font-display font-bold text-center mb-6">Crear una cuenta</h1>
              
              <div class="flex rounded-lg overflow-hidden mb-6 border border-neutral-200">
                <button 
                  class="flex-1 py-3 px-4 text-center font-medium transition-colors flex items-center justify-center" 
                  @click="userType = 'cliente'"
                  :class="userType === 'cliente' ? 'bg-primary-600 text-white' : 'bg-white text-neutral-700 hover:bg-neutral-50'"
                >
                  <font-awesome-icon :icon="['fas', 'user']" class="mr-2" />
                  Cliente
                </button>
                <button 
                  class="flex-1 py-3 px-4 text-center font-medium transition-colors flex items-center justify-center" 
                  @click="userType = 'prestador'"
                  :class="userType === 'prestador' ? 'bg-primary-600 text-white' : 'bg-white text-neutral-700 hover:bg-neutral-50'"
                >
                  <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-2" />
                  Prestador de servicios
                </button>
              </div>
              
              <div>
                <div v-if="userType === 'cliente'">
                  <!-- Mensaje de error -->
                  <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded mb-4">
                    <p>{{ errorMessage }}</p>
                  </div>
                  
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
                </div>
                
                <div v-else>
                  <!-- Mensaje de error -->
                  <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded mb-4">
                    <p>{{ errorMessage }}</p>
                  </div>
                  
                  <form @submit.prevent="registerProvider" class="space-y-5">
                    <div class="grid md:grid-cols-2 gap-4">
                      <div>
                        <label for="providerFirstName" class="block text-sm font-medium text-neutral-700 mb-1">Nombre</label>
                        <input 
                          type="text" 
                          class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                          id="providerFirstName" 
                          v-model="firstName" 
                          required
                        >
                      </div>
                      <div>
                        <label for="providerLastName" class="block text-sm font-medium text-neutral-700 mb-1">Apellido</label>
                        <input 
                          type="text" 
                          class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                          id="providerLastName" 
                          v-model="lastName" 
                          required
                        >
                      </div>
                    </div>
                    
                    <div>
                      <label for="businessName" class="block text-sm font-medium text-neutral-700 mb-1">Nombre comercial o empresa</label>
                      <input 
                        type="text" 
                        class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                        id="businessName" 
                        v-model="businessName" 
                        required
                      >
                    </div>
                    
                    <div>
                      <label for="providerEmail" class="block text-sm font-medium text-neutral-700 mb-1">Correo electrónico</label>
                      <input 
                        type="email" 
                        class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                        id="providerEmail" 
                        v-model="email" 
                        required
                      >
                    </div>
                    
                    <div>
                      <label for="phone" class="block text-sm font-medium text-neutral-700 mb-1">Teléfono</label>
                      <input 
                        type="tel" 
                        class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                        id="phone" 
                        v-model="phone" 
                        required
                      >
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                      <div>
                        <label for="providerPassword" class="block text-sm font-medium text-neutral-700 mb-1">Contraseña</label>
                        <input 
                          type="password" 
                          class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                          id="providerPassword" 
                          v-model="password" 
                          required
                        >
                      </div>
                      <div>
                        <label for="providerConfirmPassword" class="block text-sm font-medium text-neutral-700 mb-1">Confirmar contraseña</label>
                        <input 
                          type="password" 
                          class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors" 
                          id="providerConfirmPassword" 
                          v-model="confirmPassword" 
                          required
                        >
                      </div>
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-neutral-700 mb-2">Plan de suscripción</label>
                      <div class="border border-neutral-300 rounded-lg p-4 space-y-3">
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input 
                              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full" 
                              type="radio" 
                              name="subscriptionPlan" 
                              id="plan1" 
                              value="1" 
                              v-model="subscriptionPlan" 
                              checked
                            >
                          </div>
                          <label class="ml-2 block text-sm text-neutral-700" for="plan1">
                            <span class="font-semibold">Rango 1 - Gratuito</span> - Registro básico con nombre y dirección
                          </label>
                        </div>
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input 
                              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full" 
                              type="radio" 
                              name="subscriptionPlan" 
                              id="plan2" 
                              value="2" 
                              v-model="subscriptionPlan"
                            >
                          </div>
                          <label class="ml-2 block text-sm text-neutral-700" for="plan2">
                            <span class="font-semibold">Rango 2 - Básico</span> - Incluye teléfono, redes sociales, imágenes y videos
                          </label>
                        </div>
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input 
                              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full" 
                              type="radio" 
                              name="subscriptionPlan" 
                              id="plan3" 
                              value="3" 
                              v-model="subscriptionPlan"
                            >
                          </div>
                          <label class="ml-2 block text-sm text-neutral-700" for="plan3">
                            <span class="font-semibold">Rango 3 - Premium</span> - Todo lo anterior + reseñas, asesoría y reportes
                          </label>
                        </div>
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input 
                              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full" 
                              type="radio" 
                              name="subscriptionPlan" 
                              id="plan4" 
                              value="4" 
                              v-model="subscriptionPlan"
                            >
                          </div>
                          <label class="ml-2 block text-sm text-neutral-700" for="plan4">
                            <span class="font-semibold">Rango 4 - Destacado</span> - Todo lo anterior + posicionamiento destacado
                          </label>
                        </div>
                      </div>
                    </div>
                    
                    <div class="flex items-start">
                      <div class="flex items-center h-5">
                        <input 
                          class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded" 
                          type="checkbox" 
                          id="providerTermsCheck" 
                          v-model="termsAccepted" 
                          required
                        >
                      </div>
                      <label class="ml-2 block text-sm text-neutral-700" for="providerTermsCheck">
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
                        {{ authStore.loading ? 'Registrando...' : 'Registrarme como prestador' }}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
              
              <div class="mt-6 text-center">
                <p class="text-sm text-neutral-600">¿Ya tienes una cuenta? <router-link to="/login" class="text-primary-600 hover:text-primary-800 font-medium">Inicia sesión</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

// Cliente y prestador comparten algunos campos
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const termsAccepted = ref(false);
const errorMessage = ref('');

// Campos específicos de prestador
const userType = ref('cliente');
const businessName = ref('');
const phone = ref('');

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

// Registrar cliente
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
      router.push('/');
    } else {
      errorMessage.value = authStore.error || 'Error al registrarse';
    }
  } catch (error) {
    console.error('Error en registro:', error);
    errorMessage.value = 'Error al procesar el registro';
  }
}

// Registrar prestador
async function registerProvider() {
  if (!validatePasswords()) return;
  
  errorMessage.value = '';
  
  try {
    // Primero registramos el usuario básico
    const userData = {
      username: email.value,
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      perfil: {
        es_prestador: true,
        telefono: phone.value
      },
      prestador_data: {
        nombre_comercial: businessName.value
      }
    };
    
    const success = await authStore.register(userData);
    
    if (success) {
      // Redirigir al onboarding para completar el perfil
      router.push('/onboarding');
    } else {
      errorMessage.value = authStore.error || 'Error al registrarse';
    }
  } catch (error) {
    console.error('Error en registro de prestador:', error);
    errorMessage.value = 'Error al procesar el registro';
  }
}
</script>

<style scoped>
/* Todos los estilos ahora están en las clases de Tailwind */
</style>
