<template>
  <div class="app">
    
    <button class="open-btn" @click="isSidebarVisible = true">☰</button>

    <Sidebar :isVisible="isSidebarVisible" @close="isSidebarVisible = false" />

    <div class="content" :class="{ 'content-shifted': isSidebarVisible }">
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
    }
  },
  methods: {
    async handleImportData() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/import-csv')
        console.log('Import response:', response.data)

        const machinesResponse = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 50 },
        })
        this.machines = machinesResponse.data.machines

        const toolsResponse = await axios.get('http://127.0.0.1:5000/tools', {
          params: { page: 1, per_page: 30 },
        })
        this.tools = toolsResponse.data.tools || []
      } catch (error) {
        console.error('Error importing data:', error)
      }
    },
  },
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
