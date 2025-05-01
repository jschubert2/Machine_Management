<template>
    <div class="sidebar" :class="{ hidden: !isVisible }">
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
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Sidebar',
    props: {
      isVisible: {
        type: Boolean,
        default: true,
      },
    },
  };
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
  }
  
  .sidebar.hidden {
    transform: translateX(-100%);
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
  </style>