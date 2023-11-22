<script setup>
  import { ref, computed } from 'vue'
  import { useMovieStore } from '../stores/movies';
  import { useRoute } from 'vue-router'
  import MovieDetailInfo from '../components/movie/MovieDetailInfo.vue'
  import MovieReviewList from '../components/movie/MovieReviewList.vue'

  const route = useRoute()
  const store = useMovieStore()

  store.getMovieDetail(route.params.id)
  store.getMovieReview(route.params.id)
</script>

<template>
  <div class="container">
    <MovieDetailInfo v-if="store.movieDetail" />
    <MovieReviewList v-if="store.movieDetail"/>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    gap: 3rem;
    width: 90%;
    padding-bottom: 2rem;
  }
</style>