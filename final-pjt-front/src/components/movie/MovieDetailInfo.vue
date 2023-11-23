<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMovieStore } from '../../stores/movies'
  import { useUserStore } from '../../stores/user'
  import MovieTrailer from './MovieTrailer.vue'
  import Badge from '../common/Badge.vue'

  const store = useMovieStore()
  const userStore = useUserStore()
  const router = useRouter()

  const image = function(path) {
    return `https://image.tmdb.org/t/p/original/${path}`
  }

  const createReview = function() {
    router.push({name: 'create', params: {movieId: store.movieDetail.id}})
  }
</script>

<template>
  <div class="info">
    <div class="left-box">
      <div class="title-box">
        <h2 class="title">{{ store.movieDetail.title }}</h2>
        <span class="text">⭐{{ store.movieDetail.vote_average }}</span>
      </div>
      <hr>
      <p class="text"><b class="md-text">상영일</b> - {{ store.movieDetail.release_date }}</p>
      <p class="text"><b class="md-text">장르</b> - <Badge class="genre text-bg-signature" v-for="genre in store.movieDetail.genres" :name="genre.name" /></p>
      <p class="text"><b class="md-text">감독</b> - {{ store.movieDetail.director }}</p>
      <p class="text">{{ store.movieDetail.overview }}</p>
      <hr>
      <div class="buttons">
        <div class="left-buttons">
          <div class="watch-button btn-box">
            <button v-if="store.movieDetail.isWatch" class="button" @click.prevent="store.watchMovie">
              <img src="../../assets/watch_fill.svg" alt="">
            </button>
            <button v-else class="button" @click.prevent="store.watchMovie">
              <img src="../../assets/watch.svg" alt="">
            </button>
          </div>
          <div class="like-button btn-box">
            <button v-if="store.movieDetail.isLike" class="button" @click.prevent="store.likeMovie">
              <img src="../../assets/like_fill.svg" alt="">
            </button>
            <button v-else class="button" @click.prevent="store.likeMovie">
              <img src="../../assets/like.svg" alt="">
            </button>
            <span>{{ store.movieDetail.like_movie_users_count }}</span>
          </div>
          <div class="unlike-button btn-box">
            <button v-if="store.movieDetail.isDislike" class="button" @click.prevent="store.unlikeMovie">
              <img src="../../assets/unlike_fill.svg" alt="">
            </button>
            <button v-else class="button" @click.prevent="store.unlikeMovie">
              <img src="../../assets/unlike.svg" alt="">
            </button>
            <span>{{ store.movieDetail.dislike_movie_users_count }}</span>
          </div>
          <div class="favorite-button btn-box">
            <button v-if="store.movieDetail.isFavorite" class="button" @click.prevent="store.favoriteMovie">
              <img src="../../assets/favorite_fill.svg" alt="">
            </button>
            <button v-else class="button" @click.prevent="store.favoriteMovie">
              <img src="../../assets/favorite.svg" alt="">
            </button>
            <span>{{ store.movieDetail.favorite_movie_users_count }}</span>
          </div>
          <button class="button" data-bs-toggle="modal" data-bs-target="#trailerModal" >
            <img src="../../assets/youtube.svg" alt="">
          </button>
        </div>
        <button v-if="userStore.token" class="btn" @click="createReview">리뷰 쓰기</button>
      </div>
      <MovieTrailer :movie="store.movieDetail" />
    </div>
    <img class="poster" :src=image(store.movieDetail.poster_path) alt="">
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
    gap: 2rem;
    align-items: center;
  }

  .left-box {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex-grow: 1;
  }

  .poster {
    width: 20%;
    height: 80%;
  }

  .text {
    margin: 0;
  }

  .md-text {
    font-size: large;
  }

  .title {
    font-weight: bold;
  }

  .buttons {
    display: flex;
    align-items: center;
  }

  .left-buttons {
    display: flex;
    align-items: center;
    flex-grow: 1;
    gap: .5rem
  }

  .button {
    border: none;
    background-color: black;
  }

  .btn {
    background-color: #7B61FF;
    color: white;
  }

  .btn:hover {
    background-color: #7459fb93;
    color: white;
  }

  .btn-box {
    display: flex;
    align-items: center;
  }

  .genre {
    margin: 0 .25rem;
  }

  .text-bg-signature {
    color: white;
    background-color: #7B61FF;
    cursor: default;
  }
</style>
