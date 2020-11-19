import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import {constantRoutes, resetRouter,notFoundRouter} from '@/router'
import routerFormat from '@/utils/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    roles: [],
    routers: constantRoutes,
    addRouters: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
      state.roles = roles
  },
  SET_ROUTERS: (state, routers) => {
    state.addRouters = routers; //路由访问
    state.routers = [...(constantRoutes || []), ...(routers || []), ...(notFoundRouter || [])]; //菜单显示,404最后加入
    // state.routers = constantRouterMap.concat(routers).concat(notFoundRouter); //菜单显示,404最后加入
  },
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    let data = new FormData();
    let Base64 = require('js-base64').Base64;
    data.append('username',userInfo.username.trim());
    data.append('password', Base64.encode(userInfo.password));
    return new Promise((resolve, reject) => {
      login(data).then(response => {
        commit('SET_TOKEN', response.data.token);
        setToken(response.data.token);
        resolve();
      }).catch(error => {
        reject(error);
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { rows } = response.data
        if (!rows) {
          reject('Verification failed, please Login again.')
        }
        // commit('SET_AVATAR', avatar)
        commit('SET_ROUTERS', routerFormat(rows.routers))
        commit('SET_NAME', rows.user_name)
        commit('SET_ROLES', rows.role_code)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

