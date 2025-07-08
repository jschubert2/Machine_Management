<template>
  <div class="app">
    <!-- Sidebar is shown on all pages except the login view -->
    <Sidebar
      v-if="!isLoginPage"
      :isVisible="isSidebarVisible"
      :userFullName="userFullName"
      @close="isSidebarVisible = false"
    />

    <!-- Button to open the sidebar if it’s hidden -->
    <button
      v-if="!isLoginPage"
      class="open-btn"
      @click="isSidebarVisible = true"
    >
      ☰
    </button>

    <!-- Main content area; class is used to shift layout when sidebar is open -->
    <div class="content" :class="{ 'content-shifted': isSidebarVisible && !isLoginPage }">
      <router-view
        :machines="machines"
        :tools="tools"
        @import-data="handleImportData"
      />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import axios from 'axios'

export default {
  components: { Sidebar },

  data() {
    return {
      isSidebarVisible: true,  // Controls sidebar visibility
      machines: [],            // Machines fetched from backend
      tools: [],               // Tools fetched from backend
      userFullName: '',        // Full name of logged-in user (for sidebar display)
    }
  },

  computed: {
    // Determine if the current route is the login page
    isLoginPage() {
      return this.$route.name === 'Login'
    }
  },

  methods: {
    /**
     * Triggered by child component to import data via backend API.
     * Then refreshes machine and tool data.
     */
    async handleImportData() {
      try {
        await axios.post('http://127.0.0.1:5000/import-csv')
        await this.fetchMachines()
        await this.fetchTools()
      } catch (error) {
        console.error('Import error:', error)
      }
    },

    /**
     * Fetch machine list from backend.
     */
    async fetchMachines() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 50 },
        });
        this.machines = response.data.machines || [];
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    },

    /**
     * Fetch tool list from backend.
     */
    async fetchTools() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/tools', {
          params: { page: 1, per_page: 30 },
        });
        this.tools = response.data.tools || [];
      } catch (error) {
        console.error('Error fetching tools:', error);
      }
    },

    /**
     * Ensures that the currently authenticated user exists in the backend DB.
     * If not, it automatically registers them using token information.
     */
    async ensureUserExists() {
      const token = this.$keycloak?.tokenParsed;
      if (!token) return;

      const username = token.preferred_username;
      const first_name = token.given_name;
      const last_name = token.family_name;

      // Store full name for use in sidebar
      this.userFullName = `${first_name} ${last_name}`;

      try {
        // Step 1: Check if user already exists
        const res = await axios.get('http://127.0.0.1:5000/users');
        const exists = res.data?.some(u => u.username === username);

        if (exists) {
          console.log(`ℹ️ User already exists: ${username}`);
          return;
        }

        // Step 2: If not, create new user in backend
        await axios.post('http://127.0.0.1:5000/user', {
          username,
          first_name,
          last_name
        }, {
          headers: {
            Authorization: `Bearer ${this.$keycloak.token}` // 🔐 Token required for authentication
          }
        });

        console.log(`✅ Created new user: ${username}`);
      } catch (err) {
        console.error('❌ Failed to ensure user exists:', err);
      }
    }
  },

  /**
   * On mount:
   * - Ensure current user is registered in backend
   * - Fetch machine and tool data
   */
  mounted() {
    this.ensureUserExists();
    this.fetchMachines();
    this.fetchTools();
  }
}
</script>

<style scoped>
.app {
  display: flex;
  position: relative;
}

.open-btn {
  position: fixed;
  top: 10px;
  left: 10px;
  background: #1a2a44;
  color: white;
  border: none;
  font-size: 1.5rem;
  padding: 5px 10px;
  z-index: 1100;
  cursor: pointer;
}

.content {
  padding: 20px;
  width: 100%;
  transition: margin-left 0.3s ease;
}

.content-shifted {
  margin-left: 220px;
}
</style>
