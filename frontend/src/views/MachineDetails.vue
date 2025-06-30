<template>
  <div class="modal" v-if="isOpen">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Machine Details</h2>
      </div>
      <div class="modal-body">
        <div class="detail-item">
          <span class="label">ID:</span>
          <span class="value">{{ localMachine?.id || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Name:</span>
          <span class="value">{{ localMachine?.name || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Attached Tool:</span>
          <span class="value">{{ localMachine?.attached_tool || 'Not assigned' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Tool Wear:</span>
          <span class="value">{{ localMachine?.tool_wear || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Last Maintenance:</span>
          <span class="value">{{ lastMaintenance || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Next Maintenance:</span>
          <span class="value">{{ nextMaintenance || 'N/A' }}</span>
        </div>
      </div>
      <div class="modal-footer">
        <button class="action-btn" @click="openToolAssignment">Assign Tool</button>
        <button class="close-btn" @click="close">Close</button>
      </div>
    </div>

    <div class="tool-modal" v-if="isToolModalOpen">
      <div class="tool-modal-content">
        <div class="tool-modal-header">
          <h3>Assign Tool</h3>
        </div>
        <div class="tool-modal-body">
          <select v-model="selectedToolId">
            <option disabled value="">Select a tool</option>
            <option v-for="tool in tools" :key="tool.id" :value="tool.id">
              {{ tool.name }} (Wear: {{ tool.metrics?.[0]?.wear_level ?? 'N/A' }}%)
            </option>
          </select>
        </div>
        <div class="tool-modal-footer">
          <button class="action-btn" @click="assignTool" :disabled="!selectedToolId">Assign</button>
          <button class="close-btn" @click="closeToolModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- maintenance register -->
    <div class="maintenance-modal" v-if="isMaintenanceModalOpen">
      <div class="maintenance-modal-content">
        <div class="maintenance-modal-header">
          <h3>Register Maintenance</h3>
          <button class="modal-close-btn" @click="closeMaintenanceModal">×</button>
        </div>
        <div class="maintenance-modal-body">
          <div class="form-group">
            <label for="performed-by">Performed By</label>
            <input id="performed-by" v-model="performedBy" placeholder="Enter technician name" />
          </div>
          <div class="form-group">
            <label for="maintenance-date">Date</label>
            <input id="maintenance-date" type="date" v-model="maintenanceDate" lang="en" />
          </div>
          <div class="form-group">
            <label>Maintenance Type</label>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" value="performed" v-model="maintenanceType" />
                Performed
              </label>
              <label class="radio-label">
                <input type="radio" value="planned" v-model="maintenanceType" />
                Planned
              </label>
            </div>
          </div>
          <div class="form-group">
            <label for="notes">Notes</label>
            <textarea id="notes" v-model="maintenanceNotes" placeholder="Enter notes..."></textarea>
          </div>
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
        <div class="maintenance-modal-footer">
          <button class="register-btn" @click="registerMaintenance" :disabled="!maintenanceType || !performedBy || !maintenanceDate">Register</button>
        </div>
      </div>
    </div>

    <div class="history-modal" v-if="isHistoryModalOpen">
      <div class="history-modal-content">
        <div class="history-modal-header">
          <h3>Maintenance History</h3>
          <button class="modal-close-btn" @click="closeHistoryModal">×</button>
        </div>
        <div class="history-modal-body">
          <div v-if="maintenanceHistory.length === 0" class="no-history">
            No maintenance history available.
          </div>
          <div v-else class="history-list">
            <div v-for="record in maintenanceHistory" :key="record.id" class="history-item">
              <p><strong>Date:</strong> {{ record.date }}</p>
              <p><strong>Performed By:</strong> {{ record.performed_by }}</p>
              <p><strong>Notes:</strong> {{ record.notes || 'None' }}</p>
              <p><strong>Type:</strong> {{ record.planned ? 'Planned' : 'Performed' }}</p>
            </div>
          </div>
        </div>
        <div class="history-modal-footer">
          <button class="close-btn" @click="closeHistoryModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'MachineDetails',
  props: {
    machine: {
      type: Object,
      default: null,
    },
  },
  setup(props, { emit }) {
    const isOpen = ref(false);
    const isToolModalOpen = ref(false);
    const isMaintenanceModalOpen = ref(false);
    const isHistoryModalOpen = ref(false);
    const tools = ref([]);
    const machines = ref([]);
    const maintenanceHistory = ref([]);
    const selectedToolId = ref('');
    const localMachine = ref(null);
    const performedBy = ref('');
    const maintenanceDate = ref('');
    const maintenanceType = ref('');
    const maintenanceNotes = ref('');
    const successMessage = ref('');
    const errorMessage = ref('');
    const lastMaintenance = ref(null);
    const nextMaintenance = ref(null);

    watch(() => props.machine, (newMachine) => {
      localMachine.value = { ...newMachine };
    }, { immediate: true });

    const open = async () => {
      isOpen.value = true;
      await fetchTools();
      await fetchMachines();
      await fetchAssignedTool();
      await fetchMaintenanceHistory();
    };

    const close = () => {
      isOpen.value = false;
      emit('close');
    };

    const openToolAssignment = () => {
      isToolModalOpen.value = true;
    };

    const closeToolModal = () => {
      isToolModalOpen.value = false;
      selectedToolId.value = '';
    };

    const openMaintenanceModal = () => {
      isMaintenanceModalOpen.value = true;
      successMessage.value = '';
      errorMessage.value = '';
      performedBy.value = '';
      maintenanceDate.value = '';
      maintenanceType.value = '';
      maintenanceNotes.value = '';
    };

    const closeMaintenanceModal = () => {
      isMaintenanceModalOpen.value = false;
      performedBy.value = '';
      maintenanceDate.value = '';
      maintenanceType.value = '';
      maintenanceNotes.value = '';
      successMessage.value = '';
      errorMessage.value = '';
    };

    const openHistoryModal = () => {
      isHistoryModalOpen.value = true;
    };

    const closeHistoryModal = () => {
      isHistoryModalOpen.value = false;
    };
// get request for tools 
    const fetchTools = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/tools', {
          params: { page: 1, per_page: 100 },
        });
        tools.value = response.data.tools || [];
      } catch (error) {
        console.error('Error fetching tools:', error);
      }
    };
//get request for machines 
    const fetchMachines = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 100 },
        });
        machines.value = response.data.machines || [];
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    };
//get request for assigned tools
    const fetchAssignedTool = async () => {
      if (!props.machine?.id) return;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/machines/${props.machine.id}/tool`);
        const tool = response.data;
        const updatedMachine = {
          ...localMachine.value,
          attached_tool: tool.tool_name || 'Not assigned',
          tool_wear: tool.wear_level !== null ? `${tool.wear_level}%` : 'N/A',
        };
        localMachine.value = updatedMachine;
        emit('update:machine', updatedMachine);
      } catch (error) {
        console.error('Error fetching assigned tool:', error);
        const updatedMachine = {
          ...localMachine.value,
          attached_tool: 'Not assigned',
          tool_wear: 'N/A',
        };
        localMachine.value = updatedMachine;
        emit('update:machine', updatedMachine);
      }
    };

//get request for maintenance history
    const fetchMaintenanceHistory = async () => {
      if (!props.machine?.id) return;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/machines/${props.machine.id}/maintenance`);
        console.log('Maintenance history response:', response.data);
        maintenanceHistory.value = response.data.maintenance_logs || [];
        updateMaintenanceDates();
      } catch (error) {
        console.error('Error fetching maintenance history:', error);
        maintenanceHistory.value = [];
      }
    };

    const updateMaintenanceDates = () => {
  const now = new Date();

  const performedRecords = maintenanceHistory.value
    .filter(record => !record.planned)
    .sort((a, b) => new Date(b.date) - new Date(a.date));

  const plannedRecords = maintenanceHistory.value
    .filter(record => record.planned && new Date(record.date) > now)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  lastMaintenance.value = performedRecords.length > 0 ? performedRecords[0].date : null;
  nextMaintenance.value = plannedRecords.length > 0 ? plannedRecords[0].date : null;
};

//put request to assign tool
    const assignTool = async () => {
      if (!props.machine?.id || !selectedToolId.value) return;
      try {
        await axios.put(`http://127.0.0.1:5000/machines/${props.machine.id}/tool`, {
          tool_id: selectedToolId.value,
        });
        await fetchAssignedTool();
        closeToolModal();
      } catch (error) {
        console.error('Error assigning tool:', error);
      }
    };

    const registerMaintenance = async () => {
      if (!maintenanceType.value || !performedBy.value || !maintenanceDate.value) return;

      const payload = {
        machine_id: localMachine.value?.id,
        performed_by: performedBy.value,
        date: maintenanceDate.value,
        notes: maintenanceNotes.value || '',
        planned: maintenanceType.value === 'planned',
      };
//
      try {
        const response = await axios.post('http://127.0.0.1:5000/maintenance', payload);
        successMessage.value = maintenanceType.value === 'performed' 
          ? 'Maintenance log added successfully!' 
          : 'Maintenance planned successfully';
        errorMessage.value = '';
        await new Promise(resolve => setTimeout(resolve, 500)); 
        await fetchMaintenanceHistory(); 
        updateMaintenanceDates(); 
      } catch (error) {
        console.error('Error registering maintenance:', error);
        errorMessage.value = 'Failed to register maintenance. Please try again.';
        successMessage.value = '';
      }
    };

    return {
      isOpen,
      isToolModalOpen,
      isMaintenanceModalOpen,
      isHistoryModalOpen,
      tools,
      machines,
      maintenanceHistory,
      selectedToolId,
      localMachine,
      performedBy,
      maintenanceDate,
      maintenanceType,
      maintenanceNotes,
      successMessage,
      errorMessage,
      lastMaintenance,
      nextMaintenance,
      open,
      close,
      openToolAssignment,
      closeToolModal,
      openMaintenanceModal,
      closeMaintenanceModal,
      openHistoryModal,
      closeHistoryModal,
      assignTool,
      registerMaintenance,
    };
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 12px;
  width: 600px;
  max-width: 90%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(90deg, #f0f4f8, #e0e7f0);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.6em;
  color: #2d3748;
  font-weight: 600;
  text-align: center;
}

.modal-body {
  padding: 25px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #edf2f7;
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 500;
  color: #4a5568;
  font-size: 1.1em;
}

.value {
  font-weight: 600;
  color: #2d3748;
  font-size: 1.1em;
}

.modal-footer {
  padding: 15px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: linear-gradient(90deg, #e0e7f0, #f0f4f8);
}

.action-btn {
  padding: 10px 20px;
  background-color: #3182ce;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  background-color: #2b6cb0;
  transform: translateY(-2px);
}

.action-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.close-btn {
  padding: 10px 20px;
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.close-btn:hover {
  background-color: #c53030;
  transform: translateY(-2px);
}

.tool-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.tool-modal-content {
  background-color: #fff;
  border-radius: 12px;
  width: 300px;
  max-width: 90%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.tool-modal-header {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(90deg, #f0f4f8, #e0e7f0);
}

.tool-modal-header h3 {
  margin: 0;
  font-size: 1.3em;
  color: #2d3748;
  font-weight: 600;
}

.tool-modal-body {
  padding: 20px;
}

.tool-modal-body select {
  width: 100%;
  padding: 10px;
  font-size: 1.1em;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tool-modal-footer {
  padding: 15px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: linear-gradient(90deg, #e0e7f0, #f0f4f8);
}

.maintenance-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.maintenance-modal-content {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  width: 450px;
  max-width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.maintenance-modal-header {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(90deg, #edf2f7, #e2e8f0);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.maintenance-modal-header h3 {
  margin: 0;
  font-size: 1.3em;
  color: #2d3748;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  color: #a0aec0;
  cursor: pointer;
  transition: color 0.3s;
}

.modal-close-btn:hover {
  color: #718096;
}

.maintenance-modal-body {
  padding: 15px;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  font-size: 0.9em;
  color: #4a5568;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group select,
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  font-size: 0.9em;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  background-color: #fff;
  color: #2d3748;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group select:focus,
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #63b3ed;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.form-group textarea {
  height: 80px;
  resize: vertical;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  font-size: 0.9em;
  color: #4a5568;
}

.radio-label input {
  margin-right: 6px;
}

.radio-label input:focus {
  outline: none;
}

.success-message {
  color: #48bb78;
  font-size: 0.9em;
  margin-top: 8px;
  text-align: center;
  padding: 6px;
  background-color: #f0fff4;
  border-radius: 8px;
}

.error-message {
  color: #f56565;
  font-size: 0.9em;
  margin-top: 8px;
  text-align: center;
  padding: 6px;
  background-color: #fff5f5;
  border-radius: 8px;
}

.maintenance-modal-footer {
  padding: 12px 15px;
  border-top: 1px solid #e2e8f0;
  background: linear-gradient(90deg, #e2e8f0, #edf2f7);
  display: flex;
  justify-content: flex-end;
}

.register-btn {
  padding: 8px 20px;
  background-color: #48bb78;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.register-btn:hover {
  background-color: #38a169;
  transform: translateY(-2px);
}

.register-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.history-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.history-modal-content {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  width: 450px;
  max-width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.history-modal-header {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(90deg, #edf2f7, #e2e8f0);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-modal-header h3 {
  margin: 0;
  font-size: 1.3em;
  color: #2d3748;
  font-weight: 600;
}

.history-modal-body {
  padding: 15px;
  max-height: 400px;
  overflow-y: auto;
}

.no-history {
  text-align: center;
  color: #4a5568;
  font-size: 1em;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #f7fafc;
}

.history-item p {
  margin: 5px 0;
  font-size: 0.9em;
  color: #2d3748;
}

.history-item p strong {
  color: #4a5568;
}

.history-modal-footer {
  padding: 12px 15px;
  border-top: 1px solid #e2e8f0;
  background: linear-gradient(90deg, #e2e8f0, #edf2f7);
  display: flex;
  justify-content: flex-end;
}
</style>