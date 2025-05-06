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
            <td>{{ machine.created_at }}</td>
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
import axios from 'axios';
import MachineDetails from './MachineDetails.vue';

export default {
name: 'MachineTable',
components: { MachineDetails },
data() {
  return {
    machines: [],
    currentPage: 1,
    itemsPerPage: 10,
    selectedMachine: null,
    totalPages: 1
  };
},
computed: {
  paginatedMachines() {
    return this.machines;
  }
},
methods: {
  async fetchMachines() {
    try {
      const response = await axios.get('http://localhost:5000/machines', {
        params: {
          page: this.currentPage,
          per_page: this.itemsPerPage
        }
      });
      this.machines = response.data.machines;
      this.totalPages = response.data.pages;
    } catch (error) {
      console.error('Failed to fetch machines:', error);
    }
  },
  getStatusClass(status) {
    return {
      'status-green': status === 'Running',
      'status-red': status === 'Offline',
    };
  },
  selectMachine(machine) {
    this.selectedMachine = machine;
  }
},
watch: {
  currentPage() {
    this.fetchMachines();
  }
},
mounted() {
  this.fetchMachines();
}
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