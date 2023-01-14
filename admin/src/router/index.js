import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/dashboard',
    component: Home,
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: '/user',
        name: 'user',
        component: () => import('../views/User.vue')
      },
      {
        path: '/template',
        name: 'template',
        component: () => import('../views/Template.vue')
      },
      {
        path: '/history',
        name: 'history',
        component: () => import('../views/History.vue')
      },
      {
        path: '/send',
        name: 'send',
        component: () => import('../views/Send.vue')
      },
      {
        path: '/mutiple',
        name: 'mutiple',
        component: () => import('../views/Mutiple.vue')
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
