import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import keycloak from './keycloak';

keycloak.init({ onLoad: 'login-required', checkLoginIframe: false }).then(authenticated => {
  if (!authenticated) {
    window.location.reload();
  } else {
    const app = createApp(App);
    app.use(router);
    app.use(store);
    app.config.globalProperties.$keycloak = keycloak;
    app.mount('#app');
  }
}).catch(err => {
  console.error('Keycloak init failed', err);
});

