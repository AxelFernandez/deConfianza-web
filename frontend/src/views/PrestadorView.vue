<template>
  <div class="prestador-view">
    <section class="prestador-header bg-primary text-white py-4">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="mb-2">Nombre del Prestador</h1>
            <div class="d-flex align-items-center mb-3">
              <div class="rating me-2">
                <font-awesome-icon :icon="['fas', 'star']" class="text-warning" v-for="star in 5" :key="star" />
              </div>
              <span>(24 reseñas)</span>
            </div>
            <p class="mb-0">
              <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="me-2" />
              Mendoza, Argentina
            </p>
          </div>
          <div class="col-md-4 text-md-end mt-3 mt-md-0">
            <button class="btn btn-light me-2">
              <font-awesome-icon :icon="['fas', 'phone']" class="me-2" />
              Contactar
            </button>
            <button class="btn btn-outline-light">
              <font-awesome-icon :icon="['far', 'bookmark']" class="me-2" />
              Guardar
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="prestador-content py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8">
            <!-- Galería de imágenes -->
            <div class="card mb-4">
              <div class="card-body">
                <h2 class="h4 card-title mb-3">Galería</h2>
                <div class="row g-3">
                  <div class="col-4" v-for="i in 6" :key="i">
                    <img :src="`https://via.placeholder.com/150?text=Imagen+${i}`" 
                         alt="Imagen de servicio" class="img-fluid rounded">
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Descripción -->
            <div class="card mb-4">
              <div class="card-body">
                <h2 class="h4 card-title mb-3">Acerca de</h2>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate eu pharetra nec, 
                  mattis ac neque. Duis vulputate commodo lectus, ac blandit elit tincidunt id. Sed rhoncus, tortor sed 
                  eleifend tristique, tortor mauris molestie elit, et lacinia ipsum quam nec dui.
                </p>
              </div>
            </div>
            
            <!-- Servicios ofrecidos -->
            <div class="card mb-4">
              <div class="card-body">
                <h2 class="h4 card-title mb-3">Servicios ofrecidos</h2>
                <div class="row">
                  <div class="col-md-6">
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 1
                      </li>
                      <li class="mb-2">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 2
                      </li>
                      <li>
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 3
                      </li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <ul class="list-unstyled">
                      <li class="mb-2">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 4
                      </li>
                      <li class="mb-2">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 5
                      </li>
                      <li>
                        <font-awesome-icon :icon="['fas', 'check']" class="text-primary me-2" />
                        Servicio 6
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Reseñas -->
            <div class="card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h2 class="h4 card-title mb-0">Reseñas (24)</h2>
                  <button class="btn btn-primary btn-sm">Dejar reseña</button>
                </div>
                
                <!-- Reseñas individuales -->
                <div v-for="i in 3" :key="i" class="review mb-3">
                  <div class="d-flex align-items-center mb-1">
                    <strong class="me-2">Usuario Ejemplo {{ i }}</strong>
                    <div class="rating">
                      <font-awesome-icon :icon="['fas', 'star']" class="text-warning" v-for="star in 5" :key="star" />
                    </div>
                    <small class="text-muted ms-auto">hace {{ i }} días</small>
                  </div>
                  <p class="mb-0">
                    Excelente servicio, muy profesional y puntual. Recomendado al 100%.
                  </p>
                  <hr v-if="i < 3">
                </div>
                
                <a href="#" class="d-block text-center">Ver todas las reseñas</a>
              </div>
            </div>
          </div>
          
          <div class="col-lg-4 mt-4 mt-lg-0">
            <!-- Tarjeta de información de contacto -->
            <div class="card mb-4 sticky-top" style="top: 20px">
              <div class="card-body">
                <h3 class="h5 card-title mb-3">Información de contacto</h3>
                <ul class="list-unstyled">
                  <li class="mb-3">
                    <font-awesome-icon :icon="['fas', 'phone']" class="me-2 text-primary" />
                    +54 9 261 123-4567
                  </li>
                  <li class="mb-3">
                    <font-awesome-icon :icon="['fas', 'envelope']" class="me-2 text-primary" />
                    contacto@ejemplo.com
                  </li>
                  <li class="mb-3">
                    <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="me-2 text-primary" />
                    Mendoza, Argentina
                  </li>
                  <li>
                    <font-awesome-icon :icon="['fas', 'clock']" class="me-2 text-primary" />
                    Lunes a Viernes: 9:00 - 18:00
                  </li>
                </ul>
                
                <div class="social-links mt-3">
                  <a href="#" class="me-2 text-primary">
                    <font-awesome-icon :icon="['fab', 'facebook']" size="lg" />
                  </a>
                  <a href="#" class="me-2 text-primary">
                    <font-awesome-icon :icon="['fab', 'instagram']" size="lg" />
                  </a>
                  <a href="#" class="text-primary">
                    <font-awesome-icon :icon="['fab', 'whatsapp']" size="lg" />
                  </a>
                </div>
                
                <div class="mt-4">
                  <button class="btn btn-primary w-100 mb-2">
                    <font-awesome-icon :icon="['fas', 'phone']" class="me-2" />
                    Contactar ahora
                  </button>
                  <button class="btn btn-outline-primary w-100">
                    <font-awesome-icon :icon="['fas', 'share-alt']" class="me-2" />
                    Compartir
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
// El ID del prestador se puede obtener con route.params.id
</script>

<style scoped>
.rating {
  color: #ffc107;
}

.prestador-header {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.social-links a {
  text-decoration: none;
  transition: opacity 0.3s;
}

.social-links a:hover {
  opacity: 0.8;
}
</style>
