<script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
  import { useProfileStore } from '../stores/profile'
  import UpdateModal from '../components/profile/UpdateModal.vue'

  const profileStore = useProfileStore()
  const route = useRoute()
  const router = useRouter()
  const userId = ref(route.params.userId)

  onMounted(() => {
    profileStore.getProfile(userId.value)
  })

  onBeforeRouteUpdate((to, from) => {
    profileStore.getProfile(to.params.userId)
  })

  const image = function (path) {
    return `${profileStore.API_URL}${path}`
  }

  watch(() => profileStore.pType, (newValue, oldValue) => {
    profileStore.getProfile(userId.value)
  })
</script>

<template>
  <div class="container">
    <h1 class="text">{{ profileStore.profileInfo.username }}의 프로피일</h1>
    <img :src="image(profileStore.profileInfo.profile_image)" alt="">
    <img :src="profileStore.profileInfo.rate_image" alt="">
    <p>팔로워: {{ profileStore.profileInfo.followers.length }}</p>
    <p>팔로잉: {{ profileStore.profileInfo.followings.length }}</p>
    <p>관심있는 장르: <span v-for="genre in profileStore.profileInfo.like_genres">{{ genre.name }}</span></p>
    <p>관심없는 장르: <span v-for="genre in profileStore.profileInfo.hate_genres">{{ genre.name }}</span></p>
    <button class="button" data-bs-toggle="modal" data-bs-target="#updateModal" >정보 변경</button>
    <UpdateModal />
  </div>
</template>

<style scoped>
  .text {
    color: white;
  }

  p {
    color: white;
  }
</style>
