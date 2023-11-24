<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, onBeforeRouteUpdate } from 'vue-router'
  import { useCommunityStore } from '../stores/community';

  const communityStore = useCommunityStore()
  const route = useRoute()
  const reviewId = ref(route.params.reviewId)

  onBeforeRouteUpdate((to, from) => {
    reviewId.value = to.params.reviewId
  })

  onMounted(() => {
    communityStore.getReviewDetail(reviewId.value)
    communityStore.getComments(reviewId.value)
  })

  const content = ref('')

  const createComment = function () {
    const payload = {
      'reviewId': reviewId.value,
      'content': content.value
    }
    communityStore.createComment(payload)
    content.value = ''
  }
</script>

<template>
  <div>
    <h3>{{ communityStore.reviewDetail.title }}</h3>
    <p>{{ communityStore.reviewDetail.content }}</p>
    <p>좋아요 - {{ communityStore.reviewDetail.like_count }}</p>
    <p>싫어요 - {{ communityStore.reviewDetail.dislike_count }}</p>
    <button @click="updateReview">수정</button>
    <button @click="communityStore.deleteReview(reviewId)">삭제</button>
    <p>댓글 - {{ communityStore.reviewDetail.comment_count ? communityStore.comments.length : communityStore.reviewDetail.comment_count }}</p>
    <div v-if="communityStore.reviewDetail.comment_count" class="comment-list">
      <div class="comment" v-for="comment in communityStore.comments" :key="comment">
        <p>{{ comment.write_comment_user.username }}</p>
        <p>{{ comment.content }}</p>
      </div>
    </div>
    <form class="comment-form" @submit.prevent="createComment">
      <textarea v-model.trim="content"></textarea>
      <button type="submit">댓글 쓰기</button>
    </form>
  </div>
</template>

<style scoped>
</style>