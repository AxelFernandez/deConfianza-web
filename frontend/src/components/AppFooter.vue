<template>
  <footer class="bg-gradient-to-br from-primary-500 to-primary-600 text-white">
    <div class="container-custom section-padding">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Company Info -->
        <div class="lg:col-span-1">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">DC</span>
            </div>
            <h3 class="text-xl font-display font-bold">DE CONFIANZA</h3>
          </div>
          <p class="text-primary-100 mb-6 leading-relaxed">
            Conectando profesionales y oficios de confianza con quienes los necesitan.
          </p>
          <div class="flex space-x-4">
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors duration-200"
              aria-label="Facebook"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors duration-200"
              aria-label="Instagram"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.014 5.367 18.647.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.477-3.34-1.262-.48-.422-.86-.926-1.118-1.488-.257-.562-.386-1.174-.386-1.836 0-.662.129-1.274.386-1.836.258-.562.639-1.066 1.118-1.488.892-.785 2.043-1.262 3.34-1.262s2.448.477 3.34 1.262c.48.422.86.926 1.118 1.488.257.562.386 1.174.386 1.836 0 .662-.129 1.274-.386 1.836-.258.562-.639 1.066-1.118 1.488-.892.785-2.043 1.262-3.34 1.262zm7.598-9.02h-3.23V5.99h3.23v1.977z"/>
              </svg>
            </a>
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors duration-200"
              aria-label="LinkedIn"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Links -->
        <div v-if="!isLandingOnlyMode">
          <h4 class="text-lg font-semibold mb-4">Enlaces</h4>
          <ul class="space-y-3">
            <li>
              <router-link 
                to="/" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Inicio
              </router-link>
            </li>
            <li>
              <router-link 
                to="/buscar" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Buscar
              </router-link>
            </li>
            <li>
              <router-link 
                to="/registrar" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Registrarse
              </router-link>
            </li>
            <li>
              <router-link 
                to="/login" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Ingresar
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Categories -->
        <div v-if="!isLandingOnlyMode">
          <h4 class="text-lg font-semibold mb-4">Categorías</h4>
          <ul class="space-y-3">
            <li>
              <a 
                href="#" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Oficios
              </a>
            </li>
            <li>
              <a 
                href="#" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Profesiones
              </a>
            </li>
            <li>
              <a 
                href="#" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Servicios a domicilio
              </a>
            </li>
            <li>
              <a 
                href="#" 
                class="text-primary-100 hover:text-white transition-colors duration-200"
              >
                Servicios online
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Contacto</h4>
          <ul class="space-y-3">
            <li class="flex items-center space-x-3">
              <svg class="w-5 h-5 text-primary-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span class="text-primary-100">info@deconfianza.com</span>
            </li>
            <li class="flex items-center space-x-3">
              <svg class="w-5 h-5 text-primary-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <span class="text-primary-100">+54 9 261 123-4567</span>
            </li>
            <li class="flex items-center space-x-3">
              <svg class="w-5 h-5 text-primary-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="text-primary-100">Mendoza, Argentina</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Copyright -->
    <div class="bg-primary-700 py-4">
      <div class="container-custom">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <p class="text-primary-200 text-sm">
            &copy; {{ currentYear }} DE CONFIANZA. Todos los derechos reservados.
          </p>
          <div class="flex space-x-6 text-sm">
            <a href="#" class="text-primary-200 hover:text-white transition-colors duration-200">
              Términos de Servicio
            </a>
            <a href="#" class="text-primary-200 hover:text-white transition-colors duration-200">
              Privacidad
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';

const currentYear = ref(new Date().getFullYear());
const isLandingOnlyMode = ref(import.meta.env.VITE_LANDING_ONLY_MODE === 'true');
</script>