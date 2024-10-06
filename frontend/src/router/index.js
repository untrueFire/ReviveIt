import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Logout from '../views/Logout.vue';
import Register from '../views/Register.vue';
import User from '../views/User.vue';
import AddItem from '../views/AddItem.vue';
import EditItem from '../views/EditItem.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/user',
    name: 'User',
    component: User,
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/additem',
    name: 'AddItem',
    component: AddItem
  },
  {
    path: '/edit/:id',
    name: 'EditItem',
    component: EditItem
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;