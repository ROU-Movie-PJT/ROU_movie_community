<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
  import { useMovieStore } from '../stores/movies'
  import MovieCard from '../components/home/MovieCard.vue';

  const route = useRoute()
  const router = useRouter()
  const keyword = ref(route.params.keyword)
  const movieStore = useMovieStore()

  onMounted(() => {
    movieStore.getSearchResult(keyword.value)
  })

  onBeforeRouteUpdate((to, from) => {
    movieStore.getSearchResult(to.params.keyword)
    keyword.value = to.params.keyword
  })

  const goDetail = function(id) {
    router.push({name: 'movie_detail', params: {id: id}})
  }
</script>

<template>
  <div class="container">
    <h3 class="title">"{{ keyword }}" 검색 결과</h3>
    <div class="result-list">
      <MovieCard class="result-card" v-for="movie in movieStore.searchResult" :item="movie" @click="goDetail(movie.movie_id)" />
      <div class="space"></div>
    </div>
  </div>
</template>

<style scoped>
  .container {
    padding: 2rem 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .title {
    color: white;
    font-weight: bold;
  }

  .result-list {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    justify-content: space-between;
  }

  .result-card {
    width: 13%;
  }

  .space {
    flex-grow: 1;
  }
</style>
