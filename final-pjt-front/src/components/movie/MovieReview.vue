<script setup>
  import { RouterLink } from 'vue-router';
  defineProps({
    review: Object
  })

  const image = function(path) {
    return `http://localhost:8000${path}`
  }

  const defaultImagePath = '/src/assets/profile.png'
</script>

<template>
  <div class="review-content">
    <div class="left-box">
      <div class="circle">
        <img class="writer-img" :src="review.write_review_user.profile_image ? image(review.write_review_user.profile_image) : defaultImagePath" alt="" >
      </div>
      <div class="text-box">
        <p class="title">{{ review.title }}</p>
        <p class="content">{{ review.content }}</p>
      </div>
    </div>
    <div class="right-box">
      <div class="icon-list">
        <div class="icon-box">
          <img class="icon" src="../../assets/comment.svg" alt="">
          <span>{{ review.comment_count }}</span>
        </div>
        <div class="icon-box">
          <img class="icon" src="../../assets/like_color.svg" alt="">
          <span>{{ review.like_review_users.length }}</span>
        </div>
        <div class="icon-box">
          <img class="icon" src="../../assets/unlike_color.svg" alt="">
          <span>{{ review.dislike_review_users.length }}</span>
        </div>
      </div>
      <p class="writer">by. <RouterLink class="link" :to="{name: 'profile', params: {userId: review.write_review_user.id}}">{{ review.write_review_user.username }}</RouterLink></p>
    </div>
  </div>
</template>

<style scoped>
  .review-content {
    background-color: white;
    border-radius: 5px;
    padding: 1rem;
    display: flex;
  }

  .left-box {
    display: flex;
    gap: 1rem;
    flex-grow: 1;
  }

  .circle {
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    overflow: hidden;
  }

  .writer-img {
    height: 100%;
    width: 100%;
  }

  .right-box {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  p {
    margin: 0;
  }

  .title {
    font-weight: bold;
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