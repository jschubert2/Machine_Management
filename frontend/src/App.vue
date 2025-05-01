<template>
  <div class="app">
    <button class="toggle-sidebar" @click="toggleSidebar">
      <i :class="isSidebarVisible ? 'fas fa-times' : 'fas fa-bars'"></i>
    </button>

    <Sidebar :is-visible="isSidebarVisible" />

    <div class="content" :class="{ 'content-shifted': isSidebarVisible }">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';

export default {
  components: { Sidebar },
  data() {
    return {
      isSidebarVisible: true,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
  },
};
</script>

<style>
.app {
  display: flex;
  position: relative;
}

.toggle-sidebar {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000;
  padding: 6px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.0em; 
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px; 
  height: 32px;
}

.toggle-sidebar:hover {
  background-color: #0056b3;
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