/**DashboardView.vue
 *
 * Purpose:
 * A dynamic dashboard page that allows users to:
 * - Select a machine and time range
 * - View KPIs (OEE, Availability, Performance, Quality)
 * - Toggle which metrics appear in the chart
 * - Visualize time-series KPI data using Chart.js
 * 
 * Key features:
 * - Reactive KPI data and chart updating
 * - Adaptive time formatting based on date range
 * - Metric visibility toggle using checkbox UI
 * - REST API integration with Flask backend
 * - Uses Chart.js and date-fns for time-based charts
 */

<template>
  <!-- Main container for the dashboard page -->
  <div class="dashboard">
    <h2>Dashboard</h2>

    <!-- Machine and time range selection controls -->
    <div class="controls">
      
      <!-- Dropdown for selecting a machine (bound to selectedMachineId) -->
      <select v-model="selectedMachineId">
        <option disabled value="">Select a machine</option>
        <option v-for="m in machines" :key="m.id" :value="m.id">
          {{ m.name }}
        </option>
      </select>

      <!-- Dropdown for selecting the number of days to display KPI data -->
      <select v-model.number="timeRange">
        <option v-for="d in ranges" :key="d" :value="d">
          Last {{ labelOf(d) }}
        </option>
      </select>
    </div>

    <!-- Static KPI boxes showing the current values of each metric -->
    <div class="kpi-squares">
      <div class="kpi-square oee">
        <h3>OEE</h3>
        <p>{{ kpi.oee }}%</p>
      </div>
      <div class="kpi-square availability">
        <h3>Availability</h3>
        <p>{{ kpi.availability }}%</p>
      </div>
      <div class="kpi-square performance">
        <h3>Performance</h3>
        <p>{{ kpi.performance }}%</p>
      </div>
      <div class="kpi-square quality">
        <h3>Quality</h3>
        <p>{{ kpi.output_quality }}%</p>
      </div>
    </div>

    <!-- Additional KPI cards rendered dynamically using the MetricCard component -->
    <div class="metrics">
      <MetricCard
        v-for="card in cards"
        :key="card.label"
        :label="card.label"
        :value="card.value"
      />
    </div>

    <!-- Checkboxes that control the visibility of each metric in the chart -->
    <div class="metric-toggle">
      <label v-for="t in metricTypes" :key="t">
        <input type="checkbox" :value="t" v-model="visibleMetrics" />
        {{ pretty(t) }}
      </label>
    </div>

    <!-- Chart.js canvas element for rendering time-series KPI data -->
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import { getISOWeek, startOfISOWeek, formatISO } from 'date-fns';

// Define available metric types and their display colors
const metricTypes = ['oee', 'availability', 'performance', 'output_quality'] as const;
const colorMap = {
  oee: '#007bff',
  availability: '#28a745',
  performance: '#ffc107',
  output_quality: '#dc3545'
};

// Available time range options in days
const ranges = [7, 30, 90] as const;

// Machine selection and data containers
const machines = ref<{ id: string; name: string }[]>([]);
const selectedMachineId = ref('');
const timeRange = ref(7);
const visibleMetrics = ref<string[]>([...metricTypes]);
const loading = ref(false);

// Holds the latest raw backend response per metric
let latestRaw: Record<string, any[]> | null = null;

// Reactive KPI container
const kpi = reactive<Record<string, number>>({
  oee: 0,
  availability: 0,
  performance: 0,
  output_quality: 0
});

// Axios instance for API calls
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 8000
});

// Format a metric type to readable label
const pretty = (t: string) => t.replace('_', ' ').toUpperCase();

// Convert days to label for dropdown (e.g., 30 → "30 days")
const labelOf = (d: number) => (d === 90 ? '3 months' : `${d} days`);

// Compute average of an array
function avg(arr: number[]): number {
  return arr.length ? +(arr.reduce((a, b) => a + b) / arr.length).toFixed(2) : 0;
}

// MetricCard component shown below KPI blocks
const MetricCard = {
  props: { label: String, value: [String, Number] },
  template: `<div class="metric"><h3>{{ label }}</h3><p>{{ value }}%</p></div>`
};

// Derived metric card values based on current KPIs
const cards = computed(() => [
  { label: 'OEE', value: kpi.oee },
  { label: 'Availability', value: kpi.availability },
  { label: 'Performance', value: kpi.performance },
  { label: 'Quality', value: kpi.output_quality }
]);

// Chart reference and instance
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

/**
 * Builds or updates the KPI line chart using Chart.js.
 * Called after metrics are loaded and chart canvas is ready.
 */
