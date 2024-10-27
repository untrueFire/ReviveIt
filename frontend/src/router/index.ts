import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import RegisterView from '../views/RegisterView.vue'
import UserView from '../views/UserView.vue'
import AddItem from '../views/AddItem.vue'
import EditItem from '../views/EditItem.vue'
import NotificationView from '../views/NotificationView.vue'
import WoodenFishView from '../views/WoodenFishView.vue'
import ViewItem from '../views/ViewItem.vue'
import NotFound from '../views/NotFound.vue'
import { useStore } from '../stores'
import { updateUser } from '../utils/api'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HomeView,
            meta: {
                title: '首页',
            },
        },
        {
            path: '/login',
            name: 'Login',
            component: LoginView,
            meta: {
                title: '登录',
            },
        },
        {
            path: '/register',
            name: 'Register',
            component: RegisterView,
            meta: {
                title: '注册',
            },
        },
        {
            path: '/user',
            name: 'User',
            component: UserView,
            meta: {
                title: '我的',
                needLogin: true,
            },
        },
        {
            path: '/logout',
            name: 'Logout',
            component: LogoutView,
            meta: {
                title: '登出确认',
                needLogin: true,
            },
        },
        {
            path: '/addItem',
            name: 'AddItem',
            component: AddItem,
            meta: {
                title: '添加物品',
                needLogin: true,
            },
        },
        {
            path: '/edit/:id',
            name: 'EditItem',
            component: EditItem,
            meta: {
                title: '更新物品',
                needLogin: true,
            },
        },
        {
            path: '/notifications',
            name: 'Notifications',
            component: NotificationView,
            meta: {
                title: '通知',
                needLogin: true,
            },
        },
        {
            path: '/woodenFish',
            name: 'WoodenFish',
            component: WoodenFishView,
            meta: {
                title: '电子木鱼',
                needLogin: true,
            },
        },
        {
            path: '/view/:id',
            name: 'ViewItem',
            component: ViewItem,
            meta: {
                title: '物品详情',
                needLogin: true,
            },
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'NotFound',
            component: NotFound,
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
        next({ name: 'Login' })
    } else {
        next()
    }
})

export default router
