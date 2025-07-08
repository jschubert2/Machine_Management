<template>
  <!-- Sidebar navigation component, shown based on visibility flag -->
  <div class="sidebar" :class="{ hidden: !isVisible }">
    <!-- Button to close sidebar, emits 'close' event to parent -->
    <button class="close-btn" @click="$emit('close')">✖</button>

    <!-- User identity section, only shown if full name is available -->
    <div class="user-info" v-if="userFullName">
      👤 {{ userFullName }}
    </div>

    <!-- Application navigation links -->
    <nav>
      <ul>
        <!-- Link to Dashboard view -->
        <li>
          <router-link to="/" :class="{ active: $route.name === 'Dashboard' }">
            Dashboard
          </router-link>
        </li>

        <!-- Link to Machines table -->
        <li>
          <router-link to="/machines" :class="{ active: $route.name === 'Machines' }">
            Machines
          </router-link>
        </li>

        <!-- Link to Tools table -->
        <li>
          <router-link to="/tools" :class="{ active: $route.name === 'Tools' }">
            Tools
          </router-link>
        </li>

        <!-- Technician-specific functionality -->
        <li v-if="isTechnician">
          <router-link to="/register-maintenance" :class="{ active: $route.name === 'RegisterMaintenance' }">
            Register Maintenance
          </router-link>
        </li>

        <!-- Accessible by both Admins and Technicians -->
        <li>
          <router-link to="/maintenance-history" :class="{ active: $route.name === 'MaintenanceHistory' }">
            Maintenance History
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Logout action -->
    <button class="logout-button" @click="logout">
      Logout
    </button>
  </div>
</template>

<script>
// Import Keycloak instance for authentication control
import keycloak from '../keycloak'

/**
 * Sidebar Component
 *
 * Displays the application's main navigation menu depending on user role.
 * Visible on all views except the login screen. Role-specific options are conditionally rendered.
 *
 * Props:
 * @prop {Boolean} isVisible - Controls whether the sidebar is shown or hidden
 * @prop {String} userFullName - Full name of the currently logged-in user
 *
 * Computed:
 * @computed isTechnician - Checks if the logged-in user has the 'Technician' role
 *
 * Methods:
 * @method logout - Triggers Keycloak logout and redirects to the application root
 */
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
    /**
     * Determines whether the current user holds the 'Technician' role.
     * This affects visibility of technician-specific menu items.
     *
     * @return {Boolean} true if user is a Technician, false otherwise
     */
    isTechnician() {
      return keycloak.tokenParsed?.realm_access?.roles?.includes('Technician');
    }
  },
  methods: {
    /**
     * Logs the user out via Keycloak and redirects to the application's base URL.
     * Used to end session and return to login.
     */
    logout() {
      keycloak.logout({
        redirectUri: window.location.origin
      });
    }
  }
}
</script>

<style scoped>
/* Styles for the sidebar container */
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
