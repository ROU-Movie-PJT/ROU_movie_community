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
    <div>
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

  p {
    margin: 0;
  }

  .title {
    font-weight: bold;
  }
  .writer {
    color: grey;
    font-size: small;
  }
</style>