<template>
  <div class="min-h-screen bg-green-50 flex items-center justify-center py-10">
    <div class="max-w-md w-full mx-4">
      <div class="bg-white rounded-2xl shadow-lg border border-green-200 p-8 text-center">
        <!-- Icono de éxito -->
        <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <font-awesome-icon :icon="['fas', 'check']" class="text-green-600 text-3xl" />
        </div>
        
        <!-- Título -->
        <h1 class="text-2xl font-bold text-gray-900 mb-2">¡Suscripción Activa!</h1>
        
        <!-- Mensaje -->
        <p class="text-gray-600 mb-6">
          Tu pago se procesó correctamente. Ya puedes acceder a todos los beneficios de tu plan.
        </p>
        
        <!-- Información del pago (si está disponible) -->
        <div v-if="paymentInfo" class="bg-green-50 rounded-lg p-4 mb-6 text-left">
          <h3 class="font-semibold text-green-900 mb-2">Detalles de la suscripción</h3>
          <div class="space-y-1 text-sm text-green-800">
            <div v-if="paymentInfo.plan">
              <span class="font-medium">Plan:</span> {{ paymentInfo.plan }}
            </div>
            <div v-if="paymentInfo.fecha_pago">
              <span class="font-medium">Fecha:</span> {{ formatDate(paymentInfo.fecha_pago) }}
            </div>
            <div v-if="paymentInfo.fecha_fin">
              <span class="font-medium">Válido hasta:</span> {{ formatDate(paymentInfo.fecha_fin) }}
            </div>
          </div>
        </div>
        
        <!-- Estado de carga -->
        <div v-if="loading" class="mb-6">
          <font-awesome-icon :icon="['fas', 'spinner']" class="text-green-600 text-xl animate-spin" />
          <p class="text-sm text-gray-600 mt-2">Verificando tu suscripción...</p>
        </div>
        
        <!-- Error -->
        <div v-if="error" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p class="text-yellow-800 text-sm">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="mr-2" />
            {{ error }}
          </p>
        </div>
        
        <!-- Botones de acción -->
        <div class="space-y-3">
          <button 
            @click="irAlDashboard" 
            class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-colors"
          >
            Ir al Dashboard
          </button>
          
          <button 
            @click="verMisSuscripciones" 
            class="w-full border border-green-600 text-green-600 hover:bg-green-50 font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Ver mis suscripciones
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
const error = ref('');
const paymentInfo = ref(null);

// Verificar pago al montar el componente
onMounted(async () => {
  const paymentId = route.query.payment_id;
  
  if (paymentId) {
    await verificarPago(paymentId);
  }
});

async function verificarPago(paymentId) {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await mercadoPagoService.verificarPago(paymentId);
    paymentInfo.value = response.data;
    
    if (!response.data.activa) {
      error.value = 'La suscripción aún no está activa. Puede tomar unos minutos en procesarse.';
    }
  } catch (err) {
    console.error('Error verificando pago:', err);
    error.value = 'No se pudo verificar el estado de tu suscripción, pero el pago fue exitoso.';
  } finally {
    loading.value = false;
  }
}

function irAlDashboard() {
  router.push('/prestador/dashboard');
}

function verMisSuscripciones() {
  // Implementar cuando tengamos la página de suscripciones
  router.push('/prestador/dashboard');
}

function formatDate(dateString) {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-AR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (e) {
    return dateString;
  }
}
</script>
