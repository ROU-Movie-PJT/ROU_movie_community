<script setup>
  import axios from 'axios'
  import { useMovieStore } from '../../stores/movies';
  import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'

  const store = useMovieStore()

  const video = function (id) {
    return `https://www.youtube.com/embed/${id}`
  }
</script>

<template>
  <div></div>
</template>

<style scoped>
  .video {
    width: 100%;
    height: 55vh;
  }
</style>
