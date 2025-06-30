<template>
  <div class="login-wrapper">
    <div class="login-left">
      <div class="login-box">
        <img :src="logo" alt="Logo" class="logo" />
        <h1 class="title">Machine Management System</h1>
        <p class="subtitle">Please log in with your organization account</p>
        <button class="login-button" @click="login">Sign in with Keycloak</button>
      </div>
    </div>
    <div class="login-right">
      <img :src="sideImage" alt="Visual" class="side-image" />
    </div>
  </div>
</template>

<script>
import logo from '../assets/logo.png'
import sideImage from '../assets/mainimage.png'
import keycloak from '../keycloak'

export default {
  name: 'LoginView',
  data() {
    return { logo, sideImage }
  },
  methods: {
    login() {
      keycloak.login()
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
  overflow: hidden;
}

.login-left, .login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  background: white;
  border-radius: 16px;
  padding: 3rem 2.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 420px;
  width: 100%;
}

.logo {
  height: 120px;
  margin-bottom: 1.5rem;
}

.title {
  margin: 0.5rem 0;
  font-size: 28px;
  font-weight: 700;
  color: #111;
}

.subtitle {
  color: #666;
  font-size: 15px;
  margin-bottom: 2rem;
}

.login-button {
  padding: 14px 28px;
  font-size: 16px;
  background-color: #3c4caf;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: #2f3e9e;
}

.side-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0;
}
</style>
