import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DetailView from '../views/DetailView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import CreateView from '../views/CreateView.vue'
import UpdateUserInfoView from '../views/UpdateUserInfoView.vue'
import SearchResultView from '../views/SearchResultView.vue'
import ProfileView from '../views/ProfileView.vue'
import ChangePasswordView from '../views/ChangePasswordView.vue'

const router = createRouter({
  scrollBehavior(to, from) {
    return {top: 0}
  },
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/movies/:id',
      name: 'movie_detail',
      component: DetailView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/community/create/:movieId',
      name: 'create',
      component: CreateView
    },
    {
      path: '/accounts/update',
      name: 'update_account',
      component: UpdateUserInfoView
    },
    {
      path: '/search/:keyword',
      name: 'search',
      component: SearchResultView
    },
    {
      path: '/profile/:userId',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/accounts/change_password',
      name: 'change_password',
      component: ChangePasswordView
    }
  ]
})

export default router
