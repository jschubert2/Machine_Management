<template>
  <div class="app">
    <Sidebar
      v-if="!isLoginPage"
      :isVisible="isSidebarVisible"
      :userFullName="userFullName"
      @close="isSidebarVisible = false"
    />
    <button
      v-if="!isLoginPage"
      class="open-btn"
      @click="isSidebarVisible = true"
    >
      ☰
    </button>

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
      isSidebarVisible: true,
      machines: [],
      tools: [],
      userFullName: '',
    }
  },
  computed: {
    isLoginPage() {
      return this.$route.name === 'Login'
    }
  },
  methods: {
    async handleImportData() {
      try {
        await axios.post('http://127.0.0.1:5000/import-csv')
        await this.fetchMachines()
        await this.fetchTools()
      } catch (error) {
        console.error('Import error:', error)
      }
    },
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

    async ensureUserExists() {
      const token = this.$keycloak?.tokenParsed;
      if (!token) return;

      const username = token.preferred_username;
      const first_name = token.given_name;
      const last_name = token.family_name;
      this.userFullName = `${first_name} ${last_name}`;
      console.log(`token username ${username}`);

      try {
        // 1. Получить всех пользователей
        const res = await axios.get('http://127.0.0.1:5000/users');
        const exists = res.data?.some(u => u.username === username);
        console.log(`exists ${exists}`);

        if (exists) {
          console.log(`ℹ️ User already exists: ${username}`);
          return;
        }

        // 2. Добавить, если не найден
        await axios.post('http://127.0.0.1:5000/user', {
          username,
          first_name: first_name,
          last_name: last_name
        }, {
          headers: {
            Authorization: `Bearer ${this.$keycloak.token}`
          }
        });

        console.log(`✅ Created new user: ${username}`);
      } catch (err) {
        console.error('❌ Failed to ensure user exists:', err);
      }
    }
  },
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
