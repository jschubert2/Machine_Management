<template>
  <div class="dashboard">
    <h2>Dashboard</h2>

    <div class="controls">
      <select v-model="selectedMachine" @change="fetchMetrics">
        <option disabled value="">Select a machine</option>
        <option v-for="machine in machines" :key="machine.id" :value="machine.name">
          {{ machine.name }}
        </option>
      </select>

      <select v-model="timeRange" @change="fetchMetrics">
        <option :value="7">Last 7 days</option>
        <option :value="30">Last 30 days</option>
        <option :value="365">Last year</option>
      </select>

      <button @click="importCsv" :disabled="loading">Import CSV</button>
    </div>

    <div class="metrics">
      <div class="metric">
        <h3>OEE</h3>
        <p>{{ average.oee }}%</p>
      </div>
      <div class="metric">
        <h3>Availability</h3>
        <p>{{ average.availability }}%</p>
      </div>
      <div class="metric">
        <h3>Performance</h3>
        <p>{{ average.performance }}%</p>
      </div>
      <div class="metric">
        <h3>Quality</h3>
        <p>{{ average.quality }}%</p>
      </div>
    </div>

    <canvas ref="chartCanvas" width="800" height="300"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'DashboardView',
  data() {
    return {
      machines: [],
      selectedMachine: '',
      timeRange: 7,
      average: {
        oee: 0,
        availability: 0,
        performance: 0,
        quality: 0
      },
      chart: null,
      loading: false
    };
  },
  methods: {
    async importCsv() {
      this.loading = true;
      try {
        await axios.post('http://localhost:5000/import-csv');
        await this.fetchMachines();
        if (this.selectedMachine) await this.fetchMetrics();
      } catch (error) {
        alert('Failed to import CSV');
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async fetchMachines() {
      try {
        const res = await axios.get('http://localhost:5000/machines', {
          params: { page: 1, per_page: 100 }
        });
        this.machines = res.data.machines;
        if (this.machines.length && !this.selectedMachine) {
          this.selectedMachine = this.machines[0].name;
          await this.fetchMetrics();
        }
      } catch (error) {
        console.error('Failed to load machines', error);
      }
    },
    async fetchMetrics() {
      if (!this.selectedMachine) return;

      try {
        const machine = this.machines.find(m => m.name === this.selectedMachine);
        if (!machine) return;

        const id = machine.id;
        const days = this.timeRange;

        const metricTypes = ['oee', 'availability', 'performance', 'output_quality'];
        const metricResults = {};

        for (const type of metricTypes) {
          const res = await axios.get(`http://localhost:5000/machines/${id}/dashboard/${type}`, {
            params: { days }
          });

          const values = res.data.data.map(m => m.value);
          const average = values.length ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2) : 0;

          metricResults[type] = {
            values: values,
            average: average,
            timestamps: res.data.data.map(m => m.timestamp)
          };
        }

        this.average = {
          oee: metricResults.oee.average,
          availability: metricResults.availability.average,
          performance: metricResults.performance.average,
          quality: metricResults.output_quality.average
        };

        const datasets = metricTypes.map(type => ({
          label: type,
          data: metricResults[type].values,
          borderColor: this.getColor(type),
          fill: false,
          tension: 0.1
        }));

        if (this.chart) this.chart.destroy();
        const ctx = this.$refs.chartCanvas.getContext('2d');
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: metricResults.oee.timestamps,
            datasets
          },
          options: {
            responsive: true,
            scales: {
              y: {
                min: 0,
                max: 100
              }
            }
          }
        });

      } catch (error) {
        console.error('Failed to load metrics', error);
      }
    },
    getColor(key) {
      return {
        oee: '#007bff',
        availability: '#28a745',
        performance: '#ffc107',
        output_quality: '#dc3545'
      }[key] || '#000';
    }
  },
  watch: {
    selectedMachine() {
      this.fetchMetrics();
    },
    timeRange() {
      this.fetchMetrics();
    }
  },
  mounted() {
    this.fetchMachines();
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

select, button {
  padding: 8px 12px;
  font-size: 1em;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.metric {
  background-color: #fff;
  padding: 16px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  text-align: center;
}

.metric h3 {
  margin: 0;
  font-size: 1.2em;
  color: #1a2a44;
}

.metric p {
  margin: 8px 0 0;
  font-size: 1.6em;
  font-weight: bold;
  color: #007bff;
}
</style>
