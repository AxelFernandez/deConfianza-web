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

    <!-- SECTORES destacados con scroll -->
    <section v-if="!isLandingOnlyMode" class="py-10">
      <div class="container-custom">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-neutral-800">Sectores destacados</h2>
          <span class="text-sm text-neutral-500">Desliza para ver más</span>
        </div>
        <div class="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-2">
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Electricistas</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Plomeros</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Carpinteros</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Jardinería</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Abogados</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Contadores</button>
          <button class="snap-start shrink-0 px-4 py-2 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium">Psicología</button>
        </div>
      </div>
    </section>

    <!-- TESTIMONIOS apilados -->
    <section v-if="!isLandingOnlyMode" class="section-padding bg-neutral-50">
      <div class="container-custom">
        <div class="mb-12">
          <h2 class="text-3xl font-display font-bold text-neutral-900">Lo que dicen de nosotros</h2>
          <p class="text-neutral-600 mt-2">Historias reales, confianza real.</p>
        </div>

        <div class="relative">
          <div class="grid md:grid-cols-3 gap-6">
            <div class="card rotate-[-1.5deg] translate-y-1">
              <p class="text-neutral-700">“Encontré un electricista en minutos y pude ver reseñas verificadas. Todo salió perfecto.”</p>
              <div class="mt-4 text-sm text-neutral-500">Lucía, Godoy Cruz</div>
            </div>
            <div class="card rotate-[1.2deg] -translate-y-1">
              <p class="text-neutral-700">“Como prestador, recibo consultas claras y reseñas que suman a mi reputación.”</p>
              <div class="mt-4 text-sm text-neutral-500">Julián, Guaymallén</div>
            </div>
            <div class="card rotate-[-0.8deg]">
              <p class="text-neutral-700">“Me gustó que sea simple, sin vueltas y con foco en la confianza.”</p>
              <div class="mt-4 text-sm text-neutral-500">Paula, Ciudad</div>
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
