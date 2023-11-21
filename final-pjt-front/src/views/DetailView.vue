<script setup>
  import { ref } from 'vue'
  import { useMovieStore } from '../stores/movies';
  import { useRoute } from 'vue-router'
  import MovieDetailInfo from '../components/movie/MovieDetailInfo.vue'
  
  const route = useRoute()
  const store = useMovieStore()

  store.getMovieDetail(route.params.id)
</script>

<template>
  <div class="container">
    <MovieDetailInfo v-if="store.movieDetail" />
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
  }
</style>