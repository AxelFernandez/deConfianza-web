<template>
  <div class="min-h-screen bg-yellow-50 flex items-center justify-center py-10">
    <div class="max-w-md w-full mx-4">
      <div class="bg-white rounded-2xl shadow-lg border border-yellow-200 p-8 text-center">
        <!-- Icono de pendiente -->
        <div class="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <font-awesome-icon :icon="['fas', 'clock']" class="text-yellow-600 text-3xl" />
        </div>
        
        <!-- Título -->
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Pago Pendiente</h1>
        
        <!-- Mensaje -->
        <p class="text-gray-600 mb-6">
          Tu pago está siendo procesado. Te notificaremos cuando se complete la transacción.
        </p>
        
        <!-- Información del pago (si está disponible) -->
        <div v-if="paymentInfo" class="bg-yellow-50 rounded-lg p-4 mb-6 text-left">
          <h3 class="font-semibold text-yellow-900 mb-2">Detalles del pago</h3>
          <div class="space-y-1 text-sm text-yellow-800">
            <div v-if="paymentInfo.plan">
              <span class="font-medium">Plan:</span> {{ paymentInfo.plan }}
            </div>
            <div v-if="paymentInfo.estado">
              <span class="font-medium">Estado:</span> {{ paymentInfo.estado }}
            </div>
          </div>
        </div>
        
        <!-- Información adicional -->
        <div class="bg-blue-50 rounded-lg p-4 mb-6 text-left">
          <h3 class="font-semibold text-blue-900 mb-2">¿Qué sigue?</h3>
          <ul class="space-y-2 text-sm text-blue-800">
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'info-circle']" class="text-blue-600 mr-2 mt-0.5 text-xs" />
              <span>El procesamiento puede tomar unos minutos</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'envelope']" class="text-blue-600 mr-2 mt-0.5 text-xs" />
              <span>Te enviaremos un email cuando se complete</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'refresh']" class="text-blue-600 mr-2 mt-0.5 text-xs" />
              <span>Puedes verificar el estado en tu dashboard</span>
            </li>
          </ul>
        </div>
        
        <!-- Estado de carga -->
        <div v-if="loading" class="mb-6">
          <font-awesome-icon :icon="['fas', 'spinner']" class="text-yellow-600 text-xl animate-spin" />
          <p class="text-sm text-gray-600 mt-2">Verificando estado del pago...</p>
        </div>
        
        <!-- Botones de acción -->
        <div class="space-y-3">
          <button 
            @click="verificarEstado" 
            :disabled="loading"
            class="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50"
          >
            <font-awesome-icon v-if="loading" :icon="['fas', 'spinner']" class="animate-spin mr-2" />
            Verificar Estado
          </button>
          
          <button 
            @click="irAlDashboard" 
            class="w-full border border-yellow-600 text-yellow-600 hover:bg-yellow-50 font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Ir al Dashboard
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
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { mercadoPagoService } from '../services/api';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// Estado
const loading = ref(false);
const paymentInfo = ref(null);

// Verificar pago al montar el componente
onMounted(async () => {
  const paymentId = route.query.payment_id;
  
  if (paymentId) {
    await verificarEstado(paymentId);
  }
});

async function verificarEstado(paymentId = null) {
  const id = paymentId || route.query.payment_id;
  
  if (!id) {
    console.warn('No se encontró payment_id en la URL');
    return;
  }
  
  loading.value = true;
  
  try {
    const response = await mercadoPagoService.verificarPago(id);
    paymentInfo.value = response.data;
    
    // Si el pago fue aprobado, redirigir a la página de éxito
    if (response.data.estado === 'approved') {
      router.replace(`/suscripcion/exito?payment_id=${id}`);
    }
    // Si fue rechazado, redirigir a la página de cancelado
    else if (['rejected', 'cancelled'].includes(response.data.estado)) {
      router.replace(`/suscripcion/cancelado?payment_id=${id}`);
    }
  } catch (error) {
    console.error('Error verificando pago:', error);
  } finally {
    loading.value = false;
  }
}

function irAlDashboard() {
  router.push('/prestador/dashboard');
}

function irAlInicio() {
  router.push('/');
}
</script>
