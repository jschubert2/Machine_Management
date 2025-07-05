<template>
  <div class="machine-list">
    <h2>Machines</h2>

    <div class="filters">
      <template v-if="isAdmin">
        <label class="import-label">
          <input type="file" accept=".csv" @change="importCsv" style="display:none" ref="importInput" />
          <button class="import-btn" @click.prevent="$refs.importInput.click()">import CSV</button>
        </label>
      </template>
      <select v-model="selectedStatus">
        <option value="">All Statuses</option>
        <option>Running</option>
        <option>Offline</option>
      </select>
      <select v-model="selectedCategory">
        <option value="">All Categories</option>
        <option>Manual</option>
        <option>Automatic</option>
      </select>
      <div class="date-range">
        <label>Created At:</label>
        <input type="date" v-model="startDate" />
        <span>to</span>
        <input type="date" v-model="endDate" />
      </div>
    </div>

    <div v-if="isAdmin && !machinesLoaded" class="no-data">upload CSV file to display machines</div>
    <div v-else>
      <div v-if="paginatedMachines.length === 0" class="no-data">
        No data available.
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th @click="toggleSort('name')">
              Name {{ sortBy === 'name' ? (sortAsc ? '↑' : '↓') : '' }}
            </th>
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

      <div class="pagination" v-if="paginatedMachines.length > 0">
        <button @click="previousPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
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
import keycloak from '../keycloak';

export default {
  name: 'MachineTable',
  components: { MachineDetails },
  setup() {
    const store = useStore();
    const selectedMachine = ref(null);
    const machineDetailsModal = ref(null);
    const currentPage = ref(1);
    const itemsPerPage = 30;
    const selectedStatus = ref('');
    const selectedCategory = ref('');
    const startDate = ref('');
    const endDate = ref('');
    const sortBy = ref('name');
    const sortAsc = ref(true);
    const importInput = ref(null);
    const machines = ref([]); // для админа
    const machinesLoaded = ref(false); // для админа

    // Определяем роли
    const roles = keycloak.tokenParsed?.realm_access?.roles || [];
    const isAdmin = roles.includes('Admin');
    const isTechnician = roles.includes('Technician');

    // Для technician — грузим с сервера
    onMounted(() => {
      if (isTechnician) {
        store.dispatch('fetchMachines');
      }
      if (isAdmin) {
        // если нужно, можно подгружать из localStorage
        const saved = localStorage.getItem('adminMachines');
        if (saved) {
          machines.value = JSON.parse(saved);
          machinesLoaded.value = true;
        }
      }
    });

    // Для technician — используем store, для admin — локальный массив
    const machinesSource = computed(() => {
      if (isTechnician) return store.state.machines;
      if (isAdmin) return machines.value;
      return [];
    });

    const importCsv = (event) => {
      if (!isAdmin) return;
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length > 0) {
          const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
          const data = lines.slice(1).map(line => {
            const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
            const row = {};
            headers.forEach((header, idx) => {
              row[header] = values[idx] || '';
            });
            return row;
          });
          machines.value = data;
          machinesLoaded.value = true;
          currentPage.value = 1;
          localStorage.setItem('adminMachines', JSON.stringify(data));
        }
      };
      reader.readAsText(file);
      event.target.value = '';
    };

    const openMachineDetails = (machineId) => {
      const machine = machinesSource.value.find((m) => m.id === machineId);
      if (machine) {
        selectedMachine.value = { ...machine };
        if (machineDetailsModal.value) {
          machineDetailsModal.value.open();
        }
      }
    };

    const closeMachineDetails = () => {
      selectedMachine.value = null;
    };

    const updateMachine = (updatedMachine) => {
      selectedMachine.value = { ...updatedMachine };
      store.commit('updateMachine', updatedMachine);
    };

    const filteredMachines = computed(() => {
      return machinesSource.value.filter(machine => {
        const statusMatch = selectedStatus.value === '' || machine.status === selectedStatus.value;
        const categoryMatch = selectedCategory.value === '' || machine.category === selectedCategory.value;

        const createdAt = machine.created_at ? new Date(machine.created_at).toISOString().split('T')[0] : null;
        const startMatch = !startDate.value || (createdAt && createdAt >= startDate.value);
        const endMatch = !endDate.value || (createdAt && createdAt <= endDate.value);

        return statusMatch && categoryMatch && startMatch && endMatch;
      });
    });

    const sortedMachines = computed(() => {
      const sorted = [...filteredMachines.value];
      sorted.sort((a, b) => {
        const valA = a[sortBy.value] || '';
        const valB = b[sortBy.value] || '';
        return sortAsc.value
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      });
      return sorted;
    });

    const paginatedMachines = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      return sortedMachines.value.slice(start, end);
    });

    const totalPages = computed(() => {
      return Math.ceil(sortedMachines.value.length / itemsPerPage) || 1;
    });

    const previousPage = () => {
      if (currentPage.value > 1) currentPage.value--;
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++;
    };

    const toggleSort = (column) => {
      if (sortBy.value === column) {
        sortAsc.value = !sortAsc.value;
      } else {
        sortBy.value = column;
        sortAsc.value = true;
      }
    };

    return {
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
      sortBy,
      sortAsc,
      toggleSort,
      paginatedMachines,
      importCsv,
      importInput,
      isAdmin,
      isTechnician,
      machinesLoaded,
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

.import-label {
  margin-left: auto;
  display: flex;
  align-items: center;
}

.import-btn {
  background: #38a169;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 7px 18px;
  font-size: 1em;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s;
}

.import-btn:hover {
  background: #2f855a;
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
  cursor: pointer;
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
