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
        <button
          class="action-btn"
          v-if="isTechnician"
          @click="openToolAssignment"
        >
          Assign Tool
        </button>
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
            <option
              v-for="tool in tools"
              :key="tool.id"
              :value="tool.id"
            >
              {{ tool.name }} (Wear: {{ tool.metrics?.[0]?.wear_level ?? 'N/A' }}%)
            </option>
          </select>
        </div>
        <div class="tool-modal-footer">
          <button class="action-btn" @click="assignTool" :disabled="!selectedToolId">
            Assign
          </button>
          <button class="close-btn" @click="closeToolModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue';
import axios from 'axios';
import keycloak from '../keycloak';

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
    const tools = ref([]);
    const machines = ref([]);
    const selectedToolId = ref('');
    const localMachine = ref(null);
    const lastMaintenance = ref(null);
    const nextMaintenance = ref(null);

    const isTechnician = computed(() =>
      keycloak?.tokenParsed?.realm_access?.roles.includes('Technician')
    );

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

    const fetchMaintenanceHistory = async () => {
      if (!props.machine?.id) return;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/machines/${props.machine.id}/maintenance`);
        updateMaintenanceDates(response.data.maintenance_logs || []);
      } catch (error) {
        console.error('Error fetching maintenance history:', error);
      }
    };

    const updateMaintenanceDates = (logs) => {
      const now = new Date();
      const performed = logs.filter(log => !log.planned).sort((a, b) => new Date(b.date) - new Date(a.date));
      const planned = logs.filter(log => log.planned && new Date(log.date) > now).sort((a, b) => new Date(a.date) - new Date(b.date));
      lastMaintenance.value = performed.length > 0 ? performed[0].date : null;
      nextMaintenance.value = planned.length > 0 ? planned[0].date : null;
    };

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

    return {
      isOpen,
      isToolModalOpen,
      tools,
      machines,
      selectedToolId,
      localMachine,
      lastMaintenance,
      nextMaintenance,
      isTechnician,
      open,
      close,
      openToolAssignment,
      closeToolModal,
      assignTool,
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
</style>