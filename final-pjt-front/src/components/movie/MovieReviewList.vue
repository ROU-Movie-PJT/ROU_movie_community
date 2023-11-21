<script setup>
  import { ref } from 'vue'
  import { useMovieStore } from '../../stores/movies'
  import MovieReview from './MovieReview.vue'

  const store = useMovieStore()

  const isAllList = ref(false)

  const onToggle = function () {
    isAllList.value = !isAllList.value
  }
</script>

<template>
  <div class="content">
    <h3 class="title">사용자 리뷰</h3>
    <p v-if="isAllList" class="sm-font blue" @click="onToggle">닫기</p>
    <p v-else class="sm-font white" @click="onToggle">전체 목록</p>
    <MovieReview v-for="review in isAllList ? store.movieReview : store.movieReview.slice(0, 3)" :review="review" />
  </div>
</template>

<style scoped>
  .content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .title {
    font-weight: bold;
    color: white;
    margin: 0;
  }
  .sm-font {
    font-size: small;
    text-align: end;
    cursor: pointer;
  }
  .blue {
    color: dodgerblue;
  }
  .white {
    color: white;
  }
</style>