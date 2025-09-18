<template>
  <div class="register-view py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-7">
          <div class="card shadow">
            <div class="card-body p-4 p-md-5">
              <h1 class="h3 text-center mb-4">Crear una cuenta</h1>
              
              <ul class="nav nav-pills mb-4" id="registerTab" role="tablist">
                <li class="nav-item flex-fill text-center" role="presentation">
                  <button 
                    class="nav-link w-100" 
                    id="client-tab" 
                    type="button" 
                    role="tab" 
                    aria-controls="client" 
                    aria-selected="true"
                    @click="userType = 'cliente'"
                    :class="{ active: userType === 'cliente' }"
                  >
                    <font-awesome-icon :icon="['fas', 'user']" class="me-2" />
                    Cliente
                  </button>
                </li>
                <li class="nav-item flex-fill text-center" role="presentation">
                  <button 
                    class="nav-link w-100" 
                    id="provider-tab" 
                    type="button" 
                    role="tab" 
                    aria-controls="provider" 
                    aria-selected="false"
                    @click="userType = 'prestador'"
                    :class="{ active: userType === 'prestador' }"
                  >
                    <font-awesome-icon :icon="['fas', 'briefcase']" class="me-2" />
                    Prestador de servicios
                  </button>
                </li>
              </ul>
              
              <div class="tab-content" id="registerTabContent">
                <div v-if="userType === 'cliente'" id="client" role="tabpanel" aria-labelledby="client-tab">
                  <form @submit.prevent="register">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="firstName" class="form-label">Nombre</label>
                        <input type="text" class="form-control" id="firstName" v-model="firstName" required>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="lastName" class="form-label">Apellido</label>
                        <input type="text" class="form-control" id="lastName" v-model="lastName" required>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label for="email" class="form-label">Correo electrónico</label>
                      <input type="email" class="form-control" id="email" v-model="email" required>
                    </div>
                    
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="password" class="form-label">Contraseña</label>
                        <input type="password" class="form-control" id="password" v-model="password" required>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="confirmPassword" class="form-label">Confirmar contraseña</label>
                        <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required>
                      </div>
                    </div>
                    
                    <div class="form-check mb-4">
                      <input class="form-check-input" type="checkbox" id="termsCheck" v-model="termsAccepted" required>
                      <label class="form-check-label" for="termsCheck">
                        Acepto los <a href="#" class="text-primary">Términos y condiciones</a> y la <a href="#" class="text-primary">Política de privacidad</a>
                      </label>
                    </div>
                    
                    <div class="d-grid">
                      <button type="submit" class="btn btn-primary">
                        <font-awesome-icon :icon="['fas', 'user-plus']" class="me-2" />
                        Crear cuenta
                      </button>
                    </div>
                  </form>
                </div>
                
                <div v-else id="provider" role="tabpanel" aria-labelledby="provider-tab">
                  <form @submit.prevent="registerProvider">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="providerFirstName" class="form-label">Nombre</label>
                        <input type="text" class="form-control" id="providerFirstName" v-model="firstName" required>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="providerLastName" class="form-label">Apellido</label>
                        <input type="text" class="form-control" id="providerLastName" v-model="lastName" required>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label for="businessName" class="form-label">Nombre comercial o empresa</label>
                      <input type="text" class="form-control" id="businessName" v-model="businessName" required>
                    </div>
                    
                    <div class="mb-3">
                      <label for="providerEmail" class="form-label">Correo electrónico</label>
                      <input type="email" class="form-control" id="providerEmail" v-model="email" required>
                    </div>
                    
                    <div class="mb-3">
                      <label for="phone" class="form-label">Teléfono</label>
                      <input type="tel" class="form-control" id="phone" v-model="phone" required>
                    </div>
                    
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="providerPassword" class="form-label">Contraseña</label>
                        <input type="password" class="form-control" id="providerPassword" v-model="password" required>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="providerConfirmPassword" class="form-label">Confirmar contraseña</label>
                        <input type="password" class="form-control" id="providerConfirmPassword" v-model="confirmPassword" required>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">Plan de suscripción</label>
                      <div class="subscription-plans">
                        <div class="form-check mb-2">
                          <input class="form-check-input" type="radio" name="subscriptionPlan" id="plan1" value="1" v-model="subscriptionPlan" checked>
                          <label class="form-check-label" for="plan1">
                            <strong>Rango 1 - Gratuito</strong> - Registro básico con nombre y dirección
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input class="form-check-input" type="radio" name="subscriptionPlan" id="plan2" value="2" v-model="subscriptionPlan">
                          <label class="form-check-label" for="plan2">
                            <strong>Rango 2 - Básico</strong> - Incluye teléfono, redes sociales, imágenes y videos
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input class="form-check-input" type="radio" name="subscriptionPlan" id="plan3" value="3" v-model="subscriptionPlan">
                          <label class="form-check-label" for="plan3">
                            <strong>Rango 3 - Premium</strong> - Todo lo anterior + reseñas, asesoría y reportes
                          </label>
                        </div>
                        <div class="form-check">
                          <input class="form-check-input" type="radio" name="subscriptionPlan" id="plan4" value="4" v-model="subscriptionPlan">
                          <label class="form-check-label" for="plan4">
                            <strong>Rango 4 - Destacado</strong> - Todo lo anterior + posicionamiento destacado
                          </label>
                        </div>
                      </div>
                    </div>
                    
                    <div class="form-check mb-4">
                      <input class="form-check-input" type="checkbox" id="providerTermsCheck" v-model="termsAccepted" required>
                      <label class="form-check-label" for="providerTermsCheck">
                        Acepto los <a href="#" class="text-primary">Términos y condiciones</a> y la <a href="#" class="text-primary">Política de privacidad</a>
                      </label>
                    </div>
                    
                    <div class="d-grid">
                      <button type="submit" class="btn btn-primary">
                        <font-awesome-icon :icon="['fas', 'user-plus']" class="me-2" />
                        Registrarme como prestador
                      </button>
                    </div>
                  </form>
                </div>
              </div>
              
              <div class="mt-4 text-center">
                <p class="mb-0">¿Ya tienes una cuenta? <router-link to="/login" class="text-primary">Inicia sesión</router-link></p>
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

// Cliente y prestador comparten algunos campos
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const termsAccepted = ref(false);

// Campos específicos de prestador
const userType = ref('cliente');
const businessName = ref('');
const phone = ref('');
const subscriptionPlan = ref('1');

const register = () => {
  // Lógica para registrar cliente
  console.log('Registrando cliente:', {
    firstName: firstName.value,
    lastName: lastName.value,
    email: email.value
  });
};

const registerProvider = () => {
  // Lógica para registrar prestador
  console.log('Registrando prestador:', {
    firstName: firstName.value,
    lastName: lastName.value,
    businessName: businessName.value,
    email: email.value,
    phone: phone.value,
    subscriptionPlan: subscriptionPlan.value
  });
};
</script>

<style scoped>
.register-view {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.subscription-plans {
  border: 1px solid var(--gray-300);
  padding: 1rem;
  border-radius: 0.375rem;
}

.nav-pills .nav-link.active {
  background-color: var(--primary-color);
}

.nav-pills .nav-link {
  color: var(--gray-700);
}

.nav-pills .nav-link:not(.active):hover {
  color: var(--primary-color);
  background-color: var(--gray-100);
}
</style>
