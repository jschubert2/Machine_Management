<template>
  <div class="machine-list">
    <h2>Machines</h2>
    <button @click="importData" :disabled="machines.length > 0">Import</button>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Group</th>
          <th>Status</th>
          <th>Created At</th>
          <th>Category</th>
          <th>Manufacturer</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="machine in paginatedMachines" :key="machine.id" @click="openMachineDetails(machine.id)">
          <td>{{ machine.id }}</td>
          <td>{{ machine.name }}</td>
          <td>{{ machine.group }}</td>
          <td>{{ machine.status }}</td>
          <td>{{ machine.created_at || 'N/A' }}</td>
          <td>{{ machine.category || 'N/A' }}</td>
          <td>{{ machine.manufacturer || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button @click="previousPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
    <machine-details
      ref="machineDetailsModal"
      :machine="selectedMachine"
      @close="closeMachineDetails"
      @update:machine="updateMachine"
    />
  </div>
</template>

<script>
import { useStore } from 'vuex';
import { computed, ref } from 'vue';
import MachineDetails from '../views/MachineDetails.vue';

export default {
  name: 'MachineTable',
  components: { MachineDetails },
  setup() {
    const store = useStore();
    const machines = computed(() => store.state.machines);
    const selectedMachine = ref(null);
    const machineDetailsModal = ref(null);
    const currentPage = ref(1);
    const itemsPerPage = 30;

    const openMachineDetails = (machineId) => {
      console.log('Opening details for machineId:', machineId); // Отладка
      const machine = machines.value.find(m => m.id === machineId);
      if (machine) {
        selectedMachine.value = { ...machine, attached_tool: null, tool_wear: null }; // Изначально пусто
        if (machineDetailsModal.value) {
          machineDetailsModal.value.open();
          console.log('Modal opened'); // Отладка
        } else {
          console.error('machineDetailsModal is not initialized');
        }
      } else {
        console.error('Machine not found in store');
      }
    };

    const closeMachineDetails = () => {
      selectedMachine.value = null;
      if (machineDetailsModal.value) {
        machineDetailsModal.value.close();
      }
    };

    const updateMachine = (updatedMachine) => {
      selectedMachine.value = updatedMachine;
      const index = machines.value.findIndex(m => m.id === updatedMachine.id);
      if (index !== -1) {
        machines.value.splice(index, 1, updatedMachine);
      }
    };

    const importData = async () => {
      try {
        await fetch('http://127.0.0.1:5000/import-csv', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        await store.dispatch('fetchMachines');
        currentPage.value = 1;
        console.log('Data imported successfully');
      } catch (error) {
        console.error('Error importing data:', error);
      }
    };

    const paginatedMachines = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      return machines.value.slice(start, end);
    });

    const totalPages = computed(() => {
      return Math.ceil(machines.value.length / itemsPerPage);
    });

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
      }
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
      }
    };

    return {
      machines,
      paginatedMachines,
      selectedMachine,
      openMachineDetails,
      closeMachineDetails,
      updateMachine,
      importData,
      machineDetailsModal,
      currentPage,
      totalPages,
      previousPage,
      nextPage,
    };
  },
};
</script>

<style scoped>
.machine-list {
  padding: 20px;
}

h2 {
  margin-bottom: 10px;
  font-size: 1.5em;
  color: #333;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #2c3e50;
  color: white;
  font-weight: bold;
}

tr {
  transition: background-color 0.2s;
}

tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

td {
  color: #333;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.pagination button {
  padding: 8px 16px;
}
</style>