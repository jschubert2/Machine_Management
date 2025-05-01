import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';
import MachineTable from '../views/MachineTable.vue';
import ToolTable from '../views/ToolTable.vue';

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/machines', name: 'Machines', component: MachineTable },
  { path: '/tools', name: 'Tools', component: ToolTable },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;