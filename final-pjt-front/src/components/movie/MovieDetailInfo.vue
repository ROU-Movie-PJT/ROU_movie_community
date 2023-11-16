<script setup>
  import { ref } from 'vue'
  import MovieTrailer from './MovieTrailer.vue';
  defineProps({
    info: Object
  })

  const image = function(path) {
    return `https://image.tmdb.org/t/p/original/${path}`
  }
</script>

<template>
  <div class="info">
    <div class="left-box">
      <div class="title-box">
        <h3 class="title">{{ info.title }}</h3>
        <span class="text">⭐{{ info.vote_average }}</span>
      </div>
      <hr>
      <p class="text"><b class="md-text">상영일</b> - {{ info.release_date }}</p>
      <p class="text"><b class="md-text">장르</b> - 액션, 코미디</p>
      <p class="text"><b class="md-text">감독</b> - 미야자키 하야오</p>
      <p class="text">{{ info.overview }}</p>
      <div class="buttons">
        <button class="button">
          <img src="../../assets/watch.svg" alt="">
        </button>
        <button class="button">
          <img src="../../assets/like.svg" alt="">
        </button>
        <button class="button">
          <img src="../../assets/unlike.svg" alt="">
        </button>
        <button class="button">
          <img src="../../assets/favorite.svg" alt="">
        </button>
        <button class="button" data-bs-toggle="modal" data-bs-target="#trailerModal" >
          <img src="../../assets/youtube.svg" alt="">
        </button>
      </div>
      <MovieTrailer :movie="info" />
    </div>
    <img class="poster" :src=image(info.poster_path) alt="">
  </div>
</template>

<style scoped>
  .title-box {
    display: flex;
    gap: .5rem;
    align-items: baseline;
  }
  
  .info {
    color: white;
    display: flex;
    margin-top: 3rem;
    gap: 4rem;
  }

  .left-box {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .poster {
    width: 185px;
    height: 260px;
  }

  .text {
    margin: 0;
    font-size: small;
    font-family: 'Pretendard-ExtraLight';
  }

  .md-text {
    font-size: medium;
  }

  .title {
    font-weight: bold;
  }

  .button {
    border: none;
    background-color: black;
  }
</style>
