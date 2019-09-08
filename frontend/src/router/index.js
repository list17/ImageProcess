import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login.vue'
import register from '@/components/Register.vue'
import help from '@/components/Help.vue'
import image_processing from '@/components/ImageProcess.vue'
//const login = resolve => require(['@/components/login'], resolve)

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: login,
      alias: '/login',
      meta: {
        navbar_active: false,
        icon_active: false,
        title: '登录',
      }
    }, {
      path: '/image_processing',
      name: 'image_processing',
      component: image_processing,
      meta: {
        requireAuth: false,
        navbar_active: false,
        icon_active: true,
        title: '进行图像处理',
      }
    } ,{
      path: '/register',
      name: 'register',
      component: register,
      meta: {
        navbar_active: false,
        icon_active: false,
        title: '注册',
      }
    }, {
      path: '/help',
      name: 'help',
      component: help,
    }
  ]
})
