<script setup>
  import { RouterView } from 'vue-router'
  import NavBar from './components/common/NavBar.vue'
  import Header from './components/common/Header.vue'
  import TopBtn from './components/common/TopBtn.vue'
  import { onMounted } from 'vue'
  import { useMovieStore } from './stores/movies'

  const store = useMovieStore()

  store.getRecommendMovies()
  store.getTrendMovies()
</script>

<template>
  <div class="content">
    <TopBtn href="#" />
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
