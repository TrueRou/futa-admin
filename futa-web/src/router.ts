import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/pages/dashboard.vue'
import Admin from './pages/admin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin
    }
  ]
})

export default router
