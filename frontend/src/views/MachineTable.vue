<template>
    <div class="machine-table-container">
      <div class="machine-table">
        <h2>Machine View</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Category</th>
              <th>Status</th>
              <th>Manufacturer</th>
              <th>Date of creation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="machine in paginatedMachines" :key="machine.id" @click="selectMachine(machine)">
              <td>{{ machine.id }}</td>
              <td>{{ machine.name }}</td>
              <td>{{ machine.category }}</td>
              <td :class="getStatusClass(machine.status)">{{ machine.status }}</td>
              <td>{{ machine.manufacturer }}</td>
              <td>{{ machine.createdAt }}</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button :disabled="currentPage === 1" @click="currentPage--">Prev</button>
          <span>{{ currentPage }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
        </div>
      </div>
      <MachineDetails v-if="selectedMachine" :machine="selectedMachine" @close="selectedMachine = null" />
    </div>
  </template>
  
  <script>
  import MachineDetails from './MachineDetails.vue';
  
  export default {
    name: 'MachineTable',
    components: { MachineDetails },
    data() {
      return {
        machines: [
          { id: 183, name: 'Machine 1', category: 'Auto', status: 'Running', manufacturer: 'German AG', createdAt: '04.04.2025', attachedTool: 'Tool 1', toolWear: 81, lastMaintenance: '05.09.2024', nextMaintenance: '18.09.2025' },
          { id: 184, name: 'Machine 2', category: 'Manual', status: 'Offline', manufacturer: 'Musterman AG', createdAt: '04.04.2025', attachedTool: 'Tool 2', toolWear: 14, lastMaintenance: '10.08.2024', nextMaintenance: '10.08.2025' },
          { id: 185, name: 'Machine 3', category: 'Auto', status: 'Running', manufacturer: 'Fantastic Machines', createdAt: '04.04.2025', attachedTool: 'Tool 3', toolWear: 0, lastMaintenance: '15.07.2024', nextMaintenance: '15.07.2025' },
          { id: 186, name: 'Machine 4', category: 'Manual', status: 'Offline', manufacturer: 'German AG', createdAt: '04.04.2025', attachedTool: 'Tool 4', toolWear: 60, lastMaintenance: '20.06.2024', nextMaintenance: '20.06.2025' },
          { id: 187, name: 'Machine 5', category: 'Auto', status: 'Running', manufacturer: 'Musterman AG', createdAt: '04.04.2025', attachedTool: 'Tool 5', toolWear: 30, lastMaintenance: '25.05.2024', nextMaintenance: '25.05.2025' },
          { id: 188, name: 'Machine 6', category: 'Manual', status: 'Offline', manufacturer: 'Fantastic Machines', createdAt: '04.04.2025', attachedTool: 'Tool 6', toolWear: 70, lastMaintenance: '30.04.2024', nextMaintenance: '30.04.2025' },
          { id: 189, name: 'Machine 7', category: 'Auto', status: 'Running', manufacturer: 'German AG', createdAt: '04.04.2025', attachedTool: 'Tool 7', toolWear: 10, lastMaintenance: '05.03.2024', nextMaintenance: '05.03.2025' },
          { id: 190, name: 'Machine 8', category: 'Manual', status: 'Offline', manufacturer: 'Musterman AG', createdAt: '04.04.2025', attachedTool: 'Tool 8', toolWear: 0, lastMaintenance: '10.02.2024', nextMaintenance: '10.02.2025' },
          { id: 191, name: 'Machine 9', category: 'Auto', status: 'Running', manufacturer: 'Fantastic Machines', createdAt: '04.04.2025', attachedTool: 'Tool 9', toolWear: 5, lastMaintenance: '15.01.2024', nextMaintenance: '15.01.2025' },
          { id: 192, name: 'Machine 10', category: 'Manual', status: 'Offline', manufacturer: 'German AG', createdAt: '04.04.2025', attachedTool: 'Tool 10', toolWear: 0, lastMaintenance: '20.12.2023', nextMaintenance: '20.12.2024' },
          { id: 193, name: 'Machine 11', category: 'Auto', status: 'Running', manufacturer: 'Musterman AG', createdAt: '04.04.2025', attachedTool: 'Tool 11', toolWear: 82, lastMaintenance: '25.11.2023', nextMaintenance: '25.11.2024' },
          { id: 194, name: 'Machine 12', category: 'Manual', status: 'Offline', manufacturer: 'Fantastic Machines', createdAt: '04.04.2025', attachedTool: 'Tool 12', toolWear: 54, lastMaintenance: '30.10.2023', nextMaintenance: '30.10.2024' },
        ],
        currentPage: 1,
        itemsPerPage: 10,
        selectedMachine: null,
      };
    },
    computed: {
      paginatedMachines() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.machines.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.machines.length / this.itemsPerPage);
      },
    },
    methods: {
      getStatusClass(status) {
        return {
          'status-green': status === 'Running',
          'status-red': status === 'Offline',
        };
      },
      selectMachine(machine) {
        this.selectedMachine = machine;
      },
    },
  };
  </script>
  
  <style scoped>
  .machine-table-container {
    display: flex;
    position: relative;
  }
  
  .machine-table {
    flex: 1;
    padding: 20px;
  }
  
  h2 {
    color: #333;
    margin-bottom: 20px;
    font-size: 1.8em;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  th,
  td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #f4f4f4;
    color: #333;
    font-weight: 600;
  }
  
  tr:hover {
    background-color: #f9f9f9;
    cursor: pointer;
  }
  
  .status-green {
    color: #28a745;
    font-weight: bold;
  }
  
  .status-red {
    color: #dc3545;
    font-weight: bold;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .pagination button {
    padding: 8px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .pagination button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .pagination button:hover:not(:disabled) {
    background-color: #0056b3;
  }
  
  .pagination span {
    font-size: 1.1em;
    color: #333;
  }
  </style>