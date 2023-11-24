<script setup>
  import { ref } from 'vue'
  import { useUserStore } from '../stores/user';
  import { RouterLink } from 'vue-router';

  const store = useUserStore()

  const username = ref('')
  const password = ref('')

  const login = function () {
    const payload = {
      username: username.value,
      password: password.value
    }

    store.login(payload)
  }
</script>

<template>
  <div class="content-box">
    <div class="login-box">
      <h2><b>로그인</b></h2>
      <form class="login-form" @submit.prevent="login">
        <div class="login-item">
          <label for="username">아이디</label>
          <input required class="input" type="text" id="username" v-model.trim="username">
        </div>
        <div class="login-item">
          <label for="password">비밀번호</label>
          <input required class="input" type="password" id="password" v-model.trim="password">
        </div>
        <hr>
        <span class="sm-font" v-if="store.loginErrMsg.non_field_errors">* {{ store.loginErrMsg.non_field_errors }}</span>
        <button type="submit" class="login-btn">로그인</button>
      </form>
      <RouterLink :to="{name: 'register'}">회원가입</RouterLink>
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

  .login-box {
    text-align: center;
    width: 40%;
    background-color: gainsboro;
    padding: 1.5rem;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }

  .login-form {
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }
  
  .login-item {
    display: flex;
    flex-direction: column;
    text-align: start;
    gap: .25rem;
  }

  .login-btn {
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
