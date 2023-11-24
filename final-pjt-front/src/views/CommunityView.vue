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
  <div class="container">
    <h1 class="title">ROU 커뮤니티</h1>
    <div class="content">
      <button @click="createReview" class="btn btn-signature">게시글 생성</button>
      <div v-if="communityStore.reviews" class="review-list">
        <div v-for="review in communityStore.reviews.results" :key="review" @click="goDetail(review.id)">
          <div class="review">
            <div class="left-box">
              <h4 class="review-title">{{ review.title }}</h4>
              <p class="review-content">{{ review.content }}</p>
            </div>
            <div class="right-box">
              <div class="icon-list">
                <div class="icon-box">
                  <img class="icon" src="../assets/comment.svg" alt="">
                  <span>{{ review.comment_count }}</span>
                </div>
                <div class="icon-box">
                  <img class="icon" src="../assets/like_color.svg" alt="">
                  <span>{{ review.like_count }}</span>
                </div>
                <div class="icon-box">
                  <img class="icon" src="../assets/unlike_color.svg" alt="">
                  <span>{{ review.dislike_count }}</span>
                </div>
              </div>
              <p class="writer">by. <RouterLink class="link" @click.stop.prevent :to="{name: 'profile', params: {userId: review.write_review_user.id}}">{{ review.write_review_user.username }}</RouterLink></p>
            </div>
          </div>
          <hr class="line">
        </div>
      </div>
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
    font-weight: bold;
    color: white;
    margin: 0;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .line {
    color: white;
    margin-bottom: 0;
  }

  .btn-signature {
    background-color: #7B61FF;
    color: white;
    align-self: flex-end;
  }

  .review-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .review {
    background-color: gainsboro;
    padding: 1rem;
    border-radius: 10px;
    display: flex;
  }

  p, h4 {
    margin: 0;
  }

  .left-box {
    width: 75%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .review-title {
    font-weight: bold;
  }

  .right-box {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: space-between;
  }

  .writer {
    color: grey;
    font-size: small;
    text-align: end;
  }

  .icon {
    width: 20px;
    height: 20px;
  }

  .icon-box {
    display: flex;
    gap: .25rem;
  }

  .icon-list {
    display: flex;
    gap: 1rem;
  }

  .link:visited {
    color: grey;
  }
</style>