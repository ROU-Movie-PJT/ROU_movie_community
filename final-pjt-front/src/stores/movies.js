import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const recommendMovies = ref({})
  
  const getMovieList = function(sortNum) {
    axios({
      method: 'get',
      url: `${API_URL}/movies/${sortNum}/sort/`,
    })
    .then(res => {
      console.log(res.data)
      recommendMovies.value[sortNum] = res.data
    })
  }
  
  const getRecommendMovies = function () {
    for (let i = 1; i < 6; i++) {
      if (i !== 4) {
        getMovieList(i)
      }
    }
  }
  
  return { recommendMovies, getMovieList, getRecommendMovies }
}, { persist: true })