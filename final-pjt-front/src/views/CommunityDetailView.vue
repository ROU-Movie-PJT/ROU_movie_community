<script setup>
  import { ref, onMounted, watch, onUpdated, computed } from 'vue'
  import { useRoute, onBeforeRouteUpdate } from 'vue-router'
  import { useCommunityStore } from '../stores/community';
import router from '../router';

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

  watch(() => reviewId.value, (newValue, oldValue) => {
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

  const deleteComment = function (commentId) {
    const payload = {
      'reviewId': reviewId.value,
      'commentId': commentId
    }
    communityStore.deleteComment(payload)
  }

  const updateReview = function () {
    router.push({name: 'community_update', params: {reviewId: reviewId.value}})
  }

  const createdDate = computed(() => {
    const date = new Date(communityStore.reviewDetail.created_at)
    return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
  })
</script>

<template>
  <div class="content-box" v-if="communityStore.reviewDetail">
    <div class="review-box">
      <div class="title-box">
        <h3 class="title">{{ communityStore.reviewDetail.title }}</h3>
        <div class="sm-font-box">
          <span class="sm-font">by. {{ communityStore.reviewDetail.write_review_user.username }}</span>
          <span class="sm-font">{{ createdDate }}</span>
        </div>
      </div>
      <div class="icon-list">
        <div class="icon-box">
          <img @click="communityStore.likeReview(reviewId)" class="icon" src="../assets/like_color.svg" alt="" >
          <span>{{ communityStore.reviewDetail.like_count }}</span>
        </div>
        <div class="icon-box">
          <img @click="communityStore.dislikeReview(reviewId)" class="icon" src="../assets/unlike_color.svg" alt="">
          <span>{{ communityStore.reviewDetail.dislike_count }}</span>
        </div>
      </div>
      <p>{{ communityStore.reviewDetail.content }}</p>
      <div class="btn-box">
        <button class="btn btn-signature" @click="updateReview">수정</button>
        <button class="btn btn-signature" @click="communityStore.deleteReview(reviewId)">삭제</button>
      </div>
      <div class="comment-box">
        <p class="comment-count">댓글 ({{ communityStore.reviewDetail.comment_count }})</p>
        <hr>
        <div v-if="communityStore.reviewDetail.comment_count" class="comment-list">
          <div class="comment" v-for="(comment, idx) in communityStore.comments" :key="comment.id">
            <p>{{ comment.write_comment_user.username }} - {{ comment.content }}</p>
            <div class="comment-btn-box">
              <button class="sm-btn btn btn-signature" @click="editComment">수정</button>
              <button class="sm-btn btn btn-signature" @click="deleteComment(comment.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
      <form class="comment-form" @submit.prevent="createComment">
        <textarea class="textarea" v-model.trim="content"></textarea>
        <button type="submit" class="comment-btn btn btn-signature">등록</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
  h3, p {
    margin: 0;
  }

  .comment-count {
    font-weight: bold;
  }

  .content-box {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .review-box {
    width: 60%;
    background-color: gainsboro;
    padding: 1.5rem;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .title {
    font-weight: bold;
  }

  .sm-font-box {
    display: flex;
    gap: .5rem;
  }

  .sm-font {
    color: grey;
    font-size: small;
  }

  .icon {
    width: 20px;
    height: 20px;
  }

  .icon-box {
    display: flex;
    gap: .25rem;
  }

  hr {
    margin: .5rem 0;
  }

  .icon-list {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
  }

  .btn-box {
    display: flex;
    gap: .5rem;
    justify-content: flex-end;
  }

  .comment-btn-box {
    display: flex;
    gap: .5rem;
  }

  .comment {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: white;
    padding: .5rem 1rem;
    border-radius: 5px;
  }

  .btn-signature {
    background-color: #7459fb;
    color: white;
    padding: .25rem .5rem;
  }

  .comment-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .textarea {
    border-radius: 10px;
    resize: none;
    outline: none;
    padding: 1rem;
    flex-grow: 1;
  }

  .comment-form {
    display: flex;
    gap: .25rem;
  }

  .comment-btn {
    width: 20%;
  }

  .sm-btn {
    font-size: small;
  }
</style>