/**
 * Vuex Store Configuration
 *
 * This store module manages the global application state for machines.
 * It includes reactive state, mutation logic to update it, and asynchronous
 * actions to fetch data from the backend API.
 */

import { createStore } from 'vuex';
import axios from 'axios';

/**
 * Create Vuex store instance.
 * State:
 * - machines: holds the list of all production machines
 * Mutations:
 * - setMachines: replaces the entire machine list
 * - updateMachine: updates a single machine in-place by ID
 * Actions:
 * - fetchMachines: retrieves machine data from the backend and commits it to the store
 */
export default createStore({
  state: {
    // List of all machine objects in the system
    machines: [],
  },

  mutations: {
    /**
     * Replaces the existing list of machines with a new one.
     * @param {Object} state - Vuex state object
     * @param {Array} machines - Array of machine objects from the backend
     */
    setMachines(state, machines) {
      state.machines = machines;
    },

    /**
     * Updates an existing machine in the state array by ID.
     * If the machine is found, its properties are merged with the updated values.
     * @param {Object} state - Vuex state object
     * @param {Object} updatedMachine - Machine object containing updated values
     */
    updateMachine(state, updatedMachine) {
      const index = state.machines.findIndex(m => m.id === updatedMachine.id);
      if (index !== -1) {
        state.machines[index] = { ...state.machines[index], ...updatedMachine };
      }
    },
  },

  actions: {
    /**
     * Fetches the first page of machine data from the backend API.
     * Commits the result using the setMachines mutation.
     * Logs an error if the request fails.
     *
     * @param {Function} commit - Vuex commit function
     */
    async fetchMachines({ commit }) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/machines', {
          params: { page: 1, per_page: 50 }, // Pagination parameters
        });
        commit('setMachines', response.data.machines);
      } catch (error) {
        console.error('Error fetching machines:', error); // Log for debugging
      }
    },
  },
});
