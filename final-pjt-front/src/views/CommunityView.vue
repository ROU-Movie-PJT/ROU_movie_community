<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useCommunityStore } from '../stores/community';

  const communityStore = useCommunityStore()
  const router = useRouter()

  onMounted(() => {
    communityStore.getReviews()
  })

  const createReview = function () {
    router.push({name: 'create', params: {movieId: 0}})
  }

  const goDetail = function (reviewId) {
    router.push({name: 'community_detail', params: {reviewId: reviewId}})
  }
</script>

<template>
  <div>
    <h1>ROU 커뮤니티</h1>
    <button @click="createReview">게시글 생성</button>
    <div v-if="communityStore.reviews" class="review-list">
      <div class="review" v-for="review in communityStore.reviews.results" :key="review" @click="goDetail(review.id)">
        <p>제목 - {{ review.title }}</p>
        <p>내용 - {{ review.content }}</p>
        <p>좋아요 - {{ review.like_count }}</p>
        <p>싫어요 - {{ review.dislike_count }}</p>
        <p>댓글 - {{ review.comment_count }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>