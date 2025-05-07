<template>
  <div class="machine-details-overlay">
    <div class="machine-details">
      <button class="close-btn" @click="$emit('close')">Close</button>
      <h3>Machine Details</h3>
      <div class="details-grid">
        <div><strong>ID:</strong> {{ localMachine.id }}</div>
        <div><strong>Name:</strong> {{ localMachine.name }}</div>
        <div><strong>Attached Tool:</strong> {{ localMachine.attachedTool ? localMachine.attachedTool.name : 'None' }}</div>
        <div><strong>Tool Wear:</strong> {{ localMachine.attachedTool ? `${localMachine.attachedTool.wearLevel}%` : '0%' }}</div>
        <div><strong>Last Maintenance:</strong> N/A</div>
        <div><strong>Next Maintenance:</strong> N/A</div>
      </div>
      <div class="action-buttons">
        <button class="assign-btn" @click="showToolModal = true">Assign a tool</button>
        <button class="maintenance-btn" @click="showMaintenanceModal = true">Register a maintenance</button>
        <button class="history-btn" @click="showHistoryModal = true">Maintenance history</button>
      </div>

      <!-- Модальное окно для выбора инструмента -->
      <div v-if="showToolModal" class="tool-modal-overlay">
        <div class="tool-modal">
          <h4>Select Tool</h4>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tool in availableTools" :key="tool.id" @click="selectTool(tool)" class="tool-row">
                <td>{{ tool.name }}</td>
                <td>{{ tool.type }}</td>
                <td><button @click.stop="selectTool(tool)">Select</button></td>
              </tr>
            </tbody>
          </table>
          <button class="close-modal-btn" @click="showToolModal = false">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MachineDetails',
  props: {
    machine: {
      type: Object,
      required: true,
    },
    tools: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      showToolModal: false,
      localMachine: { ...this.machine }, // Локальная копия машины для реактивного обновления
    };
  },
  computed: {
    availableTools() {
      return this.tools.filter(tool => tool.status !== 'Scrapped');
    },
  },
  watch: {
    // Синхронизируем localMachine с пропсом machine при его изменении (например, при повторном открытии)
    machine(newMachine) {
      this.localMachine = { ...newMachine };
    },
  },
  methods: {
    getStatusClass(status) {
      return {
        'status-red': status === 'Offline' || status === 'Scrapped',
        'status-yellow': status === 'In Storage',
        'status-green': status === 'Attached',
      };
    },
    getWearClass(wearLevel) {
      if (wearLevel >= 80) return 'wear-red';
      if (wearLevel >= 50) return 'wear-yellow';
      return 'wear-green';
    },
    selectTool(tool) {
      this.localMachine.attachedTool = tool; // Обновляем локальную копию сразу
      const updatedMachine = { ...this.localMachine }; // Создаём копию для эмиссии
      this.$emit('update-machine', updatedMachine); // Отправляем обновление родителю
      this.showToolModal = false;
    },
  },
};
</script>

<style scoped>
.machine-details-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.machine-details {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #c82333;
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.details-grid div {
  padding: 5px 0;
}

.status-red {
  color: #dc3545;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.assign-btn,
.maintenance-btn,
.history-btn {
  padding: 8px 16px;
  background-color: #1a2a44;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.assign-btn:hover,
.maintenance-btn:hover,
.history-btn:hover {
  background-color: #2c3e50;
}

.tool-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.tool-modal {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.tool-modal h4 {
  margin-bottom: 10px;
  color: #333;
}

.tool-modal table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
}

.tool-modal th,
.tool-modal td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.tool-modal th {
  background-color: #f4f4f4;
  color: #333;
  font-weight: 600;
}

.tool-row:hover {
  background-color: #f9f9f9;
  cursor: pointer;
}

.wear-green {
  color: #28a745;
  font-weight: bold;
}

.wear-yellow {
  color: #ffc107;
  font-weight: bold;
}

.wear-red {
  color: #dc3545;
  font-weight: bold;
}

.close-modal-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.close-modal-btn:hover {
  background-color: #c82333;
}
</style>