import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Logout from '../views/Logout.vue';
import Register from '../views/Register.vue';
import User from '../views/User.vue';
import AddItem from '../views/AddItem.vue';
import EditItem from '../views/EditItem.vue';
import NotificationView from '../views/NotificationView.vue';
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
            title: '首页'
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
            title: '登录'
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: {
            title: '注册'
        }
    },
    {
        path: '/user',
        name: 'User',
        component: User,
        meta: {
            title: '我的'
        }
    },
    {
        path: '/logout',
        name: 'Logout',
        component: Logout,
        meta: {
            title: '登出确认'
        }
    },
    {
        path: '/additem',
        name: 'AddItem',
        component: AddItem,
        meta: {
            title: '添加物品'
        }
    },
    {
        path: '/edit/:id',
        name: 'EditItem',
        component: EditItem,
        meta: {
            title: '更新物品'
        }
    },
    {
        path: '/notifications',
        name: 'Notifications',
        component: NotificationView,
        meta: {
            title: '通知'
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = 'ReviveIt | ' + to.meta.title || 'ReviveIt';
    next();
});

export default router;