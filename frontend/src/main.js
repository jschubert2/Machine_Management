import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import keycloak from './keycloak'  // 🔐 Keycloak instance initialized separately

// Initialize Keycloak before mounting the Vue app
keycloak.init({
  onLoad: 'check-sso',  // ⚙️ Attempt SSO silently (without redirect unless needed)
  silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html', // 🪞 Hidden iframe used for silent SSO
  pkceMethod: 'S256' // 🔒 Modern and secure PKCE method used for authorization code flow
}).then(authenticated => {
  // 💡 Only mount the app after Keycloak is initialized
  const app = createApp(App)
  app.use(router)         // Register Vue Router
  app.use(store)          // Register Vuex Store

  // Inject Keycloak instance globally (accessible via this.$keycloak)
  app.config.globalProperties.$keycloak = keycloak

  app.mount('#app')       // Mount the app to the DOM
})
