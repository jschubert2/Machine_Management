<template>
    <div class="tool-table">
      <h2>Overview of tools</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>Wear Level</th>
            <th>Date of creation</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tool in paginatedTools" :key="tool.id">
            <td>{{ tool.id }}</td>
            <td>{{ tool.name }}</td>
            <td>{{ tool.type }}</td>
            <td :class="getStatusClass(tool.status)">{{ tool.status }}</td>
            <td :class="getWearClass(tool.wearLevel)">{{ tool.wearLevel }}%</td>
            <td>{{ tool.createdAt }}</td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">Prev</button>
        <span>{{ currentPage }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ToolTable',
    data() {
      return {
        tools: [
          { id: 183, name: 'Tool 1', type: 'Cutter', status: 'Storage', wearLevel: 0, createdAt: '04.04.2025' },
          { id: 184, name: 'Tool 2', type: 'Nozzle', status: 'In Storage', wearLevel: 14, createdAt: '04.04.2025' },
          { id: 185, name: 'Tool 3', type: 'Saw', status: 'Storage', wearLevel: 0, createdAt: '04.04.2025' },
          { id: 186, name: 'Tool 4', type: 'Drill', status: 'Attached', wearLevel: 60, createdAt: '04.04.2025' },
          { id: 187, name: 'Tool 5', type: 'Cutter', status: 'Attached', wearLevel: 30, createdAt: '04.04.2025' },
          { id: 188, name: 'Tool 6', type: 'Nozzle', status: 'In Storage', wearLevel: 70, createdAt: '04.04.2025' },
          { id: 189, name: 'Tool 7', type: 'Saw', status: 'Attached', wearLevel: 10, createdAt: '04.04.2025' },
          { id: 190, name: 'Tool 8', type: 'Drill', status: 'Storage', wearLevel: 0, createdAt: '04.04.2025' },
          { id: 191, name: 'Tool 9', type: 'Cutter', status: 'Attached', wearLevel: 5, createdAt: '04.04.2025' },
          { id: 192, name: 'Tool 10', type: 'Nozzle', status: 'Storage', wearLevel: 0, createdAt: '04.04.2025' },
          { id: 193, name: 'Tool 11', type: 'Saw', status: 'Attached', wearLevel: 82, createdAt: '04.04.2025' },
          { id: 194, name: 'Tool 12', type: 'Drill', status: 'In Storage', wearLevel: 54, createdAt: '04.04.2025' },
          { id: 195, name: 'Tool 13', type: 'Saw', status: 'Storage', wearLevel: 0, createdAt: '04.04.2025' },
        ],
        currentPage: 1,
        itemsPerPage: 10,
      };
    },
    computed: {
      paginatedTools() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.tools.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.tools.length / this.itemsPerPage);
      },
    },
    methods: {
      getStatusClass(status) {
        return {
          'status-green': status === 'Attached',
          'status-yellow': status === 'In Storage',
          'status-red': status === 'Storage',
        };
      },
      getWearClass(wearLevel) {
        if (wearLevel >= 70) return 'wear-red';
        if (wearLevel >= 30) return 'wear-yellow';
        return 'wear-green';
      },
    },
  };
  </script>
  
  <style scoped>
  .tool-table {
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
  }
  
  .status-green {
    color: #28a745;
    font-weight: bold;
  }
  
  .status-yellow {
    color: #ffc107;
    font-weight: bold;
  }
  
  .status-red {
    color: #dc3545;
    font-weight: bold;
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