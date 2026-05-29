import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path:'/', name:'Home', component: () => import('@/views/SearchFormView.vue')},
        {path:'/register', name:'Register', component: () => import('@/views/RegistrationFormView.vue')},
        {path:'/login', name:'Login', component: () => import('@/views/LoginFormView.vue')},
        {path:'/results', name:'results', component: () => import('@/views/ResultList.vue')},
        {path:'/tour/:id', name:'tour', component: () => import('@/views/Resultpage.vue')},
    ],
})

export default router
