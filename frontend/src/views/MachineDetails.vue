<template>
    <div class="machine-details">
      <div class="details-header">
        <h3>Details</h3>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="details-content">
        <div class="detail-row">
          <span class="label">Name</span>
          <span class="value">{{ machine.name }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Attached tool</span>
          <span class="value">{{ machine.attachedTool }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Tool wear</span>
          <span class="value" :class="getWearClass(machine.toolWear)">{{ machine.toolWear }}%</span>
        </div>
        <div class="detail-row">
          <span class="label">Last Maintenance</span>
          <span class="value">{{ machine.lastMaintenance }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Next Maintenance</span>
          <span class="value">{{ machine.nextMaintenance }}</span>
        </div>
      </div>
      <div class="details-actions">
        <button class="action-btn primary">Assign a tool</button>
        <button class="action-btn primary">Register a maintenance</button>
        <button class="action-btn secondary">View Maintenance History</button>
      </div>
      <div class="details-footer">
        <button class="footer-btn edit">Edit Machine</button>
        <button class="footer-btn delete">Delete Machine</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MachineDetails',
    props: {
      machine: {
        type: Object,
        required: true,
      },
    },
    methods: {
      getWearClass(wearLevel) {
        if (wearLevel >= 70) return 'wear-red';
        if (wearLevel >= 30) return 'wear-yellow';
        return 'wear-green';
      },
    },
  };
  </script>
  
  <style scoped>
  .machine-details {
    width: 300px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    padding: 20px;
    margin: 20px;
    position: absolute;
    right: 20px;
    top: 0;
    z-index: 100;
  }
  
  .details-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .details-header h3 {
    margin: 0;
    font-size: 1.5em;
    color: #333;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.2em;
    cursor: pointer;
    color: #666;
  }
  
  .close-btn:hover {
    color: #333;
  }
  
  .details-content {
    margin-bottom: 20px;
  }
  
  .detail-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .label {
    font-weight: 600;
    color: #666;
  }
  
  .value {
    color: #333;
  }
  
  .wear-green {
    color: #28a745;
    font-weight: bold;
  }
  
  .wear-yellow {
    color: #ffc107;
    font-weight: bold;
  }
  
  .wear-red {
    color: #dc3545;
    font-weight: bold;
  }
  
  .details-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .action-btn {
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
  }
  
  .action-btn.primary {
    background-color: #1a2a44;
    color: white;
  }
  
  .action-btn.primary:hover {
    background-color: #2c3e50;
  }
  
  .action-btn.secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .action-btn.secondary:hover {
    background-color: #5a6268;
  }
  
  .details-footer {
    display: flex;
    gap: 10px;
  }
  
  .footer-btn {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
  }
  
  .footer-btn.edit {
    background-color: #1a2a44;
    color: white;
  }
  
  .footer-btn.edit:hover {
    background-color: #2c3e50;
  }
  
  .footer-btn.delete {
    background-color: #dc3545;
    color: white;
  }
  
  .footer-btn.delete:hover {
    background-color: #c82333;
  }
  </style>