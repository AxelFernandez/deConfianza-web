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
            <!-- Usuario no autenticado -->
            <div v-if="!authStore.isAuthenticated" class="flex items-center space-x-4">
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
            
            <!-- Usuario autenticado -->
            <div v-else class="flex items-center space-x-4">
              <span class="text-neutral-600 text-sm">
                Hola, {{ authStore.fullName || authStore.user?.email }}
              </span>
              <div class="relative">
                <button 
                  @click="toggleUserMenu" 
                  class="flex items-center space-x-2 text-neutral-600 hover:text-primary-500 transition-colors"
                >
                  <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-primary-600 text-sm font-medium">
                      {{ (authStore.user?.first_name?.[0] || authStore.user?.email?.[0] || 'U').toUpperCase() }}
                    </span>
                  </div>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                <!-- Dropdown menu -->
                <div v-if="isUserMenuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-neutral-200 py-2 z-50">
                  <router-link 
                    v-if="authStore.isPrestador"
                    to="/prestador/dashboard" 
                    @click="closeUserMenu"
                    class="block px-4 py-2 text-sm text-neutral-700 hover:bg-neutral-50"
                  >
                    Dashboard
                  </router-link>
                  <button 
                    @click="logout" 
                    class="block w-full text-left px-4 py-2 text-sm text-neutral-700 hover:bg-neutral-50"
                  >
                    Cerrar Sesión
                  </button>
                </div>
              </div>
            </div>
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
            <!-- Usuario no autenticado - Mobile -->
            <div v-if="!authStore.isAuthenticated" class="flex flex-col space-y-3">
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
            
            <!-- Usuario autenticado - Mobile -->
            <div v-else class="flex flex-col space-y-3">
              <span class="text-neutral-600 text-sm py-2">
                Hola, {{ authStore.fullName || authStore.user?.email }}
              </span>
              <router-link 
                v-if="authStore.isPrestador"
                to="/prestador/dashboard" 
                @click="closeMobileMenu"
                class="text-neutral-600 hover:text-primary-500 font-medium py-2 transition-colors"
              >
                Dashboard
              </router-link>
              <button 
                @click="logout" 
                class="text-left text-neutral-600 hover:text-primary-500 font-medium py-2 transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const isLandingOnlyMode = ref(import.meta.env.VITE_LANDING_ONLY_MODE === 'true');
const isMobileMenuOpen = ref(false);
const isUserMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value;
};

const closeUserMenu = () => {
  isUserMenuOpen.value = false;
};

const logout = async () => {
  await authStore.logout();
  closeUserMenu();
  closeMobileMenu();
};
</script>