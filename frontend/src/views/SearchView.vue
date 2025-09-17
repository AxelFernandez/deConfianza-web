<template>
  <div class="search-view">
    <section class="search-header bg-primary text-white py-4">
      <div class="container">
        <h1 class="mb-4">Buscar servicios</h1>
        <div class="search-form bg-white p-4 rounded shadow">
          <div class="row g-3">
            <div class="col-md-3">
              <label for="location" class="form-label text-dark">Ubicación</label>
              <input type="text" class="form-control" id="location" placeholder="Ciudad, provincia...">
            </div>
            <div class="col-md-3">
              <label for="category" class="form-label text-dark">Categoría</label>
              <select class="form-select" id="category">
                <option value="">Todas las categorías</option>
                <option value="1">Oficios</option>
                <option value="2">Profesiones</option>
              </select>
            </div>
            <div class="col-md-3">
              <label for="service" class="form-label text-dark">Servicio</label>
              <select class="form-select" id="service">
                <option value="">Todos los servicios</option>
                <option value="1">Plomería</option>
                <option value="2">Electricidad</option>
                <option value="3">Abogacía</option>
                <option value="4">Psicología</option>
              </select>
            </div>
            <div class="col-md-3 d-flex align-items-end">
              <button type="submit" class="btn btn-primary w-100">
                <font-awesome-icon :icon="['fas', 'search']" class="me-2" />
                Buscar
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="search-results py-5">
      <div class="container">
        <div class="row mb-4">
          <div class="col-md-8">
            <h2 class="mb-0">Resultados de búsqueda</h2>
          </div>
          <div class="col-md-4">
            <div class="d-flex justify-content-md-end">
              <select class="form-select w-auto">
                <option value="relevance">Relevancia</option>
                <option value="rating">Mejor calificación</option>
                <option value="newest">Más recientes</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Resultados ficticios para la maqueta -->
        <div class="row g-4">
          <div class="col-md-6 col-lg-4" v-for="i in 6" :key="i">
            <div class="card h-100 service-card">
              <div class="card-body">
                <h5 class="card-title">Servicio de ejemplo {{ i }}</h5>
                <p class="card-text mb-1">
                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="me-2 text-primary" />
                  Mendoza, Argentina
                </p>
                <p class="card-text mb-3">
                  <span class="badge bg-light text-primary me-2">Plomería</span>
                  <span class="badge bg-light text-primary">Oficios</span>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                  <div class="rating">
                    <font-awesome-icon :icon="['fas', 'star']" class="text-warning" v-for="star in 5" :key="star" />
                  </div>
                  <router-link :to="'/prestador/' + i" class="btn btn-outline-primary btn-sm">
                    Ver detalles
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paginación -->
        <nav class="mt-5">
          <ul class="pagination justify-content-center">
            <li class="page-item disabled">
              <a class="page-link" href="#" tabindex="-1" aria-disabled="true">
                <font-awesome-icon :icon="['fas', 'chevron-left']" />
              </a>
            </li>
            <li class="page-item active"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
            <li class="page-item">
              <a class="page-link" href="#">
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </section>
  </div>
</template>

<script setup>
// Código Vue si es necesario
</script>

<style scoped>
.search-header {
  position: relative;
}

.search-form {
  border-radius: 8px;
}

.service-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--gray-200);
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.rating {
  font-size: 0.9rem;
}
</style>
