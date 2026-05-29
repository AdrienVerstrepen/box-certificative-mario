import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path:'/', name:'Home', component: () => import('@/views/SearchFormView.vue')},
        {
            path:'/register',
            name:'Register',
            component: () => import('@/views/RegistrationFormView.vue'),
            meta: { guestOnly: true },
        },
        {
            path:'/login',
            name:'Login',
            component: () => import('@/views/LoginFormView.vue'),
            meta: { guestOnly: true },
        },
        {path:'/results', name:'results', component: () => import('@/views/ResultList.vue')},
        {path:'/tour/:id', name:'tour', component: () => import('@/views/Resultpage.vue')},
    ],
})

router.beforeEach((to) => {
    const user = localStorage.getItem('user')
    if (to.meta.guestOnly && user) {
        return { name: 'Home' }
    }
})

export default router
