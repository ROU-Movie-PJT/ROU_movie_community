import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  
  const store = useUserStore()
  const router = useRouter()

  const createMovieReview = function (payload) {
    const movieId = payload.movieId
    const title = payload.title
    const content = payload.content
    axios({
      method: 'post',
      url: `${API_URL}/community/${movieId}/review/`,
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(() => {
        router.push({name: 'movie_detail', params: {id: movieId}})
      })
  }

  const reviews = ref()

  const getReviews = function () {
    axios({
      method: 'get',
      url: `${API_URL}/community/`
    })
      .then(res => reviews.value = res.data)
  }

  const createReview = function (payload) {
    const title = payload.title
    const content = payload.content

    axios({
      method: 'post',
      url: `${API_URL}/community/`,
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        //상세 페이지로 가기
        router.push({name: 'community'})
      })
  }

  const updateReview = function (payload) {
    const title = payload.title
    const content = payload.content
    const reviewId = payload.reviewId

    axios({
      method: 'put',
      url: `${API_URL}/community/${reviewId}/`,
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        //상세 페이지로 가기
        router.push({name: 'community'})
      })
  }

  const deleteReview = function (reviewId) {
    axios({
      method: 'delete',
      url: `${API_URL}/community/${reviewId}/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(() => {
        router.push({name: 'community'})
      })
  }

  const reviewDetail = ref()

  const getReviewDetail = function (reviewId) {
    axios({
      method: 'get',
      url: `${API_URL}/community/${reviewId}/`
    })
      .then(res => {
        reviewDetail.value = res.data
      })
  }

  const likeReview = function (reviewId) {
    axios({
      method: 'post',
      url: `${API_URL}/community/${reviewId}/like/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        reviewDetail.value.like_count = res.data.count
      })
  }

  const dislikeReview = function (reviewId) {
    axios({
      method: 'post',
      url: `${API_URL}/community/${reviewId}/dislike/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        reviewDetail.value.dislike_count = res.data.count
      })
  }

  const comments = ref()

  const getComments = function (reviewId) {
    axios({
      method: 'get',
      url: `${API_URL}/community/${reviewId}/comment/`
    })
      .then(res => comments.value = res.data.reply_comments)
  }

  const createComment = function (payload) {
    const reviewId = payload.reviewId
    const content = payload.content

    axios({
      method: 'post',
      url: `${API_URL}/community/${reviewId}/comment/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        content
      }
    })
      .then(res => comments.value = res.data.reply_comments)
  }

  const updateComment = function (payload) {
    const reviewId = payload.reviewId
    const commentId = payload.commentId
    const content = payload.content

    axios({
      method: 'put',
      url: `${API_URL}/community/${reviewId}/comment/${commentId}/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        content
      }
    })
      .then(res => {
        comments.value = res.data.reply_comments
      })
  }

  const likeComment = function (payload) {
    const reviewId = payload.reviewId
    const commentId = payload.commentId

    axios({
      method: 'post',
      url: `${API_URL}/community/${reviewId}/like/${commentId}/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
      .then(res => {
        comments.value = res.data.reply_comments
      })
  }

  return { 
    createMovieReview,
    reviews,
    getReviews,
    createReview,
    updateReview,
    deleteReview,
    reviewDetail,
    getReviewDetail,
    likeReview,
    dislikeReview,
    getComments,
    createComment,
    comments,
    updateComment,
    likeComment
  }
}, { persist: true})