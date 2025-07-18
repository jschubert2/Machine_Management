<template>
  <div class="tool-table-container">
    <div class="header-row">
      <h2>Tool Overview</h2>
    </div>

    <div class="filters">
      <!-- Filter tools by type -->
      <select v-model="filterType">
        <option value="">All Types</option>
        <option v-for="type in toolTypes" :key="type">{{ type }}</option>
      </select>

      <!-- Filter tools by status -->
      <select v-model="filterStatus">
        <option value="">All Statuses</option>
        <option>Attached</option>
        <option>Scrapped</option>
        <option>Storage</option>
      </select>

      <!-- Filter tools by creation date -->
      <div class="date-range">
        <label>Created At Period:</label>
        <input type="date" v-model="filterStartDate" />
        <span>to</span>
        <input type="date" v-model="filterEndDate" />
      </div>

      <!-- Sort by wear level -->
      <button @click="toggleSortOrder">
        Sort Wear Level {{ sortOrder === 'asc' ? '↑' : '↓' }}
      </button>
    </div>

    <div v-if="filteredAndSortedTools.length > 0">
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

            <!-- Apply color-coded class based on status -->
            <td :class="statusClass(tool.metrics?.[0]?.status)">
              {{ tool.metrics?.[0]?.status || '-' }}
            </td>

            <!-- Highlight tools with wear > 80% -->
            <td :class="wearLevelClass(tool.metrics?.[0]?.wear_level)">
              {{ tool.metrics?.[0]?.wear_level ?? '-' }}
            </td>

            <td>{{ tool.metrics?.[0]?.storage_location || '-' }}</td>
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
      currentPage: 1,         // Current pagination page
      perPage: 30,            // Items per page
      isLoading: false,
      filterType: '',         // Dropdown filter
      filterStatus: '',
      filterStartDate: '',
      filterEndDate: '',
      sortOrder: 'asc',       // Wear level sort order
    };
  },
  computed: {
    // Extracts unique tool types from the dataset
    toolTypes() {
      const types = this.tools.map(t => t.type).filter(Boolean);
      return [...new Set(types)];
    },

    // Filters and sorts tools based on user inputs
    filteredAndSortedTools() {
      return this.tools
        .filter(t => {
          const status = t.metrics?.[0]?.status?.toLowerCase();

          const typeMatch = this.filterType === '' || t.type === this.filterType;

          const statusMatch =
            this.filterStatus === '' ||
            status === this.filterStatus.toLowerCase() ||
            (status === 'in storage' && this.filterStatus.toLowerCase() === 'storage'); // normalize "in storage"

          const date = new Date(t.created_at);
          const start = this.filterStartDate ? new Date(this.filterStartDate) : null;
          const end = this.filterEndDate ? new Date(this.filterEndDate) : null;
          const dateMatch = (!start || date >= start) && (!end || date <= end);

          return typeMatch && statusMatch && dateMatch;
        })
        .sort((a, b) => {
          const aWear = a.metrics?.[0]?.wear_level ?? 0;
          const bWear = b.metrics?.[0]?.wear_level ?? 0;
          return this.sortOrder === 'asc' ? aWear - bWear : bWear - aWear;
        });
    },

    // Returns only the current page’s slice
    paginatedTools() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredAndSortedTools.slice(start, start + this.perPage);
    },

    // Calculates number of total pages
    totalPages() {
      return Math.ceil(this.filteredAndSortedTools.length / this.perPage);
    },
  },
  methods: {
    // Update current page if in bounds
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },

    // Toggle between ascending and descending wear level sort
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    },

    // Returns class name based on tool status
    statusClass(status) {
      switch (status?.toLowerCase()) {
        case 'attached': return 'status-attached';
        case 'scrapped': return 'status-scrapped';
        case 'storage':
        case 'in storage': return 'status-storage';
        default: return '';
      }
    },

    // Highlights high-wear tools
    wearLevelClass(level) {
      return typeof level === 'number' && level > 80 ? 'wear-high' : '';
    },
  },
};
</script>

<style scoped>
.tool-table-container {
  padding: 0 20px 20px 20px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.header-row h2 {
  margin: 0;
  font-size: 1.4em;
  color: #333;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
  align-items: center;
}

.filters select,
.filters input {
  padding: 6px 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
}

.date-range input[type="date"] {
  padding: 5px 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
}

th, td {
  padding: 9px 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
  justify-content: center;
}

.pagination span {
  font-size: 1em;
  color: #333;
}

.no-data-message {
  text-align: center;
  padding: 15px;
  color: #666;
}

.status-attached { color: green; font-weight: bold; }
.status-scrapped { color: red; font-weight: bold; }
.status-storage { color: orange; font-weight: bold; }
.wear-high { color: red; font-weight: bold; }

h2 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.5em;
  color: #333;
}
</style>
