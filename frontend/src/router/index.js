// Vue Router configuration for the application
import { createRouter, createWebHistory } from 'vue-router';

// View components used for routing
import DashboardView from '../views/DashboardView.vue';
import MachineTable from '../views/MachineTable.vue';
import ToolTable from '../views/ToolTable.vue';
import RegisterMaintenance from '../views/RegisterMaintenance.vue';
import MaintenanceHistory from '../views/MaintenanceHistory.vue';
import LoginView from '../views/LoginView.vue';

import keycloak from '../keycloak'; // Keycloak instance for authentication control

/**
 * Application route definitions.
 * Each route maps a path to a Vue component.
 * `meta.requiresAuth` marks routes that require user to be authenticated via Keycloak.
 */
const routes = [
  { path: '/', name: 'Login', component: LoginView }, // Public login view

  { path: '/dashboard', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/machines', name: 'Machines', component: MachineTable, meta: { requiresAuth: true } },
  { path: '/tools', name: 'Tools', component: ToolTable, meta: { requiresAuth: true } },
  { path: '/register-maintenance', name: 'RegisterMaintenance', component: RegisterMaintenance, meta: { requiresAuth: true } },
  { path: '/maintenance-history', name: 'MaintenanceHistory', component: MaintenanceHistory, meta: { requiresAuth: true } },

  // Redirect all unknown routes to login page
  { path: '/:catchAll(.*)', redirect: '/' }
];

/**
 * Creates a Vue Router instance using HTML5 history mode
 * and applies the defined routes.
 */
const router = createRouter({
  history: createWebHistory(),
  routes
});

/**
 * Global navigation guard
 *
 * Purpose:
 * - Prevents unauthenticated users from accessing protected routes
 * - Prevents authenticated users from returning to login page manually
 *
 * @param {RouteLocationNormalized} to - The target route being navigated to
 * @param {RouteLocationNormalized} from - The current route being navigated from
 * @param {Function} next - Function to resolve navigation
 */
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !keycloak.authenticated) {
    // Redirect unauthenticated users to login
    next('/');
  } else if (to.path === '/' && keycloak.authenticated) {
    // Redirect already logged-in users away from login page
    next('/dashboard');
  } else {
    next(); // Allow navigation
  }
});

export default router;
