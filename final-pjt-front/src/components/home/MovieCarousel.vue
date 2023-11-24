<script setup>
  import { useMovieStore } from '../../stores/movies';
  import 'vue3-carousel/dist/carousel.css'
  import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'

  const store = useMovieStore()

  const video = function (id) {
    return `https://www.youtube.com/embed/${id}`
  }
</script>

<template>
  <Carousel :items-to-show="1" autoplay="3000" :wrap-around="true">
    <template v-for="movie in store.trendMovies" :key="movie">
      <Slide v-if="movie.videos">
        <div class="carousel__item">
          <iframe class="video" :src="video(movie.videos)" frameborder="0" width="100%" height="300px"></iframe>
        </div>
      </Slide>
    </template>

    <template #addons>
      <Navigation/>
    </template>
  </Carousel>
</template>

<style scoped>
  .video {
    width: 100%;
    height: 55vh;
  }

  .carousel__item {
    width: 100%;
  }
</style>
