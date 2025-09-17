<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero bg-primary text-white">
      <div class="container py-5">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <h1 class="display-4 fw-bold mb-3">Encuentra servicios de confianza</h1>
            <p class="lead mb-4">Conectamos a clientes con los mejores profesionales y oficios cerca de ti. Servicios verificados y recomendados por la comunidad.</p>
            <div class="d-flex flex-wrap gap-2">
              <router-link to="/buscar" class="btn btn-light btn-lg px-4 text-primary fw-semibold">
                <font-awesome-icon :icon="['fas', 'search']" class="me-2" />
                Buscar servicios
              </router-link>
              <router-link to="/registrar" class="btn btn-outline-light btn-lg px-4 fw-semibold">
                <font-awesome-icon :icon="['fas', 'user-plus']" class="me-2" />
                Ofrece tus servicios
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <img src="../assets/hero-image.svg" alt="Servicios de confianza" class="img-fluid hero-image">
          </div>
        </div>
      </div>
      <div class="wave-divider">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 100" preserveAspectRatio="none">
          <path fill="#ffffff" fill-opacity="1" d="M0,32L60,42.7C120,53,240,75,360,74.7C480,75,600,53,720,48C840,43,960,53,1080,58.7C1200,64,1320,64,1380,64L1440,64L1440,100L1380,100C1320,100,1200,100,1080,100C960,100,840,100,720,100C600,100,480,100,360,100C240,100,120,100,60,100L0,100Z"></path>
        </svg>
      </div>
    </section>

    <!-- Categorías Section -->
    <section class="categories py-5">
      <div class="container">
        <h2 class="text-center mb-5 fw-bold">Explora por categoría</h2>
        <div class="row g-4">
          <div class="col-md-6">
            <div class="category-card h-100 p-4 rounded shadow-sm d-flex flex-column align-items-center text-center">
              <div class="category-icon mb-3 rounded-circle d-flex align-items-center justify-content-center">
                <font-awesome-icon :icon="['fas', 'tools']" class="fa-2x text-primary" />
              </div>
              <h3 class="h4 mb-3">Oficios</h3>
              <p class="mb-4">Plomeros, carpinteros, electricistas, jardineros y más servicios para tu hogar.</p>
              <router-link to="/buscar?categoria=oficios" class="btn btn-outline-primary mt-auto">Ver oficios</router-link>
            </div>
          </div>
          <div class="col-md-6">
            <div class="category-card h-100 p-4 rounded shadow-sm d-flex flex-column align-items-center text-center">
              <div class="category-icon mb-3 rounded-circle d-flex align-items-center justify-content-center">
                <font-awesome-icon :icon="['fas', 'briefcase']" class="fa-2x text-primary" />
              </div>
              <h3 class="h4 mb-3">Profesionales</h3>
              <p class="mb-4">Abogados, contadores, médicos, psicólogos y otros servicios profesionales.</p>
              <router-link to="/buscar?categoria=profesionales" class="btn btn-outline-primary mt-auto">Ver profesionales</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Cómo Funciona Section -->
    <section class="how-it-works py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5 fw-bold">¿Cómo funciona?</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number mb-3">1</div>
              <h3 class="h4 mb-3">Busca</h3>
              <p>Encuentra los servicios que necesitas filtrando por ubicación, categoría y especialidad.</p>
              <div class="step-icon">
                <font-awesome-icon :icon="['fas', 'search']" class="fa-3x text-primary" />
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number mb-3">2</div>
              <h3 class="h4 mb-3">Compara</h3>
              <p>Revisa perfiles, calificaciones y reseñas para elegir al prestador que más te convenga.</p>
              <div class="step-icon">
                <font-awesome-icon :icon="['fas', 'star']" class="fa-3x text-primary" />
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number mb-3">3</div>
              <h3 class="h4 mb-3">Contacta</h3>
              <p>Comunícate directamente con el prestador y coordina el servicio que necesitas.</p>
              <div class="step-icon">
                <font-awesome-icon :icon="['fas', 'handshake']" class="fa-3x text-primary" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Join Us -->
    <section class="join-us py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <h2 class="fw-bold mb-4">¿Ofreces servicios? ¡Únete a nuestra plataforma!</h2>
            <p class="mb-4">Expande tu negocio llegando a más clientes. Regístrate como prestador de servicios y aprovecha los beneficios de formar parte de DE CONFIANZA.</p>
            <div class="benefits mb-4">
              <div class="benefit d-flex align-items-start mb-3">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-primary me-2 mt-1" />
                <div>
                  <h4 class="h5 mb-1">Mayor visibilidad</h4>
                  <p class="mb-0">Destaca tu negocio en las búsquedas de servicios.</p>
                </div>
              </div>
              <div class="benefit d-flex align-items-start mb-3">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-primary me-2 mt-1" />
                <div>
                  <h4 class="h5 mb-1">Nuevos clientes</h4>
                  <p class="mb-0">Conecta con personas que buscan exactamente tus servicios.</p>
                </div>
              </div>
              <div class="benefit d-flex align-items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-primary me-2 mt-1" />
                <div>
                  <h4 class="h5 mb-1">Gestión sencilla</h4>
                  <p class="mb-0">Administra tu perfil, reseñas y comunicación fácilmente.</p>
                </div>
              </div>
            </div>
            <router-link to="/registrar" class="btn btn-primary btn-lg">Comenzar ahora</router-link>
          </div>
          <div class="col-lg-6 text-center">
            <img src="../assets/join-us-image.svg" alt="Únete a DE CONFIANZA" class="img-fluid join-image">
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
// Código Vue si es necesario
</script>

<style scoped>
.hero {
  position: relative;
  padding: 4rem 0 8rem;
  overflow: hidden;
}

.wave-divider {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  line-height: 0;
}

.wave-divider svg {
  width: 100%;
  height: 100px;
}

.category-icon {
  width: 80px;
  height: 80px;
  background-color: var(--gray-100);
  transition: transform 0.3s ease;
}

.category-card {
  border: 1px solid var(--gray-200);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.category-card:hover .category-icon {
  transform: scale(1.1);
}

.step-number {
  width: 40px;
  height: 40px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-weight: bold;
  font-size: 1.2rem;
}

.step-card {
  background-color: white;
  border-radius: 8px;
  height: 100%;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.step-card:hover {
  transform: translateY(-5px);
}

.step-icon {
  margin-top: 1.5rem;
  opacity: 0.8;
}

.join-image, .hero-image {
  max-height: 400px;
}

@media (max-width: 991.98px) {
  .hero {
    padding-bottom: 6rem;
  }
}
</style>
