<template>
  <div class="machine-list">
    <h2>Machines</h2>

    <div class="filters">
      <!-- Admin-only file import logic (CSV handled via <input type="file">) -->
      <template v-if="isAdmin">
        <label class="import-label">
          <!-- Hidden file input triggered programmatically -->
          <input type="file" accept=".csv" @change="importCsv" style="display:none" ref="importInput" />

          <!-- Trigger file input with custom button (required for style) -->
          <button class="import-btn" @click.prevent="$refs.importInput.click()">import CSV</button>

          <!-- Clear imported data from localStorage -->
          <button class="clear-btn" @click="clearImport" v-if="machinesLoaded">clear</button>
        </label>
      </template>

      <!-- Simple dropdown filters (no comment needed) -->
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

      <!-- Custom date range filter for creation date -->
      <div class="date-range">
        <label>Created At:</label>
        <input type="date" v-model="startDate" />
        <span>to</span>
        <input type="date" v-model="endDate" />
      </div>
    </div>

    <!-- Admin sees prompt to upload if no CSV yet -->
    <div v-if="isAdmin && !machinesLoaded" class="no-data">
      upload CSV file to display machines
    </div>

    <div v-else>
      <!-- If no machines match filters -->
      <div v-if="paginatedMachines.length === 0" class="no-data">
        No data available.
      </div>

      <!-- Main machine data table -->
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <!-- Sortable column with direction toggle and indicator -->
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
          <!-- Each row opens machine detail modal -->
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

      <!-- Pagination controls (simple, obvious logic) -->
      <div class="pagination" v-if="paginatedMachines.length > 0">
        <button @click="previousPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>

    <!-- MachineDetails modal instance (ref + events) -->
    <machine-details
      ref="machineDetailsModal"
      :machine="selectedMachine"
      @close="closeMachineDetails"
      @update:machine="updateMachine"
    />
  </div>
</template>

<script>
/**
 * MachineTable.vue
 *
 * Purpose:
 * Displays a list of production machines in a table with support for:
 * - CSV-based import (Admin)
 * - Real-time fetch from backend via Vuex (Technician)
 * - Filtering by status, category, and creation date
 * - Sorting and pagination
 * - Opening machine detail modal with tool assignment and maintenance view
 */

import { useStore } from 'vuex';
import { computed, ref, onMounted } from 'vue';
import MachineDetails from '../views/MachineDetails.vue';
import keycloak from '../keycloak';

export default {
  name: 'MachineTable',
  components: { MachineDetails },

  setup() {
    const store = useStore();

    // Machine selection and modal ref
    const selectedMachine = ref(null);
    const machineDetailsModal = ref(null);

    // Pagination
    const currentPage = ref(1);
    const itemsPerPage = 30;

    // Filter state
    const selectedStatus = ref('');
    const selectedCategory = ref('');
    const startDate = ref('');
    const endDate = ref('');

    // Sorting
    const sortBy = ref('name');
    const sortAsc = ref(true);

    // File input for CSV import
    const importInput = ref(null);

    // Local data for Admin users
    const machines = ref([]);
    const machinesLoaded = ref(false);

    // Role check using Keycloak
    const roles = keycloak.tokenParsed?.realm_access?.roles || [];
    const isAdmin = roles.includes('Admin');
    const isTechnician = roles.includes('Technician');

    /**
     * Lifecycle hook: On mount, fetch or load machine data based on user role.
     * - Technicians load from backend (via Vuex)
     * - Admins load from localStorage (CSV import)
     */
    onMounted(() => {
      if (isTechnician) {
        store.dispatch('fetchMachines');
      }
      if (isAdmin) {
        const saved = localStorage.getItem('adminMachines');
        if (saved) {
          machines.value = JSON.parse(saved);
          machinesLoaded.value = true;
        }
      }
    });

    /**
     * Computed source of machine list depending on role.
     */
    const machinesSource = computed(() => {
      if (isTechnician) return store.state.machines;
      if (isAdmin) return machines.value;
      return [];
    });

    /**
     * Handles CSV import and parses it into machine objects.
     * Only accessible to Admin users.
     */
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

    /**
     * Opens the modal showing detailed info for the selected machine.
     */
    const openMachineDetails = (machineId) => {
      const machine = machinesSource.value.find((m) => m.id === machineId);
      if (machine) {
        selectedMachine.value = { ...machine };
        if (machineDetailsModal.value) {
          machineDetailsModal.value.open();
        }
      }
    };

    /**
     * Closes the machine detail modal.
     */
    const closeMachineDetails = () => {
      selectedMachine.value = null;
    };

    /**
     * Updates a machine entry after changes (e.g. tool assignment).
     * Uses Vuex mutation to keep store consistent.
     */
    const updateMachine = (updatedMachine) => {
      selectedMachine.value = { ...updatedMachine };
      store.commit('updateMachine', updatedMachine);
    };

    /**
     * Filters machines by status, category, and date range.
     */
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

    /**
     * Sorts filtered machines based on current column and direction.
     */
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

    /**
     * Returns only the machines visible on the current page.
     */
    const paginatedMachines = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      return sortedMachines.value.slice(start, end);
    });

    /**
     * Calculates total number of pages based on filtered data.
     */
    const totalPages = computed(() => {
      return Math.ceil(sortedMachines.value.length / itemsPerPage) || 1;
    });

    /**
     * Moves pagination one page backward.
     */
    const previousPage = () => {
      if (currentPage.value > 1) currentPage.value--;
    };

    /**
     * Moves pagination one page forward.
     */
    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++;
    };

    /**
     * Handles column sort toggle when user clicks table header.
     */
    const toggleSort = (column) => {
      if (sortBy.value === column) {
        sortAsc.value = !sortAsc.value;
      } else {
        sortBy.value = column;
        sortAsc.value = true;
      }
    };

    /**
     * Clears admin-imported machine data and resets state.
     */
    const clearImport = () => {
      machines.value = [];
      machinesLoaded.value = false;
      localStorage.removeItem('adminMachines');
    };

    // Bind all variables/functions to template
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
      clearImport,
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

.clear-btn {
  background: #e53e3e;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 7px 18px;
  font-size: 1em;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s;
}

.clear-btn:hover {
  background: #c53030;
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
