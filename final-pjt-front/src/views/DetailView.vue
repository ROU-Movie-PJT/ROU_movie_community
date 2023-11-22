<script setup>
  import { ref, onMounted } from 'vue'
  import { useMovieStore } from '../stores/movies';
  import { useRoute, onBeforeRouteUpdate } from 'vue-router'
  import MovieDetailInfo from '../components/movie/MovieDetailInfo.vue'
  import MovieReviewList from '../components/movie/MovieReviewList.vue'
  import MovieActorList from '../components/movie/MovieActorList.vue';
  import GenreRecommend from '../components/movie/GenreRecommend.vue';

  const route = useRoute()
  const store = useMovieStore()

  const movieId = ref(route.params.id)

  onMounted(() => {
    store.getMovieDetail(movieId.value)
    store.getMovieReview(movieId.value)
    store.getGenreRecommendMovies(store.movieDetail.genres)
  })

  onBeforeRouteUpdate((to, from) => {
    store.getMovieDetail(to.params.id)
    store.getMovieReview(to.params.id)
    store.getGenreRecommendMovies(store.movieDetail.genres)
  })
</script>

<template>
  <div class="container">
    <MovieDetailInfo v-if="store.movieDetail" />
    <MovieActorList v-if="store.movieDetail" />
    <MovieReviewList v-if="store.movieDetail"/>
    <GenreRecommend v-if="store.movieDetail" />
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