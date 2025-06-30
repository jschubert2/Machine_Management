<template>
  <div class="tool-table-container">
    <h2>Tool Overview</h2>
    <div v-if="tools.length > 0">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>Wear Level</th>
            <th>Storage Location</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tool in paginatedTools" :key="tool.id">
            <td>{{ tool.id }}</td>
            <td>{{ tool.name }}</td>
            <td>{{ tool.type }}</td>
            <td :class="statusClass(tool.metrics?.[0]?.status)"> {{ tool.metrics?.[0]?.status || '-' }} </td>
            <td :class="wearLevelClass(tool.metrics?.[0]?.wear_level)"> {{ tool.metrics?.[0]?.wear_level ?? '-' }} </td>
            <td>{{ tool.metrics && tool.metrics[0] ? tool.metrics[0].storage_location : '-' }}</td>
            <td>{{ tool.created_at }}</td>
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
      <p>No data available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ToolTable',
  props: {
    tools: {
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
      return Math.ceil(this.tools.length / this.perPage);
    },
    paginatedTools() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.tools.slice(start, end);
    },
  },
  methods: {
  changePage(page) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  },
  statusClass(status) {
    switch (status?.toLowerCase()) {
      case 'attached':
        return 'status-attached';
      case 'scrapped':
        return 'status-scrapped';
      case 'storage':
      case 'in storage':
        return 'status-storage';
      default:
        return '';
    }
  },
  wearLevelClass(level) {
    return typeof level === 'number' && level > 80 ? 'wear-high' : '';
  }
}
};
</script>

<style scoped>
.tool-table-container {
  padding: 0 20px 20px 20px;
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
.status-attached {
  color: green;
  font-weight: bold;
}
.status-scrapped {
  color: red;
  font-weight: bold;
}
.status-storage {
  color: orange;
  font-weight: bold;
}
.wear-high {
  color: red;
  font-weight: bold;
}
h2 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.5em;
  color: #333;
}
</style>