// src/keycloak.js
import Keycloak from 'keycloak-js';

// 🔐 Create and configure Keycloak instance with required parameters
const keycloak = new Keycloak({
  url: 'http://localhost:8080',         // URL of the Keycloak auth server
  realm: 'machine_management',          // Realm configured in Keycloak
  clientId: 'frontend',                 // Client ID registered for this frontend app
});

export default keycloak;
