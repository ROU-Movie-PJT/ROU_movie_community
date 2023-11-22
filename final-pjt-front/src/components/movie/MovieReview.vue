<script setup>
  defineProps({
    review: Object
  })
</script>

<template>
  <div class="review-content">
    <p class="title">{{ review.title }}</p>
    <p class="content">{{ review.content }}</p>
  </div>
</template>

<style scoped>
  .review-content {
    background-color: white;
    border-radius: 5px;
    padding: 1rem;
  }

  .title {
    font-weight: bold;
    margin: 0;
  }

  .content {
    margin: 0;
  }
</style>