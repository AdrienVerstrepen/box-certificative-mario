import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path:'/', name:'Home', component: () => import('@/views/SearchFormView.vue')},
        {path:'/register', name:'Register', component: () => import('@/views/RegistrationFormView.vue')},
        {path:'/login', name:'Login', component: () => import('@/views/LoginFormView.vue')},
    ],
})

export default router
