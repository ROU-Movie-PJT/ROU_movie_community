import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'
import _ from 'lodash'

export const useMovieStore = defineStore('movie', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const userStore = useUserStore()

  const recommendMovies = ref({})

  const choice = {
    1: '액션',
    2: '모험',
    3: '애니메이션',
    4: '코미디',
    5: '범죄',
    6: '다큐멘터리',
    7: '드라마',
    8: '가족',
    9: '판타지',
    10: '역사',
    11: '공포',
    12: '음악',
    13: '미스터리',
    14: '로맨스',
    15: 'SF',
    16: 'TV 영화',
    17: '스릴러',
    18: '전쟁',
    19: '서부',
  }
  
  const getMovieList = function(sortNum) {
    axios({
      method: 'get',
      url: `${API_URL}/movies/${sortNum}/sort/`,
    })
    .then(res => {
      //console.log(res.data)
      recommendMovies.value[sortNum] = res.data
    })
  }
  
  const getRecommendMovies = function () {
    recommendMovies.value = {}
    for (let i = 20; i < 24; i++) {
      getMovieList(i)
    }
    for (let i = 1; i < 20; i++) {
      getMovieList(i)
    }
  }

  const trendMovies = ref()

  const getTrendMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/movies/trend/`
    })
      .then(res => {
        trendMovies.value = res.data
      })
  }

  const movieDetail = ref()

  const getMovieDetail = function (movie_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/movies/${movie_pk}`,
      headers: {
        Authorization: userStore.token ? `Token ${userStore.token}`: null
      }
    })
      .then(res => {
        movieDetail.value = res.data
      })
  }
  
  const movieReview = ref()

  const getMovieReview = function (movie_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/movies/${movie_pk}/review/`
    })
      .then(res => {
        movieReview.value = res.data.write_movie_review
        movieReview.value.comment_count = res.data.comment_count
      })
  }

  const watchMovie = function () {
    axios({
      method: 'post',
      url: `${API_URL}/movies/${movieDetail.value.id}/watching/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        movieDetail.value.watching_movie_users_count = res.data.watching_movie_users_count
        movieDetail.value.watching_movie_users = res.data.watching_movie_users
        movieDetail.value.isWatch = res.data.isWatch
      })
  }

  const likeMovie = function () {
    axios({
      method: 'post',
      url: `${API_URL}/movies/${movieDetail.value.id}/like/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        movieDetail.value.like_movie_users_count = res.data.like_movie_users_count
        movieDetail.value.like_movie_users = res.data.like_movie_users
        movieDetail.value.isLike = res.data.isLike
      })
  }

  const unlikeMovie = function () {
    axios({
      method: 'post',
      url: `${API_URL}/movies/${movieDetail.value.id}/dislike/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        movieDetail.value.dislike_movie_users_count = res.data.dislike_movie_users_count
        movieDetail.value.dislike_movie_users = res.data.dislike_movie_users
        movieDetail.value.isDislike = res.data.isDislike
      })
  }

  const favoriteMovie = function () {
    axios({
      method: 'post',
      url: `${API_URL}/movies/${movieDetail.value.id}/favorite/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        movieDetail.value.favorite_movie_users_count = res.data.favorite_movie_users_count
        movieDetail.value.favorite_movie_users = res.data.favorite_movie_users
        movieDetail.value.isFavorite = res.data.isFavorite
      })
  }

  const genreRecommendMovies = ref([])

  const getGenreRecommendMovies = function(genres) {
    genreRecommendMovies.value = []
    for (const key in genres) {
      axios({
        method: 'get',
        url: `${API_URL}/movies/${genres[key].id}/genre/`
      })
        .then(res => {
          genreRecommendMovies.value = genreRecommendMovies.value.concat(res.data)
          genreRecommendMovies.value = _.uniqBy(genreRecommendMovies.value, 'movie_id')
        })
    }
  }

  return { 
    recommendMovies, 
    getMovieList, 
    getRecommendMovies, 
    choice, 
    getTrendMovies, 
    trendMovies, 
    movieDetail, 
    getMovieDetail, 
    movieReview, 
    getMovieReview, 
    watchMovie, 
    likeMovie, 
    unlikeMovie, 
    favoriteMovie,
    getGenreRecommendMovies,
    genreRecommendMovies
  }
}, { persist: true })