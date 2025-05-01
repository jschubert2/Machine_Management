<template>
    <div class="dashboard">
      <h2>Dashboard</h2>
      <div class="metrics">
        <div class="metric">
          <h3>OEE</h3>
          <p>85%</p>
        </div>
        <div class="metric">
          <h3>Availability</h3>
          <p>90%</p>
        </div>
        <div class="metric">
          <h3>Performance</h3>
          <p>80%</p>
        </div>
        <div class="metric">
          <h3>Quality</h3>
          <p>95%</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardView',
  };
  </script>
  
  <style scoped>
  .dashboard {
    padding: 20px;
  }
  
  h2 {
    color: #333;
    margin-bottom: 20px;
    font-size: 1.8em;
  }
  
  .metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }
  
  .metric {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .metric h3 {
    margin: 0;
    font-size: 1.2em;
    color: #1a2a44;
  }
  
  .metric p {
    margin: 10px 0 0;
    font-size: 1.8em;
    font-weight: bold;
    color: #007bff;
  }
  </style>