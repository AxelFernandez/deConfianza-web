import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Importar iconos solid
import { 
  faSearch, faMapMarkerAlt, faThLarge, faTools, 
  faChevronDown, faChevronLeft, faChevronRight, faStar, 
  faUser, faBriefcase, faPhone, faEnvelope, faClock, 
  faCheck, faBookmark, faShareAlt, faSpinner, faUserPlus,
  faSignInAlt, faEye, faEyeSlash, faLock
} from '@fortawesome/free-solid-svg-icons'

// Importar iconos regular
import { faBookmark as farBookmark } from '@fortawesome/free-regular-svg-icons'

// Importar iconos de marcas
import { faFacebook, faGoogle, faInstagram, faWhatsapp } from '@fortawesome/free-brands-svg-icons'

// Importar plugin de Google Auth
import GoogleAuth from './plugins/googleAuth'

// Agregar iconos a la biblioteca
library.add(
  // Solid
  faSearch, faMapMarkerAlt, faThLarge, faTools, 
  faChevronDown, faChevronLeft, faChevronRight, faStar,
  faUser, faBriefcase, faPhone, faEnvelope, faClock,
  faCheck, faBookmark, faShareAlt, faSpinner, faUserPlus,
  faSignInAlt, faEye, faEyeSlash, faLock,
  
  // Regular
  farBookmark,
  
  // Brands
  faFacebook, faGoogle, faInstagram, faWhatsapp
)

import './assets/main.css'

const app = createApp(App)

// Registrar el componente FontAwesomeIcon globalmente
app.component('font-awesome-icon', FontAwesomeIcon)

// Usar plugins
app.use(createPinia())
app.use(router)
app.use(GoogleAuth, {
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
})

app.mount('#app')