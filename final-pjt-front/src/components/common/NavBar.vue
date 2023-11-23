<script setup>
  import { computed } from 'vue'
  import { RouterLink } from 'vue-router'
  import { useUserStore } from '../../stores/user'

  const userStore = useUserStore()

  const isUser = computed(() => {
    return userStore.user !== null
  })
</script>

<template>
  <div class="navbar">
    <a class="home" href="/">
      <img class="logo" src="../../assets/logo.png" alt="logo">
    </a>
    <ul class="menu">
      <li>
        <RouterLink class="link" :to="{name: 'home'}">Home</RouterLink>
      </li>
      <li v-if="isUser">
        <RouterLink class="link" :to="{name: 'profile', params: {userId: userStore.user}}">Profile</RouterLink>
      </li>
      <li v-if="isUser">
        <RouterLink class="link" to="/">Quiz</RouterLink>
      </li>
      <li>
        <RouterLink class="link" :to="{name: 'community'}">Community</RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    background-color: #222222;
    width: 200px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    padding: 0;
    z-index: 501;
  }

  .home {
    display: block;
    margin: 1rem 0;
  }

  .logo {
    vertical-align: top;
    width: 200px;

  }

  .menu {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .link {
    color: white;
    font-size: 26px;
    text-decoration: none;
    font-weight: bold;
    text-align: center;
  }

  @media screen and (max-width: 47em) {
    .navbar {
      display: none;
    }
  }
</style>