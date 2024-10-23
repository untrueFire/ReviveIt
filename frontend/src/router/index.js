import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Logout from '../views/Logout.vue';
import Register from '../views/Register.vue';
import User from '../views/User.vue';
import AddItem from '../views/AddItem.vue';
import EditItem from '../views/EditItem.vue';
import NotificationView from '../views/NotificationView.vue';
import WoodenFishView from '../views/WoodenFishView.vue';
import ViewItem from '../views/ViewItem.vue';
import NotFound from '../views/NotFound.vue';
import { useStore } from '../store';
import { updateUser } from '../utils/api';
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
            title: '我的',
            needLogin: true
        }
    },
    {
        path: '/logout',
        name: 'Logout',
        component: Logout,
        meta: {
            title: '登出确认',
            needLogin: true
        }
    },
    {
        path: '/additem',
        name: 'AddItem',
        component: AddItem,
        meta: {
            title: '添加物品',
            needLogin: true
        }
    },
    {
        path: '/edit/:id',
        name: 'EditItem',
        component: EditItem,
        meta: {
            title: '更新物品',
            needLogin: true
        }
    },
    {
        path: '/notifications',
        name: 'Notifications',
        component: NotificationView,
        meta: {
            title: '通知',
            needLogin: true
        }
    },
    {
        path: '/woodenfish',
        name: 'WoodenFish',
        component: WoodenFishView,
        meta: {
            title: '电子木鱼',
            needLogin: true
        }
    },
    {
        path: '/view/:id',
        name: 'ViewItem',
        component: ViewItem,
        meta: {
            title: '物品详情',
            needLogin: true
        }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound
      }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, _from, next) => {
    document.title = 'ReviveIt | ' + to.meta.title || 'ReviveIt';
    const store = useStore();
    await updateUser();
    if (to.meta.needLogin && !store.isLoggedIn) {
        const message = window.$message;
        message.error('需要登录');
        next({'name': 'Login'});
    } else {
        next();
    }
});

export default router;