// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'core-js/features/promise';
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'

import VueCodeMirror from 'vue-codemirror-lite'
import CodeMirror from 'codemirror/lib/codemirror'
import ElementUI from 'element-ui'
import VueCookies from 'vue-cookies'
import axios from 'axios'

import 'url-search-params-polyfill'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/icon/iconfont.css'
import 'codemirror/lib/codemirror.css'
import util from './utils/util'
import VueBrowserUpdate from 'vue-browserupdate';

// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import 'highlight.js/styles/github.css'

axios.defaults.baseURL = '/api';
axios.defaults.withCredentials = false;

// store.commit('logout')

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          store.commit('logout');
          if (router.currentRoute.path !== 'login')
            router.replace({
              path: '/not_login',
            });
      }
    }
    return Promise.reject(error);
  }
);


Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(VueCodeMirror);
Vue.use(VueCookies);
Vue.use(util);
Vue.prototype.$axios = axios;
Vue.use(VueBrowserUpdate, {
  options: {
    required: {i: 11, f: 25, o: 17, s: 9, c: -3},
    insecure: true,
    api: 2018.12
  },
});

let routeList = []

router.beforeEach((to, from, next) => {
  // to.meta.routeList = routeList
  if (to.meta.requireAuth) {
    // if (router.app.$cookies.get('username') != null) {
    if (store.state.username) {
      next()
    } else {
      next('/not_login');
      // router.app.$message('请登录')
    }
  } else {
    next()
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
