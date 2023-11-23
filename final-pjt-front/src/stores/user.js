import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const token = ref(null)
  const user = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  const registerErrMsg = ref({})

  const loginErrMsg = ref({})
  const changePasswordErrMsg = ref({})

  const register = function(payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const email = payload.email
    const region = payload.region
    const birth = payload.birth

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, email, region, birth
      }
    }) 
      .then(() => {
        console.log('회원가입 완료')
        registerErrMsg.value = {}
        router.push({name: 'login'})
      })
      .catch(err => {
        registerErrMsg.value = {}
        console.log(err.response.data)
        for (const key in err.response.data) {
          registerErrMsg.value[key] = err.response.data[key][0]
        }
        console.log(registerErrMsg.value)
      })
  }

  const userInfo = ref()

  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${user.value}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        userInfo.value = res.data
      })
  }

  const login = function (payload) {
    const username = payload.username
    const password = payload.password

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        loginErrMsg.value = {}
        token.value = res.data.key
        user.value = res.data.user
        localStorage.setItem('username', username)
        getUserInfo()
        console.log('로그인 성공')
        loginErrMsg.value = {}
        router.push({name: 'home'})
      })
      .catch(err => {
        loginErrMsg.value = {}
        console.log(err)
        for (const key in err.response.data) {
          loginErrMsg.value[key] = err.response.data[key][0]
        }
      })
  }

  const logout = function () {
    axios({
      method: 'POST',
      url: `${API_URL}/accounts/logout/`,
    })
      .then(() => {
        token.value = null
        localStorage.setItem('username', '')
        userInfo.value = null
        router.push({name: 'login'})
      })
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const updateUserInfo = function (formData) {
    axios({
      method: 'put',
      url: `${API_URL}/accounts/profile/${user.value}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: formData,
    })
      .then(res => {
        userInfo.value = res.data
        router.push({name: 'profile', params: {userId: user.value}})
      })
  }

  const changePassword = function (payload) {
    const new_password1 = payload.new_password1
    const new_password2 = payload.new_password2
    axios({
      method: 'post',
      url: `${API_URL}/accounts/password/change/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        new_password1,
        new_password2
      }
    })
      .then(() => {
        console.log('비밀번호 변경 완료!')
        changePasswordErrMsg.value = {}
        router.push({name: 'profile', params: {userId: user.value}})
      })
      .catch(err => {
        changePasswordErrMsg.value = {}
        for (const key in err.response.data) {
          changePasswordErrMsg.value[key] = err.response.data[key][0]
        }
      })
  }

  const resign = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/delete/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        logout()
      })
  }

  return {
    token, 
    API_URL, 
    register, 
    registerErrMsg, 
    login, 
    loginErrMsg, 
    isLogin, 
    logout, 
    user, 
    getUserInfo, 
    userInfo, 
    updateUserInfo,
    changePassword,
    changePasswordErrMsg,
    resign
  }
}, { persist: true })