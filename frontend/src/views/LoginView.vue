<template>
  <div class="login-view py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow">
            <div class="card-body p-4 p-md-5">
              <h1 class="h3 text-center mb-4">Iniciar sesión</h1>
              
              <form @submit.prevent="login">
                <div class="mb-3">
                  <label for="email" class="form-label">Correo electrónico</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <font-awesome-icon :icon="['fas', 'envelope']" />
                    </span>
                    <input 
                      type="email" 
                      class="form-control" 
                      id="email" 
                      v-model="email" 
                      required
                      placeholder="correo@ejemplo.com"
                    >
                  </div>
                </div>
                
                <div class="mb-4">
                  <label for="password" class="form-label">Contraseña</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <font-awesome-icon :icon="['fas', 'lock']" />
                    </span>
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="password" 
                      v-model="password" 
                      required
                      placeholder="Contraseña"
                    >
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button"
                      @click="showPassword = !showPassword"
                    >
                      <font-awesome-icon :icon="showPassword ? ['fas', 'eye-slash'] : ['fas', 'eye']" />
                    </button>
                  </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center mb-4">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="remember" v-model="remember">
                    <label class="form-check-label" for="remember">
                      Recordarme
                    </label>
                  </div>
                  <a href="#" class="text-primary">¿Olvidaste tu contraseña?</a>
                </div>
                
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary">
                    <font-awesome-icon :icon="['fas', 'sign-in-alt']" class="me-2" />
                    Iniciar sesión
                  </button>
                </div>
              </form>
              
              <div class="mt-4 text-center">
                <p class="mb-0">¿No tienes una cuenta? <router-link to="/registrar" class="text-primary">Regístrate</router-link></p>
              </div>
              
              <div class="separator text-center my-4">
                <span>O inicia sesión con</span>
              </div>
              
              <div class="row g-2">
                <div class="col">
                  <button class="btn btn-outline-secondary w-100">
                    <font-awesome-icon :icon="['fab', 'google']" class="me-2" />
                    Google
                  </button>
                </div>
                <div class="col">
                  <button class="btn btn-outline-secondary w-100">
                    <font-awesome-icon :icon="['fab', 'facebook']" class="me-2" />
                    Facebook
                  </button>
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
import { ref } from 'vue';

const email = ref('');
const password = ref('');
const remember = ref(false);
const showPassword = ref(false);

const login = () => {
  // Aquí iría la lógica de inicio de sesión
  console.log('Iniciando sesión con:', email.value, password.value);
};
</script>

<style scoped>
.login-view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
}

.separator {
  position: relative;
}

.separator::before,
.separator::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background-color: var(--gray-300);
}

.separator::before {
  left: 0;
}

.separator::after {
  right: 0;
}

.separator span {
  background-color: white;
  padding: 0 10px;
  color: var(--gray-600);
  font-size: 0.9rem;
}
</style>
