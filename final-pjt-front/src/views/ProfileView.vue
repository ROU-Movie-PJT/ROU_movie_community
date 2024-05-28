<script setup>
  import { ref, onMounted, watch, computed } from 'vue'
  import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
  import { useProfileStore } from '../stores/profile'
  import { useUserStore } from '../stores/user'
  import UpdateModal from '../components/profile/UpdateModal.vue'
  import MovieCard from '../components/home/MovieCard.vue'
  import Badge from '../components/common/Badge.vue'

  const profileStore = useProfileStore()
  const userStore = useUserStore()
  const route = useRoute()
  const router = useRouter()
  const userId = ref(route.params.userId)
  const category = ref(1)

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
    <div class="user-image">
      <img class="rate-image" :src="profileStore.profileInfo.rate_image" alt="">
      <div class="profile-circle">
        <img class="profile-img" :src="profileStore.profileInfo.profile_image ? image(profileStore.profileInfo.profile_image) : defaultImagePath" alt="">
      </div>
    </div>
    <h1 class="text">{{ profileStore.profileInfo.username }}</h1>
    <div class="btn-box">
      <button v-if="isSelf" class="btn btn-signature" data-bs-toggle="modal" data-bs-target="#updateModal" >선호/불호 장르 변경</button>
      <button v-if="isSelf" class="btn btn-signature" @click="updateUserInfo">사용자 정보 변경</button>
      <button v-if="!isSelf" class="btn btn-signature" @click="follow(userId)">{{ profileStore.profileInfo.followers.find(el => el.id === userStore.user) ? '언팔로우' : '팔로우' }}</button>
    </div>
    <div class="preference">
      <p class="genres">선호 장르: <Badge class="text-bg-primary" v-for="genre in profileStore.profileInfo.like_genres" :name="genre.name" /></p>
      <p class="genres">불호 장르: <Badge class="text-bg-secondary" v-for="genre in profileStore.profileInfo.hate_genres" :name="genre.name" /></p>
    </div>
    <a v-if="isSelf" class="resign" @click="userStore.resign">회원 탈퇴</a>
    <div class="list-box">
      <div v-if="profileStore.profileInfo.followers.length > 0" class="follower-list list">
        <p>팔로워: {{ profileStore.profileInfo.followers.length }}</p>
        <div class="user-info" v-for="follower in profileStore.profileInfo.followers" :key="follower">
          <div class="circle">
            <img class="profile-img" :src="follower.profile_image ? image(follower.profile_image) : defaultImagePath" alt="">
          </div>
          <p>{{ follower.username }}</p>
        </div>
      </div>
      <div v-if="profileStore.profileInfo.followings.length > 0" class="following-list list">
        <p>팔로잉: {{ profileStore.profileInfo.followings.length }}</p>
        <div class="user-info" v-for="following in profileStore.profileInfo.followings" :key="following">
          <div class="circle">
            <img class="profile-img" :src="following.profile_image ? image(following.profile_image) : defaultImagePath" alt="">
          </div>
          <p>{{ following.username }}</p>
          <!-- <button v-if="userStore.user == userId" class="btn btn-signature btn-sm" @click="follow(following.id)">언팔로우</button> -->
        </div>
      </div>
      <div v-if="profileStore.profileInfo.friends.length > 0" class="friend-list list">
        <p>친구: {{ profileStore.profileInfo.friends.length }}</p>
        <div class="user-info" v-for="friend in profileStore.profileInfo.friends" :key="friend">
          <div class="circle">
            <img :src="friend.profile_image ? image(friend.profile_image) : defaultImagePath" alt="" class="profile-img">
          </div>
          <p>{{ friend.username }}</p>
        </div>
      </div>
    </div>
    <div class="user-data">
      <div class="menu">
        <p @click="selectCategory(0)">좋아요한 영화</p>
        <p @click="selectCategory(1)">찜한 영화</p>
        <p @click="selectCategory(2)">시청한 영화</p>
        <p @click="selectCategory(3)">싫어요한 영화</p>
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

  .user-info {
    display: flex;
    align-items: center;
    gap: .5rem;
  }

  .list-box {
    display: flex;
    justify-content: space-between;
  }

  .list {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: .5rem;
    max-height: 30vh;
    overflow-y: auto;
    padding: 1rem;
  }

  .list::-webkit-scrollbar {
    width: 5px;
    background-color: gainsboro;
    border-radius: 5px;
  }

  .list::-webkit-scrollbar-thumb {
    background-color: gray;
    border-radius: 5px;
    background-clip: padding-box;
    border: 1px solid transparent;
  }

  .info {
    display: flex;
    align-items: center;
    gap: .5rem;
  }

  .circle {
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    overflow: hidden;
    background-color: white;
  }

  .profile-circle {
    width: 10rem;
    height: 10rem;
    border-radius: 50%;
    overflow: hidden;
    background-color: white;
  }

  .profile-img {
    width: 100%;
    height: 100%;
  }

  .container {
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  p {
    margin: 0;
  }

  .preference {
    padding: 1rem 1.5rem;
    background-color: gainsboro;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .genres {
    display: flex;
    gap: .5rem;
    color: black;
    font-weight: bold;
    align-items: center;
  }

  .btn-box {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .btn-signature {
    background-color: #7B61FF;
    color: white;
  }

  .resign {
    color: grey;
  }
</style>
