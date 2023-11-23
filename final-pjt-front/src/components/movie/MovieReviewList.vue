<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useMovieStore } from '../../stores/movies'
  import MovieReview from './MovieReview.vue'

  const store = useMovieStore()
  const route = useRoute()

  onMounted(() => {
    store.getMovieReview(route.params.id)
  })

  const isAllList = ref(false)

  const onToggle = function () {
    isAllList.value = !isAllList.value
  }

  const isReviewValid = computed(() => {
    return store.movieReview.length
  })
</script>

<template>
  <div class="content">
    <h3 class="title">사용자 리뷰</h3>
    <div v-if="isReviewValid" class="review-list">
      <p v-if="isAllList" class="sm-font blue" @click="onToggle">닫기</p>
      <p v-else class="sm-font white" @click="onToggle">전체 목록</p>
      <MovieReview v-for="review in isAllList ? store.movieReview : store.movieReview.slice(0, 3)" :review="review" />
    </div>
    <div v-else class="review-list">
      <p class="none-review">아직 리뷰가 존재하지 않습니다.</p>
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
  .sm-font {
    font-size: small;
    text-align: end;
    cursor: pointer;
    margin: 0;
  }
  .blue {
    color: dodgerblue;
  }
  .white {
    color: white;
  }

  .review-list {
    border: 1px solid gainsboro;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    gap: .5rem;
    padding: 1rem;
  }

  .none-review {
    color: grey;
    margin: 0;
  }
</style>