<template>
  <div class="machine-table-container">
    <h2>Machine Overview</h2>
    <div class="button-group">
      <button @click="$emit('import-data')" :disabled="isLoading">Import Data</button>
    </div>
    <div v-if="machines.length > 0">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Category</th>
            <th>Status</th>
            <th>Manufacturer</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="machine in paginatedMachines" :key="machine.id">
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
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
    <div v-else class="no-data-message">
      <p>No data available. Please click "Import Data" to load machines.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MachineTable',
  props: {
    machines: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      currentPage: 1,
      perPage: 30,
      isLoading: false,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.machines.length / this.perPage);
    },
    paginatedMachines() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.machines.slice(start, end);
    },
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    getStatusClass(status) {
      return {
        'status-green': status === 'Running',
        'status-red': status === 'Offline',
      };
    },
  },
};
</script>

<style scoped>
.machine-table-container {
  padding: 20px;
}
.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  border: 1px solid #ddd;
}
.status-green {
  color: green;
}
.status-red {
  color: red;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  justify-content: center;
}
.pagination span {
  font-size: 1em;
  color: #333;
}
.no-data-message {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>