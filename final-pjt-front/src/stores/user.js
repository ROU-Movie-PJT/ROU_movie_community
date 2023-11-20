import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const token = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  const registerErrMsg = ref({})

  const loginErrMsg = ref({})

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
        console.log('로그인 성공')
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
        router.push({name: 'home'})
      })
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  return {token, API_URL, register, registerErrMsg, login, loginErrMsg, isLogin, logout}
}, { persist: true })