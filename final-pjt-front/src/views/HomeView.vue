<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import Carousel from '../components/home/Carousel.vue'
  import Badge from '../components/common/Badge.vue'
  import MovieCard from '../components/home/MovieCard.vue'

  const router = useRouter()

  const genres = ref(['액션', '모험', '애니메이션', '코미디', '범죄', '다큐멘터리', '드라마', '가족', '판타지', '역사', '공포', '음악', '미스터리', '로맨스', 'SF', '스릴러', '전쟁', '서부'])
  const favoriteGenres = ref(['액션', '모험', '애니메이션'])
  const viewMore = ref(false)
  const activeBadge = ref('전체')

  const moreGenres = function() {
    viewMore.value = !viewMore.value
  }

  const selectBadge = function(badge) {
    activeBadge.value = badge
  }

  const goDetail = function(id) {
    router.push({name: 'movie_detail', params: {id: id}})
  }
</script>

<template>
  <div class="container">
    <Carousel />
    <div class="badges">
      <Badge 
        :class="{'text-bg-primary': activeBadge === '전체', 'text-bg-secondary': activeBadge !== '전체'}" 
        name="전체"
        @click="selectBadge('전체')"
      />
      <Badge 
        v-for="genre in viewMore ? genres : favoriteGenres" 
        :class="{'text-bg-secondary': activeBadge !== genre, 'text-bg-primary': activeBadge === genre}" 
        :name="genre"
        @click="selectBadge(genre)"
      />
      <Badge class="text-bg-light" @click="moreGenres" :name="viewMore ? 'X' : '더보기'" />
    </div>
    <div class="card-list">
      <MovieCard v-for="(item, idx) in new Array(7)" @click="goDetail(idx)" />
    </div>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
    height: 100%;
    padding: 2rem 0;
    gap: 2rem;
  }

  .badges {
    width: 100%;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .card-list {
    display: flex;
    justify-content: space-between;
  }
</style>
