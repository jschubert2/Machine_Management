<template>
  <div class="machine-list">
    <h2>Machines</h2>
    <div v-if="machines.length === 0" class="no-data">
      No data available.
    </div>
    <table v-else>
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
        <tr
          v-for="machine in paginatedMachines"
          :key="machine.id"
          @click="openMachineDetails(machine.id)"
        >
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
    <div class="pagination" v-if="machines.length > 0">
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
import { computed, ref, onMounted } from 'vue';
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

    onMounted(() => {
      store.dispatch('fetchMachines');
    });

    const openMachineDetails = (machineId) => {
      const machine = machines.value.find((m) => m.id === machineId);
      if (machine) {
        selectedMachine.value = { ...machine };
        if (machineDetailsModal.value) {
          machineDetailsModal.value.open();
        }
      }
    };

    const closeMachineDetails = () => {
      selectedMachine.value = null;
      if (machineDetailsModal.value) {
        machineDetailsModal.value.close();
      }
    };

    const updateMachine = (updatedMachine) => {
      selectedMachine.value = { ...updatedMachine };
      store.commit('updateMachine', updatedMachine);
    };

    const filteredMachines = computed(() => {
      return machines.value.filter(machine => {
        const statusMatch = selectedStatus.value === '' || machine.status === selectedStatus.value;
        const categoryMatch = selectedCategory.value === '' || machine.category === selectedCategory.value;

        const createdAt = machine.created_at ? new Date(machine.created_at).toISOString().split('T')[0] : null;
        const startMatch = !startDate.value || (createdAt && createdAt >= startDate.value);
        const endMatch = !endDate.value || (createdAt && createdAt <= endDate.value);

        return statusMatch && categoryMatch && startMatch && endMatch;
      });
    });

    const paginatedMachines = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      return filteredMachines.value.slice(start, end);
    });

    const totalPages = computed(() => {
      return Math.ceil(filteredMachines.value.length / itemsPerPage);
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
      filteredMachines,
      paginatedMachines,
      selectedMachine,
      openMachineDetails,
      closeMachineDetails,
      updateMachine,
      machineDetailsModal,
      currentPage,
      totalPages,
      previousPage,
      nextPage,
      selectedStatus,
      selectedCategory,
      startDate,
      endDate,
    };
  },
};
</script>

<style scoped>
.machine-list {
  padding: 10px 20px 20px 20px;
}

h2 {
  margin: 0 0 8px 0; 
  color: #333;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 8px; 
}

button:hover {
  background-color: #0056b3;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
}

.filters select,
.filters input {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date-range label {
  font-weight: 500;
  white-space: nowrap;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

th,
td {
  padding: 10px 14px;
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
  margin-top: 15px;
  gap: 10px;
}

.pagination button {
  padding: 6px 14px;
}

.no-data {
  color: #666;
  margin-top: 15px;
  font-style: italic;
}
</style>

