<template>
  <div class="maintenance-history">
    <h2>Maintenance history</h2>

    <div class="controls">
      <!-- Dropdown to select machine, required before loading history -->
      <select v-model="selectedMachineId">
        <option value="" disabled>choose machine...</option>
        <option v-for="machine in machines" :key="machine.id" :value="machine.id">
          {{ machine.name }}
        </option>
      </select>
    </div>

    <!-- Initial hint to prompt machine selection -->
    <div v-if="!selectedMachineId" class="hint">choose machine to show history...</div>

    <div v-else>
      <!-- Message shown when no history exists -->
      <div v-if="history.length === 0" class="hint">No maintenance history found.</div>

      <!-- Animated list with staggered rendering -->
      <transition-group name="stagger-fade-slide" tag="div">
        <div
          v-for="(item, idx) in history"
          :key="item.id"
          class="history-card"
          :style="{'--stagger-index': idx}"
        >
          <div class="history-row"><b>Date:</b> {{ item.date }}</div>
          <div class="history-row"><b>Performed By:</b> {{ item.performed_by }}</div>
          <div class="history-row"><b>Notes:</b> <i>{{ item.notes }}</i></div>
          <div class="history-row"><b>Type:</b> {{ item.planned ? 'planned' : 'performed' }}</div>
        </div>
      </transition-group>
    </div>

    <!-- Error display for failed API calls -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'MaintenanceHistory',

  data() {
    return {
      machines: [],              // List of all machines (populated on mount)
      selectedMachineId: '',     // Currently selected machine ID from dropdown
      history: [],               // Rendered entries (added with stagger effect)
      errorMessage: '',          // Shown when API calls fail
      _fullHistory: [],          // Full raw history for the selected machine
      _staggerTimeouts: [],      // Array of timeouts used for staggered animation
    };
  },

  watch: {
    /**
     * Watcher: when selected machine changes, load history or reset view.
     */
    selectedMachineId(newVal) {
      if (newVal) this.fetchHistory();
      else this.history = [];
    }
  },

  methods: {
    /**
     * Fetches all available machines from the backend.
     * Populates the dropdown menu.
     */
    async fetchMachines() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 100 }
        });
        this.machines = res.data.machines || [];
      } catch (e) {
        this.errorMessage = 'Failed to load machines.';
      }
    },

    /**
     * Fetches the maintenance history for the selected machine.
     * Uses internal array to store full result and then delegates to animation function.
     */
    async fetchHistory() {
      this.errorMessage = '';
      this.history = [];
      this._fullHistory = [];

      // Clear any ongoing stagger animations
      this._staggerTimeouts.forEach(t => clearTimeout(t));
      this._staggerTimeouts = [];

      if (!this.selectedMachineId) return;

      try {
        const res = await axios.get(`http://127.0.0.1:5000/machines/${this.selectedMachineId}/maintenance`);
        this._fullHistory = res.data.maintenance_logs || [];
        this.staggerShowHistory(); // Show items one by one with animation
      } catch (e) {
        this.errorMessage = 'Failed to load maintenance history.';
      }
    },

    /**
     * Shows history items one by one with delay between each,
     * to create a staggered visual animation effect.
     */
    staggerShowHistory() {
      this.history = [];

      // Clear any previous timeouts to avoid duplicates
      this._staggerTimeouts.forEach(t => clearTimeout(t));
      this._staggerTimeouts = [];

      // Schedule entries with delay
      this._fullHistory.forEach((item, idx) => {
        const timeout = setTimeout(() => {
          this.history.push(item);
        }, idx * 120); // 120ms per item
        this._staggerTimeouts.push(timeout);
      });
    },
  },

  /**
   * Lifecycle: fetch machine list once component is mounted.
   */
  mounted() {
    this.fetchMachines();
  },

  /**
   * Lifecycle: clear any running timeouts on unmount to avoid memory leaks.
   */
  beforeUnmount() {
    this._staggerTimeouts.forEach(t => clearTimeout(t));
  }
};
</script>

<style scoped>
.maintenance-history {
  padding: 0 20px 20px 20px;
}
h2 {
  margin-top: 0;
  margin-bottom: 30px;
  font-size: 1.5em;
  color: #333;
}
.controls {
  display: flex;
  flex-direction: row;
  gap: 24px;
  margin-bottom: 36px;
  width: 100%;
  max-width: 900px;
  align-items: flex-end;
}
select {
  flex: 1 1 0;
  padding: 8px 16px;
  border-radius: 6px;
  border: 1.5px solid #ccc;
  font-size: 1.1em;
  width: 100%;
  max-width: 100%;
}
.hint {
  color: #888;
  margin: 16px 0;
  font-size: 1.18em;
}
.history-card {
  background: #f5f5f5;
  border-radius: 18px;
  padding: 32px 40px;
  margin-bottom: 32px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  font-size: 1.18em;
  width: 100%;
  max-width: 700px;
}
.history-row {
  margin-bottom: 16px;
}
.error-message {
  color: #e53e3e;
  font-weight: 500;
  margin-top: 24px;
}
.stagger-fade-slide-enter-active {
  transition: all 0.5s cubic-bezier(.23,1.02,.64,1);
}
.stagger-fade-slide-leave-active {
  transition: all 0.3s cubic-bezier(.23,1.02,.64,1);
  position: absolute;
}
.stagger-fade-slide-enter-from {
  opacity: 0;
  transform: translateY(40px) scale(0.96);
}
.stagger-fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.stagger-fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.stagger-fade-slide-leave-to {
  opacity: 0;
  transform: translateY(40px) scale(0.96);
}
.stagger-fade-slide-move {
  transition: transform 0.5s cubic-bezier(.23,1.02,.64,1);
}
.stagger-fade-slide-enter-active .history-card {
  transition-delay: calc(var(--stagger-index) * 80ms);
}
</style> 