<script setup>
  import { onMounted, ref } from 'vue'
  import { useMovieStore } from '../../stores/movies'
  import { useRouter } from 'vue-router'
  import MovieCard from '../home/MovieCard.vue'
  import _ from 'lodash'

  const store = useMovieStore()
  const router = useRouter()

  onMounted(() => {
    store.getContentRecommendMovies()
  })

  const goDetail = function (movieId) {
    router.push({name: 'movie_detail', params: {id: movieId}})
  }
</script>

<template>
  <div class="recommend-list">
    <h3 class="title">"{{ store.movieDetail.title }}" 와(과) 비슷한 영화</h3>
    <div class="card-list">
      <MovieCard @click="goDetail(movie.movie_id)" class="movie-card" v-for="movie in _.shuffle(store.contentRecommendMovies)" :item="movie"/>
      <div class="space"></div>
    </div>
  </div>
</template>

<style scoped>
  .recommend-list {
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }

  .movie-card {
    width: 13%;
  }

  .card-list {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    justify-content: space-between;
  }

  .title {
    font-weight: bold;
    color: white;
    margin: 0;
  }

  .space {
    flex-grow: 1;
  }
</style>
