import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// Leer el feature flag del entorno
const isLandingOnlyMode = import.meta.env.VITE_LANDING_ONLY_MODE === 'true'

// Definir las rutas según el modo
const baseRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }
]

const fullRoutes = [
  ...baseRoutes,
  {
    path: '/buscar',
    name: 'search',
    component: () => import('../views/SearchView.vue')
  },
  {
    path: '/prestador/:id',
    name: 'prestador',
    component: () => import('../views/PrestadorView.vue')
  },
  {
    path: '/registrar',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: isLandingOnlyMode ? baseRoutes : fullRoutes
})

export default router
