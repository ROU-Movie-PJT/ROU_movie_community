<script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMovieStore } from '../stores/movies'
  import Carousel from '../components/home/Carousel.vue'
  import Badge from '../components/common/Badge.vue'
  import MovieCard from '../components/home/MovieCard.vue'

  const store = useMovieStore()
  const router = useRouter()

  const choice = {
    12: '모험',
    14: '판타지',
    16: '애니메이션',
    18: '드라마',
    27: '공포',
    28: '액션',
    35: '코미디',
    36: '역사',
    37: '서부',
    53: '스릴러',
    80: '범죄',
    99: '다큐멘터리',
    878: 'SF',
    9648: '미스터리',
    10402: '음악',
    10749: '로맨스',
    10751: '가족',
    10752: '전쟁',
    10770: 'TV 영화'
  }
  const favoriteGenres = ref({
    14: '판타지',
    28: '액션',
    35: '코미디',
  })
  const viewMore = ref(false)
  const activeBadge = ref(0)

  const moreGenres = function() {
    viewMore.value = !viewMore.value
  }

  const selectBadge = function(badge) {
    activeBadge.value = badge
  }

  const goDetail = function(id) {
    router.push({name: 'movie_detail', params: {id: id}})
  }

  watch(activeBadge, (newValue, oldValue) => {
    if (activeBadge.value === 0) {
      store.getRecommendMovies()
    } else {
      store.getMovieList(activeBadge.value)
    }
  })
</script>

<template>
  <div class="container">
    <Carousel />
    <div class="badges">
      <Badge 
        :class="{'text-bg-primary': activeBadge === 0, 'text-bg-secondary': activeBadge !== 0}" 
        name="추천"
        @click="selectBadge(0)"
      />
      <Badge 
        v-for="genre in viewMore ? Object.keys(choice) : Object.keys(favoriteGenres)" 
        :class="{'text-bg-secondary': activeBadge !== genre, 'text-bg-primary': activeBadge === genre}" 
        :name="choice[genre]"
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
