import axios from 'axios';

// Crear instancia de axios con configuración base
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000
});

// Interceptor para manejar tokens de autenticación
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Interceptor para manejar respuestas y renovar tokens
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && error.response?.data?.code === 'token_not_valid') {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8001/api'}/usuarios/token/refresh/`, {
            refresh: refreshToken
          });
          const newToken = response.data.access;
          localStorage.setItem('token', newToken);
          // Reintentar la petición original
          error.config.headers.Authorization = `Bearer ${newToken}`;
          return apiClient.request(error.config);
        } catch (refreshError) {
          // Si falla el refresh, logout
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Servicios API para prestadores
export const prestadorService = {
  // Obtener un prestador por ID
  getPrestador(id) {
    return apiClient.get(`/servicios/prestadores/${id}/`);
  },
  
  // Obtener lista de prestadores con filtros opcionales
  getPrestadores(params = {}) {
    return apiClient.get('/servicios/prestadores/', { params });
  },
  
  // Obtener reseñas de un prestador
  getResenasPrestador(id) {
    return apiClient.get(`/servicios/prestadores/${id}/resenas/`);
  },
  
  // Enviar una nueva reseña
  crearResena(prestadorId, data) {
    return apiClient.post(`/servicios/prestadores/${prestadorId}/resenas/`, data);
  },
  
  // Registrar visualización de perfil
  registrarVisualizacion(prestadorId) {
    return apiClient.post('/servicios/registrar-visualizacion/', { prestador_id: prestadorId });
  }
};

// Servicios API para autenticación
export const authService = {
  login(credentials) {
    return apiClient.post('/usuarios/login/', credentials);
  },
  
  loginWithGoogle(tokenData) {
    // Enviamos credential devuelto por Google One Tap / OAuth
    return apiClient.post('/usuarios/login/google/', tokenData);
  },
  
  register(userData) {
    return apiClient.post('/usuarios/register/', userData);
  },
  
  logout() {
    return apiClient.post('/usuarios/logout/');
  },
  
  getCurrentUser() {
    return apiClient.get('/usuarios/me/');
  },
  
  updateProfile(userData) {
    return apiClient.put('/usuarios/update_me/', userData);
  },
  
  changePassword(passwordData) {
    return apiClient.post('/usuarios/change-password/', passwordData);
  },
};

// Servicios para onboarding / planes
export const onboardingService = {
  getPlanes() {
    return apiClient.get('/usuarios/planes/');
  },
  completeOnboarding(data) {
    return apiClient.post('/usuarios/complete_onboarding/', data);
  }
};

// Servicios API para búsqueda
export const searchService = {
  buscar(params) {
    return apiClient.get('/servicios/prestadores/', { params });
  }
};

// Catálogo (categorías, rubros, servicios)
export const catalogService = {
  getCategorias() {
    return apiClient.get('/servicios/categorias/');
  },
  getRubros(params = {}) {
    return apiClient.get('/servicios/rubros/', { params });
  },
  getServicios(params = {}) {
    return apiClient.get('/servicios/servicios/', { params });
  },
};

// Servicios del prestador
export const misServiciosService = {
  getMisServicios() {
    return apiClient.get('/servicios/mis-servicios/');
  },
  createServicio(data) {
    return apiClient.post('/servicios/mis-servicios/', data);
  },
  updateServicio(id, data) {
    return apiClient.put(`/servicios/mis-servicios/${id}/`, data);
  },
  deleteServicio(id) {
    return apiClient.delete(`/servicios/mis-servicios/${id}/`);
  },
  
  getDashboard() {
    return apiClient.get('/servicios/dashboard/');
  },
  
  getMisResenas() {
    return apiClient.get('/servicios/mis-resenas/');
  },
  
  registrarVisualizacion(prestadorId) {
    return apiClient.post('/servicios/registrar-visualizacion/', { prestador_id: prestadorId });
  }
};

export const mercadoPagoService = {
  crearPreferencia(planCode) {
    return apiClient.post('/suscripciones/crear-preferencia/', { plan: planCode });
  },
  verificarPago(paymentId) {
    return apiClient.get(`/suscripciones/verificar-pago/${paymentId}/`);
  },
  misSuscripciones() {
    return apiClient.get('/suscripciones/mis-suscripciones/');
  },
};

export default apiClient;