function buildOrUpdateChart(dataset: any[]) {
  const ctx = chartCanvas.value?.getContext('2d');
  if (!ctx) return;

  const allValues = dataset.flatMap(d => d.data as number[]);
  const yMin = Math.max(0, Math.min(...allValues) - 5);
  const yMax = Math.min(100, Math.max(...allValues) + 5);

  if (!chart) {
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dataset[0].labels,
        datasets: dataset
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            position: 'top',
            onClick: (_, legendItem) => {
              const type = metricTypes[legendItem.datasetIndex as number];
              toggleMetric(type);
            }
          },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.dataset.label}: ${ctx.formattedValue}%`
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: { unit: unitFor(timeRange.value), tooltipFormat: 'yyyy-MM-dd' },
            ticks: { maxRotation: 45 }
          },
          y: {
            min: yMin,
            max: yMax,
            ticks: { callback: v => `${v}%` }
          }
        }
      }
    });
  } else {
    chart.options.scales!.x['time'].unit = unitFor(timeRange.value);
    chart.data.labels = dataset[0].labels;
    chart.data.datasets = dataset;
    chart.options.scales!.y.min = yMin;
    chart.options.scales!.y.max = yMax;
    chart.update();
  }
}

// Return the time unit (day/week/month) based on selected range
function unitFor(days: number) {
  if (days <= 30) return 'day';
  if (days <= 90) return 'week';
  return 'month';
}

/**
 * Fetches the machine list from the backend.
 * Automatically selects the first machine on initial load.
 */
async function fetchMachines() {
  const { data } = await api.get('/machines', { params: { page: 1, per_page: 100 } });
  machines.value = data.machines;
  if (machines.value.length && !selectedMachineId.value) {
    selectedMachineId.value = machines.value[0].id;
  }
}

/**
 * Fetches KPI data for the selected machine and range,
 * calculates averages, and updates the chart accordingly.
 */
async function fetchMetrics() {
  if (!selectedMachineId.value) return;
  const id = selectedMachineId.value;
  const days = timeRange.value;
  const ctrl = new AbortController();

  try {
    const raw: Record<string, { value: number; timestamp: string }[]> = {};

    await Promise.all(
      metricTypes.map(async type => {
        const res = await api.get(`/machines/${id}/dashboard/${type}`, {
          params: { days },
          signal: ctrl.signal
        });
        raw[type] = res.data.data;
      })
    );

    latestRaw = raw;

    const datasets = metricTypes.map(type => {
      const { values, labels } = prepareSeries(raw[type]);
      kpi[type] = avg(values);

      return {
        label: pretty(type),
        data: values,
        labels,
        borderColor: colorMap[type],
        tension: 0.2,
        pointRadius: 3,
        pointHoverRadius: 5,
        hidden: !visibleMetrics.value.includes(type)
      };
    });

    await nextTick();
    buildOrUpdateChart(datasets);
  } catch (e) {
    if (axios.isCancel(e)) return;
    console.error(e);
  }
}

/**
 * Aggregates and averages KPI data by week if range = 90 days,
 * or returns raw timestamped series for shorter ranges.
 */
function prepareSeries(src: { value: number; timestamp: string }[]) {
  if (timeRange.value === 90) {
    const weekBuckets: Record<string, { sum: number; count: number; label: string }> = {};

    for (const entry of src) {
      const date = new Date(entry.timestamp);
      const weekKey = `${date.getFullYear()}-W${getISOWeek(date)}`;
      const label = formatISO(startOfISOWeek(date), { representation: 'date' });

      if (!weekBuckets[weekKey]) {
        weekBuckets[weekKey] = { sum: 0, count: 0, label };
      }

      weekBuckets[weekKey].sum += entry.value;
      weekBuckets[weekKey].count += 1;
    }

    const sorted = Object.values(weekBuckets).sort((a, b) => a.label.localeCompare(b.label));

    return {
      values: sorted.map(w => +(w.sum / w.count).toFixed(2)),
      labels: sorted.map(w => w.label)
    };
  }

  return {
    values: src.map(d => d.value),
    labels: src.map(d => d.timestamp)
  };
}

/**
 * Toggles visibility of a KPI line in the chart.
 */
function toggleMetric(type: string) {
  const idx = visibleMetrics.value.indexOf(type);
  if (idx === -1) visibleMetrics.value.push(type);
  else visibleMetrics.value.splice(idx, 1);
}

// Reactively update chart visibility when checkbox selection changes
watch(visibleMetrics, () => {
  if (!chart) return;
  metricTypes.forEach((t, i) => {
    chart!.setDatasetVisibility(i, visibleMetrics.value.includes(t));
  });
  chart!.update();
});

/**
 * Sends request to reset and import CSV data to the backend.
 * Reloads the machines list on completion.
 */
async function importCsv() {
  loading.value = true;
  try {
    await api.post('/import-csv');
    await fetchMachines();
  } finally {
    loading.value = false;
  }
}

// Lifecycle hooks
onMounted(fetchMachines);
watch([selectedMachineId, timeRange], fetchMetrics);
onBeforeUnmount(() => {
  chart?.destroy();
});
</script>

<style scoped>
.dashboard {
  padding: 0 20px 20px 20px;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

select,
button {
  padding: 8px 12px;
  font-size: 1em;
}

.kpi-squares {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.kpi-square {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.kpi-square h3 {
  margin: 0;
  font-size: 1.1em;
  color: #1a2a44;
}

.kpi-square p {
  margin: 8px 0 0;
  font-size: 1.8em;
  font-weight: 600;
  color: #000;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.metric {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.metric h3 {
  margin: 0;
  font-size: 1.2em;
  color: #1a2a44;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
}

canvas {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 100%;
}

h2 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.5em;
  color: #333;
}
</style>

