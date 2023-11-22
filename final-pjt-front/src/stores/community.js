import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  
  const store = useUserStore()
  const router = useRouter()

  const createReview = function (payload) {
    const movieId = payload.movieId
    const title = payload.title
    const content = payload.content
    axios({
      method: 'post',
      url: `${API_URL}/community/${movieId}/review/`,
      data: {
        title: title,
        content: content
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(() => {
        router.push({name: 'movie_detail', params: {id: movieId}})
      })
  }

  return { createReview }
}, { persist: true})