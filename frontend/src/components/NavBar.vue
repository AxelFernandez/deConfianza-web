<template>
  <nav class="bg-white shadow-sm border-b border-neutral-200 sticky top-0 z-50">
    <div class="container-custom">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link 
          to="/" 
          class="flex items-center space-x-2 text-xl font-display font-bold hover:opacity-80 transition-opacity"
        >
          <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">DC</span>
          </div>
          <span>DE CONFIANZA</span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link 
            to="/" 
            class="text-neutral-600 hover:text-primary-500 font-medium transition-colors"
            active-class="text-primary-600"
          >
            Inicio
          </router-link>
          
          <router-link 
            v-if="!isLandingOnlyMode"
            to="/buscar" 
            class="text-neutral-600 hover:text-primary-500 font-medium transition-colors"
            active-class="text-primary-600"
          >
            Buscar Servicios
          </router-link>
          
          <div v-if="!isLandingOnlyMode" class="flex items-center space-x-4">
            <router-link 
              to="/login" 
              class="text-neutral-600 hover:text-primary-500 font-medium transition-colors"
            >
              Iniciar Sesión
            </router-link>
            <router-link 
              to="/registrar" 
              class="btn-primary"
            >
              Registrarse
            </router-link>
          </div>
        </div>

        <!-- Mobile menu button -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden p-2 rounded-lg text-neutral-600 hover:text-primary-500 hover:bg-neutral-50 transition-colors"
          aria-label="Abrir menú"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <div v-if="isMobileMenuOpen" class="md:hidden py-4 border-t border-neutral-200 bg-white">
        <div class="flex flex-col space-y-4">
          <router-link 
            to="/" 
            @click="closeMobileMenu"
            class="text-neutral-600 hover:text-primary-500 font-medium py-2 transition-colors"
            active-class="text-primary-600"
          >
            Inicio
          </router-link>
          
          <router-link 
            v-if="!isLandingOnlyMode"
            to="/buscar" 
            @click="closeMobileMenu"
            class="text-neutral-600 hover:text-primary-500 font-medium py-2 transition-colors"
            active-class="text-primary-600"
          >
            Buscar Servicios
          </router-link>
          
          <div v-if="!isLandingOnlyMode" class="flex flex-col space-y-3 pt-4 border-t border-neutral-200">
            <router-link 
              to="/login" 
              @click="closeMobileMenu"
              class="text-neutral-600 hover:text-primary-500 font-medium py-2 transition-colors"
            >
              Iniciar Sesión
            </router-link>
            <router-link 
              to="/registrar" 
              @click="closeMobileMenu"
              class="btn-primary inline-block text-center"
            >
              Registrarse
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

const isLandingOnlyMode = ref(import.meta.env.VITE_LANDING_ONLY_MODE === 'true');
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};
</script>