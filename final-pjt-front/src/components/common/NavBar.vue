<script setup>
  import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="navbar">
    <a class="home" href="/">
      <img class="logo" src="../../assets/logo.png" alt="logo">
    </a>
    <ul class="menu">
      <li class="link">
        <RouterLink class="link" :to="{name: 'home'}">Home</RouterLink>
      </li>
      <li class="link">
        <RouterLink class="link" to="/">Profile</RouterLink>
      </li>
      <li class="link">
        <RouterLink class="link" to="/">Quiz</RouterLink>
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
    display: block;
  }

  .link {
    color: white;
    font-size: 26px;
    text-decoration: none;
    font-weight: bold;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  @media screen and (max-width: 47em) {
    .navbar {
      display: none;
    }
  }
</style>

<style>
  .navbar {
    z-index: 501;
  }
</style>