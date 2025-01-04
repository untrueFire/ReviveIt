import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from '@/stores'
import { updateUser } from '@/utils/api'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('@/views/HomeView.vue'),
            meta: {
                title: '首页',
            },
        },
        {
            path: '/search',
            name: 'AdvancedSearch',
            component: () => import('@/views/AdvancedSearch.vue'),
            meta: {
                title: '高级搜索',
            },
        },
        {
            path: '/auth',
            name: 'Auth',
            component: () => import('@/views/AuthView.vue'),
            meta: {
                title: '认证',
            },
        },
        {
            path: '/user',
            name: 'User',
            component: () => import('@/views/UserView.vue'),
            meta: {
                title: '个人中心',
                needLogin: true,
            },
        },
        {
            path: '/addItem',
            name: 'AddItem',
            component: () => import('@/views/AddItem.vue'),
            meta: {
                title: '添加物品',
                needLogin: true,
            },
        },
        {
            path: '/edit/:id',
            name: 'EditItem',
            component: () => import('@/views/EditItem.vue'),
            meta: {
                title: '更新物品',
                needLogin: true,
            },
        },
        {
            path: '/notifications',
            name: 'Notifications',
            component: () => import('@/views/NotificationView.vue'),
            meta: {
                title: '通知',
                needLogin: true,
            },
        },
        {
            path: '/woodenFish',
            name: 'WoodenFish',
            component: () => import('@/views/WoodenFishView.vue'),
            meta: {
                title: '电子木鱼',
                needLogin: true,
            },
        },
        {
            path: '/view/:id',
            name: 'ViewItem',
            component: () => import('@/views/ViewItem.vue'),
            meta: {
                title: '物品详情',
            },
        },
        {
            path: '/admin/:pathMatch(.*)*',
            name: 'Admin',
            component: () => import('@/views/AdminView.vue'),
            meta: {
                title: '管理',
                needLogin: true,
            },
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'NotFound',
            component: () => import('@/views/NotFound.vue'),
        },
    ],
})

router.beforeEach(async (to, _from, next) => {
    document.title = 'ReviveIt | ' + to.meta.title || 'ReviveIt'
    const store = useStore()
    await updateUser()
    if (to.meta.needLogin && !store.isLoggedIn) {
        const message = window.$message
        message.error('需要登录')
        next({ name: 'Auth' })
    } else {
        next()
    }
})

export default router
