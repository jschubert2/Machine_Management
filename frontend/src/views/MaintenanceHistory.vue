<template>
  <div class="maintenance-history">
    <h2>Maintenance history</h2>
    <div class="controls">
      <select v-model="selectedMachineId">
        <option value="" disabled>choose machine...</option>
        <option v-for="machine in machines" :key="machine.id" :value="machine.id">
          {{ machine.name }}
        </option>
      </select>
    </div>
    <div v-if="!selectedMachineId" class="hint">choose machine to show history...</div>
    <div v-else>
      <div v-if="history.length === 0" class="hint">No maintenance history found.</div>
      <transition-group name="stagger-fade-slide" tag="div">
        <div v-for="(item, idx) in history" :key="item.id" class="history-card" :style="{'--stagger-index': idx}">
          <div class="history-row"><b>Date:</b> {{ item.date }}</div>
          <div class="history-row"><b>Performed By:</b> {{ item.performed_by }}</div>
          <div class="history-row"><b>Notes:</b> <i>{{ item.notes }}</i></div>
          <div class="history-row"><b>Type:</b> {{ item.planned ? 'planned' : 'performed' }}</div>
        </div>
      </transition-group>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MaintenanceHistory',
  data() {
    return {
      machines: [],
      selectedMachineId: '',
      history: [],
      errorMessage: '',
      _fullHistory: [],
      _staggerTimeouts: [],
    };
  },
  watch: {
    selectedMachineId(newVal) {
      if (newVal) this.fetchHistory();
      else this.history = [];
    }
  },
  methods: {
    async fetchMachines() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/machines', { params: { page: 1, per_page: 100 } });
        this.machines = res.data.machines || [];
      } catch (e) {
        this.errorMessage = 'Failed to load machines.';
      }
    },
    async fetchHistory() {
      this.errorMessage = '';
      this.history = [];
      this._fullHistory = [];
      this._staggerTimeouts.forEach(t => clearTimeout(t));
      this._staggerTimeouts = [];
      if (!this.selectedMachineId) return;
      try {
        const res = await axios.get(`http://127.0.0.1:5000/machines/${this.selectedMachineId}/maintenance`);
        this._fullHistory = res.data.maintenance_logs || [];
        this.staggerShowHistory();
      } catch (e) {
        this.errorMessage = 'Failed to load maintenance history.';
      }
    },
    staggerShowHistory() {
      this.history = [];
      this._staggerTimeouts.forEach(t => clearTimeout(t));
      this._staggerTimeouts = [];
      this._fullHistory.forEach((item, idx) => {
        const timeout = setTimeout(() => {
          this.history.push(item);
        }, idx * 120);
        this._staggerTimeouts.push(timeout);
      });
    },
  },
  mounted() {
    this.fetchMachines();
  },
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