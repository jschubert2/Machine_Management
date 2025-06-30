import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import keycloak from './keycloak'

keycloak.init({
  onLoad: 'check-sso',
  silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
  pkceMethod: 'S256' 
}).then(authenticated => {
  const app = createApp(App)
  app.use(router)
  app.use(store)
  app.config.globalProperties.$keycloak = keycloak
  app.mount('#app')
})
