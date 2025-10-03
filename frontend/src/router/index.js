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
  },
  {
    path: '/planes',
    name: 'planes',
    component: () => import('../views/PlanesView.vue')
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: () => import('../views/OnboardingView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/prestador/dashboard',
    name: 'prestadorDashboard',
    component: () => import('../views/prestador/DashboardView.vue'),
    meta: { requiresAuth: true, requiresPrestador: true }
  },
  {
    path: '/prestador/perfil',
    name: 'prestadorPerfil',
    component: () => import('../views/prestador/PerfilView.vue'),
    meta: { requiresAuth: true, requiresPrestador: true }
  },
  {
    path: '/prestador/configuracion',
    name: 'prestadorConfiguracion',
    component: () => import('../views/prestador/ConfiguracionView.vue'),
    meta: { requiresAuth: true, requiresPrestador: true }
  },
  {
    path: '/prestador/servicios',
    name: 'prestadorServicios',
    component: () => import('../views/prestador/ServiciosView.vue'),
    meta: { requiresAuth: true, requiresPrestador: true }
  },
  {
    path: '/prestador/resenas',
    name: 'prestadorResenas',
    component: () => import('../views/prestador/ResenasView.vue'),
    meta: { requiresAuth: true, requiresPrestador: true }
  },
  // Rutas de suscripción MercadoPago
  {
    path: '/suscripcion/exito',
    name: 'suscripcionExito',
    component: () => import('../views/SuscripcionExito.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/suscripcion/cancelado',
    name: 'suscripcionCancelado',
    component: () => import('../views/SuscripcionCancelado.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/suscripcion/pendiente',
    name: 'suscripcionPendiente',
    component: () => import('../views/SuscripcionPendiente.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: isLandingOnlyMode ? baseRoutes : fullRoutes,
  scrollBehavior(to, from, savedPosition) {
    // Si el navegador tiene una posición guardada (ej: botón atrás), usarla
    if (savedPosition) {
      return savedPosition
    }
    
    // Si hay un hash en la URL, scroll a ese elemento
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    
    // Casos especiales donde podríamos NO querer resetear el scroll
    const keepScrollRoutes = [
      // Agregar rutas aquí si en el futuro queremos mantener el scroll
      // Ejemplo: 'prestadorServicios' -> 'prestadorPerfil' (tabs del dashboard)
    ]
    
    // Si estamos navegando entre rutas que deberían mantener scroll
    if (keepScrollRoutes.includes(to.name) && keepScrollRoutes.includes(from.name)) {
      return {} // No cambiar scroll
    }
    
    // Para todas las otras navegaciones, ir al top de la página con animación suave
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          top: 0,
          left: 0,
          behavior: 'smooth'
        })
      }, 100) // Pequeño delay para asegurar que el componente se haya montado
    })
  }
})

// Protección de rutas
router.beforeEach(async (to, from, next) => {
  // Verificar token en localStorage
  const token = localStorage.getItem('token');
  const isAuthenticated = !!token;

  // Si requiere auth y no está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
    return;
  }

  // Si está autenticado, verificar onboarding desde Pinia
  if (isAuthenticated) {
    // Importar dinámicamente el store para evitar problemas de orden
    const { useAuthStore } = await import('../stores/authStore');
    const authStore = useAuthStore();
    
    // Si no tenemos user data, intentar cargarla
    if (!authStore.user && token) {
      try {
        await authStore.fetchUserProfile();
      } catch (error) {
        console.error('Error al cargar perfil:', error);
        // Si hay error, limpiar token y redirigir a login
        localStorage.removeItem('token');
        next({ name: 'login' });
        return;
      }
    }

    const perfil = authStore.user?.perfil;
    const onboardingCompleted = perfil?.onboarding_completed;
    const isPrestador = !!perfil?.es_prestador;

    // Forzar onboarding si no está completado
    if (onboardingCompleted === false && to.name !== 'onboarding') {
      next({ name: 'onboarding' });
      return;
    }

    // Si requiere ser prestador y no lo es
    if (to.meta.requiresPrestador && !isPrestador) {
      next({ name: 'home' });
      return;
    }
  }

  next();
})

export default router
