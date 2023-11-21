<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '../stores/user';

  const store = useUserStore()

  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const email = ref('')
  const region = ref('')
  const birth = ref('')

  const register = function() {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      email: email.value,
      region: region.value,
      birth: birth.value
    }
    store.register(payload)
  }

</script>

<template>
  <div class="content-box">
    <div class="register-box">
      <h2><b>회원가입</b></h2>
      <form class="register-form">
        <div class="register-item">
          <label for="username">아이디</label>
          <span class="sm-font" v-if="store.registerErrMsg.username">* {{ store.registerErrMsg.username }}</span>
          <input required class="input" type="text" id="username" v-model="username">
        </div>
        <div class="register-item">
          <label for="password1">비밀번호</label>
          <span class="sm-font" v-if="store.registerErrMsg.password1">* {{ store.registerErrMsg.password1 }}</span>
          <input required class="input" type="password" id="password1" v-model="password1">
        </div>
        <div class="register-item">
          <label for="password2">비밀번호 재확인</label>
          <span class="sm-font" v-if="store.registerErrMsg.password2">* {{ store.registerErrMsg.password2 }}</span>
          <input required class="input" type="password" id="password2" v-model="password2">
        </div>
        <div class="register-item">
          <label for="email">이메일</label>
          <span class="sm-font" v-if="store.registerErrMsg.email">* {{ store.registerErrMsg.email }}</span>
          <input required class="input" type="email" id="email" v-model="email">
        </div>
        <div class="register-item">
          <label for="birth">생년월일</label>
          <span class="sm-font" v-if="store.registerErrMsg.birth">* {{ store.registerErrMsg.birth }}</span>
          <input required class="input" type="date" id="birth" v-model="birth">
        </div>
        <div class="register-item">
          <label for="region">지역</label>
          <span class="sm-font" v-if="store.registerErrMsg.region">* {{ store.registerErrMsg.region }}</span>
          <input required class="input" type="text" id="region" v-model="region">
        </div>
        <hr>
        <span class="sm-font" v-if="store.registerErrMsg.non_field_errors">* {{ store.registerErrMsg.non_field_errors }}</span>
        <button type="submit" @click.prevent="register" class="register-btn">가입</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
  .content-box {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .register-box {
    text-align: center;
    width: 40%;
    background-color: gainsboro;
    padding: 1.5rem;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }

  .register-form {
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }
  
  .register-item {
    display: flex;
    flex-direction: column;
    text-align: start;
    gap: .25rem;
  }

  .register-btn {
    width: 100%;
    border: none;
    background-color: #7B61FF;
    border-radius: 5px;
    color: white;
    padding: .5rem;
    height: 40px;
  }

  .input {
    height: 40px;
    border: none;
    border-radius: 5px;
    outline: none;
    padding: 0 .5rem;
  }

  .sm-font {
    font-size: small;
    color: red;
  }
</style>