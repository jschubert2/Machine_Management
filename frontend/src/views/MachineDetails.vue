<template>
  <div class="modal" v-if="isOpen">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Machine Details</h2>
      </div>
      <div class="modal-body">
        <div class="detail-item">
          <span class="label">ID:</span>
          <span class="value">{{ machine?.id || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Name:</span>
          <span class="value">{{ machine?.name || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Attached Tool:</span>
          <span class="value">{{ machine?.attached_tool || 'Not assigned' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Tool Wear:</span>
          <span class="value">{{ machine?.tool_wear || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Last Maintenance:</span>
          <span class="value">N/A</span>
        </div>
        <div class="detail-item">
          <span class="label">Next Maintenance:</span>
          <span class="value">N/A</span>
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
              {{ tool.name }} (Wear: {{ tool.wear_level }}%)
            </option>
          </select>
        </div>
        <div class="tool-modal-footer">
          <button class="action-btn" @click="assignTool" :disabled="!selectedToolId">Assign</button>
          <button class="close-btn" @click="closeToolModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
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
    const tools = ref([]);
    const selectedToolId = ref('');

    const open = () => {
      console.log('Opening MachineDetails modal'); // Отладка
      isOpen.value = true;
      fetchTools();
    };

    const close = () => {
      isOpen.value = false;
      emit('close');
    };

    const openToolAssignment = () => {zzzzzzzzz
      isToolModalOpen.value = true;
    };

    const closeToolModal = () => {
      isToolModalOpen.value = false;
      selectedToolId.value = '';
    };

    const fetchTools = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/tools', {
          params: { page: 1, per_page: 100 }
        });
        tools.value = response.data.tools || [];
      } catch (error) {
        console.error('Error fetching tools:', error);
      }
    };

    const assignTool = async () => {
      if (!props.machine?.id || !selectedToolId.value) return;

      try {
        const selectedTool = tools.value.find(t => t.id === selectedToolId.value);
        await axios.put(`http://127.0.0.1:5000/machines/${props.machine.id}/tool`, {
          tool_id: selectedToolId.value,
        });
        emit('update:machine', {
          ...props.machine,
          attached_tool: selectedTool.name,
          tool_wear: selectedTool.wear_level + '%',
        });
        closeToolModal();
      } catch (error) {
        console.error('Error assigning tool:', error);
      }
    };

    return {
      isOpen,
      isToolModalOpen,
      tools,
      selectedToolId,
      open,
      close,
      openToolAssignment,
      closeToolModal,
      fetchTools,
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
  width: 400px;
  max-width: 90%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5em;
  color: #1a2a44;
  font-weight: 600;
}

.modal-body {
  padding: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f3f5;
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 500;
  color: #6b7280;
  font-size: 1em;
}

.value {
  font-weight: 600;
  color: #1a2a44;
  font-size: 1em;
}

.modal-footer {
  padding: 15px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.action-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background-color: #0056b3;
}

.action-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.close-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #c82333;
}

/* Стили для модального окна назначения инструмента */
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
}

.tool-modal-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #1a2a44;
  font-weight: 600;
}

.tool-modal-body {
  padding: 15px;
}

.tool-modal-body select {
  width: 100%;
  padding: 8px;
  font-size: 1em;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
}

.tool-modal-footer {
  padding: 10px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>