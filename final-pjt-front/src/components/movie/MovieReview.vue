<script setup>
  defineProps({
    review: Object
  })
</script>

<template>
  <div class="review-content">
    <div class="left-box">
      <p class="title">{{ review.title }}</p>
      <p class="content">{{ review.content }}</p>
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
      <p class="writer">by. {{ review.write_review_user.username }}</p>
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
    flex-grow: 1;
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
</style>