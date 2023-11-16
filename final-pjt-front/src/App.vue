<script setup>
  import { RouterView } from 'vue-router'
  import NavBar from './components/common/NavBar.vue'
  import Header from './components/common/Header.vue'
</script>

<template>
  <div class="content">
    <NavBar />
    <Header />
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
  .content {
    width: 100%;
    height: 100%;
    padding: 56px 0 0 200px;
  }

  main {
    height: 100%;
  }

  @media screen and (max-width: 47em) {
    .content {
      padding-left: 0;
    }
  }
</style>
