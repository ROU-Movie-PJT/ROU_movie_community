import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const API_URL = 'http://127.0.0.1:8000'

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
        for (const movie in trendMovies.value) {
          console.log(trendMovies.value[movie].title)
        }
      })
  }

  const movieDetail = ref()

  const getMovieDetail = function (movie_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/movies/${movie_pk}`,
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
      })
  }

  return { recommendMovies, getMovieList, getRecommendMovies, choice, getTrendMovies, trendMovies, movieDetail, getMovieDetail, movieReview, getMovieReview }
}, { persist: true })