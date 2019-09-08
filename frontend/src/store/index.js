import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        routeList: [],
        username: '',
        userEmail: '',
        nickname: ''
    },
    mutations: {
        setRouteList(state, val) {
            state.routeList = val;
        },
        logout(state) {
            state.username = '';
            state.userEmail = '';
            state.nickname = '';
        },
        login(state, val) {
            state.username = val.username;
            state.userEmail = val.userEmail;
            state.nickname = val.nickname;
        },
        changeName(state, val) {
            state.nickname = val.nickname;
        }
    },
    plugins: [createPersistedState()]
})