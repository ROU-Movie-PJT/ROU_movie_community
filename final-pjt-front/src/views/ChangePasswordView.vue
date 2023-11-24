<script setup>
  import { ref } from 'vue'
  import { useUserStore } from '../stores/user';

  const store = useUserStore()

  const password1 = ref('')
  const password2 = ref('')

  const changePassword = function () {
    const payload = {
      new_password1: password1.value,
      new_password2: password2.value
    }

    store.changePassword(payload)
  }
</script>

<template>
  <div class="content-box">
    <div class="login-box">
      <h2><b>비밀번호 변경</b></h2>
      <form class="login-form" @submit.prevent="changePassword">
        <div class="login-item">
          <label for="password1">새 비밀번호</label>
          <input required class="input" type="password" id="password1" v-model.trim="password1">
        </div>
        <div class="login-item">
          <label for="password2">새 비밀번호 확인</label>
          <input required class="input" type="password" id="password2" v-model.trim="password2">
        </div>
        <span class="sm-font" v-if="store.changePasswordErrMsg.new_password2">* {{ store.changePasswordErrMsg.new_password2 }}</span>
        <hr>
        <button type="submit" class="login-btn">비밀번호 변경</button>
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
