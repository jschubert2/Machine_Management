import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    machines: [],
  },
  mutations: {
    setMachines(state, machines) {
      state.machines = machines;
    },
    updateMachine(state, updatedMachine) {
      const index = state.machines.findIndex(m => m.id === updatedMachine.id);
      if (index !== -1) {
        state.machines[index] = { ...state.machines[index], ...updatedMachine };
      }
    },
  },
  actions: {
    async fetchMachines({ commit }) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 50 },
        });
        commit('setMachines', response.data.machines);
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    },
  },
});