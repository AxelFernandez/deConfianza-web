<template>
  <div class="home">
    <!-- HERO con banda diagonal y emblema -->
    <section class="relative overflow-hidden">
      <!-- Banda diagonal -->
      <div class="absolute -top-32 -left-20 w-[140%] h-96 bg-primary-50 rotate-[-6deg] shadow-[0_40px_120px_-60px_rgba(59,130,246,0.5)]"></div>

      <div class="relative container-custom pt-24 lg:pt-32 pb-16">
        <div class="grid lg:grid-cols-[1.1fr_0.9fr] gap-12 items-center">
          <!-- Texto principal -->
          <div>
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-display font-bold text-neutral-900 leading-tight">
              Servicios en los que podés <span class="text-primary-600">confiar</span>
            </h1>
            <p class="mt-6 text-lg md:text-xl text-neutral-600 max-w-2xl">
              Conectamos a clientes con los mejores profesionales y oficios cerca de ti. Servicios verificados y recomendados por la comunidad.
            </p>

          

            <!-- CTAs -->
            <div class="mt-8 flex flex-col sm:flex-row gap-4">
              <router-link v-if="!isLandingOnlyMode" to="/buscar" class="btn-primary inline-flex items-center justify-center">
                Buscar servicios
              </router-link>
              <router-link v-if="!isLandingOnlyMode" to="/registrar" class="btn-outline inline-flex items-center justify-center">
                Ofrecer mis servicios
              </router-link>
            </div>
          </div>

          <!-- Emblema + Handshake en tarjeta -->
          <div class="relative">
          
            <!-- Tarjeta handshake -->
            <div class="relative inline-block isolate group">
              <div class="pointer-events-none absolute -inset-10 bg-gradient-to-br from-primary-200/60 to-primary-100/40 blur-3xl rounded-[2.5rem]"></div>
              <div class="relative bg-white rounded-[1.75rem] border border-neutral-200/70 shadow-2xl p-6 lg:p-8 ring-1 ring-primary-200/30 will-change-transform transition-transform duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:-translate-y-2 group-hover:shadow-3xl group-hover:ring-2 group-hover:ring-primary-200/60 animate-float">
                <img src="../assets/conexiones.png" alt="Apretón de manos - confianza" class="w-56 max-w-md mx-auto lg:max-w-lg drop-shadow-xl select-none" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BUSCAR POR: Oficios o Profesión -->
    <section v-if="!isLandingOnlyMode" class="section-padding bg-white">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-display font-bold text-neutral-900 mb-3">
            Explora por categoría
          </h2>
          <p class="text-neutral-600">Elegí cómo querés buscar: por oficios o por profesión.</p>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
          <!-- Oficios -->
          <div class="card card-hover group">
            <div class="text-center">
              <div class="w-20 h-20 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                <svg class="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 8.172V5L8 4z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-neutral-900 mb-3">Oficios</h3>
              <p class="text-neutral-600 mb-6">Plomería, electricidad, carpintería, jardinería y más.</p>
              <router-link to="/buscar?categoria=oficios" class="btn-outline w-full">Ver oficios</router-link>
            </div>
          </div>

          <!-- Profesionales -->
          <div class="card card-hover group">
            <div class="text-center">
              <div class="w-20 h-20 bg-gradient-to-br from-accent-100 to-accent-200 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                <svg class="w-10 h-10 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-neutral-900 mb-3">Profesionales</h3>
              <p class="text-neutral-600 mb-6">Abogacía, contabilidad, medicina, psicología y más.</p>
              <router-link to="/buscar?categoria=profesionales" class="btn-outline w-full">Ver profesionales</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ¿Cómo funciona? Pasos -->
    <section v-if="!isLandingOnlyMode" class="section-padding bg-neutral-50">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-display font-bold text-neutral-900 mb-3">¿Cómo funciona?</h2>
          <p class="text-neutral-600">En tres pasos, resolvés lo que necesitás.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center group">
            <div class="w-16 h-16 bg-primary-500 text-white rounded-full grid place-items-center mx-auto mb-6 font-bold text-xl group-hover:scale-110 transition-transform">1</div>
            <div class="card">
              <h3 class="text-xl font-semibold mb-2">Busca</h3>
              <p class="text-neutral-600">Filtrá por ubicación, categoría y especialidad para encontrar el servicio ideal.</p>
            </div>
          </div>
          <div class="text-center group">
            <div class="w-16 h-16 bg-accent-500 text-white rounded-full grid place-items-center mx-auto mb-6 font-bold text-xl group-hover:scale-110 transition-transform">2</div>
            <div class="card">
              <h3 class="text-xl font-semibold mb-2">Compara</h3>
              <p class="text-neutral-600">Leé reseñas verificadas y mirá calificaciones para decidir con confianza.</p>
            </div>
          </div>
          <div class="text-center group">
            <div class="w-16 h-16 bg-primary-600 text-white rounded-full grid place-items-center mx-auto mb-6 font-bold text-xl group-hover:scale-110 transition-transform">3</div>
            <div class="card">
              <h3 class="text-xl font-semibold mb-2">Contacta</h3>
              <p class="text-neutral-600">Conectá directo con el prestador y coordiná el servicio sin intermediarios.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Únete a la plataforma -->
    <section v-if="!isLandingOnlyMode" class="section-padding bg-white">
      <div class="container-custom">
        <div class="grid lg:grid-cols-2 gap-10 items-center">
          <div>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-neutral-900 mb-4">¿Ofrecés servicios? ¡Unite ahora!</h2>
            <p class="text-neutral-600 mb-6">Potenciá tu presencia con un perfil verificado, reseñas reales y herramientas para crecer.</p>
            <ul class="space-y-3 mb-8">
              <li class="flex items-start gap-3"><span class="mt-1 w-5 h-5 rounded-full bg-primary-100 grid place-items-center text-primary-600">✓</span><span>Mayor visibilidad en búsquedas</span></li>
              <li class="flex items-start gap-3"><span class="mt-1 w-5 h-5 rounded-full bg-primary-100 grid place-items-center text-primary-600">✓</span><span>Clientes con intención real</span></li>
              <li class="flex items-start gap-3"><span class="mt-1 w-5 h-5 rounded-full bg-primary-100 grid place-items-center text-primary-600">✓</span><span>Gestión simple de tu reputación</span></li>
            </ul>
            <router-link to="/registrar" class="btn-secondary">Crear mi perfil</router-link>
          </div>
          <div class="text-center">
            <div class="relative inline-block">
              <div class="absolute inset-0 bg-gradient-to-br from-accent-200 to-primary-200 rounded-3xl transform -rotate-6 opacity-20"></div>
              <img src="../assets/join-us-image.svg" alt="Únete a DE CONFIANZA" class="relative w-full max-w-md mx-auto lg:max-w-lg" />
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- CTA FINAL / LANDING ONLY -->
    <section class="section-padding">
      <div class="container-custom">
        <div class="bg-white border border-neutral-200 rounded-2xl p-8 lg:p-10 shadow-sm grid lg:grid-cols-[1.2fr_0.8fr] gap-8 items-center">
          <div>
            <h3 class="text-2xl md:text-3xl font-display font-semibold text-neutral-900">Empezá a construir confianza hoy</h3>
            <p class="mt-3 text-neutral-600">Sumate como prestador o encontrá profesionales verificados. Todo en un solo lugar.</p>
          </div>
          <div class="flex justify-start lg:justify-end gap-4">
            <router-link v-if="!isLandingOnlyMode" to="/buscar" class="btn-primary">Buscar servicios</router-link>
            <router-link v-if="!isLandingOnlyMode" to="/registrar" class="btn-outline">Registrarme</router-link>
            <button v-if="isLandingOnlyMode" class="btn-primary">Proximamente</button>
          </div>
        </div>
      </div>
    </section>
  </div>
 </template>

<script setup>
import { ref } from 'vue';

const isLandingOnlyMode = ref(import.meta.env.VITE_LANDING_ONLY_MODE === 'true');
</script>
