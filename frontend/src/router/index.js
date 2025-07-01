import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';
import MachineTable from '../views/MachineTable.vue';
import ToolTable from '../views/ToolTable.vue';
import RegisterMaintenance from '../views/RegisterMaintenance.vue';
import MaintenanceHistory from '../views/MaintenanceHistory.vue';
import LoginView from '../views/LoginView.vue';
import keycloak from '../keycloak';

const routes = [
  { path: '/', name: 'Login', component: LoginView },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/machines', name: 'Machines', component: MachineTable, meta: { requiresAuth: true } },
  { path: '/tools', name: 'Tools', component: ToolTable, meta: { requiresAuth: true } },
  { path: '/register-maintenance', name: 'RegisterMaintenance', component: RegisterMaintenance, meta: { requiresAuth: true } },
  { path: '/maintenance-history', name: 'MaintenanceHistory', component: MaintenanceHistory, meta: { requiresAuth: true } },
  { path: '/:catchAll(.*)', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !keycloak.authenticated) {
    next('/');
  } else if (to.path === '/' && keycloak.authenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;