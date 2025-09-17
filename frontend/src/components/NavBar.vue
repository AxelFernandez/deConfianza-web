<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-primary">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        DE CONFIANZA
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Inicio</router-link>
          </li>
          <li class="nav-item" v-if="!isLandingOnlyMode">
            <router-link class="nav-link" to="/buscar">Buscar</router-link>
          </li>
        </ul>
        <ul class="navbar-nav" v-if="!isLandingOnlyMode">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Ingresar</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link btn btn-light text-primary px-3" to="/registrar">Registrarse</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as bootstrap from 'bootstrap';

const isLandingOnlyMode = ref(import.meta.env.VITE_LANDING_ONLY_MODE === 'true');

onMounted(() => {
  // Inicializar los componentes de Bootstrap que requieran JavaScript
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
})
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  margin: 0 5px;
}
</style>
