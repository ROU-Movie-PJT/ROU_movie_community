<script setup>
  defineProps({
    item: Object
  })

  const image = function (path) {
    return `https://image.tmdb.org/t/p/original/${path}`
  }
</script>

<template>
  <img class="poster" :src="image(item.poster_path)" alt="">
</template>

<style scoped>
  .poster {
    width: 100%;
    cursor: pointer;
  }
</style>
