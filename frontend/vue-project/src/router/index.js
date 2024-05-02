import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import Debts from '@/views/Debts.vue'
import Records from '@/views/Records.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: App
    },
    {
      path: '/Debts',
      name: 'Debts',
      component: Debts
    },
    {
      path: '/Records',
      name: 'Records',
      component: Records
    }
  ]
})

export default router
