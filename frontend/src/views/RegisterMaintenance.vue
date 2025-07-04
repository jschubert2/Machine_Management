<template>
  <div class="register-maintenance">
    <h2>Register Maintenance</h2>
    <form @submit.prevent="registerMaintenance" ref="regForm">
      <div class="form-row">
        <label>Machine</label>
        <select v-model="selectedMachineId" required>
          <option value="" disabled>choose machine...</option>
          <option v-for="machine in machines" :key="machine.id" :value="machine.id">
            {{ machine.name }}
          </option>
        </select>
      </div>

      <div class="form-row">
        <label>Performed By</label>
        <input :value="fullName" type="text" readonly />
      </div>

      <div class="form-row">
        <label>Date</label>
        <input v-model="date" type="date" required />
      </div>

      <div class="form-row">
        <label>Maintenance Type</label>
        <div class="maintenance-type">
          <label><input type="radio" value="performed" v-model="maintenanceType" required /> Performed</label>
          <label><input type="radio" value="planned" v-model="maintenanceType" required /> Planned</label>
        </div>
      </div>

      <div class="form-row">
        <label>Notes</label>
        <textarea v-model="notes" rows="3" />
      </div>

      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>

    <button class="register-btn" @click="submitForm">Register</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterMaintenance',
  data() {
    return {
      machines: [],
      selectedMachineId: '',
      date: '',
      maintenanceType: '',
      notes: '',
      fullName: 'Unknown User',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async fetchMachines() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 100 },
        });
        this.machines = res.data.machines || [];
      } catch (e) {
        this.errorMessage = 'Failed to load machines.';
      }
    },
    async registerMaintenance() {
      this.successMessage = '';
      this.errorMessage = '';

      const token = this.$keycloak?.tokenParsed;
      const username = token?.preferred_username;

      if (!username) {
        this.errorMessage = 'Cannot register maintenance: username not found.';
        return;
      }

      try {
        await axios.post('http://127.0.0.1:5000/maintenance', {
          machine_id: this.selectedMachineId,
          performed_by: username, // 👈 отправляем username
          date: this.date,
          notes: this.notes,
          planned: this.maintenanceType === 'planned',
        });
        this.successMessage = 'Maintenance registered successfully!';
        this.selectedMachineId = '';
        this.date = '';
        this.maintenanceType = '';
        this.notes = '';
      } catch (e) {
        console.error('Registration error:', e);
        this.errorMessage = 'Failed to register maintenance.';
      }
    },
    submitForm() {
      this.$refs.regForm.requestSubmit();
    },
  },
  async mounted() {
    const token = this.$keycloak?.tokenParsed;
    if (token) {
      this.fullName = `${token.given_name} ${token.family_name}`;
    }
    await this.fetchMachines();
  },
};
</script>

<style scoped>
.register-maintenance {
  padding: 0 20px 20px 20px;
  position: relative;
  min-height: 90vh;
}
h2 {
  margin-top: 0;
  margin-bottom: 30px;
  font-size: 1.5em;
  color: #333;
}
form {
  display: flex;
  flex-direction: column;
  gap: 32px;
  width: 100%;
  max-width: 900px;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
.form-row input,
.form-row select {
  width: 100%;
  padding: 8px 16px;
  font-size: 1.1em;
}
.form-row textarea {
  width: 100%;
  min-width: 0;
  max-width: 100%;
  font-size: 1.1em;
  padding: 12px 16px;
}
label {
  font-weight: 500;
  font-size: 1.18em;
}
input, select, textarea {
  padding: 18px 16px;
  border: 1.5px solid #ccc;
  border-radius: 6px;
  font-size: 1.18em;
  width: 100%;
  box-sizing: border-box;
}
input[readonly] {
  background-color: #f4f4f4;
  color: #555;
  cursor: not-allowed;
}
.maintenance-type {
  display: flex;
  gap: 40px;
  margin-top: 4px;
}
.maintenance-type label {
  font-weight: 400;
  font-size: 1.18em;
}
.register-btn {
  background: #28a745;
  color: #fff;
  border: none;
  padding: 10px 32px;
  border-radius: 6px;
  font-size: 1.1em;
  cursor: pointer;
  font-weight: 500;
  align-self: flex-end;
  margin-top: 24px;
}
.register-btn:hover {
  background: #218838;
}
.success-message {
  color: #28a745;
  font-weight: 500;
  margin-top: 20px;
}
.error-message {
  color: #e53e3e;
  font-weight: 500;
  margin-top: 20px;
}
</style>
