import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from './user'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useProfileStore = defineStore('profile', () => {
  const route = useRoute()
  const API_URL = 'http://127.0.0.1:8000'
  const userStore = useUserStore()
  const pType = ref('like')
  const profileInfo = ref(null)

  const initChoice = [
    {'genre': '액션', 'isSelected': false},
    {'genre': '모험', 'isSelected': false},
    {'genre': '애니메이션', 'isSelected': false},
    {'genre': '코미디', 'isSelected': false},
    {'genre': '범죄', 'isSelected': false},
    {'genre': '다큐멘터리', 'isSelected': false},
    {'genre': '드라마', 'isSelected': false},
    {'genre': '가족', 'isSelected': false},
    {'genre': '판타지', 'isSelected': false},
    {'genre': '역사', 'isSelected': false},
    {'genre': '공포', 'isSelected': false},
    {'genre': '음악', 'isSelected': false},
    {'genre': '미스터리', 'isSelected': false},
    {'genre': '로맨스', 'isSelected': false},
    {'genre': 'SF', 'isSelected': false},
    {'genre': 'TV 영화', 'isSelected': false},
    {'genre': '스릴러', 'isSelected': false},
    {'genre': '전쟁', 'isSelected': false},
    {'genre': '서부', 'isSelected': false}
  ]

  const likeChoice = ref([
    {'genre': '액션', 'isSelected': false},
    {'genre': '모험', 'isSelected': false},
    {'genre': '애니메이션', 'isSelected': false},
    {'genre': '코미디', 'isSelected': false},
    {'genre': '범죄', 'isSelected': false},
    {'genre': '다큐멘터리', 'isSelected': false},
    {'genre': '드라마', 'isSelected': false},
    {'genre': '가족', 'isSelected': false},
    {'genre': '판타지', 'isSelected': false},
    {'genre': '역사', 'isSelected': false},
    {'genre': '공포', 'isSelected': false},
    {'genre': '음악', 'isSelected': false},
    {'genre': '미스터리', 'isSelected': false},
    {'genre': '로맨스', 'isSelected': false},
    {'genre': 'SF', 'isSelected': false},
    {'genre': 'TV 영화', 'isSelected': false},
    {'genre': '스릴러', 'isSelected': false},
    {'genre': '전쟁', 'isSelected': false},
    {'genre': '서부', 'isSelected': false}
  ])

  const hateChoice = ref([
    {'genre': '액션', 'isSelected': false},
    {'genre': '모험', 'isSelected': false},
    {'genre': '애니메이션', 'isSelected': false},
    {'genre': '코미디', 'isSelected': false},
    {'genre': '범죄', 'isSelected': false},
    {'genre': '다큐멘터리', 'isSelected': false},
    {'genre': '드라마', 'isSelected': false},
    {'genre': '가족', 'isSelected': false},
    {'genre': '판타지', 'isSelected': false},
    {'genre': '역사', 'isSelected': false},
    {'genre': '공포', 'isSelected': false},
    {'genre': '음악', 'isSelected': false},
    {'genre': '미스터리', 'isSelected': false},
    {'genre': '로맨스', 'isSelected': false},
    {'genre': 'SF', 'isSelected': false},
    {'genre': 'TV 영화', 'isSelected': false},
    {'genre': '스릴러', 'isSelected': false},
    {'genre': '전쟁', 'isSelected': false},
    {'genre': '서부', 'isSelected': false}
  ])

  const updateChoice = function () {
    if (pType.value === 'like') {
      likeChoice.value = initChoice
      profileInfo.value.like_genres.forEach(genre => {
        const idx = likeChoice.value.findIndex(el => el.genre === genre.name)
        likeChoice.value[idx].isSelected = !likeChoice.value[idx].isSelected
      })
    } else {
      hateChoice.value = initChoice
      profileInfo.value.hate_genres.forEach(genre => {
        const idx = hateChoice.value.findIndex(el => el.genre === genre.name)
        hateChoice.value[idx].isSelected = !hateChoice.value[idx].isSelected
      })
    }
  }

  const getProfile = function (userId) {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${userId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        profileInfo.value = res.data
        const friends = res.data.followers.filter(follower => {
          return res.data.followings.some(following => following.id === follower.id)
        })
        profileInfo.value.friends = friends
        updateChoice()
      })
  }

  const updateProfile = function () {
    const selectedGenres = []
    if (pType.value == 'like') {
      likeChoice.value.forEach(choice => {
        if (choice.isSelected) {
          selectedGenres.push(choice.genre)
        }
      })
    } else {
      hateChoice.value.forEach(choice => {
        if (choice.isSelected) {
          selectedGenres.push(choice.genre)
        }
      })
    }

    axios({
      method: 'put',
      url: `${API_URL}/accounts/preference/${pType.value}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        genres: selectedGenres.join(',')
      }
    })
      .then(res => {
        if (pType.value == 'like') {
          profileInfo.value.like_genres = res.data.like_genres
          updateChoice()
          pType.value = 'hate'
        } else {
          profileInfo.value.hate_genres = res.data.hate_genres
          updateChoice()
          pType.value = 'like'
        }
      })
  }

  const follow = function (userId) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/follow/${userId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then(res => {
        if (route.params.userId === userStore.user) {
          getProfile(userStore.user)
        } else {
          profileInfo.value.followers = res.data.followers
          profileInfo.value.followings = res.data.followings
        }
      })
  }

  return { 
    API_URL, 
    profileInfo, 
    getProfile, 
    likeChoice, 
    hateChoice, 
    pType,
    updateProfile,
    updateChoice,
    initChoice,
    follow
   }
}, { persist: true })