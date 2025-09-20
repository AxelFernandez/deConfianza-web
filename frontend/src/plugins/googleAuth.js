// Configuración para Google OAuth / Google Identity Services
let googleAuth = null; // accounts.id
let googleClient = null; // oauth2 token client (no usado para ID token)
let loaded = false;

export const initGoogleAuth = (clientId) => {
  return new Promise((resolve, reject) => {
    // Evitar cargar dos veces
    if (loaded || (typeof window !== 'undefined' && window.google && window.google.accounts)) {
      loaded = true;
      return resolve(true);
    }

    // Cargar la API de Google
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      try {
        // Marcar como cargado
        loaded = true;
        resolve(true);
      } catch (error) {
        reject(error);
      }
    };
    script.onerror = (error) => {
      reject(error);
    };
    document.head.appendChild(script);
  });
};

export const renderGoogleButton = (elementId) => {
  if (!loaded) {
    console.error('Google Identity Services no cargado');
    return;
  }
  if (!googleAuth) {
    console.warn('Inicializando accounts.id por primera vez');
  }
  if (window.google && window.google.accounts?.id) {
    window.google.accounts.id.renderButton(
      document.getElementById(elementId),
      {
        theme: 'outline',
        size: 'large',
        width: '100%',
        text: 'signin_with',
        shape: 'rectangular',
        logo_alignment: 'left',
        locale: 'es_ES',
      }
    );
  }
};

// Obtener ID token (credential) mediante One Tap / Sign In With Google
export const getIdCredential = (clientId) => {
  if (!loaded) {
    return Promise.reject('Google Identity Services no cargado');
  }
  return new Promise((resolve, reject) => {
    try {
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: (response) => {
          if (!response || !response.credential) {
            reject('No se obtuvo credential de Google');
          } else {
            resolve(response);
          }
        },
        auto_select: false,
        cancel_on_tap_outside: true,
        use_fedcm_for_prompt: false,
      });
      // Mostrar prompt
      window.google.accounts.id.prompt((notification) => {
        // Si no se muestra el prompt o el usuario lo omite, no rechazamos aquí
      });
    } catch (error) {
      reject(error);
    }
  });
};

export default {
  install: (app, options) => {
    const clientId = options?.clientId || import.meta.env.VITE_GOOGLE_CLIENT_ID;
    
    if (!clientId) {
      console.error('Google Client ID no está configurado');
      return;
    }
    
    // Inicializar Google Auth al cargar la aplicación
    initGoogleAuth(clientId).catch(error => {
      console.error('Error al inicializar Google Auth:', error);
    });
    
    // Exponer funciones globalmente
    app.config.globalProperties.$googleAuth = {
      renderButton: renderGoogleButton,
      getIdCredential: () => getIdCredential(clientId)
    };
  }
};


