<template>
  <footer class="bg-primary text-white mt-auto">
    <div class="container py-4">
      <div class="row">
        <div class="col-lg-4 mb-4 mb-lg-0">
          <h5 class="mb-3">DE CONFIANZA</h5>
          <p>Conectando profesionales y oficios de confianza con quienes los necesitan.</p>
          <div class="social-icons">
            <a href="#" class="me-3"><font-awesome-icon :icon="['fab', 'facebook']" /></a>
            <a href="#" class="me-3"><font-awesome-icon :icon="['fab', 'instagram']" /></a>
            <a href="#" class="me-3"><font-awesome-icon :icon="['fab', 'twitter']" /></a>
            <a href="#"><font-awesome-icon :icon="['fab', 'linkedin']" /></a>
          </div>
        </div>
        <div class="col-lg-2 col-md-4 mb-4 mb-md-0">
          <h5 class="mb-3">Enlaces</h5>
          <ul class="list-unstyled">
            <li class="mb-2"><router-link to="/" class="text-white">Inicio</router-link></li>
            <li class="mb-2"><router-link to="/buscar" class="text-white">Buscar</router-link></li>
            <li class="mb-2"><router-link to="/registrar" class="text-white">Registrarse</router-link></li>
            <li><router-link to="/login" class="text-white">Ingresar</router-link></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-4 mb-4 mb-md-0">
          <h5 class="mb-3">Categorías</h5>
          <ul class="list-unstyled">
            <li class="mb-2"><a href="#" class="text-white">Oficios</a></li>
            <li class="mb-2"><a href="#" class="text-white">Profesiones</a></li>
            <li class="mb-2"><a href="#" class="text-white">Servicios a domicilio</a></li>
            <li><a href="#" class="text-white">Servicios online</a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-4">
          <h5 class="mb-3">Contacto</h5>
          <ul class="list-unstyled">
            <li class="mb-2"><font-awesome-icon :icon="['fas', 'envelope']" class="me-2" /> info@deconfianza.com</li>
            <li class="mb-2"><font-awesome-icon :icon="['fas', 'phone']" class="me-2" /> +54 9 261 123-4567</li>
            <li><font-awesome-icon :icon="['fas', 'map-marker-alt']" class="me-2" /> Mendoza, Argentina</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="bg-primary-dark py-3">
      <div class="container text-center">
        <small>&copy; {{ currentYear }} DE CONFIANZA. Todos los derechos reservados.</small>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';
const currentYear = ref(new Date().getFullYear());
</script>

<style scoped>
footer {
  background-color: var(--primary-color);
}

.bg-primary-dark {
  background-color: var(--primary-dark);
}

footer a {
  text-decoration: none;
  transition: opacity 0.3s;
}

footer a:hover {
  opacity: 0.8;
}

.social-icons a {
  font-size: 1.5rem;
  color: white;
}
</style>
