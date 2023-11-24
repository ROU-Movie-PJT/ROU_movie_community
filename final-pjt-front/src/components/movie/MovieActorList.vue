<script setup>
  import MovieActor from './MovieActor.vue';
  import { useMovieStore } from '../../stores/movies';
  import { computed } from 'vue'
  const store = useMovieStore()

  const isActorValid = computed(() => {
    return store.movieDetail.actors.length
  })
</script>

<template>
  <div class="content">
    <h3 class="title">출연진</h3>
    <div v-if="isActorValid" class="actor-list">
      <MovieActor v-for="actor in store.movieDetail.actors.slice(0,9)" :actor="actor"/>
    </div>
    <div v-else class="actor-list">
      <p class="none-actor">출연 배우가 존재하지 않습니다.</p>
    </div>
  </div>
</template>

<style scoped>
  .content {
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }
  .title {
    font-weight: bold;
    color: white;
    margin: 0;
  }
  .actor-list {
    border: 1px solid gainsboro;
    border-radius: 5px;
    display: flex;
    gap: .5rem;
    padding: 1rem;
    flex-wrap: wrap;
  }

  .none-actor {
    color: grey;
    margin: 0;
  }
</style>
