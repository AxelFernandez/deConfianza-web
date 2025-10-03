<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div>
            <nav class="flex items-center space-x-2 text-sm text-gray-500 mb-1">
              <router-link to="/prestador/dashboard" class="hover:text-blue-600 transition-colors">
                Dashboard
              </router-link>
              <span v-if="breadcrumb">/</span>
              <span v-if="breadcrumb" class="text-gray-900 font-medium">{{ breadcrumb }}</span>
            </nav>
            <h1 class="text-2xl font-bold text-gray-900">{{ title }}</h1>
            <p v-if="subtitle" class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Plan badge -->
            <router-link 
              to="/planes"
              class="hidden sm:flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all shadow-sm group"
            >
              <font-awesome-icon :icon="['fas', 'crown']" class="mr-2" />
              <span class="font-medium">{{ planName || 'Plan' }}</span>
              <font-awesome-icon :icon="['fas', 'chevron-right']" class="ml-2 text-xs" />
            </router-link>
            
            <button 
              @click="$emit('logout')"
              class="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-2" />
              <span class="hidden sm:inline">Salir</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Sidebar -->
        <aside class="lg:col-span-1">
          <DashboardNavigation :dashboard-data="dashboardData" />
        </aside>

        <!-- Main Content -->
        <main class="lg:col-span-3">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import DashboardNavigation from './DashboardNavigation.vue';

defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: String,
  breadcrumb: String,
  planName: String,
  dashboardData: Object
});

defineEmits(['logout']);
</script>
