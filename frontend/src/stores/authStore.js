import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', () => {
  // Estado
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || null);
  const loading = ref(false);
  const error = ref(null);
  
  // Getters
  const isAuthenticated = computed(() => !!token.value);
  const isPrestador = computed(() => user.value?.perfil?.es_prestador || false);
  const fullName = computed(() => {
    if (!user.value) return '';
    return `${user.value.first_name} ${user.value.last_name}`.trim();
  });
  
  // Acciones
  async function login(credentials) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.login(credentials);
      token.value = response.data.token;
      localStorage.setItem('token', token.value);
      
      // Cargar datos del usuario
      await fetchUserProfile();
      
      return true;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al iniciar sesión';
      console.error('Error al iniciar sesión:', err);
      return false;
    } finally {
      loading.value = false;
    }
  }
  
  async function loginWithGoogle(credential) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.loginWithGoogle({ credential });
      
      // El backend devuelve 'access' en lugar de 'token'
      token.value = response.data.access || response.data.token;
      localStorage.setItem('token', token.value);
      
      // Guardar también el refresh token si existe
      if (response.data.refresh) {
        localStorage.setItem('refreshToken', response.data.refresh);
      }
      
      // Siempre cargar perfil completo desde el backend para obtener 'perfil.onboarding_completed'
      await fetchUserProfile();
      
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || err.response?.data?.message || 'Error al iniciar sesión con Google';
      console.error('Error al iniciar sesión con Google:', err);
      return false;
    } finally {
      loading.value = false;
    }
  }
  
  async function register(userData) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.register(userData);
      token.value = response.data.token;
      localStorage.setItem('token', token.value);
      
      // Cargar datos del usuario
      await fetchUserProfile();
      
      return true;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrarse';
      console.error('Error al registrarse:', err);
      return false;
    } finally {
      loading.value = false;
    }
  }
  
  async function logout() {
    try {
      // Solo intentar logout en el backend si hay token
      if (token.value) {
        await authService.logout();
      }
    } catch (err) {
      console.error('Error al cerrar sesión:', err);
    } finally {
      // Siempre limpiar datos locales
      token.value = null;
      user.value = null;
      localStorage.removeItem('token');
      router.push('/');
    }
  }
  
  async function fetchUserProfile() {
    if (!token.value) return null;
    
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.getCurrentUser();
      user.value = response.data;
      return user.value;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener perfil';
      console.error('Error al obtener perfil:', err);
      
      // Si hay error 401, hacer logout
      if (err.response?.status === 401) {
        logout();
      }
      
      return null;
    } finally {
      loading.value = false;
    }
  }
  
  async function updateProfile(userData) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.updateProfile(userData);
      user.value = response.data;
      return true;
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar perfil';
      console.error('Error al actualizar perfil:', err);
      return false;
    } finally {
      loading.value = false;
    }
  }
  
  // Inicializar: cargar perfil si hay token
  if (token.value) {
    fetchUserProfile();
  }
  
  return {
    // Estado
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    isPrestador,
    fullName,
    
    // Acciones
    login,
    loginWithGoogle,
    register,
    logout,
    fetchUserProfile,
    updateProfile
  };
});
