<script setup>
  import { ref, onMounted, watch, computed } from 'vue'
  import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
  import { useProfileStore } from '../stores/profile'
  import { useUserStore } from '../stores/user'
  import UpdateModal from '../components/profile/UpdateModal.vue'
  import MovieCard from '../components/home/MovieCard.vue'

  const profileStore = useProfileStore()
  const userStore = useUserStore()
  const route = useRoute()
  const router = useRouter()
  const userId = ref(route.params.userId)
  const category = ref(3)

  onMounted(() => {
    profileStore.getProfile(userId.value)
  })

  onBeforeRouteUpdate((to, from) => {
    userId.value = to.params.userId
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

  const isSelf = computed(() => {
    return userId.value == userStore.user
  })

  const follow = function (userId) {
    if (userId == userStore.user) {
      window.alert('본인은 팔로우 할 수 없습니다.')
    } else {
      profileStore.follow(userId)
    }
  }

  const defaultImagePath = '/src/assets/profile.png'

  const selectCategory = function (idx) {
    category.value = idx
  }

  const goDetail = function (id) {
    router.push({name: 'movie_detail', params: {id: id}})
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
    <button v-if="isSelf" class="button" data-bs-toggle="modal" data-bs-target="#updateModal" >선호/불호 장르 변경</button>
    <button v-if="isSelf" class="button" @click="updateUserInfo">사용자 정보 변경</button>
    <button v-if="isSelf" class="button" @click="userStore.resign">회원 탈퇴</button>
    <button v-if="!isSelf" class="button" @click="follow(userId)">{{ profileStore.profileInfo.followers.find(el => el.id === userStore.user) ? '언팔로우' : '팔로우' }}</button>
    <div class="follower-list">
      <div v-for="follower in profileStore.profileInfo.followers" :key="follower">
        <div class="circle">
          <img class="profile-img" :src="follower.profile_image ? image(follower.profile_image) : defaultImagePath" alt="">
        </div>
        <p>{{ follower.username }}</p>
      </div>
    </div>
    <div class="following-list">
      <div v-for="following in profileStore.profileInfo.followings" :key="following">
        <div class="circle">
          <img :src="following.profile_image ? image(following.profile_image) : defaultImagePath" alt="" class="profile-img">
        </div>
        <p>{{ following.username }}</p>
        <button v-if="following.id !== userStore.user" class="button" @click="follow(following.id)">언팔로우</button>
      </div>
    </div>
    <div class="friend-list">
      <div v-for="friend in profileStore.profileInfo.friends" :key="friend">
        <div class="circle">
          <img :src="friend.profile_image ? image(friend.profile_image) : defaultImagePath" alt="" class="profile-img">
        </div>
        <p>{{ friend.username }}</p>
      </div>
    </div>
    <div class="user-movie">
      <div v-if="category === 0" class="like-movie-list">
        <MovieCard v-for="movie in profileStore.profileInfo.like_movies" :key="movie" :item="movie" @click="goDetail(movie.movie_id)" />
      </div>
      <div v-else-if="category === 1" class="favorite-movie-list">
        <MovieCard v-for="movie in profileStore.profileInfo.favorite_movies" :key="movie" :item="movie" @click="goDetail(movie.movie_id)" />
      </div>
      <div v-else-if="category === 2" class="watching-movie-list">
        <MovieCard v-for="movie in profileStore.profileInfo.watching_movies" :key="movie" :item="movie" @click="goDetail(movie.movie_id)" />
      </div>
      <div v-else-if="category === 3" class="dislike-movie-list">
        <MovieCard v-for="movie in profileStore.profileInfo.dislike_movies" :key="movie" :item="movie" @click="goDetail(movie.movie_id)" />
      </div>
    </div>
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

  .circle {
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    overflow: hidden;
    background-color: white;
  }

  .profile-img {
    width: 100%;
    height: 100%;
  }
</style>
