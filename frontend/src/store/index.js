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
  },
  actions: {
    async fetchMachines({ commit }) {
      const response = await axios.get('http://127.0.0.1:5000/machines', {
        params: { page: 1, per_page: 100 } 
      });
      commit('setMachines', response.data.machines || []);
    },
  },
});