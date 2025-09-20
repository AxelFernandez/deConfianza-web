<template>
  <div class="min-h-screen bg-red-50 flex items-center justify-center py-10">
    <div class="max-w-md w-full mx-4">
      <div class="bg-white rounded-2xl shadow-lg border border-red-200 p-8 text-center">
        <!-- Icono de cancelación -->
        <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <font-awesome-icon :icon="['fas', 'times']" class="text-red-600 text-3xl" />
        </div>
        
        <!-- Título -->
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Pago Cancelado</h1>
        
        <!-- Mensaje -->
        <p class="text-gray-600 mb-6">
          El pago fue cancelado o no se pudo procesar. No se realizó ningún cargo a tu cuenta.
        </p>
        
        <!-- Información adicional -->
        <div class="bg-red-50 rounded-lg p-4 mb-6 text-left">
          <h3 class="font-semibold text-red-900 mb-2">¿Qué puedes hacer?</h3>
          <ul class="space-y-2 text-sm text-red-800">
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-red-600 mr-2 mt-0.5 text-xs" />
              <span>Intentar el pago nuevamente</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-red-600 mr-2 mt-0.5 text-xs" />
              <span>Elegir un método de pago diferente</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-red-600 mr-2 mt-0.5 text-xs" />
              <span>Contactar con soporte si el problema persiste</span>
            </li>
          </ul>
        </div>
        
        <!-- Botones de acción -->
        <div class="space-y-3">
          <button 
            @click="intentarNuevamente" 
            class="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-3 px-6 rounded-lg transition-colors"
          >
            Intentar Nuevamente
          </button>
          
          <button 
            @click="volverAlOnboarding" 
            class="w-full border border-red-600 text-red-600 hover:bg-red-50 font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Volver al Onboarding
          </button>
          
          <button 
            @click="irAlInicio" 
            class="w-full text-gray-600 hover:text-gray-800 font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Ir al Inicio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

function intentarNuevamente() {
  // Volver al onboarding en el paso de resumen
  router.push('/onboarding');
}

function volverAlOnboarding() {
  router.push('/onboarding');
}

function irAlInicio() {
  router.push('/');
}
</script>
