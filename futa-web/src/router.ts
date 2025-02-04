import { createRouter, createWebHistory } from 'vue-router'
import Index from '@/pages/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:path?',
      name: 'Page',
      component: Index
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/pages/admin/index.vue'),
      children: [
        {
          path: 'pages',
          name: 'AdminPages',
          component: () => import('@/pages/admin/pages/index.vue')
        },
        {
          path: 'reports',
          name: 'AdminReports',
          component: () => import('@/pages/admin/reports/index.vue')
        },
        {
          path: 'reports/:id',
          name: 'AdminReport',
          component: () => import('@/pages/admin/reports/[id]/index.vue')
        },
      ]
    }
  ]
})

export default router
