<template>
  <div class="sidebar" :class="{ hidden: !isVisible }">
    <button class="close-btn" @click="$emit('close')">✖</button>

    <!-- 👤 Показываем имя пользователя -->
    <div class="user-info" v-if="userFullName">
      👤 {{ userFullName }}
    </div>

    <nav>
      <ul>
        <li>
          <router-link to="/" :class="{ active: $route.name === 'Dashboard' }">
            Dashboard
          </router-link>
        </li>
        <li>
          <router-link to="/machines" :class="{ active: $route.name === 'Machines' }">
            Machines
          </router-link>
        </li>
        <li>
          <router-link to="/tools" :class="{ active: $route.name === 'Tools' }">
            Tools
          </router-link>
        </li>
        <!-- Только для Technician -->
        <li v-if="isTechnician">
          <router-link to="/register-maintenance" :class="{ active: $route.name === 'RegisterMaintenance' }">
            Register Maintenance
          </router-link>
        </li>
        <li>
          <router-link to="/maintenance-history" :class="{ active: $route.name === 'MaintenanceHistory' }">
            Maintenance history
          </router-link>
        </li>
      </ul>
    </nav>

    <button class="logout-button" @click="logout">
      Logout
    </button>
  </div>
</template>

<script>
import keycloak from '../keycloak'

export default {
  name: 'Sidebar',
  props: {
    isVisible: {
      type: Boolean,
      default: true,
    },
    userFullName: {
      type: String,
      default: ''
    }
  },
  computed: {
    isTechnician() {
      return keycloak.tokenParsed?.realm_access?.roles?.includes('Technician');
    }
  },
  methods: {
    logout() {
      keycloak.logout({
        redirectUri: window.location.origin
      });
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #1a2a44;
  padding: 20px;
  padding-top: 60px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  transition: transform 0.3s ease;
  z-index: 1000;
}

.sidebar.hidden {
  transform: translateX(-100%);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.user-info {
  font-size: 1.05em;
  color: #f0f0f0;
  padding: 10px 0;
  border-bottom: 1px solid #ffffff22;
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

a {
  text-decoration: none;
  color: #ffffff;
  font-size: 1.1em;
  display: block;
  padding: 10px 15px;
  border-radius: 4px;
}

a:hover {
  background-color: #2c3e50;
}

a.active {
  background-color: #e0e7ff;
  color: #1a2a44;
}

.logout-button {
  margin-top: 20px;
  width: 100%;
  padding: 10px;
  font-size: 1em;
  background-color: #3c4caf;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.logout-button:hover {
  background-color: #c0392b;
}
</style>
