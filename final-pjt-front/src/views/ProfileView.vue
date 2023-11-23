<script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
  import { useProfileStore } from '../stores/profile'
  import { useUserStore } from '../stores/user'
  import UpdateModal from '../components/profile/UpdateModal.vue'

  const profileStore = useProfileStore()
  const userStore = useUserStore()
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

  const updateUserInfo = function () {
    router.push({name: 'update_account'})
  }
</script>

<template>
  <div v-if="profileStore.profileInfo" class="container">
    <h1 class="text">{{ profileStore.profileInfo.username }}의 프로피일</h1>
    <img :src="image(profileStore.profileInfo.profile_image)" alt="">
    <img :src="profileStore.profileInfo.rate_image" alt="">
    <p>팔로워: {{ profileStore.profileInfo.followers.length }}</p>
    <p>팔로잉: {{ profileStore.profileInfo.followings.length }}</p>
    <p>관심있는 장르: <span v-for="genre in profileStore.profileInfo.like_genres">{{ genre.name }}</span></p>
    <p>관심없는 장르: <span v-for="genre in profileStore.profileInfo.hate_genres">{{ genre.name }}</span></p>
    <button class="button" data-bs-toggle="modal" data-bs-target="#updateModal" >선호/불호 장르 변경</button>
    <button class="button" @click="updateUserInfo">사용자 정보 변경</button>
    <button class="button" @click="userStore.resign">회원 탈퇴</button>
    <button class="button">팔로우</button>
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
